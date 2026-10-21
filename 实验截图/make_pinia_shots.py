# -*- coding: utf-8 -*-
"""实验四（Pinia）关键代码截图渲染：pygments 分词 + PIL 绘制深色编辑器风格"""
import os
from pygments import lex
from pygments.token import Token
from pygments.lexers import get_lexer_by_name
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\86180\vue_xiangmu\实验截图"
MONO = r"C:\Windows\Fonts\consola.ttf"
CN = r"C:\Windows\Fonts\msyh.ttc"

BG = (40, 44, 52)          # 编辑器背景
FG = (171, 178, 191)       # 默认文字
GUTTER = (48, 53, 63)      # 行号底色
LINE_NO = (108, 116, 131)  # 行号颜色
TITLE_BG = (33, 37, 44)    # 标题条
BORDER = (62, 70, 85)

COLORS = {
    Token.Keyword: (198, 120, 221),
    Token.Keyword.Constant: (198, 120, 221),
    Token.Keyword.Declaration: (198, 120, 221),
    Token.Keyword.Namespace: (198, 120, 221),
    Token.Name: (224, 108, 117),
    Token.Name.Function: (97, 175, 239),
    Token.Name.Tag: (224, 108, 117),
    Token.Name.Attribute: (224, 108, 117),
    Token.Name.Builtin: (224, 108, 117),
    Token.Name.Class: (229, 192, 123),
    Token.Name.Decorator: (229, 192, 123),
    Token.String: (152, 195, 121),
    Token.String.Doc: (152, 195, 121),
    Token.String.Double: (152, 195, 121),
    Token.String.Single: (152, 195, 121),
    Token.String.Interpol: (152, 195, 121),
    Token.Number: (209, 154, 102),
    Token.Number.Integer: (209, 154, 102),
    Token.Comment: (92, 99, 112),
    Token.Comment.Single: (92, 99, 112),
    Token.Operator: (171, 178, 191),
    Token.Punctuation: (171, 178, 191),
    Token.Literal: (209, 154, 102),
    Token.Literal.String: (152, 195, 121),
}


def cjk(ch):
    return ord(ch) > 0x2E7F


def render(path, title, code, font_size=17):
    lexer = get_lexer_by_name('vue', stripall=False)
    try:
        tokens = list(lex(code, lexer))
    except Exception:
        tokens = [(Token.Text, code)]

    lines = code.split('\n')
    line_h = 30
    pad_l = 58
    pad_r = 22
    pad_t = 46
    mono = ImageFont.truetype(MONO, font_size)
    cn = ImageFont.truetype(CN, font_size)

    # 计算最大行宽
    max_w = 0
    for line_text in lines:
        w = 0
        for ch in line_text:
            w += (cn.getlength(ch) if cjk(ch) else mono.getlength(ch))
        max_w = max(max_w, int(w))
    img_w = max_w + pad_l + pad_r
    img_h = pad_t + line_h * len(lines) + 26

    img = Image.new('RGB', (img_w, img_h), BG)
    d = ImageDraw.Draw(img)

    # 标题条
    d.rectangle([0, 0, img_w, 36], fill=TITLE_BG)
    title_font = ImageFont.truetype(CN, 15)
    d.text((14, 9), title, font=title_font, fill=(152, 195, 121))
    # 三个圆点
    for i, c in enumerate([(224, 108, 117), (229, 192, 123), (152, 195, 121)]):
        d.ellipse([img_w - 74 + i * 20, 12, img_w - 62 + i * 20, 24], fill=c)

    # 行号列底
    d.rectangle([0, 36, pad_l - 20, img_h], fill=GUTTER)

    # 逐 token 渲染
    y = pad_t
    cur_line = 0
    for tok_type, text in tokens:
        while '\n' in text:
            before, after = text.split('\n', 1)
            if before:
                draw_token(d, mono, cn, before, tok_type, y)
            y += line_h
            text = after
            cur_line += 1
        if text:
            draw_token(d, mono, cn, text, tok_type, y)

    # 行号
    ln_font = ImageFont.truetype(MONO, font_size - 2)
    for i in range(len(lines)):
        d.text((14, pad_t + i * line_h + 4), str(i + 1), font=ln_font, fill=LINE_NO)

    # 底部边框
    d.rectangle([0, img_h - 4, img_w, img_h], fill=BORDER)
    img.save(path)


def draw_token(d, mono, cn, text, tok_type, y):
    x = 58
    color = FG
    for tt, c in COLORS.items():
        if tt in tok_type:
            color = c
            break
    for ch in text:
        f = cn if cjk(ch) else mono
        d.text((x, y), ch, font=f, fill=color)
        x += int(f.getlength(ch))


S1 = """// ===== 1. 安装并注册 Pinia（src/main.js）=====
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createPinia())   // ① 安装 Pinia 状态管理
app.use(router)
app.mount('#app')

// ===== 2. 用户 Store（src/stores/userStore.js）=====
export const useUserStore = defineStore('user', {
  // state：共享状态（登录态用 sessionStorage 持久化）
  state: () => ({
    profile: loadJSON('profile', { name: '刘博霖', studentId: '249981216' }),
    skills: [...],
    isAuthed: sessionStorage.getItem('admin_authed') === '1',
    isDark: false
  }),
  // getters：派生状态（依赖 state 自动重算）
  getters: {
    titleSuffix: (state) => `${state.profile.name}的个人主页`,
    skillCount: (state) => state.skills.length
  },
  // actions：修改状态的方法（写回 localStorage 持久化）
  actions: {
    login() {
      this.isAuthed = true
      sessionStorage.setItem('admin_authed', '1')
    },
    logout() {
      this.isAuthed = false
      sessionStorage.removeItem('admin_authed')
    },
    updateProfile(data) {
      Object.assign(this.profile, data)
      localStorage.setItem('profile', JSON.stringify(this.profile))
    },
    toggleDark() { this.isDark = !this.isDark }
  }
})"""

