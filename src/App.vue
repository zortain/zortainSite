<script setup>
import { ref, computed } from 'vue'
import { dishes } from './data/dishes.js'
import FoodIcon from './components/FoodIcon.vue'

const N = dishes.length
const rand = (min, max) => Math.random() * (max - min) + min
const mod = (n, m) => ((n % m) + m) % m

// 展示用的环形序列索引（只渲染当前位置附近 7 个，兼顾性能）
const pos = ref(2 * N) // 初始停在第 3 组，保证左右有足够项
const spinning = ref(false)
const result = ref(null) // 最终选中的餐点对象

const centerId = computed(() => dishes[mod(pos.value, N)].id)

// 需要渲染的相对位置：-3..3
const slots = computed(() => {
  const list = []
  for (let off = -3; off <= 3; off++) {
    const p = pos.value + off
    list.push({ off, dish: dishes[mod(p, N)], key: p })
  }
  return list
})

// 每项的横向位置 / 缩放 / 层级 / 透明度
function styleFor(off) {
  const SP = 128 // 单项间距 px
  const x = off * SP
  const d = Math.abs(off)
  let scale
  if (spinning.value) scale = d === 0 ? 1 : 0.92 - Math.min(d, 2) * 0.03 // 滚动时缩放差异小，突出“流动”
  else scale = d === 0 ? 1.28 : d === 1 ? 0.82 : d === 2 ? 0.6 : 0 // 静止：中间放大，两侧递减，其余隐藏
  const z = 10 - d
  const opacity = !spinning.value && d >= 3 ? 0 : 1
  return {
    transform: `translateX(${x}px) scale(${scale})`,
    zIndex: z,
    opacity,
    filter: d >= 2 ? 'saturate(0.9)' : 'none'
  }
}

function pick() {
  if (spinning.value) return
  result.value = null
  spinning.value = true

  // 随机抽一个最终餐点
  const winnerIndex = Math.floor(Math.random() * N)
  const duration = rand(3000, 7000) // 3s ~ 7s

  // 目标位置：在当前基础上至少再走 6 整圈，然后对齐到 winner
  const start = pos.value
  const cur = mod(start, N)
  let delta = mod(winnerIndex - cur, N) + 6 * N
  const target = start + delta

  const startTs = performance.now()
  // ease-out-cubic：开始快、结尾慢
  const ease = (t) => 1 - Math.pow(1 - t, 3)

  function frame(now) {
    const t = Math.min(1, (now - startTs) / duration)
    pos.value = Math.round(start + (target - start) * ease(t))
    if (t < 1) {
      requestAnimationFrame(frame)
    } else {
      pos.value = target
      spinning.value = false
      result.value = dishes[winnerIndex]
    }
  }
  requestAnimationFrame(frame)
}

function again() {
  result.value = null
}
</script>

<template>
  <div class="page">
    <header class="head">
      <h1 class="title">吃&nbsp;啥</h1>
      <p class="subtitle">选择困难症救星 · {{ N }} 种人气餐点，命运替你决定</p>
    </header>

    <section class="stage">
      <div class="pointer">▼</div>
      <div class="viewport">
        <div
          v-for="s in slots"
          :key="s.key"
          class="item"
          :class="{ winner: !spinning && s.off === 0 && result }"
          :style="styleFor(s.off)"
        >
          <span v-if="!spinning && s.off === 0 && result" class="winner-halo"></span>
          <FoodIcon :id="s.dish.id" />
        </div>
      </div>
      <div class="cur-name">{{ dishes[((pos % N) + N) % N].name }}</div>
    </section>

    <button class="pick-btn" :disabled="spinning" @click="pick">
      {{ spinning ? '美味转转转…' : result ? '再来一次' : '帮我点餐' }}
    </button>

    <!-- 结果弹窗 -->
    <transition name="pop">
      <div v-if="result" class="modal-mask" @click.self="again">
        <div class="modal">
          <div class="modal-tag">今天就吃它啦 🎉</div>
          <div class="modal-icon"><FoodIcon :id="result.id" /></div>
          <h2 class="modal-name">{{ result.name }}</h2>
          <div class="modal-region">{{ result.region }}</div>
          <div class="modal-tags">
            <span v-for="t in result.tags" :key="t" class="tag">{{ t }}</span>
          </div>
          <p class="modal-desc">{{ result.desc }}</p>
          <button class="modal-btn" @click="again">就这么定了，开吃！</button>
        </div>
      </div>
    </transition>

    <footer class="foot">随机时长 3–7 秒 · 结果纯前端生成</footer>
  </div>
</template>

<style scoped>
* { box-sizing: border-box; }

