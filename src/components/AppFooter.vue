<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <p>© 2026 {{ profileName }}（学号：249981216）· Powered by Vue 3 + Vue Router</p>
      <p class="footer-links">
        <RouterLink to="/home" class="footer-link">首页</RouterLink>
        <span class="dot">·</span>
        <RouterLink to="/projects" class="footer-link">我的项目</RouterLink>
        <span class="dot">·</span>
        <RouterLink to="/about" class="footer-link">关于我</RouterLink>
      </p>
    </div>
  </footer>
</template>

<script setup>
// ===== 组件通信：props 向下传数据 =====
defineProps({
  profileName: { type: String, default: '刘博霖' }
})
</script>

<style scoped>
.app-footer {
  margin-top: 48px;
  border-top: 1px solid var(--glass-border);
  background: var(--glass-strong);
  backdrop-filter: blur(16px) saturate(1.4);
  -webkit-backdrop-filter: blur(16px) saturate(1.4);
}
.footer-inner {
  max-width: 860px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  color: var(--muted);
  font-size: 13px;
}
.footer-links { display: flex; align-items: center; gap: 8px; }
.footer-link { color: var(--muted); text-decoration: none; transition: color 0.25s; }
.footer-link:hover { color: var(--accent); }
.dot { opacity: 0.6; }
</style>
