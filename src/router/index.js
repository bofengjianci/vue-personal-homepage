// ===== Vue Router 路由表 =====
// 基础路由：/home 首页、/projects 项目、/about 关于、/login 登录、/admin 后台管理
// 动态路由：/projects/:id 项目详情（嵌套在项目页下）
// 嵌套路由：/projects 为父路由，''（列表）与 ':id'（详情）为其子路由
// 重定向：/  →  /home（默认首页）；未匹配路径 → 404 页面
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/userStore'

// 视图组件（views 目录，每个路由对应一个页面）
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import LoginView from '../views/LoginView.vue'
import AdminView from '../views/AdminView.vue'
import NotFoundView from '../views/NotFoundView.vue'

// 项目页父路由：ProjectsView 提供统一容器，子路由分别渲染列表/详情
const ProjectsView = () => import('../views/ProjectsView.vue')
const ProjectListView = () => import('../views/ProjectListView.vue')
const ProjectDetailView = () => import('../views/ProjectDetailView.vue')
// 文章相关页面（懒加载）
const ArticleListView = () => import('../views/ArticleListView.vue')
const ArticleManageView = () => import('../views/ArticleManageView.vue')

const routes = [
  // 默认地址重定向到首页
  { path: '/', redirect: '/home' },

  // 首页（个人主页）：个人简介 + 技能 + 项目预览
  {
    path: '/home',
    name: 'home',
    component: HomeView,
    meta: { title: '首页' }
  },

  // 项目页（父路由，嵌套子路由）
  {
    path: '/projects',
    name: 'projects',
    component: ProjectsView,
    // 修复：命名路由跳转父路由时不自动匹配空子路由（vue-router 4.6.x 行为），
    // 显式重定向到默认子路由 project-list，保证导航到 /projects 能渲染列表
    redirect: { name: 'project-list' },
    meta: { title: '项目' },
    children: [
      // 子路由 path 为空 → /projects 直接显示项目列表
      {
        path: '',
        name: 'project-list',
        component: ProjectListView
      },
      // 动态路由参数 :id → /projects/1 显示对应项目详情
      {
        path: ':id',
        name: 'project-detail',
        component: ProjectDetailView
      }
    ]
  },

  // 关于页
  {
    path: '/about',
    name: 'about',
    component: AboutView,
    meta: { title: '关于' }
  },

  // 登录页（身份认证）
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { title: '登录' }
  },

  // 文章列表页（访客可直接访问，只展示已发布文章）
  {
    path: '/articles',
    name: 'article-list',
    component: ArticleListView,
    meta: { title: '文章' }
  },

  // 后台管理页：requiresAuth 标记 → 路由守卫拦截未登录访问
  {
    path: '/admin',
    name: 'admin',
    component: AdminView,
    meta: { title: '后台管理', requiresAuth: true }
  },

  // 文章管理页（登录后可见，增删改查入口）
  {
    path: '/admin/articles',
    name: 'article-manage',
    component: ArticleManageView,
    meta: { title: '文章管理', requiresAuth: true }
  },

  // 404 兜底：所有未匹配路径 → 页面未找到
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // 滚动行为：切换路由时回到页面顶部
  scrollBehavior() {
    return { top: 0 }
  }
})

// ===== 全局前置守卫（beforeEach）=====
// 职责一：根据路由 meta.title 更新浏览器标签页标题（userStore 的 profile）
// 职责二：requiresAuth 权限校验——未登录访问后台 → 跳登录页并记录原目标地址
router.beforeEach((to, from) => {
  const userStore = useUserStore()

  // 更新浏览器标题（跟随页面内容变化）
  document.title = to.meta?.title
    ? `${to.meta.title} · ${userStore.titleSuffix}`
    : userStore.titleSuffix

  // 权限守卫：目标页面要求登录，但当前未登录
  if (to.meta?.requiresAuth && !userStore.isAuthed) {
    // 携带 redirect 参数，登录成功后跳回原目标
    return {
      name: 'login',
      query: { redirect: to.fullPath }
    }
  }
})

export default router
