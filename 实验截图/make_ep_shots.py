# -*- coding: utf-8 -*-
"""实验五（Element Plus）关键代码截图渲染：pygments 分词 + PIL 绘制深色编辑器风格"""
import os
from pygments import lex
from pygments.token import Token
from pygments.lexers import get_lexer_by_name
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\86180\vue_xiangmu\实验截图"
MONO = r"C:\Windows\Fonts\consola.ttf"
CN = r"C:\Windows\Fonts\msyh.ttc"

BG = (40, 44, 52)
FG = (171, 178, 191)
GUTTER = (48, 53, 63)
LINE_NO = (108, 116, 131)
TITLE_BG = (33, 37, 44)
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

    d.rectangle([0, 0, img_w, 36], fill=TITLE_BG)
    title_font = ImageFont.truetype(CN, 15)
    d.text((14, 9), title, font=title_font, fill=(152, 195, 121))
    for i, c in enumerate([(224, 108, 117), (229, 192, 123), (152, 195, 121)]):
        d.ellipse([img_w - 74 + i * 20, 12, img_w - 62 + i * 20, 24], fill=c)

    d.rectangle([0, 36, pad_l - 20, img_h], fill=GUTTER)

    y = pad_t
    for tok_type, text in tokens:
        while '\n' in text:
            before, after = text.split('\n', 1)
            if before:
                draw_token(d, mono, cn, before, tok_type, y)
            y += line_h
            text = after
        if text:
            draw_token(d, mono, cn, text, tok_type, y)

    ln_font = ImageFont.truetype(MONO, font_size - 2)
    for i in range(len(lines)):
        d.text((14, pad_t + i * line_h + 4), str(i + 1), font=ln_font, fill=LINE_NO)

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


S1 = """// ===== 1. 安装并注册 Element Plus（src/main.js）=====
import { createApp } from 'vue'
import ElementPlus from 'element-plus'          // ① 引入组件库
import 'element-plus/dist/index.css'            // ② 引入默认样式
import zhCn from 'element-plus/es/locale/lang/zh-cn'  // ③ 中文语言包
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createPinia())
app.use(ElementPlus, { locale: zhCn })          // ④ 全局注册（组件+语言）
app.use(router)
app.mount('#app')

// ===== 主题适配（src/App.vue :root 覆盖）=====
:root {
  --el-color-primary: #65a30d;      // 青柠绿主色（与站点一致）
  --el-color-primary-light-3: #84cc16;
  --el-border-radius-base: 10px;    // 圆角统一
}"""

S2 = """// ===== 2. 布局组件重构整体结构（src/components/MainLayout.vue）=====
// el-container 垂直容器 + el-header / el-main / el-footer 三段式布局
<template>
  <el-container direction="vertical" class="layout-root">
    <el-header height="auto" class="layout-header">
      <slot name="header" />            <!-- 具名插槽：顶部导航 -->
    </el-header>

    <el-main class="layout-main">
      <slot />                          <!-- 默认插槽：页面主体 -->
    </el-main>

    <el-footer height="auto" class="layout-footer">
      <slot name="footer">
        <p>默认页脚</p>                 <!-- 具名插槽带默认内容 -->
      </slot>
    </el-footer>
  </el-container>
</template>

// 覆盖默认内边距，让玻璃拟态卡片铺满
.layout-header, .layout-main, .layout-footer { padding: 0; }"""

S3 = """// ===== 3. 菜单组件实现导航（src/components/AppHeader.vue）=====
// el-menu 水平菜单 + :router 开启路由模式 + default-active 跟随当前路由高亮
<el-menu
  mode="horizontal"
  :router="true"
  :default-active="route.path"
  :ellipsis="false"
  class="nav-menu"
>
  <el-menu-item v-for="item in navItems" :key="item.path" :index="item.path">
    {{ item.label }}
  </el-menu-item>
</el-menu>

// 导航数据（命名路由组织）
const navItems = [
  { path: '/home',     label: '🏠 首页',   name: 'home' },
  { path: '/projects', label: '🚀 项目',   name: 'projects' },
  { path: '/articles', label: '📝 文章',   name: 'article-list' },
  { path: '/about',    label: '👤 关于',   name: 'about' }
]
// 样式覆盖：透明底、青柠绿高亮、圆角 item
.nav-menu { background: transparent; border-bottom: none; }
.nav-menu :deep(.el-menu-item.is-active) { color: var(--el-color-primary); }"""

