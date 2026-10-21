<template>
  <!-- ===== 404 页面：所有未匹配的 URL 都由路由兜底到这里 ===== -->
  <section class="card nf-card">
    <div class="nf-code">404</div>
    <h2 class="nf-title">页面未找到</h2>
    <p class="nf-desc">您访问的地址 <code class="nf-path">{{ route.fullPath }}</code> 不存在，可能已被移动或输入有误。</p>
    <div class="nf-actions">
      <button class="btn" @click="router.back()">← 返回上一页</button>
      <button class="btn primary" @click="router.push({ name: 'home' })">🏠 回到首页</button>
    </div>
  </section>
</template>

<script setup>
// ===== 404：useRoute 取当前地址，useRouter 提供返回/回首页 =====
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
</script>

<style scoped>
.nf-card { text-align: center; padding: 60px 28px; }
.nf-code {
  font-size: 72px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  line-height: 1.1;
}
.nf-title { font-size: 22px; margin: 16px 0 10px; }
.nf-desc { color: var(--muted); font-size: 14px; margin-bottom: 24px; }
.nf-path {
  background: var(--input-bg);
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 13px;
  word-break: break-all;
}
.nf-actions { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
</style>
