<script setup>
import { ref, computed, onMounted } from 'vue'

const OPTIONS = [5, 10, 20]
const n = ref(10)
const loading = ref(false)
const error = ref('')
const data = ref(null)
const view = ref('analysis') // analysis(号码分析) | history(历史开奖) | model(模型说明)

const pad = x => String(x).padStart(2, '0')

async function draw() {
  loading.value = true
  error.value = ''
  try {
    const resp = await fetch(`/api/ssq?n=${n.value}`)
    const json = await resp.json()
    if (!resp.ok || !json.ok) throw new Error(json.error || `请求失败（${resp.status}）`)
    data.value = json
  } catch (e) {
    error.value = e.message || '服务暂不可用，请稍后再试'
  } finally {
    loading.value = false
  }
}

function changeN(v) {
  n.value = v
  draw()
}

const shapeItems = computed(() => {
  const sh = data.value?.predict?.shape
  if (!sh) return []
  return [
    { icon: 'oe', label: '奇偶比', value: sh.oddEven },
    { icon: 'bs', label: '大小比', value: sh.bigSmall },
    { icon: 'zone', label: '三区比', value: sh.zones.join(' · ') },
    { icon: 'sum', label: '和值', value: sh.sum },
    { icon: 'cons', label: '连号', value: sh.consec + ' 组' },
    { icon: 'rep', label: '重号', value: sh.repeat + ' 个' },
  ]
})

const factorCards = computed(() => [
  { title: '冷热频次', sub: '历史频次分布统计', goto: 'model' },
  { title: '遗漏观察', sub: '记录号码未出现期数', goto: 'model' },
  { title: '形态筛选', sub: '奇偶、大小与分区组合', goto: 'model' },
])

onMounted(draw)

