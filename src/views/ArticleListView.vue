<template>
  <section class="card articles-section">
    <div class="section-head">
      <h3 class="section-title">📝 我的文章</h3>
      <span class="article-count">共 {{ articleStore.articleCount }} 篇 · 已发布 {{ articleStore.publishedCount }} 篇</span>
    </div>

    <!-- 文章卡片列表：storeToRefs 解构出的数据，直接响应式渲染 -->
    <div v-if="publishedArticles.length" class="article-list">
      <article v-for="a in publishedArticles" :key="a.id" class="article-card">
        <div class="article-top">
          <h4 class="article-title">{{ a.title }}</h4>
          <span class="date-badge">{{ a.date }}</span>
        </div>
        <p class="article-summary">{{ a.summary }}</p>
        <div class="article-tags">
          <!-- el-tag：Element Plus 标签组件展示文章状态 -->
          <el-tag size="small" effect="plain" type="success">{{ a.status }}</el-tag>
        </div>
      </article>
    </div>

    <div v-else class="empty-state">📭 暂无已发布文章</div>
  </section>
</template>

<script setup>
// ===== 文章列表页（/articles，访客可访问）=====
// storeToRefs：把 Store 的 state/getters 解构出来，保持响应式
// （直接解构 store 会丢失响应性，storeToRefs 解构后模板中可安全使用）
import { storeToRefs } from 'pinia'
import { useArticleStore } from '../stores/articleStore'

const articleStore = useArticleStore()

// 用 storeToRefs 解构 getters 与 state，组件内可直接使用且保持响应式
const { publishedArticles } = storeToRefs(articleStore)
</script>

<style scoped>
.articles-section { margin-top: 0; }
.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.section-title { font-size: 18px; }
.article-count { font-size: 13px; color: var(--muted); }

.article-list { display: grid; gap: 14px; }
/* 玻璃拟态卡片：与首页技能卡片同风格（半透明模糊 + 悬浮阴影） */
.article-card {
  padding: 18px 20px;
  border-radius: 14px;
  background: var(--glass-item);
  backdrop-filter: blur(12px) saturate(1.3);
  -webkit-backdrop-filter: blur(12px) saturate(1.3);
  border: 1px solid var(--glass-border);
  text-align: left;
  transition: box-shadow 0.25s, transform 0.1s ease-out;
  will-change: transform;
}
.article-card:hover {
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.14);
  transform: translateY(-1px);
}
.article-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}
.article-title { font-size: 17px; }
.date-badge {
  font-size: 12px;
  color: var(--muted);
  padding: 2px 10px;
  border-radius: 999px;
  background: rgba(148, 163, 184, 0.14);
}
.article-summary {
  font-size: 14px;
  line-height: 1.8;
  color: var(--muted);
  margin-bottom: 12px;
}
.article-tags { display: flex; gap: 8px; }
.tag {
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 999px;
  background: rgba(101, 163, 13, 0.12);
  color: var(--accent);
}
.empty-state {
  text-align: center;
  color: var(--muted);
  padding: 30px 0;
  font-size: 14px;
}
</style>
