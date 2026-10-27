"""
双色球开奖抓取 + 多因子冷号加权预测（Vercel Serverless Function，纯 Python 标准库）。

接口：GET /api/ssq?n=10
  - n 仅允许 5 / 10 / 20，默认 10（近 n 期作为“冷热频次”窗口，也用于前端展示）

预测模型（自主设计的多因子模型）：
  号码级权重：
    1) 近 n 期频次：出现越多权重越低（指数衰减，核心诉求）；
    2) 遗漏值：偏好“温冷回补区”，对刚开出的热号与超深冷号都降权（钟形）；
    3) 邻号：上期开奖号 ±1 给予小幅加权。
  组合级形态：按号码权重生成大量候选，再用奇偶比 / 大小比 / 三区分布 /
    和值 / 连号 / 重号 / 012 路综合打分，挑形态最优的一注。
  蓝球：近 n 期频次反向 + 遗漏钟形（偏好温号）+ 近期奇偶大小的温和反转。

数据源：中国福利彩票官网接口（主），500 彩票网（备，海外节点更稳）。
"""

import json
import math
import random
import re
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

ALLOWED_N = (5, 10, 20)
DEFAULT_N = 10
GAP_WINDOW = 30          # 计算遗漏值使用的最长历史窗口（频次仍严格用近 n 期）
CANDIDATES = 2500        # 红球组合候选数量
PICK_TEMPERATURE = 0.05  # 在高分候选中 softmax 抽样的温度：越高越随机，越低越贴近高频形态
SUM_SIGMA = 34           # 和值偏好（均值102）的宽度

SRC = (
    "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice"
    "?name=ssq&issueCount={n}"
)
SRC_500 = "https://datachart.500.com/ssq/history/newinc/history.php?limit={n}"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
HEADERS = {"User-Agent": UA, "Referer": "https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/",
           "Accept": "application/json, text/plain, */*"}


# ============================ 数据抓取 ============================

def fetch_from_cwl(limit):
    url = SRC.format(n=limit)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=9) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("state") != 0:
        raise RuntimeError(data.get("message") or "官网接口返回异常")
    rows = []
    for item in data.get("result", []) or []:
        reds = [int(x) for x in str(item.get("red", "")).split(",") if x.strip()]
        blue_raw = str(item.get("blue", "")).strip()
        blue = int(blue_raw) if blue_raw else None
        if len(reds) != 6 or blue is None:
            continue
        rows.append({"code": item.get("code"), "date": item.get("date"),
                     "week": item.get("week"), "red": reds, "blue": blue})
    return rows


def fetch_from_500(limit):
    url = SRC_500.format(n=limit)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Referer": "https://datachart.500.com/ssq/history/history.shtml"})
    with urllib.request.urlopen(req, timeout=9) as resp:
        html = resp.read().decode("gb2312", errors="ignore")
    rows = []
    for line in re.findall(r'tr class="t_tr1">(.*?)</tr>', html, flags=re.S):
        code_m = re.search(r"<td>(\d{5,7})</td>", line)
        reds = [int(x) for x in re.findall(r't_cfont2">(\d{2})<', line)]
        blue_m = re.search(r't_cfont4">(\d{2})<', line)
        date_m = re.search(r"(\d{4}-\d{2}-\d{2})", line)
        if not code_m or len(reds) != 6 or not blue_m:
            continue
        code = code_m.group(1)
        if len(code) == 5:
            code = "20" + code
        rows.append({"code": code, "date": date_m.group(1) if date_m else "",
                     "week": "", "red": reds, "blue": int(blue_m.group(1))})
    return rows


def fetch_recent(n):
    """返回 (rows, source)。rows 为近 max(n,30) 期（最新在前），供频次/遗漏共用。"""
    limit = max(n, GAP_WINDOW)
    errors = []
    for fetcher in (fetch_from_cwl, fetch_from_500):
        try:
            rows = fetcher(limit)
            if rows:
                return rows, ("中国福利彩票官网" if fetcher is fetch_from_cwl else "500彩票网（备用）")
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))
    raise RuntimeError("; ".join(errors) or "所有数据源均不可用")


# ============================ 多因子模型 ============================

