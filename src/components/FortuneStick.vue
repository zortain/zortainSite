<script setup>
import { ref, computed } from 'vue'
import { fortunes, gradeMeta } from '../data/fortunes.js'

const phase = ref('idle') // idle | shaking | result
const current = ref(null)
let timer = null

const meta = computed(() => (current.value ? gradeMeta[current.value.grade] : null))

const digits = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
function toChineseNo(n) {
  if (n <= 10) return n === 10 ? '十' : digits[n]
  if (n < 20) return '十' + (n % 10 ? digits[n % 10] : '')
  const tens = digits[Math.floor(n / 10)] + '十'
  const ones = n % 10 ? digits[n % 10] : ''
  return tens + ones
}
const noText = computed(() => (current.value ? toChineseNo(current.value.no) : ''))
const btnText = computed(() => {
  if (phase.value === 'shaking') return '摇签中…'
  if (phase.value === 'result') return '再摇一签'
  return '心 诚 则 灵 · 摇 签'
})

function draw() {
  if (phase.value === 'shaking') return
  clearTimeout(timer)
  current.value = null
  phase.value = 'shaking'
  // 摇动约 2.2s 后出签
  timer = setTimeout(() => {
    const pick = fortunes[Math.floor(Math.random() * fortunes.length)]
    current.value = pick
    phase.value = 'result'
  }, 2200)
}
</script>

<template>
  <div class="fortune">
    <header class="f-head">
      <h1 class="f-title">摇&nbsp;签</h1>
      <p class="f-sub">静心默念所问之事，诚心摇签，随缘点化</p>
    </header>

    <!-- 签筒 -->
    <div class="altar">
      <div class="halo-ring" :class="{ ring: phase === 'result' }"></div>
      <div class="tube-wrap" :class="{ shaking: phase === 'shaking' }">
        <!-- 跳出的那支签 -->
        <div v-if="phase === 'result' && current" class="fly-stick" :style="{ background: meta.color }"></div>
        <svg class="tube" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
          <!-- 签条 -->
          <g>
            <rect x="78" y="24" width="7" height="66" rx="3.5" fill="#f4e4bc" stroke="#c9a35f" stroke-width="1.2" transform="rotate(-9 81 57)"/>
            <rect x="96" y="20" width="7" height="70" rx="3.5" fill="#f7ecc9" stroke="#c9a35f" stroke-width="1.2"/>
            <rect x="114" y="26" width="7" height="62" rx="3.5" fill="#f4e4bc" stroke="#c9a35f" stroke-width="1.2" transform="rotate(10 117 57)"/>
          </g>
          <!-- 筒身 -->
          <path d="M52 72 q48 22 96 0 l-9 92 q-39 18 -78 0 Z" fill="#c0392b"/>
          <path d="M52 72 q48 22 96 0 l-9 92 q-39 18 -78 0 Z" fill="url(#tubeShade)"/>
          <path d="M58 84 q42 17 84 0 l-7 74 q-35 15 -70 0 Z" fill="#8e2318" opacity="0.55"/>
          <!-- 金字竖匾 -->
          <rect x="84" y="100" width="32" height="52" rx="5" fill="#f3d27a" stroke="#8a6a1f" stroke-width="1.5"/>
          <text x="100" y="121" font-size="15" font-weight="700" fill="#7a2218" text-anchor="middle" font-family="serif">灵</text>
          <text x="100" y="140" font-size="15" font-weight="700" fill="#7a2218" text-anchor="middle" font-family="serif">签</text>
          <!-- 金箍 -->
          <path d="M52 72 q48 22 96 0 l-2 12 q-46 20 -92 0 Z" fill="#e8b94c"/>
          <path d="M52 72 q48 22 96 0 l-2 12 q-46 20 -92 0 Z" fill="url('#rimShade')"/>
          <ellipse cx="100" cy="72" rx="48" ry="12" fill="#f6d98a" stroke="#b0852c" stroke-width="2"/>
          <ellipse cx="100" cy="71" rx="38" ry="8" fill="#6e1d13"/>
          <!-- 底座 -->
          <ellipse cx="100" cy="168" rx="56" ry="10" fill="#7c1f15"/>
          <ellipse cx="100" cy="165" rx="56" ry="9" fill="#a52b1d"/>
          <defs>
            <linearGradient id="tubeShade" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stop-color="#ffffff" stop-opacity="0.22"/>
              <stop offset="0.5" stop-color="#ffffff" stop-opacity="0"/>
              <stop offset="1" stop-color="#000000" stop-opacity="0.22"/>
            </linearGradient>
            <linearGradient id="rimShade" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#fff3cf"/>
              <stop offset="1" stop-color="#d19a2e"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
      <!-- 香烟/光晕点缀 -->
      <div class="altar-base"></div>
    </div>

    <button class="f-btn" :disabled="phase === 'shaking'" @click="draw">{{ btnText }}</button>
    <p class="f-note">签文取自民间流传《观音灵签》，博君一笑 · 命运始终掌握在自己手中</p>

    <!-- 签文结果 -->
    <transition name="sheet">
      <div v-if="phase === 'result' && current && meta" class="sheet-mask" @click.self="phase = 'idle'">
        <div class="sheet" :style="{ background: meta.bg }">
          <div class="sheet-top">
            <span class="seal" :style="{ background: meta.color }">签</span>
            <div class="sheet-no" :style="{ color: meta.color }">第 {{ noText }}签</div>
            <span class="palace">{{ current.palace }}</span>
          </div>

          <div class="grade-badge" :style="{ background: meta.color }">{{ meta.label }}</div>
          <div class="grade-sub">{{ meta.sub }} · {{ current.image }}</div>

          <div class="poem">
            <p v-for="(line, i) in current.poem" :key="i">{{ line.replace(/[；;，,。]$/, '') }}</p>
          </div>

          <div class="verse-block">
            <div class="verse-h">解曰 · 原签</div>
            <p class="verse-classic">{{ current.classic }}</p>
          </div>
          <div class="verse-block">
            <div class="verse-h" :style="{ color: meta.color }">白话点化</div>
            <p class="verse-meaning">{{ current.meaning }}</p>
          </div>

          <div class="sheet-actions">
            <button class="sheet-btn ghost" @click="phase = 'idle'">收 下</button>
            <button class="sheet-btn solid" :style="{ background: meta.color }" @click="draw">再摇一签</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
