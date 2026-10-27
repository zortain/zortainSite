"""
双色球开奖抓取 + 冷号加权预测（Vercel Serverless Function，纯 Python 标准库）。

接口：GET /api/ssq?n=10
  - n 仅允许 5 / 10 / 20，默认 10
数据源：中国福利彩票官网开奖公告接口（findDrawNotice）。
预测策略：统计近 n 期各号码出现次数，出现次数越多权重越低（冷号更容易被随机到）。
"""

import json
import random
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

ALLOWED_N = (5, 10, 20)
DEFAULT_N = 10

SRC = (
    "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice"
    "?name=ssq&issueCount={n}"
)
SRC_500 = "https://datachart.500.com/ssq/history/newinc/history.php?limit={n}"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/",
    "Accept": "application/json, text/plain, */*",
}


def fetch_from_cwl(n):
    """主数据源：中国福利彩票官网开奖公告接口。"""
    url = SRC.format(n=n)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=9) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)
    if data.get("state") != 0:
        raise RuntimeError(data.get("message") or "官网接口返回异常")
    rows = []
    for item in data.get("result", []) or []:
        reds = [int(x) for x in str(item.get("red", "")).split(",") if x.strip()]
        blue_raw = str(item.get("blue", "")).strip()
        blue = int(blue_raw) if blue_raw else None
        if len(reds) != 6 or blue is None:
            continue
        rows.append({
            "code": item.get("code"),
            "date": item.get("date"),
            "week": item.get("week"),
            "red": reds,
            "blue": blue,
        })
    return rows


def fetch_from_500(n):
    """备用数据源：500 彩票网历史开奖（GB 编码 HTML），海外节点更稳。"""
    import re
    url = SRC_500.format(n=n)
    req = urllib.request.Request(url, headers={
        "User-Agent": HEADERS["User-Agent"],
        "Referer": "https://datachart.500.com/ssq/history/history.shtml",
    })
    with urllib.request.urlopen(req, timeout=9) as resp:
        raw = resp.read()
    html = raw.decode("gb2312", errors="ignore")
    rows = []
    for line in re.findall(r'tr class="t_tr1">(.*?)</tr>', html, flags=re.S):
        code_m = re.search(r"<td>(\d{5,7})</td>", line)
        reds = [int(x) for x in re.findall(r't_cfont2">(\d{2})<', line)]
        blue_m = re.search(r't_cfont4">(\d{2})<', line)
        date_m = re.search(r"(\d{4}-\d{2}-\d{2})", line)
        if not code_m or len(reds) != 6 or not blue_m:
            continue
        code = code_m.group(1)
        if len(code) == 5:  # 500 用 26122，补成官网的 2026122
            code = "20" + code
        rows.append({
            "code": code,
            "date": date_m.group(1) if date_m else "",
            "week": "",
            "red": reds,
            "blue": int(blue_m.group(1)),
        })
    return rows


def fetch_recent(n):
    """抓取最近 n 期（官网优先，失败降级 500），返回按期号倒序的 list[dict]。"""
    errors = []
    for fetcher in (fetch_from_cwl, fetch_from_500):
        try:
            rows = fetcher(n)
            if rows:
                return rows, ("中国福利彩票官网" if fetcher is fetch_from_cwl else "500彩票网（备用）")
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))
    raise RuntimeError("; ".join(errors) or "所有数据源均不可用")


def weighted_pick(candidates, count_map, rng):
    """
    从 candidates 中无放回抽取。权重与出现次数成反比（线性反向）：
      出现 k 次 -> 权重 = max_count - k + 1
    因此最冷号码权重最高、最热号码权重最低。
    """
    max_k = max(count_map.values()) if count_map else 0
    chosen = []
    pool = list(candidates)
    while pool:
        weights = [max(0.0001, (max_k - count_map.get(x, 0) + 1)) for x in pool]
        total = sum(weights)
        r = rng.random() * total
        acc = 0.0
        idx = len(pool) - 1
        for i, w in enumerate(weights):
            acc += w
            if r <= acc:
                idx = i
                break
        chosen.append(pool.pop(idx))
    return chosen


def predict(rows):
    """根据近 n 期统计，返回预测红球(6, 升序) 与蓝球(1)。"""
    red_cnt, blue_cnt = {}, {}
    for row in rows:
        for x in row["red"]:
            red_cnt[x] = red_cnt.get(x, 0) + 1
        blue_cnt[row["blue"]] = blue_cnt.get(row["blue"], 0) + 1

    rng = random.Random()  # 真随机
    reds = sorted(weighted_pick(range(1, 34), red_cnt, rng)[:6])
    blue = weighted_pick(range(1, 17), blue_cnt, rng)[0]

    # 近 n 期未开出的冷号（供前端展示）
    cold_red = sorted(x for x in range(1, 34) if red_cnt.get(x, 0) == 0)
    cold_blue = sorted(x for x in range(1, 17) if blue_cnt.get(x, 0) == 0)
    return {
        "red": reds,
        "blue": blue,
        "redCount": {str(k): red_cnt.get(k, 0) for k in range(1, 34)},
        "blueCount": {str(k): blue_cnt.get(k, 0) for k in range(1, 17)},
        "coldRed": cold_red,
        "coldBlue": cold_blue,
    }


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
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        try:
            n = int(qs.get("n", [str(DEFAULT_N)])[0])
        except (TypeError, ValueError):
            n = DEFAULT_N
        if n not in ALLOWED_N:
            self._send(400, {"ok": False, "error": "n 仅支持 5 / 10 / 20"})
            return
        try:
            rows, source = fetch_recent(n)
            result = predict(rows)
            self._send(200, {
                "ok": True,
                "n": n,
                "latest": rows[0],
                "draws": rows,
                "predict": result,
                "strategy": "近 %d 期出现次数越多，被随机到的权重越低（冷号优先）" % n,
                "source": source,
            })
        except Exception as exc:  # noqa: BLE001
            self._send(502, {"ok": False, "error": "抓取失败：%s" % exc})

    def log_message(self, *args):  # 静默默认访问日志
        return
