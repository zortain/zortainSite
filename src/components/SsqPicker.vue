<script setup>
import { ref, onMounted } from 'vue'

const OPTIONS = [5, 10, 20]
const n = ref(10)
const loading = ref(false)
const error = ref('')
const data = ref(null)

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
    data.value = null
  } finally {
    loading.value = false
  }
}

onMounted(draw)
</script>

<template>
  <div class="ssq">
    <div class="grid-deco" aria-hidden="true"></div>
    <div class="ssq-kicker">SSQ · MULTI-FACTOR AI PREDICTION</div>
    <h1 class="ssq-title">双色球智能预测</h1>
    <p class="ssq-sub">基于近 N 期真实开奖的多因子模型：冷热频次 · 遗漏回补 · 邻号联动 · 高频形态择优</p>

    <div class="ctrl">
      <label class="ctrl-label">参考期数</label>
      <select v-model.number="n" class="sel" :disabled="loading">
        <option v-for="o in OPTIONS" :key="o" :value="o">最近 {{ o }} 期</option>
      </select>
      <button class="btn" :disabled="loading" @click="draw">
        {{ loading ? '生成中…' : '生成一注预测' }}
      </button>
    </div>

    <p v-if="error" class="err">⚠️ {{ error }}</p>

    <transition name="pop">
      <div v-if="data && !loading" class="result">
        <div class="balls">
          <span v-for="(x, i) in data.predict.red" :key="'r' + x" class="ball red" :style="{ animationDelay: i * 70 + 'ms' }">{{ pad(x) }}</span>
          <span class="plus">+</span>
          <span class="ball blue" :style="{ animationDelay: 6 * 70 + 'ms' }">{{ pad(data.predict.blue) }}</span>
        </div>

        <div class="meta">
          <div class="meta-row">
            <span class="tag">最近开奖</span>
            <span class="meta-code">第 {{ data.latest.code }} 期 · {{ data.latest.date }}</span>
            <span class="balls mini">
              <span v-for="x in data.latest.red" :key="'lr' + x" class="ball red s">{{ pad(x) }}</span>
              <span class="ball blue s">{{ pad(data.latest.blue) }}</span>
            </span>
          </div>
          <p class="strategy">🎯 {{ data.strategy }}（数据来源：{{ data.source }}）</p>
          <div class="shape">
            <span class="sh-chip">奇偶 {{ data.predict.shape.oddEven }}</span>
            <span class="sh-chip">大小 {{ data.predict.shape.bigSmall }}</span>
            <span class="sh-chip">三区 {{ data.predict.shape.zones.join('-') }}</span>
            <span class="sh-chip">和值 {{ data.predict.shape.sum }}</span>
            <span class="sh-chip">连号 {{ data.predict.shape.consec }} 组</span>
            <span class="sh-chip">重号 {{ data.predict.shape.repeat }} 个</span>
          </div>
          <ul class="factors">
            <li v-for="(f, i) in data.predict.factors" :key="i">{{ f }}</li>
          </ul>
          <p class="cold">
            近 {{ data.n }} 期未开出的冷号 —
            红球：<b>{{ data.predict.coldRed.length ? data.predict.coldRed.map(pad).join('、') : '无' }}</b>
            ｜蓝球：<b>{{ data.predict.coldBlue.length ? data.predict.coldBlue.map(pad).join('、') : '无' }}</b>
          </p>
        </div>

        <div class="history">
          <div class="hist-title">近 {{ data.n }} 期开奖记录</div>
          <div v-for="d in data.draws" :key="d.code" class="hist-row">
            <span class="hist-code">{{ d.code }}</span>
            <span class="hist-date">{{ d.date }}</span>
            <span class="balls mini">
              <span v-for="x in d.red" :key="d.code + 'r' + x" class="ball red s">{{ pad(x) }}</span>
              <span class="ball blue s">{{ pad(d.blue) }}</span>
            </span>
          </div>
        </div>
      </div>
    </transition>

    <p class="disclaimer">
      本结果由历史数据多因子加权随机生成，彩票每期开奖为独立随机事件，历史规律不代表未来结果，任何方法均无法提高中奖概率，仅供娱乐，请理性购彩。
    </p>
  </div>
