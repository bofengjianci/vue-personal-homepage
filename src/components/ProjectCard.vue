<template>
  <article
    class="project-card"
    :class="{ 'is-featured': featured }"
    @click="emit('edit', project)"
  >
    <!-- 封面区：具名插槽 #cover，默认显示图片或首字渐变占位 -->
    <div class="project-cover">
      <slot name="cover">
        <img
          v-if="coverOk && project.image"
          :src="project.image"
          :alt="project.name"
          @error="coverOk = false"
        >
        <div v-else class="cover-fallback">{{ project.name.charAt(0) }}</div>
      </slot>
      <span v-if="featured" class="featured-badge">⭐ 着重项目</span>
    </div>

    <!-- 正文区：默认插槽，可定制卡片内容（减少重复结构） -->
    <div class="project-body">
      <slot>
        <div class="project-title-row">
          <h4 class="project-name">{{ project.name }}</h4>
          <span class="status-badge" :class="statusClass">{{ project.status }}</span>
        </div>
        <p class="project-desc">{{ project.description }}</p>
        <div v-if="project.tags && project.tags.length" class="project-tags">
          <span v-for="tag in project.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </slot>
    </div>

    <!-- 操作区：具名插槽 #actions，默认显示编辑按钮 -->
    <div class="project-actions">
      <slot name="actions">
        <button class="edit-btn" @click.stop="emit('edit', project)">✏️ 编辑</button>
      </slot>
    </div>
  </article>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

// ===== props：项目数据 + 是否着重 =====
// 数据由父组件（ProjectsSection → App.vue）传入，本组件只负责"长得什么样"
const props = defineProps({
  project: { type: Object, required: true },
  featured: { type: Boolean, default: false }
})

// ===== emits：点击卡片/编辑按钮 → 通知父组件打开编辑 =====
const emit = defineEmits(['edit'])

// 封面图加载失败时回退到首字占位（失败后自动隐藏 img）
const coverOk = ref(true)
watch(() => props.project.image, () => { coverOk.value = true })

// 状态 → 徽章样式类映射（已完成=绿 / 进行中=蓝 / 其余=灰）
const statusClass = computed(() => {
  if (props.project.status === '已完成') return 'status-done'
  if (props.project.status === '进行中') return 'status-doing'
  return 'status-planning'
})
</script>

<style scoped>
.project-card {
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--glass-item);
  backdrop-filter: blur(12px) saturate(1.3);
  -webkit-backdrop-filter: blur(12px) saturate(1.3);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.25s, transform 0.15s ease-out;
  text-align: left;
}
.project-card:hover {
  box-shadow: 0 14px 32px rgba(15, 23, 42, 0.14);
  transform: translateY(-3px);
}

/* ===== 着重项目：横跨整行、图文左右布局、封面更大 ===== */
.project-card.is-featured {
  grid-column: 1 / -1;
  flex-direction: row;
  align-items: stretch;
}
.is-featured .project-cover {
  width: 38%;
  min-height: 200px;
  flex-shrink: 0;
}

.project-cover {
  position: relative;
  height: 130px;
  overflow: hidden;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
}
.project-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.cover-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 42px;
  font-weight: 700;
  color: #fff;
}
.featured-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(251, 191, 36, 0.92);
  color: #78350f;
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 999px;
}

.project-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
}
.project-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 8px;
}
.project-name { font-size: 16px; }
.project-desc {
  flex: 1;
  font-size: 13px;
  color: var(--muted);
  line-height: 1.7;
}

/* 状态徽章：已完成=绿 / 进行中=蓝 / 规划中=灰 */
.status-badge {
  flex-shrink: 0;
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 12px;
}
.status-done { background: rgba(101, 163, 13, 0.14); color: var(--accent); }
.status-doing { background: rgba(59, 130, 246, 0.14); color: #3b82f6; }
.status-planning { background: rgba(148, 163, 184, 0.16); color: var(--muted); }

.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 12px;
}
.tag {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(101, 163, 13, 0.12);
  color: var(--accent);
}

.project-actions { padding: 0 16px 16px; }
.is-featured .project-actions { padding-top: 2px; }
.edit-btn {
  padding: 6px 14px;
  border-radius: 999px;
  border: 1px solid var(--glass-border);
  background: var(--glass-strong);
  color: var(--text);
  font-size: 13px;
  cursor: pointer;
  transition: transform 0.2s;
}
.edit-btn:hover { transform: translateY(-1px); box-shadow: var(--shadow); }
</style>