def count_map(rows_part, lo, hi, key):
    cnt = {x: 0 for x in range(lo, hi + 1)}
    for row in rows_part:
        for x in (row[key] if isinstance(row[key], list) else [row[key]]):
            cnt[x] = cnt.get(x, 0) + 1
    return cnt


def gap_map(rows, lo, hi, key):
    """每个号码距最近一次开出的期数（0=上期刚出）；窗口内未出记为窗口长度（深冷）。"""
    gaps = {x: len(rows) for x in range(lo, hi + 1)}
    for i, row in enumerate(rows):
        nums = row[key] if isinstance(row[key], list) else [row[key]]
        for x in nums:
            if x in gaps and gaps[x] == len(rows):
                gaps[x] = i
    return gaps


def gap_weight(g, mu, sigma):
    """遗漏钟形：在温冷回补区(mu)达峰，热号与超深冷号都回落。"""
    return math.exp(-((g - mu) ** 2) / (2.0 * sigma * sigma))


def weighted_sample(pool, weights, k, rng):
    """无放回按权重抽 k 个。"""
    pool = list(pool)
    w = list(weights)
    out = []
    for _ in range(k):
        total = sum(w)
        r = rng.random() * total
        acc, idx = 0.0, len(pool) - 1
        for i, vv in enumerate(w):
            acc += vv
            if r <= acc:
                idx = i
                break
        out.append(pool.pop(idx))
        w.pop(idx)
    return out


# ---- 组合形态评分（越接近历史高频形态分越高）----
def combo_score(nums, last_red):
    odd = sum(1 for x in nums if x % 2 == 1)
    big = sum(1 for x in nums if x >= 17)
    z = [sum(1 for x in nums if 1 <= x <= 11),
         sum(1 for x in nums if 12 <= x <= 22),
         sum(1 for x in nums if 23 <= x <= 33)]
    s = sum(nums)
    srt = sorted(nums)
    consec_pairs = sum(1 for a, b in zip(srt, srt[1:]) if b - a == 1)
    has_triple = any(srt[i + 2] - srt[i] == 2 for i in range(len(srt) - 2))
    repeat = len(set(nums) & set(last_red))
    routes = len({x % 3 for x in nums})

    p_odd = {3: 1.0, 2: .9, 4: .9, 1: .45, 5: .45, 0: .1, 6: .1}[odd]
    p_big = {3: 1.0, 2: .9, 4: .9, 1: .45, 5: .45, 0: .1, 6: .1}[big]
    if z == [2, 2, 2]:
        p_zone = 1.0
    elif min(z) >= 1:
        p_zone = .9
    elif max(z) >= 4:
        p_zone = .4
    elif z.count(0) == 1:
        p_zone = .6
    else:
        p_zone = .1
    p_sum = math.exp(-((s - 102) ** 2) / (2.0 * SUM_SIGMA * SUM_SIGMA))
    if has_triple:
        p_con = .7
    elif consec_pairs == 1:
        p_con = 1.0
    elif consec_pairs == 0:
        p_con = .85
    else:
        p_con = .8
    p_rep = {0: .85, 1: 1.0, 2: .9}.get(repeat, .4)
    p_route = {3: 1.0, 2: .85}.get(routes, .1)

    score = (p_odd + p_big + p_zone + p_sum + p_con + p_rep + p_route) / 7.0
    shape = {"oddEven": f"{odd}:{6 - odd}", "bigSmall": f"{big}:{6 - big}",
             "zones": z, "sum": s, "consec": consec_pairs, "repeat": repeat, "score": round(score, 3)}
    return score, shape


