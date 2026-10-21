<template>
  <section class="card projects-section">
    <div class="section-head">
      <h3 class="section-title">🚀 全部项目</h3>
      <!-- 访客视角：添加入口导向后台管理（需登录） -->
      <button class="add-btn" @click="goAdmin">＋ 添加项目</button>
    </div>

    <!-- 着重项目：大卡横贯整行 -->
    <div v-if="featuredProjects.length" class="featured-list">
      <ProjectCard
        v-for="p in featuredProjects"
        :key="p.id"
        :project="p"
        featured
        @edit="goDetail"
      />
    </div>

    <!-- 普通项目：网格布局 -->
    <div v-if="normalProjects.length" class="project-grid">
      <ProjectCard
        v-for="p in normalProjects"
        :key="p.id"
        :project="p"
        @edit="goDetail"
      />
    </div>

    <div v-if="!projectCount" class="empty-state">
      📭 还没有项目，去「后台管理」添加第一个吧
    </div>
  </section>
</template>

<script setup>
// ===== 项目列表（/projects 嵌套子路由的默认内容）=====
// Pinia：projectStore 提供数据，storeToRefs 解构 getters（featured/normal）保持响应式
// 复用可复用组件 ProjectCard（插槽定制封面/正文/操作区）
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useProjectStore } from '../stores/projectStore'
import ProjectCard from '../components/ProjectCard.vue'

const projectStore = useProjectStore()
const router = useRouter()

// storeToRefs 解构 getters：着重项目/普通项目自动按 featured 拆分
const { featuredProjects, normalProjects, projectCount } = storeToRefs(projectStore)

// 点击卡片 → 编程式跳转到动态路由详情页 /projects/:id
function goDetail(project) {
  router.push({ name: 'project-detail', params: { id: project.id } })
}

// 添加项目 → 后台管理（未登录被守卫重定向到登录页）
function goAdmin() {
  router.push({ name: 'admin' })
}
</script>

<style scoped>
.projects-section { margin-top: 0; }

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.section-title { font-size: 18px; }
.add-btn {
  padding: 8px 18px;
  border-radius: 999px;
  border: none;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s;
}
.add-btn:hover { transform: translateY(-2px); box-shadow: var(--shadow); }

.featured-list { display: grid; gap: 14px; margin-bottom: 14px; }
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 14px;
}

.empty-state {
  text-align: center;
  color: var(--muted);
  padding: 30px 0;
  font-size: 14px;
}
</style>
