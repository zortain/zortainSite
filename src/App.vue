<script setup>
import { ref } from 'vue'

const message = ref('你好呀，小皮')
</script>

<template>
  <main class="container">
    <h1 class="greeting">{{ message }}</h1>
  </main>
</template>

<style scoped>
.container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0b0d12;
}

.greeting {
  margin: 0;
  color: #ffffff;
  font-size: clamp(2rem, 6vw, 4rem);
  font-weight: 700;
  letter-spacing: 0.02em;
}
</style>