def predict(rows, n):
    recent = rows[:n]                                  # 频次窗口严格取近 n 期
    rng = random.Random()

    # ---- 红球号码级权重 ----
    red_cnt = count_map(recent, 1, 33, "red")
    red_gap = gap_map(rows, 1, 33, "red")
    last_red = rows[0]["red"]
    neighbors = {x for y in last_red for x in (y - 1, y + 1) if 1 <= x <= 33}

    red_weights = {}
    for x in range(1, 34):
        w_freq = 0.72 ** red_cnt[x]                          # 频次越高越低
        w_gap = gap_weight(red_gap[x], mu=10, sigma=8)      # 偏温冷回补
        w_nb = 1.12 if x in neighbors else 1.0              # 邻号小加权
        red_weights[x] = w_freq * w_gap * w_nb

    pool = list(range(1, 34))
    w = [red_weights[x] for x in pool]
    # 生成多组号码权重抽样的候选，按形态打分，再在高分候选里 softmax 概率择一，
    # 使整体分布贴近真实高频形态，同时保留随机性、不会每次都得到唯一“满分组合”。
    scored = []
    for _ in range(CANDIDATES):
        cand = weighted_sample(pool, w, 6, rng)
        sc, shape = combo_score(cand, last_red)
        scored.append((sorted(cand), sc, shape))
    smax = max(x[1] for x in scored)
    exps = [math.exp((x[1] - smax) / PICK_TEMPERATURE) for x in scored]
    total_e = sum(exps)
    r = rng.random() * total_e
    acc, chosen_idx = 0.0, len(scored) - 1
    for i, e in enumerate(exps):
        acc += e
        if r <= acc:
            chosen_idx = i
            break
    best, _, best_shape = scored[chosen_idx]

    # ---- 蓝球权重：频次反向 + 遗漏钟形 + 近5期奇偶/大小温和反转 ----
    blue_cnt = count_map(recent, 1, 16, "blue")
    blue_gap = gap_map(rows, 1, 16, "blue")
    last5_blue = [r["blue"] for r in rows[:5]]
    odd_recent = sum(1 for b in last5_blue if b % 2 == 1)
    big_recent = sum(1 for b in last5_blue if b >= 9)
    blue_weights = {}
    for x in range(1, 17):
        wf = 0.7 ** blue_cnt[x]
        wg = gap_weight(blue_gap[x], mu=8, sigma=7)
        wr = 1.0
        if odd_recent >= 4:
            wr *= 1.12 if x % 2 == 0 else 0.92
        elif odd_recent <= 1:
            wr *= 1.12 if x % 2 == 1 else 0.92
        if big_recent >= 4:
            wr *= 1.10 if x <= 8 else 0.94
        elif big_recent <= 1:
            wr *= 1.10 if x >= 9 else 0.94
        blue_weights[x] = wf * wg * wr
    blue = weighted_sample(list(range(1, 17)), [blue_weights[x] for x in range(1, 17)], 1, rng)[0]

    cold_red = sorted(x for x in range(1, 34) if red_cnt[x] == 0)
    cold_blue = sorted(x for x in range(1, 17) if blue_cnt[x] == 0)
    return {
        "red": best,
        "blue": blue,
        "shape": best_shape,
        "redCount": {str(k): red_cnt[k] for k in range(1, 34)},
        "blueCount": {str(k): blue_cnt[k] for k in range(1, 17)},
        "redGap": {str(k): red_gap[k] for k in range(1, 34)},
        "coldRed": cold_red,
        "coldBlue": cold_blue,
        "factors": [
            "近 %d 期频次：开出越多，权重按指数衰减（冷号优先）" % n,
            "遗漏值：偏好温冷回补区，热号与超深冷号均降权（参考近 %d 期）" % GAP_WINDOW,
            "上期邻号(±1)小幅加权",
            "从 %d 组候选按 奇偶/大小/三区/和值/连号/重号/012路 形态打分，高分候选概率择优" % CANDIDATES,
        ],
    }


# ============================ HTTP 入口 ============================

class handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        try:
            n = int(qs.get("n", [str(DEFAULT_N)])[0])
        except (TypeError, ValueError):
            n = DEFAULT_N
        if n not in ALLOWED_N:
            self._send(400, {"ok": False, "error": "n 仅支持 5 / 10 / 20"})
            return
        try:
            rows, source = fetch_recent(n)
            result = predict(rows, n)
            self._send(200, {
                "ok": True,
                "n": n,
                "latest": rows[0],
                "draws": rows[:n],
                "predict": result,
                "strategy": "多因子冷号加权：频次反向 + 遗漏回补 + 邻号，组合形态择优（近 %d 期）" % n,
                "source": source,
            })
        except Exception as exc:  # noqa: BLE001
            self._send(502, {"ok": False, "error": "抓取失败：%s" % exc})

    def log_message(self, *args):
        return
