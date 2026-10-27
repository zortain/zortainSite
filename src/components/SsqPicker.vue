<script setup>
import { ref } from 'vue'

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
</script>

<template>
  <div class="ssq">
    <h1 class="ssq-title">双色球预测</h1>
    <p class="ssq-sub">基于近 N 期真实开奖，开出越多的号码被选中的概率越低</p>

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
          <span v-for="x in data.predict.red" :key="'r' + x" class="ball red">{{ pad(x) }}</span>
          <span class="plus">+</span>
          <span class="ball blue">{{ pad(data.predict.blue) }}</span>
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
      本结果由历史频次加权随机生成，彩票开奖为独立随机事件，任何方法均无法预测，仅供娱乐，请理性购彩。
    </p>
  </div>
</template>

<style scoped>
.ssq {
  max-width: 720px;
  margin: 0 auto;
  padding: 26px 18px 60px;
  color: #2b2b2b;
}
.ssq-title {
  text-align: center;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: 2px;
  margin: 6px 0 6px;
  background: linear-gradient(90deg, #d62828, #1d4ed8);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.ssq-sub { text-align: center; color: #777; font-size: 13.5px; margin: 0 0 22px; }

.ctrl {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
.ctrl-label { font-size: 14px; color: #555; font-weight: 600; }
.sel {
  padding: 10px 14px;
  font-size: 15px;
  border-radius: 10px;
  border: 1.5px solid #d9c3ad;
  background: #fff;
  color: #333;
  cursor: pointer;
  outline: none;
}
.sel:focus { border-color: #d62828; }
.btn {
  border: none;
  cursor: pointer;
  padding: 11px 26px;
  font-size: 15.5px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #fff;
  border-radius: 999px;
  background: linear-gradient(180deg, #e8403a, #c11f1c);
  box-shadow: 0 8px 18px rgba(193, 31, 28, .32);
  transition: transform .15s ease, opacity .15s ease;
}
.btn:hover:not(:disabled) { transform: translateY(-1px); }
.btn:disabled { opacity: .6; cursor: default; }

.err {
  text-align: center;
  color: #c11f1c;
  background: #fdecec;
  border: 1px solid #f3c4c4;
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 14px;
}

.result {
  background: #fff;
  border-radius: 18px;
  padding: 26px 22px;
  box-shadow: 0 10px 30px rgba(120, 70, 30, .10);
}
.balls { display: flex; align-items: center; justify-content: center; gap: 10px; flex-wrap: wrap; }
.ball {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  font-size: 20px;
  font-weight: 800;
  color: #fff;
  font-family: 'Arial', sans-serif;
  box-shadow: inset -2px -3px 5px rgba(0, 0, 0, .18), 0 3px 6px rgba(0, 0, 0, .18);
}
.ball.red { background: radial-gradient(circle at 32% 28%, #ff6b63, #d62828 70%); }
.ball.blue { background: radial-gradient(circle at 32% 28%, #4d8bff, #1d4ed8 72%); }
.ball.s { width: 24px; height: 24px; font-size: 12px; box-shadow: inset -1px -2px 3px rgba(0,0,0,.18); }
.plus { font-size: 22px; font-weight: 800; color: #999; margin: 0 2px; }
.balls.mini { gap: 4px; }

.meta { margin-top: 22px; }
.meta-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding: 12px 0;
  border-top: 1px dashed #ead9c6;
}
.tag {
  background: #fdeceb;
  color: #c11f1c;
  font-size: 12px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 6px;
}
.meta-code { font-size: 13.5px; color: #555; font-weight: 600; }
.strategy { font-size: 13.5px; color: #444; line-height: 1.7; margin: 12px 0 6px; }
.cold { font-size: 13px; color: #666; line-height: 1.8; margin: 0; }
.cold b { color: #1d4ed8; font-weight: 700; }

.history { margin-top: 18px; border-top: 1px solid #f0e4d6; padding-top: 14px; }
.hist-title { font-size: 13.5px; font-weight: 700; color: #8a6a48; margin-bottom: 10px; }
.hist-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px 0;
  flex-wrap: wrap;
}
.hist-code { font-size: 13px; color: #333; font-weight: 700; width: 64px; }
.hist-date { font-size: 12px; color: #999; width: 116px; }

.disclaimer {
  text-align: center;
  color: #a58f78;
  font-size: 12px;
  line-height: 1.8;
  margin: 26px auto 0;
  max-width: 560px;
}

.pop-enter-active { transition: all .35s cubic-bezier(.2, .8, .3, 1.2); }
.pop-enter-from { opacity: 0; transform: translateY(14px) scale(.98); }
</style>
