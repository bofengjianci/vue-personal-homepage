<template>
  <MainLayout :is-dark="userStore.isDark">
    <!-- 具名插槽 #header：顶部导航 -->
    <template #header>
      <AppHeader v-model:is-dark="userStore.isDark" />
    </template>

    <!-- 默认插槽：路由出口（RouterView）
         根据当前 URL 渲染对应页面组件：/home → HomeView、/projects → ProjectsView… -->
    <RouterView />

    <!-- 具名插槽 #footer：底部公共区 -->
    <template #footer>
      <AppFooter :profile-name="userStore.profile.name" />
    </template>
  </MainLayout>
</template>

<script setup>
// ===== 根组件：只负责公共布局组装 + 路由出口 =====
// 页面内容与业务数据都拆分到 views 页面组件 与 Pinia Store（userStore）中
import { useUserStore } from './stores/userStore'
import MainLayout from './components/MainLayout.vue'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'

const userStore = useUserStore()
</script>

<style>
/* ===== Element Plus 主题变量覆盖：主色改为与页面一致的青柠绿 ===== */
:root {
  --el-color-primary: #65a30d;
  --el-color-primary-light-3: #84cc16;
  --el-color-primary-light-5: #a3e635;
  --el-color-primary-light-7: #d9f99d;
  --el-color-primary-light-8: #ecfccb;
  --el-color-primary-light-9: #f7fee7;
  --el-color-primary-dark-2: #4d7c0f;
  --el-border-radius-base: 10px;
  --el-border-radius-small: 8px;
}

.card {
  background: var(--glass);
  backdrop-filter: blur(18px) saturate(1.5);
  -webkit-backdrop-filter: blur(18px) saturate(1.5);
  border: 1px solid var(--glass-border);
  border-radius: 18px;
  box-shadow: var(--glass-shadow);
  padding: 28px;
  transition: box-shadow 0.3s;
}

.profile-card { text-align: center; }
.avatar-wrap {
  width: 104px;
  height: 104px;
  margin: 0 auto 14px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid var(--border);
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  display: flex;
  align-items: center;
  justify-content: center;
}
.avatar-wrap img { width: 100%; height: 100%; object-fit: cover; }
.avatar-fallback { color: #fff; font-size: 44px; font-weight: 700; }
.name { font-size: 24px; margin-bottom: 4px; }
.major { color: var(--muted); font-size: 15px; margin-bottom: 10px; }
.motto { color: var(--accent); font-size: 14px; margin-bottom: 14px; }
.bio { font-size: 14px; line-height: 1.8; max-width: 620px; margin: 0 auto; }

.detail {
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px dashed var(--border);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  text-align: left;
}
.detail-item {
  background: var(--input-bg);
  border-radius: 12px;
  padding: 10px 14px;
}
.detail-item span { display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; }
.detail-item p { font-size: 14px; word-break: break-all; }

.btn-row { display: flex; justify-content: center; gap: 12px; margin-top: 20px; flex-wrap: wrap; }
.btn {
  padding: 10px 22px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text);
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.25s;
}
.btn:hover { transform: translateY(-1px); box-shadow: var(--shadow); }
.btn.primary {
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: #fff;
  border: none;
}

.skills-card { margin-top: 24px; }
.section-title { font-size: 18px; margin-bottom: 16px; }
.search-input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: var(--input-bg);
  color: var(--text);
  font-size: 14px;
  outline: none;
  transition: box-shadow 0.25s;
}
.search-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(101, 163, 13, 0.18);
}
.result-count { font-size: 13px; color: var(--muted); margin: 12px 2px; }
.skill-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 14px;
}
.skill-item {
  background: var(--glass-item);
  backdrop-filter: blur(12px) saturate(1.3);
  -webkit-backdrop-filter: blur(12px) saturate(1.3);
  border: 1px solid var(--glass-border);
  border-radius: 14px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: box-shadow 0.25s, transform 0.1s ease-out;
  will-change: transform;
}
.skill-item:hover { box-shadow: 0 12px 28px rgba(15, 23, 42, 0.14); }
.skill-icon {
  width: 46px;
  height: 46px;
  flex-shrink: 0;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}
.skill-info { flex: 1; min-width: 0; }
.skill-info h4 { font-size: 15px; margin-bottom: 2px; }
.skill-meta { font-size: 12px; color: var(--muted); margin-bottom: 8px; }
.level-bar { height: 6px; border-radius: 999px; background: var(--border); overflow: hidden; }
.level-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  transition: width 0.5s ease;
}
.empty-state { text-align: center; color: var(--muted); padding: 30px 0; font-size: 14px; }

.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(2, 6, 23, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}
.modal {
  width: min(600px, 100%);
  max-height: 88vh;
  overflow-y: auto;
  background: var(--card);
  border-radius: 18px;
  padding: 26px;
  box-shadow: var(--shadow);
}
.modal h3 { font-size: 18px; margin-bottom: 18px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 16px; }
.form-field { display: flex; flex-direction: column; gap: 6px; }
.form-field.full { grid-column: 1 / -1; }
.form-field label { font-size: 13px; color: var(--muted); }
.form-field input,
.form-field textarea,
.form-field select {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--input-bg);
  color: var(--text);
  font-size: 14px;
  outline: none;
  transition: border-color 0.25s;
}
.form-field input:focus,
.form-field textarea:focus,
.form-field select:focus { border-color: var(--accent); }
.modal-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 22px; }

.router-link-active { color: var(--accent); font-weight: 600; }
.router-link-exact-active {
  color: var(--accent);
  font-weight: 700;
  background: rgba(101, 163, 13, 0.12);
  border-radius: 999px;
  padding: 4px 12px;
}
</style>
