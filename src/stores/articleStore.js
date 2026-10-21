// ===== 文章 Store（Pinia）：文章数据增删改查 =====
// 职责：保存文章数组（标题/摘要/正文/状态/发布日期）；
// 提供增删改查 actions 与"已发布文章"等 getters；localStorage 持久化，
// 文章列表页（访客）与文章管理页（登录后）跨页面共享同一份数据。
import { defineStore } from 'pinia'

function loadJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key)
    return raw ? JSON.parse(raw) : fallback
  } catch (e) {
    return fallback
  }
}

export const useArticleStore = defineStore('article', {
  // ---- state：文章数组（默认 3 篇文章）----
  state: () => ({
    articles: loadJSON('articles', [
      {
        id: 1,
        title: 'Vue 3 组合式 API 实战笔记',
        summary: '从 ref / reactive 到 defineProps、defineEmits、defineModel 的组件化实践记录。',
        content: '组合式 API 把同一功能的逻辑集中到 setup 中，配合 defineProps 与 defineEmits 实现组件通信，defineModel 让双向绑定更简洁。',
        status: '已发布',
        date: '2026-09-20'
      },
      {
        id: 2,
        title: '用 Vue Router 搭建多页面应用',
        summary: '基础路由、嵌套路由、动态路由参数、命名路由与路由守卫的配置总结。',
        content: '通过 RouterView 渲染、RouterLink 导航，结合 meta 元信息与 beforeEach 守卫实现标题跟随与权限控制。',
        status: '已发布',
        date: '2026-10-08'
      },
      {
        id: 3,
        title: 'Pinia 状态管理初体验',
        summary: 'state、getters、actions 与 storeToRefs 的用法，以及 localStorage 持久化方案。',
        content: '用 Pinia 统一管理用户、项目、文章三份共享状态，组件通过 storeToRefs 解构保持响应式，刷新后数据不丢失。',
        status: '草稿',
        date: '2026-10-13'
      }
    ])
  }),

  // ---- getters：派生状态 ----
  getters: {
    // 已发布文章（访客列表页只展示已发布内容）
    publishedArticles: (state) => state.articles.filter(a => a.status === '已发布'),
    // 文章总数
    articleCount: (state) => state.articles.length,
    // 已发布数量
    publishedCount: (state) => state.articles.filter(a => a.status === '已发布').length
  },

  // ---- actions：增删改查 ----
  actions: {
    // 新建：分配自增 id 后追加
    addArticle(form) {
      const nextId = this.articles.length
        ? Math.max(...this.articles.map(a => a.id)) + 1
        : 1
      this.articles.push({ ...form, id: nextId })
      this.persist()
    },
    // 编辑：按 id 替换对应项
    updateArticle(form) {
      const idx = this.articles.findIndex(a => a.id === form.id)
      if (idx !== -1) this.articles[idx] = { ...form }
      this.persist()
    },
    // 删除：按 id 过滤
    removeArticle(id) {
      const idx = this.articles.findIndex(a => a.id === id)
      if (idx !== -1) this.articles.splice(idx, 1)
      this.persist()
    },
    // 按 id 查找（编辑弹窗回填用）
    findArticle(id) {
      return this.articles.find(a => a.id === Number(id))
    },
    // 写入 localStorage（跨页面刷新后数据不丢失）
    persist() {
      localStorage.setItem('articles', JSON.stringify(this.articles))
    }
  }
})
