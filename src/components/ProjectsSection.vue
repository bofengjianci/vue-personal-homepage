<template>
  <section class="card projects-section">
    <!-- 板块头部：具名插槽 #header（默认 = 标题 + 添加按钮，父组件可整体定制） -->
    <div class="section-head">
      <slot name="header">
        <h3 class="section-title">🚀 项目展示</h3>
        <button class="add-btn" @click="emit('add')">＋ 添加项目</button>
      </slot>
    </div>

    <!-- 着重项目：大卡横贯整行，比其他项目占位更大更显眼 -->
    <div v-if="featuredProjects.length" class="featured-list">
      <ProjectCard
        v-for="p in featuredProjects"
        :key="p.id"
        :project="p"
        featured
        @edit="emit('edit', $event)"
      />
    </div>

    <!-- 普通项目：网格布局 -->
    <div v-if="normalProjects.length" class="project-grid">
      <ProjectCard
        v-for="p in normalProjects"
        :key="p.id"
        :project="p"
        @edit="emit('edit', $event)"
      />
    </div>

    <div v-if="!projects.length" class="empty-state">
      📭 还没有项目，点击右上角「添加项目」创建第一个吧
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import ProjectCard from './ProjectCard.vue'

// ===== props：项目数组（数据在 App.vue 统一管理 + localStorage 持久化） =====
const props = defineProps({
  projects: { type: Array, default: () => [] }
})

// ===== emits：板块只负责渲染与通知，增删改逻辑交给父组件 =====
const emit = defineEmits(['add', 'edit'])

// 按 featured 标记拆分：着重项目单独一排，其余进网格
const featuredProjects = computed(() => props.projects.filter(p => p.featured))
const normalProjects = computed(() => props.projects.filter(p => !p.featured))
</script>

<style scoped>
.projects-section { margin-top: 24px; }

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