</template>

<style scoped>
.ssq {
  position: relative;
  max-width: 760px;
  margin: 0 auto;
  padding: 34px 18px 64px;
  color: #dbe7ff;
  overflow: hidden;
}
.ssq > *:not(.grid-deco) { position: relative; z-index: 1; }

.grid-deco {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(94, 234, 255, .055) 1px, transparent 1px),
    linear-gradient(90deg, rgba(94, 234, 255, .055) 1px, transparent 1px);
  background-size: 38px 38px;
  -webkit-mask-image: radial-gradient(ellipse 75% 52% at 50% 0%, #000 0%, transparent 78%);
  mask-image: radial-gradient(ellipse 75% 52% at 50% 0%, #000 0%, transparent 78%);
}

.ssq-kicker {
  text-align: center;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 11.5px;
  letter-spacing: 3.5px;
  color: #5eeaff;
  opacity: .9;
  text-shadow: 0 0 14px rgba(94, 234, 255, .6);
  margin-bottom: 10px;
}
.ssq-title {
  text-align: center;
  font-size: 34px;
  font-weight: 800;
  letter-spacing: 3px;
  margin: 4px 0 8px;
  background: linear-gradient(90deg, #baf7ff, #3fe0ff 45%, #7aa2ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  filter: drop-shadow(0 0 18px rgba(63, 224, 255, .35));
}
.ssq-sub { text-align: center; color: #93a8d0; font-size: 13.5px; line-height: 1.7; margin: 0 0 24px; }

.ctrl {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 22px;
}
.ctrl-label { font-size: 14px; color: #aebfe2; font-weight: 600; letter-spacing: 1px; }
.sel {
  padding: 10px 14px;
  font-size: 15px;
  border-radius: 10px;
  border: 1px solid rgba(94, 234, 255, .32);
  background: rgba(11, 21, 45, .85);
  color: #dbe7ff;
  cursor: pointer;
  outline: none;
  transition: border-color .2s, box-shadow .2s;
}
.sel option { background: #0b1530; color: #dbe7ff; }
.sel:focus { border-color: #5eeaff; box-shadow: 0 0 0 3px rgba(94, 234, 255, .15); }
.btn {
  border: none;
  cursor: pointer;
  padding: 11px 30px;
  font-size: 15.5px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #03131f;
  border-radius: 999px;
  background: linear-gradient(180deg, #3ee9ff, #1bb6e8 58%, #1586d6);
  box-shadow: 0 0 22px rgba(34, 211, 238, .45), 0 10px 22px rgba(13, 148, 220, .32);
  transition: transform .15s ease, box-shadow .2s ease, opacity .15s ease;
}
.btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 0 30px rgba(34, 211, 238, .65), 0 12px 26px rgba(13, 148, 220, .4); }
.btn:disabled { opacity: .55; cursor: default; }

.err {
  text-align: center;
  color: #ff9aa0;
  background: rgba(255, 60, 70, .1);
  border: 1px solid rgba(255, 90, 100, .3);
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 14px;
}

.result {
  background: linear-gradient(180deg, rgba(23, 40, 74, .68), rgba(12, 22, 46, .74));
  border: 1px solid rgba(94, 234, 255, .2);
  border-radius: 20px;
  padding: 30px 24px 24px;
  box-shadow: 0 20px 55px rgba(0, 0, 0, .45), inset 0 1px 0 rgba(255, 255, 255, .06);
  backdrop-filter: blur(8px);
}
.balls { display: flex; align-items: center; justify-content: center; gap: 11px; flex-wrap: wrap; }
.balls:not(.mini) .ball { animation: ballIn .5s cubic-bezier(.2, .9, .3, 1.35) both; }
.ball {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  font-size: 21px;
  font-weight: 800;
  color: #fff;
  font-family: 'Arial', sans-serif;
  border: 1px solid rgba(255, 255, 255, .28);
}
.ball.red {
  background: radial-gradient(circle at 32% 28%, #ff8a80, #ff3b46 55%, #c81e2c);
  box-shadow: inset -2px -4px 7px rgba(0, 0, 0, .32), 0 0 16px rgba(255, 80, 90, .55), 0 5px 12px rgba(0, 0, 0, .4);
}
.ball.blue {
  background: radial-gradient(circle at 32% 28%, #8fe9ff, #22b8ff 52%, #1763e0);
  box-shadow: inset -2px -4px 7px rgba(0, 0, 0, .3), 0 0 18px rgba(45, 180, 255, .62), 0 5px 12px rgba(0, 0, 0, .4);
}
.ball.s { width: 24px; height: 24px; font-size: 12px; border-width: 1px; box-shadow: inset -1px -2px 3px rgba(0,0,0,.25), 0 0 6px rgba(94,234,255,.25); }
.plus { font-size: 24px; font-weight: 800; color: #5eeaff; text-shadow: 0 0 12px rgba(94,234,255,.7); margin: 0 2px; }
.balls.mini { gap: 4px; }
@keyframes ballIn {
  from { opacity: 0; transform: translateY(12px) scale(.35); }
  60% { transform: translateY(-3px) scale(1.1); }
  to { opacity: 1; transform: none; }
}

.meta { margin-top: 24px; }
.meta-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding: 13px 0;
  border-top: 1px dashed rgba(94, 234, 255, .2);
}
.tag {
  background: rgba(94, 234, 255, .1);
  color: #7df0ff;
  border: 1px solid rgba(94, 234, 255, .3);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 3px 10px;
  border-radius: 6px;
}
.meta-code { font-size: 13.5px; color: #c6d6f5; font-weight: 600; }
.strategy { font-size: 13.5px; color: #cdd9f2; line-height: 1.75; margin: 14px 0 6px; }
.cold { font-size: 13px; color: #9fb0d4; line-height: 1.85; margin: 0; }
.cold b { color: #7df0ff; font-weight: 700; }
.shape { display: flex; flex-wrap: wrap; gap: 7px; margin: 12px 0 6px; }
.sh-chip {
  font-size: 12px;
  color: #7df0ff;
  background: rgba(34, 211, 238, .08);
  border: 1px solid rgba(94, 234, 255, .28);
  border-radius: 999px;
  padding: 3px 11px;
  font-weight: 600;
  letter-spacing: .5px;
}
.factors { margin: 8px 0 2px; padding-left: 18px; }
.factors li { font-size: 12.5px; color: #8ea2c8; line-height: 1.8; }

.history { margin-top: 20px; border-top: 1px solid rgba(94, 234, 255, .16); padding-top: 15px; }
.hist-title { font-size: 13.5px; font-weight: 700; letter-spacing: 1px; color: #7df0ff; margin-bottom: 10px; }
.hist-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px 0;
  flex-wrap: wrap;
}
.hist-code { font-size: 13px; color: #e6f1ff; font-weight: 700; width: 64px; font-family: ui-monospace, Menlo, Consolas, monospace; }
.hist-date { font-size: 12px; color: #7c90b8; width: 110px; }

.disclaimer {
  text-align: center;
  color: #8fa2c8;
  font-size: 12.5px;
  line-height: 1.9;
  margin: 28px auto 0;
  max-width: 580px;
}

.pop-enter-active { transition: all .35s cubic-bezier(.2, .8, .3, 1.2); }
.pop-enter-from { opacity: 0; transform: translateY(14px) scale(.98); }
</style>
