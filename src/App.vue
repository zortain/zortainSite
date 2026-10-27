<script setup>
import { ref } from 'vue'
import FoodPicker from './components/FoodPicker.vue'
import FortuneStick from './components/FortuneStick.vue'
import SsqPicker from './components/SsqPicker.vue'

const tab = ref('food') // food | fortune | ssq
</script>

<template>
  <div class="app" :class="'theme-' + tab">
    <nav class="tabs">
      <button class="tab" :class="{ on: tab === 'food' }" @click="tab = 'food'">
        <span class="tab-ico">🍜</span><span>今天吃啥</span>
      </button>
      <button class="tab" :class="{ on: tab === 'fortune' }" @click="tab = 'fortune'">
        <span class="tab-ico">🎋</span><span>摇签测吉凶</span>
      </button>
      <button class="tab" :class="{ on: tab === 'ssq' }" @click="tab = 'ssq'">
        <span class="tab-ico">🎱</span><span>双色球预测</span>
      </button>
    </nav>

    <main class="panels">
      <div v-show="tab === 'food'" class="panel"><FoodPicker /></div>
      <div v-show="tab === 'fortune'" class="panel"><FortuneStick /></div>
      <div v-show="tab === 'ssq'" class="panel"><SsqPicker /></div>
    </main>
  </div>
</template>

<style scoped>
* { box-sizing: border-box; }
.app {
  min-height: 100vh;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Hiragino Sans GB', system-ui, sans-serif;
  transition: background .4s ease;
}
.theme-food {
  background:
    radial-gradient(1100px 500px at 50% -160px, #ffe9c7 0%, rgba(255, 233, 199, 0) 60%),
    linear-gradient(180deg, #fff8ef 0%, #fff3e0 100%);
}
.theme-fortune {
  background:
    radial-gradient(1100px 520px at 50% -180px, #ffe6d6 0%, rgba(255, 224, 205, 0) 62%),
    linear-gradient(180deg, #fff7ef 0%, #fdeee2 100%);
}
.theme-ssq {
  background:
    radial-gradient(1100px 520px at 50% -180px, #eef3ff 0%, rgba(224, 232, 255, 0) 62%),
    linear-gradient(180deg, #fbfcff 0%, #f1f4fb 100%);
}

.tabs {
  position: sticky;
  top: 0;
  z-index: 30;
  display: flex;
  justify-content: center;
  gap: 10px;
  padding: 14px 12px 12px;
  background: rgba(255, 251, 245, .82);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(190, 130, 70, .14);
}
.tab {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  border: none;
  cursor: pointer;
  padding: 10px 22px;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #9a7148;
  background: transparent;
  border-radius: 999px;
  transition: all .22s ease;
}
.tab .tab-ico { font-size: 18px; line-height: 1; }
.tab:hover { color: #7a4a26; background: rgba(255, 255, 255, .6); }
.theme-food .tab.on {
  color: #fff;
  background: linear-gradient(180deg, #ff8a4c 0%, #e8663a 100%);
  box-shadow: 0 8px 18px rgba(232, 102, 58, .35);
}
.theme-fortune .tab.on {
  color: #fff8ea;
  background: linear-gradient(180deg, #d8503f 0%, #b32c20 100%);
  box-shadow: 0 8px 18px rgba(179, 44, 32, .35);
}
.theme-ssq .tab.on {
  color: #fff;
  background: linear-gradient(180deg, #e8403a 0%, #1d4ed8 130%);
  box-shadow: 0 8px 18px rgba(29, 78, 216, .30);
}

.panels { width: 100%; }
.panel { animation: fadeUp .32s ease; }
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
