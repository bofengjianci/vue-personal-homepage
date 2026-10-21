<template>
  <header class="app-header">
    <div class="header-inner">
      <!-- Logo 点击回首页（含姓名+学号身份标识） -->
      <RouterLink to="/home" class="logo">
        ✨ 我的个人主页
        <span class="logo-id">刘博霖 · 249981216</span>
      </RouterLink>

      <!-- ===== Element Plus 菜单组件实现导航 =====
           el-menu：水平菜单，router 模式（点击 index 自动 router.push）
           default-active 绑定当前路由路径 → 自动高亮当前页面 -->
      <el-menu
        class="nav-menu"
        mode="horizontal"
        :default-active="route.path"
        :router="true"
        :ellipsis="false"
      >
        <el-menu-item
          v-for="item in navItems"
          :key="item.path"
          :index="item.path"
        >{{ item.label }}</el-menu-item>
      </el-menu>

      <div class="header-right">
        <!-- 后台管理入口：访客点击会先被路由守卫引导到登录页 -->
        <RouterLink class="admin-link" :to="{ name: 'admin' }">🔒 后台管理</RouterLink>
        <!-- el-button：Element Plus 按钮（text 幽灵样式）切换明暗主题 -->
        <el-button class="theme-btn" text bg @click="handleToggleTheme">
          {{ isDark ? '🌞 亮色' : '🌙 暗色' }}
        </el-button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// ===== 导航项配置（path 为路由路径，供 el-menu router 模式跳转）=====
// 新增页面时在这里添加一项：{ path: 路由路径, label: 显示文字 }
const navItems = ref([
  { path: '/home', label: '首页' },
  { path: '/projects', label: '项目' },
  { path: '/articles', label: '文章' },
  { path: '/about', label: '关于' }
])

// ===== 组件通信：defineModel 双向绑定 =====
const isDark = defineModel('is-dark', { type: Boolean, default: false })

function handleToggleTheme() {
  isDark.value = !isDark.value
}
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: var(--glass-strong);
  backdrop-filter: blur(16px) saturate(1.4);
  -webkit-backdrop-filter: blur(16px) saturate(1.4);
  border-bottom: 1px solid var(--glass-border);
  box-shadow: var(--shadow);
}
.header-inner {
  max-width: 860px;
  margin: 0 auto;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.logo {
  display: inline-flex;
  align-items: baseline;
  gap: 8px;
  font-size: 20px;
  white-space: nowrap;
  text-decoration: none;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.logo-id {
  font-size: 12px;
  color: var(--muted);
  background: none;
  -webkit-background-clip: initial;
  background-clip: initial;
  -webkit-text-fill-color: var(--muted);
}

/* ===== el-menu 导航样式覆盖：透明玻璃底 + 青柠绿高亮 ===== */
.nav-menu {
  background: transparent;
  border-bottom: none;
  --el-menu-hover-bg-color: transparent;
  --el-menu-active-color: var(--accent);
  --el-menu-text-color: var(--muted);
  --el-menu-item-height: 40px;
}
.nav-menu .el-menu-item {
  background: transparent;
  font-size: 14px;
  border-radius: 999px;
  margin: 0 4px;
  color: var(--muted);
}
.nav-menu .el-menu-item:hover {
  color: var(--accent);
  background: rgba(101, 163, 13, 0.08);
}
.nav-menu .el-menu-item.is-active {
  color: var(--accent);
  font-weight: 700;
  background: rgba(101, 163, 13, 0.12);
}

.header-right { display: flex; align-items: center; gap: 12px; }
.admin-link {
  color: var(--muted);
  text-decoration: none;
  font-size: 13px;
  transition: color 0.25s;
}
.admin-link:hover { color: var(--accent); }
.theme-btn {
  border-radius: 999px;
  border: 1px solid var(--border) !important;
  background: var(--input-bg) !important;
  color: var(--text) !important;
  font-size: 13px;
}

@media (max-width: 640px) {
  .header-inner { flex-wrap: wrap; }
  .nav-menu { order: 3; width: 100%; justify-content: center; }
  .nav-menu .el-menu-item { margin: 0 8px; }
}
</style>
