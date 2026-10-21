// ===== 用户 Store（Pinia）：登录态 + 个人简介 + 技能 =====
// 职责：管理"当前是否登录"、个人信息与技能列表；
// 路由守卫（beforeEach）通过它控制后台管理页访问，登录态用 sessionStorage 持久化。
import { defineStore } from 'pinia'

// 工具：安全读取 localStorage JSON（解析失败时回退默认值）
function loadJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key)
    return raw ? JSON.parse(raw) : fallback
  } catch (e) {
    return fallback
  }
}

export const useUserStore = defineStore('user', {
  // ---- state：共享状态 ----
  state: () => ({
    // 个人简介（编辑页修改后写回 localStorage 持久化）
    profile: loadJSON('profile', {
      name: '刘博霖',
      avatar: '',
      major: '计算机科学与技术 · 2024级 2班',
      studentId: '249981216',
      college: '人工智能与计算机学院',
      email: '2130660651@qq.com',
      phone: '13310237048',
      location: '重庆',
      birthday: '2006-06-20',
      motto: '代码如诗，生活如画。',
      bio: '热爱前端的计算机专业学生，喜欢用代码把想法变成现实，正在向 Web 前端工程师的目标努力。'
    }),
    // 技能列表（首页展示）
    skills: [
      { id: 1, name: 'HTML / CSS', category: '前端', level: '精通', percent: 90, icon: '🎨' },
      { id: 2, name: 'JavaScript', category: '前端', level: '熟练', percent: 82, icon: '⚡' },
      { id: 3, name: 'Vue 3', category: '前端框架', level: '熟练', percent: 78, icon: '🖖' },
      { id: 4, name: "Ren'Py", category: '游戏开发', level: '进阶', percent: 72, icon: '🎮' },
      { id: 5, name: 'C 语言', category: '基础', level: '熟练', percent: 75, icon: '🔧' },
      { id: 6, name: '摄影', category: '兴趣', level: '进阶', percent: 68, icon: '📷' }
    ],
    // 个人经历时间线（关于页 el-timeline 展示）
    experiences: [
      { id: 1, time: '2024-09', title: '进入重庆科技大学', desc: '就读计算机科学与技术专业，开始系统地学习编程基础。', color: 'success' },
      { id: 2, time: '2025-06', title: '完成《学生管理系统》课程设计', desc: '使用 C 语言 + 链表 + 文件读写实现的第一个完整项目。', color: 'primary' },
      { id: 3, time: '2026-03', title: '接触前端开发', desc: '自学 HTML / CSS / JavaScript，并开始尝试 Vue 3 框架。', color: 'primary' },
      { id: 4, time: '2026-10', title: '搭建个人主页', desc: '基于 Vue 3 + Vue Router + Pinia + Element Plus 完成个人主页与后台管理。', color: 'success' }
    ],
    // 登录态：sessionStorage 持久化（刷新保持，关闭浏览器失效）
    isAuthed: sessionStorage.getItem('admin_authed') === '1',
    // 主题状态（跨页面共享，App.vue 与 AppHeader 双向绑定）
    isDark: false
  }),

  // ---- getters：派生状态（带缓存，依赖 state 变化自动重算）----
  getters: {
    // 浏览器标题后缀（由路由守卫使用）
    titleSuffix: (state) => `${state.profile.name}的个人主页`,
    // 已发布技能数量
    skillCount: (state) => state.skills.length
  },

  // ---- actions：修改状态的方法 ----
  actions: {
    // 登录成功：写入登录态并持久化到 sessionStorage
    login() {
      this.isAuthed = true
      sessionStorage.setItem('admin_authed', '1')
    },
    // 退出登录：清除登录态
    logout() {
      this.isAuthed = false
      sessionStorage.removeItem('admin_authed')
    },
    // 更新个人简介：浅合并 + localStorage 持久化
    updateProfile(data) {
      Object.assign(this.profile, data)
      localStorage.setItem('profile', JSON.stringify(this.profile))
    },
    // 切换明暗主题（AppHeader 的 defineModel 绑定到该状态）
    toggleDark() {
      this.isDark = !this.isDark
    }
  }
})