S4 = """// ===== 4. 时间线组件展示个人经历（src/views/AboutView.vue）=====
// userStore 新增 experiences 时间线数据
experiences: [
  { id: 1, time: '2024-09', title: '进入重庆科技大学',
    desc: '就读计算机科学与技术专业。', color: 'success' },
  { id: 2, time: '2025-06', title: '完成《学生管理系统》课程设计',
    desc: 'C 语言 + 链表 + 文件读写实现的完整项目。', color: 'primary' },
  { id: 3, time: '2026-03', title: '接触前端开发', color: 'primary' },
  { id: 4, time: '2026-10', title: '搭建个人主页', color: 'success' }
]

// 模板：el-timeline + el-timeline-item 渲染时间线
<el-timeline class="exp-timeline">
  <el-timeline-item
    v-for="e in experiences" :key="e.id"
    :timestamp="e.time" :type="e.color" placement="top"
  >
    <div class="exp-card">
      <h4 class="exp-title">{{ e.title }}</h4>
      <p class="exp-desc">{{ e.desc }}</p>
    </div>
  </el-timeline-item>
</el-timeline>"""

S5 = """// ===== 5. 表单 + 表格组件（src/views/AdminView.vue）=====
// el-form 校验：姓名必填、邮箱格式
const profileRules = {
  name: [{ required: true, message: '姓名不能为空', trigger: 'blur' }],
  email: [{ type: 'email', message: '邮箱格式不正确', trigger: 'blur' }]
}
function saveProfile() {
  profileFormRef.value.validate((valid) => {   // 通过校验才提交
    if (!valid) return
    userStore.updateProfile({ ...profileForm.value })
    ElMessage.success('✓ 个人信息已保存')       // 消息提示组件
  })
}

// el-table 展示项目列表 + #default 插槽定制状态/操作列
<el-table :data="projects" class="ep-table">
  <el-table-column prop="name" label="项目名称" min-width="180" />
  <el-table-column label="状态" width="110">
    <template #default="{ row }">
      <el-tag :type="statusTag(row.status)" effect="plain" size="small">
        {{ row.status }}
      </el-tag>
    </template>
  </el-table-column>
</el-table>"""

S6 = """// ===== 6. 对话框 + 表单实现新增与编辑（ProjectEditModal.vue）=====
// el-dialog 对话框容器 + el-form 校验 + #footer 插槽操作按钮
<el-dialog :model-value="true" :title="isNew ? '🚀 添加项目' : '✏️ 编辑项目'"
           width="600px" align-center @close="emit('cancel')">
  <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
    <el-form-item label="项目名称 *" prop="name">
      <el-input v-model="form.name" placeholder="例如：个人主页" />
    </el-form-item>
    <el-form-item label="状态">
      <el-select v-model="form.status" class="full-width">
        <el-option label="已完成" value="已完成" />
        <el-option label="进行中" value="进行中" />
      </el-select>
    </el-form-item>
    <el-checkbox v-model="form.featured">⭐ 设为着重项目</el-checkbox>
  </el-form>
  <template #footer>
    <el-button v-if="!isNew" type="danger" plain @click="emit('remove', form.id)">
      🗑️ 删除项目
    </el-button>
    <el-button @click="emit('cancel')">取消</el-button>
    <el-button type="primary" @click="save">保存</el-button>
  </template>
</el-dialog>

// 保存：先过表单校验
function save() {
  formRef.value.validate((valid) => {
    if (!valid) return
    emit('save', { ...form.value, name: form.value.name.trim() })
  })
}"""


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    jobs = [
        ('实验五代码-1-注册ElementPlus.png', 'main.js · App.vue · Element Plus 注册与主题适配', S1),
        ('实验五代码-2-布局组件.png', 'MainLayout.vue · el-container 三段式布局', S2),
        ('实验五代码-3-菜单导航.png', 'AppHeader.vue · el-menu 路由导航', S3),
        ('实验五代码-4-时间线.png', 'AboutView.vue · el-timeline 个人经历', S4),
        ('实验五代码-5-表单与表格.png', 'AdminView.vue · el-form 校验 + el-table', S5),
        ('实验五代码-6-对话框.png', 'ProjectEditModal.vue · el-dialog 新增编辑', S6),
    ]
    for name, title, code in jobs:
        render(os.path.join(OUT, name), title, code)
        print(name, 'OK')