S2 = """// ===== 项目 Store（src/stores/projectStore.js）=====
// 增删改查 actions + 着重/普通拆分 getters + localStorage 持久化
export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: loadJSON('projects', [
      { id: 1, name: '我的个人主页', status: '已完成', featured: true },
      { id: 2, name: '文字冒险游戏', status: '进行中', featured: false },
      { id: 3, name: '学生管理系统', status: '规划中', featured: false }
    ])
  }),
  getters: {
    featuredProjects: (s) => s.projects.filter(p => p.featured), // 着重项目大卡
    normalProjects: (s) => s.projects.filter(p => !p.featured),  // 普通项目网格
    projectCount: (s) => s.projects.length                       // 项目总数
  },
  actions: {
    addProject(form) {
      this.projects.push({ ...form, id: nextId })  // 分配自增 id
      this.persist()                                // 写回 localStorage
    },
    updateProject(form) {
      const i = this.projects.findIndex(p => p.id === form.id)
      if (i !== -1) this.projects[i] = { ...form }
      this.persist()
    },
    removeProject(id) {
      const i = this.projects.findIndex(p => p.id === id)
      if (i !== -1) this.projects.splice(i, 1)
      this.persist()
    },
    findProject(id) { return this.projects.find(p => p.id === Number(id)) },
    persist() { localStorage.setItem('projects', JSON.stringify(this.projects)) }
  }
})

// ===== 文章 Store（articleStore.js）与项目 Store 同构 =====
// getters：publishedArticles / articleCount / publishedCount
// actions：addArticle / updateArticle / removeArticle / findArticle / persist"""

S3 = """// ===== 3. 文章路由 + 守卫改用 Pinia（src/router/index.js）=====
{
  path: '/articles',
  name: 'article-list',
  component: ArticleListView,
  meta: { title: '文章' }                     // 访客可直接访问
},
{
  path: '/admin/articles',
  name: 'article-manage',
  component: ArticleManageView,
  meta: { title: '文章管理', requiresAuth: true } // 需登录才能访问
}

// 全局前置守卫：更新标题 + 登录权限控制
router.beforeEach((to, from) => {
  const userStore = useUserStore()  // 守卫内获取 Pinia Store
  // ① 浏览器标题跟随页面内容（meta.title + 姓名后缀）
  document.title = to.meta?.title
    ? `${to.meta.title} · ${userStore.titleSuffix}`
    : userStore.titleSuffix
  // ② 未登录访问后台 → 跳登录页并记录原目标
  if (to.meta?.requiresAuth && !userStore.isAuthed) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
})"""

S4 = """// ===== 4. storeToRefs 解构 Store 数据（保持响应式）=====
// src/views/ArticleListView.vue —— 文章列表（getters 解构）
import { storeToRefs } from 'pinia'
import { useArticleStore } from '../stores/articleStore'

const articleStore = useArticleStore()
const { publishedArticles } = storeToRefs(articleStore)
// 直接解构 store 会丢失响应性；
// storeToRefs 解构 state/getters 后，模板中可安全使用且自动更新

// src/views/AdminView.vue —— 后台管理（state 解构 + actions 调用）
const { projects } = storeToRefs(projectStore)

function saveProject(form) {
  if (editingProject.value === 'new') {
    projectStore.addProject(form)      // 通过 actions 修改共享状态
    showToast('✓ 项目已添加')
  } else {
    projectStore.updateProject(form)
    showToast('✓ 项目已更新')
  }
  editingProject.value = null
}"""

S5 = """// ===== 5. 文章管理增删改（src/views/ArticleManageView.vue）=====
const { articles } = storeToRefs(articleStore)

function saveArticle(form) {
  if (editingArticle.value === 'new') {
    articleStore.addArticle(form)      // ① 新增（actions 调用时机）
    showToast('✓ 文章已添加')
  } else {
    articleStore.updateArticle(form)   // ② 编辑
    showToast('✓ 文章已更新')
  }
  editingArticle.value = null
}

function askRemove(a) {                // ③ 删除：二次点击确认防误删
  if (confirmRemoveId.value === a.id) {
    articleStore.removeArticle(a.id)   // 第二次点击才真正删除
    showToast('🗑️ 文章已删除')
  } else {
    confirmRemoveId.value = a.id
  }
}

// ===== 文章编辑弹窗（src/components/ArticleEditModal.vue）=====
// 表单校验：标题必填，通过后 emit 给父组件
function handleSave() {
  if (!form.title.trim()) {
    errorMsg.value = '标题不能为空'
    return
  }
  emit('save', { ...form, title: form.title.trim() })  // defineEmits 提交
}"""


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    jobs = [
        ('实验四代码-1-注册Pinia与userStore.png', 'main.js · userStore.js · Pinia 注册与用户状态', S1),
        ('实验四代码-2-projectStore与articleStore.png', 'projectStore.js · 项目数据增删改查与持久化', S2),
        ('实验四代码-3-路由守卫与文章路由.png', 'router/index.js · 路由元信息 + beforeEach 守卫', S3),
        ('实验四代码-4-storeToRefs解构.png', '组件中 storeToRefs 解构保持响应式', S4),
        ('实验四代码-5-文章管理CRUD.png', 'ArticleManageView · 文章增删改 + 弹窗校验', S5),
    ]
    for name, title, code in jobs:
        render(os.path.join(OUT, name), title, code)
        print(name, 'OK')