const ICONS = {
  oe: '<svg viewBox="0 0 24 24"><circle cx="9" cy="10" r="5" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="16" cy="15" r="4" fill="none" stroke="currentColor" stroke-width="1.7" stroke-dasharray="3 2"/></svg>',
  bs: '<svg viewBox="0 0 24 24"><path d="M4 12h16M12 4v16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><circle cx="12" cy="12" r="3" fill="currentColor"/></svg>',
  zone: '<svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16M9 4v16M15 4v16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
  sum: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.2" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 8v8M9.5 10.4c0-1 1-1.7 2.5-1.7s2.5.7 2.5 1.6c0 2.2-5 1.3-5 3.6 0 1 1.1 1.7 2.6 1.7 1.5 0 2.5-.7 2.5-1.7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  cons: '<svg viewBox="0 0 24 24"><circle cx="8.5" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="15.5" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>',
  rep: '<svg viewBox="0 0 24 24"><path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="m9 12 2 2 4-4" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}
const FACTOR_ICONS = {
  冷热频次: '<svg viewBox="0 0 24 24"><path d="M12 3c1.5 4 5 5.5 5 9a5 5 0 0 1-10 0c0-1.8 1-3 2-4.5C10 9 11 6 12 3Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>',
  遗漏观察: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 7v5l3.5 2" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
  形态筛选: '<svg viewBox="0 0 24 24"><circle cx="7" cy="7" r="2.6" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="17" cy="7" r="2.6" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="17" r="2.6" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="m9 9 2 5m4-5-2 5" stroke="currentColor" stroke-width="1.5"/></svg>',
}
function iconSvg(k) { return ICONS[k] || '' }
function factorIcon(k) { return FACTOR_ICONS[k] || '' }
</script>

<template>
  <div class="lab">
    <!-- 品牌头 + 二级导航 -->
    <header class="lab-topbar">
      <div class="brand">
        <svg class="brand-logo" viewBox="0 0 32 32" aria-hidden="true">
          <defs>
            <linearGradient id="lgCube" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stop-color="#5eeaff" /><stop offset="1" stop-color="#2b7bff" />
            </linearGradient>
          </defs>
          <path d="M16 3 28 9.5v13L16 29 4 22.5v-13Z" fill="url(#lgCube)" opacity=".22" />
          <path d="M16 3 28 9.5 16 16 4 9.5Z" fill="url(#lgCube)" />
          <path d="M4 9.5 16 16v13L4 22.5Z" fill="#1f6fe8" opacity=".85" />
          <path d="M28 9.5 16 16v13l12-6.5Z" fill="#1557c9" opacity=".9" />
        </svg>
        <span class="brand-name">双色球 · 数据研究室</span>
      </div>
      <nav class="subnav">
        <button :class="{ on: view === 'analysis' }" @click="view = 'analysis'">号码分析</button>
        <button :class="{ on: view === 'history' }" @click="view = 'history'">历史开奖</button>
        <button :class="{ on: view === 'model' }" @click="view = 'model'">模型说明</button>
      </nav>
    </header>

    <div class="lab-body">
      <p v-if="error" class="err">⚠️ {{ error }}</p>

      <!-- ============ 号码分析 ============ -->
      <template v-if="view === 'analysis'">
        <div class="page-head">
          <div>
            <h1 class="page-title">让数据，一目了然</h1>
            <p class="page-sub">历史开奖统计与号码组合参考</p>
          </div>
          <div class="head-ctrl">
            <div class="period-box">
              <svg viewBox="0 0 24 24" class="ic"><path d="M4 19V9m5 10V5m6 14v-8m5 8V8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              <select v-model.number="n" class="period-sel" :disabled="loading" @change="changeN(n)">
                <option v-for="o in OPTIONS" :key="o" :value="o">近 {{ o }} 期数据</option>
              </select>
            </div>
            <button class="gen-btn" :disabled="loading" @click="draw">
              <svg viewBox="0 0 24 24" class="ic"><path d="M12 3l1.7 4.6L18 9l-4.3 1.4L12 15l-1.7-4.6L6 9l4.3-1.4L12 3Z" fill="currentColor"/><path d="M18 14l.8 2.2L21 17l-2.2.8L18 20l-.8-2.2L15 17l2.2-.8L18 14Z" fill="currentColor"/></svg>
              {{ loading ? '生成中…' : '生成一组号码' }}
            </button>
          </div>
        </div>

        <div v-if="data && !loading" class="dash">
          <!-- 左列 -->
          <div class="col col-l">
            <!-- 本次参考组合 -->
            <section class="card combo">
              <div class="card-head">
                <div class="card-h-l">
                  <svg viewBox="0 0 24 24" class="ic cyan"><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M12 3v8.5M4 7.5l8 4 8-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
                  <div>
                    <div class="card-title">本次参考组合</div>
                    <div class="card-sub">基于近 {{ data.n }} 期历史数据</div>
                  </div>
                </div>
                <div class="random-tag">
                  <svg viewBox="0 0 24 24" class="ic sm"><path d="M21 12a9 9 0 1 1-3-6.7M21 3v5h-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  随机组合 · 仅供参考
                </div>
              </div>

              <div class="combo-balls">
                <span v-for="(x, i) in data.predict.red" :key="'c' + x" class="ball red big" :style="{ animationDelay: i * 70 + 'ms' }">{{ pad(x) }}</span>
                <span class="plus">+</span>
                <span class="ball blue big" :style="{ animationDelay: 420 + 'ms' }">{{ pad(data.predict.blue) }}</span>
              </div>

              <div class="shape-grid">
                <div v-for="s in shapeItems" :key="s.label" class="shape-cell">
                  <div class="shape-l">
                    <span class="shape-ico" v-html="iconSvg(s.icon)"></span>
                    <span class="shape-label">{{ s.label }}</span>
                  </div>
                  <div class="shape-val">{{ s.value }}</div>
                </div>
              </div>
            </section>

            <!-- 历史开奖记录 -->
            <section class="card history-card">
              <div class="card-head">
                <div class="card-h-l">
                  <svg viewBox="0 0 24 24" class="ic cyan"><rect x="4" y="4" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8 9h8M8 13h8M8 17h5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
                  <div>
                    <div class="card-title">历史开奖记录</div>
                    <div class="card-sub dim">开奖信息以官方公布为准</div>
                  </div>
                </div>
                <button class="link-btn" @click="view = 'history'">查看全部
                  <svg viewBox="0 0 24 24" class="ic sm"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </button>
              </div>

              <table class="htable">
                <thead>
                  <tr><th>期号</th><th>开奖日期</th><th>红球</th><th class="tr">蓝球</th></tr>
                </thead>
                <tbody>
                  <tr v-for="d in data.draws.slice(0, 7)" :key="d.code">
                    <td class="code">{{ d.code }}</td>
                    <td class="date">{{ d.date }}</td>
                    <td>
                      <span v-for="x in d.red" :key="d.code + x" class="ball red sm">{{ pad(x) }}</span>
                    </td>
                    <td class="tr"><span class="ball blue sm">{{ pad(d.blue) }}</span></td>
                  </tr>
                </tbody>
              </table>
            </section>
          </div>

          <!-- 右列 -->
          <div class="col col-r">
            <!-- 最近开奖 -->
            <section class="card latest">
              <div class="card-head">
                <div class="card-h-l">
                  <svg viewBox="0 0 24 24" class="ic gold"><path d="M7 4h10v4a5 5 0 0 1-10 0V4Z" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M7 5H4v2a3 3 0 0 0 3 3M17 5h3v2a3 3 0 0 1-3 3M9 20h6M12 13v7" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
                  <div class="card-title">最近开奖</div>
                </div>
                <button class="link-btn" @click="view = 'history'">查看详情
                  <svg viewBox="0 0 24 24" class="ic sm"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </button>
              </div>
              <div class="latest-code">第 {{ data.latest.code }} 期</div>
              <div class="latest-date">{{ data.latest.date }}</div>
              <div class="latest-balls">
                <span v-for="x in data.latest.red" :key="'la' + x" class="ball red">{{ pad(x) }}</span>
                <span class="ball blue">{{ pad(data.latest.blue) }}</span>
              </div>
              <div class="kv"><span class="kv-k"><svg viewBox="0 0 24 24" class="ic sm dim-ic"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>统计范围</span><span>最近 {{ data.n }} 期</span></div>
              <div class="kv"><span class="kv-k"><svg viewBox="0 0 24 24" class="ic sm dim-ic"><path d="M12 3a9 9 0 1 0 9 9M12 3v9l6-4" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>数据来源</span><span>{{ data.source }}</span></div>
            </section>

            <!-- 组合分析 -->
            <section class="card analysis">
              <div class="card-head">
                <div class="card-h-l">
                  <svg viewBox="0 0 24 24" class="ic cyan"><path d="M4 19V9m5 10V5m6 14v-8m5 8V8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/></svg>
                  <div class="card-title">组合分析</div>
                </div>
              </div>
              <button v-for="f in factorCards" :key="f.title" class="factor-row" @click="view = f.goto">
                <span class="factor-l">
                  <span class="factor-ic" v-html="factorIcon(f.title)"></span>
                  <span><b>{{ f.title }}</b><i>{{ f.sub }}</i></span>
                </span>
                <svg viewBox="0 0 24 24" class="ic sm go"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
            </section>

            <!-- 近N期未开出号码 -->
            <section class="card cold-card">
              <div class="card-head">
                <div class="card-h-l">
                  <svg viewBox="0 0 24 24" class="ic cyan"><path d="M12 3c0 4-5 5-5 9a5 5 0 0 0 10 0c0-2-1.5-3-1.5-5C14 9 12 8 12 3Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
                  <div class="card-title">近 {{ data.n }} 期未开出号码</div>
                </div>
              </div>
              <div class="cold-line">
                <span class="cold-tag red-t">红球</span>
                <span v-for="x in data.predict.coldRed" :key="'cr' + x" class="ball red ghost">{{ pad(x) }}</span>
                <span v-if="!data.predict.coldRed.length" class="cold-none">无</span>
              </div>
              <div class="cold-line">
                <span class="cold-tag blue-t">蓝球</span>
                <span v-for="x in data.predict.coldBlue" :key="'cb' + x" class="ball blue ghost">{{ pad(x) }}</span>
                <span v-if="!data.predict.coldBlue.length" class="cold-none">无</span>
              </div>
            </section>
          </div>
        </div>
        <div v-else-if="loading" class="loading-box">正在读取近 {{ n }} 期开奖数据并生成组合…</div>
      </template>

      <!-- ============ 历史开奖 ============ -->
      <template v-else-if="view === 'history'">
        <div class="page-head">
          <div>
            <h1 class="page-title">历史开奖</h1>
            <p class="page-sub">近 {{ n }} 期双色球开奖号码（数据来源：{{ data?.source || '—' }}）</p>
          </div>
          <div class="period-box">
            <svg viewBox="0 0 24 24" class="ic"><path d="M4 19V9m5 10V5m6 14v-8m5 8V8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            <select v-model.number="n" class="period-sel" :disabled="loading" @change="changeN(n)">
              <option v-for="o in OPTIONS" :key="o" :value="o">近 {{ o }} 期数据</option>
            </select>
          </div>
        </div>
        <section v-if="data" class="card full-table">
          <table class="htable big">
            <thead><tr><th>期号</th><th>开奖日期</th><th>红球</th><th class="tr">蓝球</th></tr></thead>
            <tbody>
              <tr v-for="d in data.draws" :key="d.code">
                <td class="code">{{ d.code }}</td>
                <td class="date">{{ d.date }}</td>
                <td>
                  <span v-for="x in d.red" :key="d.code + 'h' + x" class="ball red sm">{{ pad(x) }}</span>
                </td>
                <td class="tr"><span class="ball blue sm">{{ pad(d.blue) }}</span></td>
              </tr>
            </tbody>
          </table>
        </section>
      </template>

      <!-- ============ 模型说明 ============ -->
      <template v-else>
        <div class="page-head">
          <div><h1 class="page-title">模型说明</h1><p class="page-sub">多因子加权随机 · 高频形态择优</p></div>
        </div>
        <section v-if="data" class="card model-card">
          <div class="model-flow">
            <div class="mf-step"><span class="mf-no">01</span><b>冷热频次</b><p>近 N 期开出次数越多，权重按指数（0.72^次数）衰减，实现冷号优先，而非把热号完全排除。</p></div>
            <div class="mf-step"><span class="mf-no">02</span><b>遗漏回补</b><p>结合近 30 期遗漏期数，偏好“温冷回补区”，对刚开出的热号与遗漏超 20 期的深冷号同时降权。</p></div>
            <div class="mf-step"><span class="mf-no">03</span><b>邻号联动</b><p>对上期开奖号码的 ±1 邻号给予小幅加权。</p></div>
            <div class="mf-step"><span class="mf-no">04</span><b>形态择优</b><p>生成 2500 组号码权重候选，按奇偶比、大小比、三区、和值、连号、重号、012 路打分，在高分候选中概率择一，兼顾合理与随机。</p></div>
          </div>
          <ul class="model-factors">
            <li v-for="(f, i) in data.predict.factors" :key="i">{{ f }}</li>
          </ul>
          <p class="strategy-line">🎯 {{ data.strategy }}</p>
          <p class="model-warn">彩票每期开奖为相互独立的随机事件，历史规律不代表未来结果，任何模型都无法提高中奖概率。本页内容仅供数据研究与娱乐参考，请理性购彩。</p>
        </section>
      </template>

      <p class="lab-foot">历史数据不代表未来结果 · 号码组合仅供娱乐参考</p>
    </div>
  </div>
</template>

<style scoped>
.lab {
  position: relative;
  width: 100%;
  max-width: 1240px;
  margin: 0 auto;
  color: #d6e4ff;
  overflow: hidden;
}
.lab::before {
  content: '';
  position: absolute; inset: 0; pointer-events: none;
  background-image:
    linear-gradient(rgba(94, 234, 255, .045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(94, 234, 255, .045) 1px, transparent 1px);
  background-size: 40px 40px;
  -webkit-mask-image: radial-gradient(ellipse 80% 40% at 50% 0%, #000, transparent 80%);
  mask-image: radial-gradient(ellipse 80% 40% at 50% 0%, #000, transparent 80%);
}
.lab > * { position: relative; z-index: 1; }

/* 顶栏 */
.lab-topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 30px;
  border-bottom: 1px solid rgba(94, 234, 255, .14);
  background: rgba(8, 15, 32, .55);
}
.brand { display: flex; align-items: center; gap: 11px; }
.brand-logo { width: 30px; height: 30px; filter: drop-shadow(0 0 10px rgba(94,234,255,.5)); }
.brand-name { font-size: 19px; font-weight: 800; letter-spacing: 1px; color: #eaf4ff; }
.subnav { display: flex; gap: 38px; }
.subnav button {
  position: relative; background: none; border: none; cursor: pointer;
  color: #8fa2c8; font-size: 16px; font-weight: 600; letter-spacing: 2px; padding: 6px 2px;
}
.subnav button:hover { color: #cfe3ff; }
.subnav button.on { color: #eaf4ff; }
.subnav button.on::after {
  content: ''; position: absolute; left: 50%; transform: translateX(-50%); bottom: -18px;
  width: 34px; height: 3px; border-radius: 3px;
  background: linear-gradient(90deg, #22d3ee, #2b7bff);
  box-shadow: 0 0 12px rgba(34, 211, 238, .8);
}

.lab-body { padding: 30px; }

.page-head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 22px; flex-wrap: wrap; gap: 16px; }
.page-title { margin: 0; font-size: 34px; font-weight: 800; letter-spacing: 1px; color: #f3f8ff; }
.page-sub { margin: 8px 0 0; color: #7f93bb; font-size: 15px; }
.head-ctrl { display: flex; gap: 14px; align-items: center; }

.period-box {
  display: flex; align-items: center; gap: 8px;
  background: rgba(20, 36, 68, .7); border: 1px solid rgba(94, 234, 255, .25);
  border-radius: 12px; padding: 0 12px; height: 52px;
}
.period-box .ic { width: 19px; height: 19px; color: #5eeaff; }
.period-sel {
  background: transparent; border: none; outline: none; color: #dceaff; font-size: 15px;
  cursor: pointer; height: 100%; padding-right: 4px;
}
.period-sel option { background: #0e1b38; color: #dceaff; }
.gen-btn {
  display: inline-flex; align-items: center; gap: 8px; height: 52px; padding: 0 28px;
  border: none; border-radius: 12px; cursor: pointer;
  font-size: 16px; font-weight: 700; letter-spacing: 2px; color: #eaffff;
  background: linear-gradient(135deg, #18b8e6, #1d6ff2);
  box-shadow: 0 0 22px rgba(29, 140, 240, .5), 0 10px 24px rgba(13, 80, 190, .4);
  transition: transform .15s, box-shadow .2s;
}
.gen-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 0 30px rgba(34,211,238,.7), 0 12px 28px rgba(13,80,190,.5); }
.gen-btn:disabled { opacity: .55; }
.gen-btn .ic { width: 19px; height: 19px; }

/* 栅格 */
.dash { display: grid; grid-template-columns: 1fr 368px; gap: 20px; align-items: start; }
.col { display: flex; flex-direction: column; gap: 20px; min-width: 0; }

.card {
  background: linear-gradient(180deg, rgba(22, 38, 70, .62), rgba(12, 22, 46, .72));
  border: 1px solid rgba(94, 234, 255, .16);
  border-radius: 16px;
  padding: 22px 24px;
  box-shadow: 0 16px 44px rgba(0, 0, 0, .38), inset 0 1px 0 rgba(255,255,255,.05);
}
.card-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
.card-h-l { display: flex; align-items: center; gap: 11px; }
.card-title { font-size: 17px; font-weight: 800; color: #eaf4ff; letter-spacing: .5px; }
.card-sub { font-size: 12.5px; color: #7f93bb; margin-top: 3px; }
.card-sub.dim { color: #64779d; }
.ic { width: 22px; height: 22px; flex: none; }
.ic.sm { width: 16px; height: 16px; }
.ic.cyan { color: #5eeaff; }
.ic.gold { color: #f5c97a; }
.link-btn { display: inline-flex; align-items: center; gap: 3px; background: none; border: none; cursor: pointer; color: #6fc7ff; font-size: 13.5px; }
.link-btn:hover { color: #a5e4ff; }
.random-tag { display: inline-flex; align-items: center; gap: 6px; color: #8fa2c8; font-size: 13px; }

/* 球 */
.ball {
  display: inline-flex; align-items: center; justify-content: center;
  border-radius: 50%; color: #fff; font-weight: 800;
  font-family: ui-monospace, 'Arial', sans-serif; border: 1px solid rgba(255,255,255,.25);
}
.ball.red { background: radial-gradient(circle at 32% 28%, #ff7a70, #ef3340 55%, #b81a26); box-shadow: inset -2px -3px 6px rgba(0,0,0,.3), 0 0 12px rgba(239,51,64,.45); }
.ball.blue { background: radial-gradient(circle at 32% 28%, #8fe9ff, #28b0ff 52%, #1763e0); box-shadow: inset -2px -3px 6px rgba(0,0,0,.28), 0 0 12px rgba(40,176,255,.5); }
.ball.big { width: 64px; height: 64px; font-size: 27px; animation: ballIn .5s cubic-bezier(.2,.9,.3,1.3) both; }
.ball:not(.big):not(.sm):not(.ghost) { width: 38px; height: 38px; font-size: 15px; }
.ball.sm { width: 25px; height: 25px; font-size: 12px; margin-right: 5px; }
.ball.ghost { width: 27px; height: 27px; font-size: 12.5px; margin-right: 6px; opacity: .92; }
@keyframes ballIn { from { opacity: 0; transform: translateY(14px) scale(.4); } 60% { transform: translateY(-3px) scale(1.08); } to { opacity: 1; transform: none; } }

.combo-balls { display: flex; align-items: center; justify-content: center; gap: 14px; flex-wrap: wrap; padding: 16px 0 26px; }
.plus { font-size: 30px; font-weight: 800; color: #5eeaff; text-shadow: 0 0 14px rgba(94,234,255,.7); }

.shape-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; }
.shape-cell {
  background: rgba(13, 25, 50, .55); border: 1px solid rgba(94, 234, 255, .14);
  border-radius: 12px; padding: 13px 14px;
}
.shape-l { display: flex; align-items: center; gap: 7px; color: #8fa2c8; font-size: 13px; margin-bottom: 9px; }
.shape-ico { width: 17px; height: 17px; color: #5eeaff; display: inline-flex; }
.shape-ico :deep(svg) { width: 100%; height: 100%; }
.shape-val { font-size: 23px; font-weight: 800; color: #54d4f5; font-family: ui-monospace, Menlo, Consolas, monospace; }

/* 表格 */
.htable { width: 100%; border-collapse: collapse; }
.htable th { text-align: left; font-size: 13px; color: #7f93bb; font-weight: 600; padding: 0 12px 12px; border-bottom: 1px solid rgba(94,234,255,.14); }
.htable td { padding: 11px 12px; border-bottom: 1px solid rgba(94,234,255,.07); font-size: 14px; }
.htable tbody tr:last-child td { border-bottom: none; }
.htable .code { font-family: ui-monospace, Menlo, monospace; font-weight: 700; color: #e8f2ff; white-space: nowrap; }
.htable .date { color: #8fa2c8; white-space: nowrap; }
.htable .tr { text-align: right; }
.htable.big td { padding: 14px 12px; }

/* 右列 */
.latest-code { font-size: 22px; font-weight: 800; color: #eaf4ff; letter-spacing: 1px; }
.latest-date { color: #7f93bb; font-size: 13.5px; margin: 4px 0 16px; }
.latest-balls { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 18px; }
.kv { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-top: 1px solid rgba(94,234,255,.1); font-size: 14px; color: #c6d6f5; }
.kv-k { display: inline-flex; align-items: center; gap: 8px; color: #8fa2c8; }
.dim-ic { color: #6b80a8; }

.factor-row {
  display: flex; align-items: center; justify-content: space-between; width: 100%;
  background: rgba(13, 25, 50, .5); border: 1px solid rgba(94,234,255,.12);
  border-radius: 12px; padding: 14px 15px; margin-bottom: 10px; cursor: pointer;
  transition: border-color .2s, background .2s;
}
.factor-row:last-child { margin-bottom: 0; }
.factor-row:hover { border-color: rgba(94,234,255,.4); background: rgba(20,40,76,.6); }
.factor-l { display: flex; align-items: center; gap: 12px; text-align: left; }
.factor-ic { width: 26px; height: 26px; color: #5eeaff; display: inline-flex; }
.factor-ic :deep(svg) { width: 100%; height: 100%; }
.factor-l b { display: block; color: #e3eeff; font-size: 14.5px; }
.factor-l i { display: block; color: #7f93bb; font-style: normal; font-size: 12.5px; margin-top: 2px; }
.factor-row .go { color: #6b80a8; }

.cold-line { display: flex; align-items: center; flex-wrap: wrap; margin-bottom: 12px; }
.cold-line:last-child { margin-bottom: 0; }
.cold-tag { font-size: 12px; font-weight: 700; border-radius: 7px; padding: 3px 9px; margin-right: 10px; }
.red-t { color: #ff8a86; background: rgba(239,51,64,.14); border: 1px solid rgba(239,51,64,.4); }
.blue-t { color: #8fd8ff; background: rgba(40,176,255,.12); border: 1px solid rgba(40,176,255,.4); }
.cold-none { color: #64779d; font-size: 13px; }

.full-table { padding: 24px 26px; }
.loading-box { text-align: center; color: #8fa2c8; padding: 80px 0; font-size: 15px; }

/* 模型说明 */
.model-flow { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 20px; }
.mf-step { background: rgba(13,25,50,.5); border: 1px solid rgba(94,234,255,.14); border-radius: 14px; padding: 20px; }
.mf-no { font-family: ui-monospace, monospace; font-size: 14px; color: #2bb8e8; font-weight: 800; letter-spacing: 1px; }
.mf-step b { display: block; font-size: 17px; color: #eaf4ff; margin: 8px 0 8px; }
.mf-step p { margin: 0; font-size: 13.5px; color: #9db0d4; line-height: 1.8; }
.model-factors { margin: 4px 0 14px; padding-left: 20px; }
.model-factors li { font-size: 13.5px; color: #9db0d4; line-height: 1.9; }
.strategy-line { font-size: 14px; color: #c6d6f5; margin: 8px 0; }
.model-warn { font-size: 13px; color: #e0a878; line-height: 1.9; background: rgba(245,201,122,.08); border: 1px solid rgba(245,201,122,.25); border-radius: 12px; padding: 13px 16px; margin: 14px 0 0; }

.err { text-align: center; color: #ff9aa0; background: rgba(255,60,70,.1); border: 1px solid rgba(255,90,100,.3); border-radius: 12px; padding: 12px 16px; }
.lab-foot { text-align: center; color: #64779d; font-size: 12.5px; letter-spacing: 1px; margin: 28px 0 0; }

@media (max-width: 980px) {
  .dash { grid-template-columns: 1fr; }
  .shape-grid { grid-template-columns: repeat(3, 1fr); }
  .model-flow { grid-template-columns: 1fr; }
  .lab-topbar { flex-direction: column; gap: 14px; }
  .subnav { gap: 24px; }
  .subnav button.on::after { bottom: -8px; }
  .lab-body { padding: 22px 16px; }
}
</style>
