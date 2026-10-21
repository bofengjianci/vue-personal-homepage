// ===== 全局共享数据 Store（组合式 API 实现，非 Pinia）=====
// 路由页面组件（Home/Projects/About/Admin…）都从这里读取同一份数据，
// 避免"每个页面各存一份、刷新后互相不一致"的问题。
// 个人简介、项目数据与主题状态均做 localStorage 持久化；登录态用 sessionStorage。
import { reactive, ref, watch } from 'vue'// ---------- 工具：安全读取 localStorage JSON ----------
function loadJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key)
    return raw ? JSON.parse(raw) : fallback
  } catch (e) {
    return fallback
  }
}

// ---------- 个人简介 ----------
const profile = reactive(loadJSON('profile', {
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
}))

watch(profile, (val) => {
  localStorage.setItem('profile', JSON.stringify(val))
}, { deep: true })

// ---------- 技能 ----------
const skills = reactive([
  { id: 1, name: 'HTML / CSS', category: '前端', level: '精通', percent: 90, icon: '🎨' },
  { id: 2, name: 'JavaScript', category: '前端', level: '熟练', percent: 82, icon: '⚡' },
  { id: 3, name: 'Vue 3', category: '前端框架', level: '熟练', percent: 78, icon: '🖖' },
  { id: 4, name: "Ren'Py", category: '游戏开发', level: '进阶', percent: 72, icon: '🎮' },
  { id: 5, name: 'C 语言', category: '基础', level: '熟练', percent: 75, icon: '🔧' },
  { id: 6, name: '摄影', category: '兴趣', level: '进阶', percent: 68, icon: '📷' }
])

// ---------- 项目数据（数组保存名称/简介/状态/标签/图片/是否着重）----------
const projects = reactive(loadJSON('projects', [
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
    tags: ['Ren\'Py', '游戏开发'],
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
]))

watch(projects, (val) => {
  localStorage.setItem('projects', JSON.stringify(val))
}, { deep: true })

// ---------- 主题状态（跨页面保持）----------
const isDark = ref(false)

// ---------- 登录态（后台管理权限）----------
// sessionStorage 记录，刷新页面后仍保持本次会话的登录状态；关闭浏览器即失效
const isAuthed = ref(sessionStorage.getItem('admin_authed') === '1')

function login() {
  isAuthed.value = true
  sessionStorage.setItem('admin_authed', '1')
}

function logout() {
  isAuthed.value = false
  sessionStorage.removeItem('admin_authed')
}

// ---------- 个人简介更新 ----------
function updateProfile(data) {
  Object.assign(profile, data)
}

// ---------- 项目增删改 ----------
// 新建：分配自增 id；编辑：替换数组中对应项；删除：按 id 过滤
function addProject(form) {
  const nextId = projects.length
    ? Math.max(...projects.map(p => p.id)) + 1
    : 1
  projects.push({ ...form, id: nextId })
}

function updateProject(form) {
  const idx = projects.findIndex(p => p.id === form.id)
  if (idx !== -1) projects[idx] = { ...form }
}

function removeProject(id) {
  const idx = projects.findIndex(p => p.id === id)
  if (idx !== -1) projects.splice(idx, 1)
}

// 按 id 查找项目（详情页使用；找不到返回 undefined）
function findProject(id) {
  const num = Number(id)
  return projects.find(p => p.id === num)
}

// 用 reactive 包裹为单例 store：reactive 对象内部的 ref 会自动解包，
// 组件与路由守卫中 store.isAuthed / store.isDark 直接得到 boolean 值（保持响应性）
export const store = reactive({
  profile, skills, projects, isDark, isAuthed,
  login, logout,
  updateProfile, addProject, updateProject, removeProject, findProject
})

export function useStore() {
  return store
}