* { box-sizing: border-box; }
.fortune {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 16px 40px;
  color: #4a3320;
}
.f-head { text-align: center; }
.f-title {
  margin: 0;
  font-size: 52px;
  letter-spacing: 6px;
  color: #c0392b;
  text-shadow: 0 3px 0 #f3d9b0;
}
.f-sub { margin: 10px 0 0; font-size: 14px; color: #9a6f52; }

/* 签筒区 */
.altar {
  position: relative;
  width: 240px;
  height: 240px;
  margin: 24px 0 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.halo-ring {
  position: absolute;
  width: 190px; height: 190px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(243, 210, 122, .5) 0%, rgba(243, 210, 122, 0) 68%);
  opacity: .5;
  transition: transform .5s ease, opacity .5s ease;
}
.halo-ring.ring { animation: glow 1.6s ease-in-out infinite alternate; }
@keyframes glow { from { transform: scale(.9); opacity: .4; } to { transform: scale(1.12); opacity: .95; } }

.tube-wrap { position: relative; width: 200px; height: 200px; transform-origin: 50% 92%; }
.tube { width: 100%; height: 100%; filter: drop-shadow(0 14px 18px rgba(120, 40, 20, .28)); }
.tube-wrap.shaking { animation: shake .5s ease-in-out infinite; }
@keyframes shake {
  0%   { transform: rotate(0deg); }
  20%  { transform: rotate(-9deg); }
  40%  { transform: rotate(8deg); }
  60%  { transform: rotate(-6deg); }
  80%  { transform: rotate(5deg); }
  100% { transform: rotate(0deg); }
}
/* 跳出的签 */
.fly-stick {
  position: absolute;
  left: 50%;
  top: 18px;
  width: 8px;
  height: 96px;
  margin-left: -4px;
  border-radius: 4px;
  z-index: 2;
  transform-origin: bottom center;
  animation: flyUp .7s cubic-bezier(.2, .8, .3, 1.1) forwards;
  box-shadow: 0 4px 10px rgba(0, 0, 0, .25);
}
@keyframes flyUp {
  0% { transform: translateY(60px) scaleY(.3); opacity: 0; }
  60% { opacity: 1; }
  100% { transform: translateY(-46px) scaleY(1); opacity: 1; }
}

.f-btn {
  border: none;
  cursor: pointer;
  padding: 16px 50px;
  font-size: 21px;
  font-weight: 700;
  letter-spacing: 4px;
  color: #fff8ea;
  border-radius: 999px;
  background: linear-gradient(180deg, #d8503f 0%, #b32c20 100%);
  box-shadow: 0 10px 22px rgba(179, 44, 32, .38), inset 0 2px 0 rgba(255, 255, 255, .28);
  transition: transform .12s ease, box-shadow .12s ease, opacity .2s;
}
.f-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 14px 26px rgba(179, 44, 32, .45), inset 0 2px 0 rgba(255,255,255,.28); }
.f-btn:active:not(:disabled) { transform: translateY(0); }
.f-btn:disabled { opacity: .72; cursor: not-allowed; }
.f-note { margin: 14px 0 0; font-size: 12px; color: #b09077; text-align: center; max-width: 320px; line-height: 1.6; }

/* 结果签纸 */
.sheet-mask {
  position: fixed;
  inset: 0;
  background: rgba(60, 30, 18, .5);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 50;
}
.sheet {
  position: relative;
  width: 430px;
  max-width: 100%;
  max-height: 90vh;
  overflow: auto;
  border-radius: 18px;
  padding: 24px 26px 26px;
  box-shadow: 0 30px 70px rgba(0, 0, 0, .32), inset 0 0 0 2px rgba(255, 255, 255, .5);
}
.sheet::before {
  content: '';
  position: absolute;
  inset: 10px;
  border: 1.5px solid rgba(150, 90, 40, .35);
  border-radius: 12px;
  pointer-events: none;
}
.sheet-top { display: flex; align-items: center; justify-content: center; gap: 10px; position: relative; z-index: 1; }
.seal {
  color: #fff;
  width: 34px; height: 34px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 8px;
  font-size: 18px; font-weight: 700;
  font-family: serif;
}
.sheet-no { font-size: 20px; font-weight: 700; letter-spacing: 2px; font-family: 'STKaiti', 'KaiTi', serif; }
.palace { font-size: 12px; color: #9a7a52; border: 1px solid rgba(150,120,80,.5); border-radius: 6px; padding: 2px 8px; }

.grade-badge {
  margin: 14px auto 0;
  width: fit-content;
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 6px;
  padding: 7px 26px 7px 32px;
  border-radius: 999px;
  box-shadow: 0 6px 14px rgba(0,0,0,.18);
}
.grade-sub { text-align: center; margin: 9px 0 4px; font-size: 13.5px; color: #7a5a3c; letter-spacing: 1px; }

.poem {
  margin: 14px 0 16px;
  text-align: center;
  font-family: 'STKaiti', 'KaiTi', 'Songti SC', serif;
  color: #5a3a22;
}
.poem p { margin: 4px 0; font-size: 18px; line-height: 1.9; letter-spacing: 1px; }

.verse-block {
  position: relative;
  z-index: 1;
  background: rgba(255, 255, 255, .55);
  border-radius: 12px;
  padding: 11px 14px;
  margin-bottom: 10px;
  text-align: left;
}
.verse-h { font-size: 13px; font-weight: 700; color: #9a6f3a; margin-bottom: 4px; letter-spacing: 1px; }
.verse-classic { margin: 0; font-size: 13px; line-height: 1.75; color: #8a6f55; }
.verse-meaning { margin: 0; font-size: 14.5px; line-height: 1.8; color: #4a3320; }

.sheet-actions { display: flex; gap: 12px; justify-content: center; margin-top: 18px; position: relative; z-index: 1; }
.sheet-btn {
  border: none; cursor: pointer;
  padding: 12px 30px;
  font-size: 16px; font-weight: 700; letter-spacing: 2px;
  border-radius: 999px;
}
.sheet-btn.ghost { background: rgba(255,255,255,.7); color: #7a5238; box-shadow: inset 0 0 0 1.5px rgba(150,110,70,.4); }
.sheet-btn.solid { color: #fff; box-shadow: 0 8px 16px rgba(0,0,0,.2); }

.sheet-enter-active .sheet { animation: sheetIn .42s cubic-bezier(.2,.9,.3,1.15); }
.sheet-enter-from { opacity: 0; }
@keyframes sheetIn {
  0% { transform: translateY(40px) scale(.85); opacity: 0; }
  100% { transform: translateY(0) scale(1); opacity: 1; }
}
@media (max-width: 520px) {
  .sheet { width: 100%; padding: 20px 18px 22px; }
  .poem p { font-size: 16.5px; }
}
</style>
