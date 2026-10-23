<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: { type: String, required: true }
})

// 通过 Vite 的 raw 导入直接内嵌 SVG（透明背景、矢量、可随容器缩放）
const modules = import.meta.glob('../assets/food/*.svg', {
  query: '?raw',
  import: 'default',
  eager: true
})
const map = {}
for (const key in modules) {
  const name = key.split('/').pop().replace('.svg', '')
  map[name] = modules[key]
}
const html = computed(() => map[props.id] || '')
</script>

<template>
  <span class="food-icon" v-html="html" aria-hidden="true"></span>
</template>

<style scoped>
.food-icon {
  display: inline-flex;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: center;
  line-height: 0;
}
.food-icon :deep(svg) {
  width: 100%;
  height: 100%;
  display: block;
}
</style>
