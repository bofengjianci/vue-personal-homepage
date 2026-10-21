// ===== 项目 Store（Pinia）：项目数据增删改查 =====
// 职责：保存项目数组（名称/简介/状态/标签/图片/是否着重）；
// 提供增删改查 actions 与"着重/普通"拆分 getters；localStorage 持久化，
// 项目列表页、详情页、后台管理页跨页面共享同一份数据。
import { defineStore } from 'pinia'

function loadJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key)
    return raw ? JSON.parse(raw) : fallback
  } catch (e) {
    return fallback
  }
}

export const useProjectStore = defineStore('project', {
  // ---- state：项目数组（默认 3 个项目）----
  state: () => ({
    projects: loadJSON('projects', [
      {
        id: 1,
        name: '我的个人主页',
        description: '基于 Vue 3 组合式 API 开发的个人主页，包含主题切换、技能展示、项目展示与本地数据持久化，正在持续迭代。',
        status: '已完成',
        tags: ['Vue 3', 'Vite', '组合式 API'],
        image: '',
        featured: true
      },
      {
        id: 2,
        name: '文字冒险游戏',
        description: "使用 Ren'Py 开发的文字冒险游戏，包含分支剧情与多结局系统。",
        status: '进行中',
        tags: ["Ren'Py", '游戏开发'],
        image: '',
        featured: false
      },
      {
        id: 3,
        name: '学生管理系统',
        description: '数据结构课程设计：使用链表 + 文件读写实现的 C 语言学生管理系统。',
        status: '规划中',
        tags: ['C 语言'],
        image: '',
        featured: false
      }
    ])
  }),

  // ---- getters：派生状态 ----
  getters: {
    // 着重项目：单独一排大卡展示（比普通项目更显眼）
    featuredProjects: (state) => state.projects.filter(p => p.featured),
    // 普通项目：进网格布局
    normalProjects: (state) => state.projects.filter(p => !p.featured),
    // 项目总数
    projectCount: (state) => state.projects.length
  },

  // ---- actions：增删改查 ----
  actions: {
    // 新建：分配自增 id 后追加
    addProject(form) {
      const nextId = this.projects.length
        ? Math.max(...this.projects.map(p => p.id)) + 1
        : 1
      this.projects.push({ ...form, id: nextId })
      this.persist()
    },
    // 编辑：按 id 替换数组中的对应项
    updateProject(form) {
      const idx = this.projects.findIndex(p => p.id === form.id)
      if (idx !== -1) this.projects[idx] = { ...form }
      this.persist()
    },
    // 删除：按 id 过滤
    removeProject(id) {
      const idx = this.projects.findIndex(p => p.id === id)
      if (idx !== -1) this.projects.splice(idx, 1)
      this.persist()
    },
    // 查找（详情页使用；找不到返回 undefined → 无效地址分支）
    findProject(id) {
      const num = Number(id)
      return this.projects.find(p => p.id === num)
    },
    // 写入 localStorage（跨页面刷新后数据不丢失）
    persist() {
      localStorage.setItem('projects', JSON.stringify(this.projects))
    }
  }
})