.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 36px 16px 40px;
  background:
    radial-gradient(1100px 500px at 50% -160px, #ffe9c7 0%, rgba(255, 233, 199, 0) 60%),
    linear-gradient(180deg, #fff8ef 0%, #fff3e0 100%);
  color: #4a3320;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Hiragino Sans GB', system-ui, sans-serif;
}

.head { text-align: center; }
.title {
  margin: 0;
  font-size: 52px;
  letter-spacing: 6px;
  color: #e8663a;
  text-shadow: 0 3px 0 #ffd9a8;
}
.subtitle { margin: 10px 0 0; font-size: 14px; color: #a07a55; }

.stage {
  position: relative;
  width: 640px;
  max-width: 100%;
  margin: 26px 0 22px;
}
.pointer {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  color: #e8663a;
  font-size: 22px;
  z-index: 20;
  filter: drop-shadow(0 2px 2px rgba(0, 0, 0, .15));
}
.viewport {
  position: relative;
  height: 260px;
  overflow: hidden;
  border-radius: 28px;
  background: rgba(255, 255, 255, .65);
  box-shadow: inset 0 0 0 2px rgba(232, 102, 58, .12), 0 10px 30px rgba(201, 120, 60, .12);
  -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 16%, #000 84%, transparent 100%);
  mask-image: linear-gradient(90deg, transparent 0, #000 16%, #000 84%, transparent 100%);
}
.item {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 150px;
  height: 150px;
  margin: -75px 0 0 -75px;
  transform-origin: center center;
  will-change: transform;
}
.winner-halo {
  position: absolute;
  inset: -6%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 200, 90, .55) 0%, rgba(255, 200, 90, 0) 70%);
  animation: halo 1.1s ease-in-out infinite alternate;
  z-index: -1;
}
@keyframes halo {
  from { transform: scale(.92); opacity: .5; }
  to { transform: scale(1.12); opacity: 1; }
}
.cur-name {
  margin-top: 14px;
  text-align: center;
  font-size: 22px;
  font-weight: 700;
  color: #6b4423;
  min-height: 30px;
}

.pick-btn {
  border: none;
  cursor: pointer;
  padding: 16px 58px;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 3px;
  color: #fff;
  border-radius: 999px;
  background: linear-gradient(180deg, #ff8a4c 0%, #e8663a 100%);
  box-shadow: 0 10px 22px rgba(232, 102, 58, .38), inset 0 2px 0 rgba(255, 255, 255, .35);
  transition: transform .12s ease, box-shadow .12s ease, opacity .2s;
}
.pick-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 14px 26px rgba(232, 102, 58, .45), inset 0 2px 0 rgba(255,255,255,.35); }
.pick-btn:active:not(:disabled) { transform: translateY(0); }
.pick-btn:disabled { opacity: .7; cursor: not-allowed; }

/* 弹窗 */
.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(74, 51, 32, .45);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 50;
}
.modal {
  width: 420px;
  max-width: 100%;
  max-height: 90vh;
  overflow: auto;
  background: #fffdf9;
  border-radius: 26px;
  padding: 26px 26px 28px;
  text-align: center;
  box-shadow: 0 30px 70px rgba(0, 0, 0, .28);
}
.modal-tag { color: #e8663a; font-weight: 700; font-size: 16px; }
.modal-icon { width: 170px; height: 170px; margin: 6px auto 4px; animation: popin .5s ease; }
.modal-name { margin: 6px 0 2px; font-size: 30px; color: #4a3320; }
.modal-region { color: #a07a55; font-size: 14px; margin-bottom: 10px; }
.modal-tags { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-bottom: 12px; }
.tag {
  font-size: 12px;
  color: #c25a2e;
  background: #ffe9d8;
  border-radius: 999px;
  padding: 4px 12px;
}
.modal-desc {
  font-size: 14.5px;
  line-height: 1.8;
  color: #6b5340;
  text-align: left;
  margin: 0 0 20px;
}
.modal-btn {
  border: none;
  cursor: pointer;
  padding: 13px 40px;
  font-size: 17px;
  font-weight: 700;
  color: #fff;
  border-radius: 999px;
  background: linear-gradient(180deg, #ff8a4c 0%, #e8663a 100%);
  box-shadow: 0 8px 18px rgba(232, 102, 58, .35);
}

.foot { margin-top: 26px; font-size: 12px; color: #b89a7d; }

@keyframes popin {
  0% { transform: scale(.4) rotate(-8deg); opacity: 0; }
  70% { transform: scale(1.08) rotate(2deg); }
  100% { transform: scale(1) rotate(0); opacity: 1; }
}
.pop-enter-active .modal { animation: popin .35s ease; }
.pop-enter-from { opacity: 0; }
</style>
