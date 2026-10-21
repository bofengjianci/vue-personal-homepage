<template>
  <!-- ===== 项目详情页（动态路由 /projects/:id）===== -->
  <div class="card detail-card">
    <!-- 有效项目：显示详情 -->
    <template v-if="project">
      <div class="detail-cover">
        <img v-if="coverOk && project.image" :src="project.image" :alt="project.name" @error="coverOk = false">
        <div v-else class="detail-cover-fallback">{{ project.name.charAt(0) }}</div>
        <span v-if="project.featured" class="featured-badge">⭐ 着重项目</span>
      </div>

      <div class="detail-head">
        <h2 class="detail-name">{{ project.name }}</h2>
        <span class="status-badge" :class="statusClass">{{ project.status }}</span>
      </div>

      <p class="detail-desc">{{ project.description }}</p>

      <div v-if="project.tags && project.tags.length" class="project-tags">
        <span v-for="tag in project.tags" :key="tag" class="tag">{{ tag }}</span>
      </div>

      <div class="detail-meta">
        <span>项目 ID：{{ project.id }}</span>
        <span>URL 参数：{{ route.params.id }}</span>
      </div>

      <div class="detail-actions">
        <!-- 编程式导航：返回上一页（浏览器历史后退） -->
        <button class="btn" @click="goBack">← 返回上一页</button>
        <!-- 编程式导航：返回项目列表 -->
        <button class="btn primary" @click="goList">返回项目列表</button>
      </div>
    </template>

    <!-- 无效详情地址（找不到对应项目）：
         显示友好提示 + 提供返回列表入口，而不是直接报错 -->
    <div v-else class="not-found-inner">
      <div class="nf-icon">🔍</div>
      <h2 class="nf-title">未找到该项目</h2>
      <p class="nf-desc">地址 {{ route.fullPath }} 中的项目 ID "{{ route.params.id }}" 不存在，可能已被删除或地址有误。</p>
      <div class="detail-actions">
        <button class="btn" @click="goBack">← 返回上一页</button>
        <button class="btn primary" @click="goList">返回项目列表</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// ===== 项目详情：useRoute() 读取动态参数，useRouter() 编程式跳转 =====
// Pinia：projectStore.findProject 根据 :id 查找项目（找不到返回 undefined → 无效地址分支）
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectStore } from '../stores/projectStore'

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()

// 通过动态路由参数 :id 在 projectStore 中查找项目
const project = computed(() => projectStore.findProject(route.params.id))

// 封面图加载失败回退占位
const coverOk = ref(true)
watch(() => project.value?.image, () => { coverOk.value = true })

// 状态 → 徽章样式类
const statusClass = computed(() => {
  if (project.value?.status === '已完成') return 'status-done'
  if (project.value?.status === '进行中') return 'status-doing'
  return 'status-planning'
})

// 编程式导航：返回上一页（useRouter().back()）
function goBack() {
  router.back()
}

// 编程式导航：返回项目列表（命名路由跳转）
function goList() {
  router.push({ name: 'projects' })
}
</script>

<style scoped>
.detail-card { text-align: left; }
.detail-cover {
  position: relative;
  height: 220px;
  border-radius: 14px;
  overflow: hidden;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  margin-bottom: 20px;
}
.detail-cover img { width: 100%; height: 100%; object-fit: cover; display: block; }
.detail-cover-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 72px;
  font-weight: 700;
  color: #fff;
}
.featured-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(251, 191, 36, 0.92);
  color: #78350f;
  font-size: 13px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 999px;
}
.detail-head {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
.detail-name { font-size: 24px; }
.status-badge {
  flex-shrink: 0;
  padding: 3px 12px;
  border-radius: 999px;
  font-size: 13px;
}
.status-done { background: rgba(101, 163, 13, 0.14); color: var(--accent); }
.status-doing { background: rgba(59, 130, 246, 0.14); color: #3b82f6; }
.status-planning { background: rgba(148, 163, 184, 0.16); color: var(--muted); }
.detail-desc { font-size: 15px; line-height: 1.9; color: var(--text); margin-bottom: 16px; }
.project-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.tag {
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 999px;
  background: rgba(101, 163, 13, 0.12);
  color: var(--accent);
}
.detail-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--muted);
  padding: 12px 14px;
  border-radius: 10px;
  background: var(--input-bg);
  margin-bottom: 20px;
}
.detail-actions { display: flex; gap: 12px; flex-wrap: wrap; }

/* 无效地址提示 */
.not-found-inner { text-align: center; padding: 30px 10px; }
.nf-icon { font-size: 52px; margin-bottom: 12px; }
.nf-title { font-size: 22px; margin-bottom: 10px; }
.nf-desc { color: var(--muted); font-size: 14px; line-height: 1.8; margin-bottom: 20px; word-break: break-all; }
</style>
