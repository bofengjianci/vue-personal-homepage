<template>
  <div class="admin-page">
    <!-- ===== 顶部栏 ===== -->
    <div class="admin-top">
      <h2 class="admin-title">🛠️ 后台管理</h2>
      <el-button type="danger" plain @click="handleLogout">🚪 退出登录</el-button>
    </div>

    <!-- ===== 0. 文章管理入口（独立页面，同样受守卫保护）===== -->
    <section class="card admin-card">
      <div class="admin-head">
        <h3 class="admin-card-title">📝 文章管理</h3>
        <RouterLink class="entry-link" :to="{ name: 'article-manage' }">→ 进入文章管理页</RouterLink>
      </div>
      <p class="admin-hint">管理个人主页的文章列表（标题、摘要、正文、状态、日期）</p>
    </section>

    <!-- ===== 1. 个人信息编辑（Element Plus 表单 + 校验）=====
         el-form：表单容器；el-form-item：表单项（label/prop 关联校验）
         el-input / el-date-picker：输入控件；rules 实现姓名必填、邮箱格式校验 -->
    <section class="card admin-card">
      <h3 class="admin-card-title">👤 编辑个人信息</h3>
      <el-form
        ref="profileFormRef"
        :model="profileForm"
        :rules="profileRules"
        label-position="top"
        class="profile-form"
      >
        <div class="form-grid">
          <div class="form-field">
            <el-form-item label="姓名 *" prop="name">
              <el-input v-model="profileForm.name" placeholder="请输入姓名" />
            </el-form-item>
          </div>
          <div class="form-field">
            <el-form-item label="头像图片地址（留空显示姓名首字）">
              <el-input v-model="profileForm.avatar" placeholder="https://..." />
            </el-form-item>
          </div>
          <div class="form-field full">
            <el-form-item label="专业班级">
              <el-input v-model="profileForm.major" />
            </el-form-item>
          </div>
          <div class="form-field">
            <el-form-item label="学号">
              <el-input v-model="profileForm.studentId" />
            </el-form-item>
          </div>
          <div class="form-field">
            <el-form-item label="学院">
              <el-input v-model="profileForm.college" />
            </el-form-item>
          </div>
          <div class="form-field">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="profileForm.email" placeholder="name@example.com" />
            </el-form-item>
          </div>
          <div class="form-field">
            <el-form-item label="电话">
              <el-input v-model="profileForm.phone" />
            </el-form-item>
          </div>
          <div class="form-field">
            <el-form-item label="所在城市">
              <el-input v-model="profileForm.location" />
            </el-form-item>
          </div>
          <div class="form-field">
            <el-form-item label="生日">
              <el-date-picker
                v-model="profileForm.birthday"
                type="date"
                value-format="YYYY-MM-DD"
                placeholder="选择日期"
                class="full-width"
              />
            </el-form-item>
          </div>
          <div class="form-field full">
            <el-form-item label="座右铭">
              <el-input v-model="profileForm.motto" />
            </el-form-item>
          </div>
          <div class="form-field full">
            <el-form-item label="个人简介">
              <el-input v-model="profileForm.bio" type="textarea" :rows="3" />
            </el-form-item>
          </div>
        </div>
      </el-form>
      <div class="admin-actions">
        <el-button @click="resetProfile">↺ 取消修改</el-button>
        <el-button type="primary" @click="saveProfile">💾 保存修改</el-button>
      </div>
    </section>

    <!-- ===== 2. 项目管理（Element Plus 表格）=====
         el-table / el-table-column：数据表格展示项目；
         #default 插槽定制状态标签与操作按钮列 -->
    <section class="card admin-card">
      <div class="admin-head">
        <h3 class="admin-card-title">📁 项目管理</h3>
        <el-button type="primary" @click="openAdd">＋ 添加项目</el-button>
      </div>

      <el-table :data="projects" class="ep-table">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="name" label="项目名称" min-width="180" />
        <el-table-column label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="statusTag(row.status)" effect="plain" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="着重" width="90">
          <template #default="{ row }">{{ row.featured ? '⭐ 是' : '—' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row)">✏️ 编辑</el-button>
            <el-button
              size="small"
              :type="confirmRemoveId === row.id ? 'danger' : 'warning'"
              plain
              @click="askRemove(row)"
            >{{ confirmRemoveId === row.id ? '确认删除？' : '🗑️ 删除' }}</el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="暂无项目，点击「添加项目」创建" :image-size="70" />
        </template>
      </el-table>
    </section>

    <!-- ===== 项目编辑弹窗（el-dialog 对话框 + 表单）===== -->
    <ProjectEditModal
      v-if="editingProject !== null"
      :project="editingProject === 'new' ? null : editingProject"
      :is-new="editingProject === 'new'"
      @save="saveProject"
      @cancel="closeProjectEdit"
      @remove="removeProject"
    />
  </div>
</template>

<script setup>
// ===== 后台管理页（路由守卫 requiresAuth 保护，未登录不可访问）=====
// Pinia：userStore 管个人信息/登录态，projectStore 管项目数据；storeToRefs 解构保持响应式
// Element Plus：el-form 校验、el-table 列表、el-tag 状态、el-button 操作、ElMessage 轻提示
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/userStore'
import { useProjectStore } from '../stores/projectStore'
import ProjectEditModal from '../components/ProjectEditModal.vue'

const userStore = useUserStore()
const projectStore = useProjectStore()
const router = useRouter()

// storeToRefs 解构项目数组：增删改后表格自动更新（保持响应式）
const { projects } = storeToRefs(projectStore)

// ---------- 个人信息编辑表单（el-form 校验）----------
const profileFormRef = ref(null)
// 打开页面时从 userStore 拷贝一份，保存才写回 store（取消可丢弃修改）
const profileForm = ref({ ...userStore.profile })

// 表单校验规则：姓名必填、邮箱格式
const profileRules = {
  name: [{ required: true, message: '姓名不能为空', trigger: 'blur' }],
  email: [{ type: 'email', message: '邮箱格式不正确', trigger: 'blur' }]
}

// 取消修改：表单重置为 store 当前值
function resetProfile() {
  profileForm.value = { ...userStore.profile }
  showToast('已取消修改，表单已重置', 'info')
}

// 保存修改：先通过表单校验 → 调用 userStore.updateProfile → 提示
function saveProfile() {
  profileFormRef.value.validate((valid) => {
    if (!valid) return
    userStore.updateProfile({ ...profileForm.value })
    showToast('✓ 个人信息已保存')
  })
}

// ---------- 项目管理 ----------
const editingProject = ref(null)
// 二次点击确认删除：第一次点击进入"确认删除？"状态，5 秒内再次点击才真正删除
const confirmRemoveId = ref(null)
let confirmTimer = 0

function openAdd() {
  editingProject.value = 'new'
}

function openEdit(project) {
  editingProject.value = project
}

function closeProjectEdit() {
  editingProject.value = null
}

// 保存：调用 projectStore 的 actions（新建 addProject / 编辑 updateProject）
function saveProject(form) {
  if (editingProject.value === 'new') {
    projectStore.addProject(form)
    showToast('✓ 项目已添加')
  } else {
    projectStore.updateProject(form)
    showToast('✓ 项目已更新')
  }
  editingProject.value = null
}

// 删除前二次确认，避免误删（不依赖原生 confirm 弹窗）
function askRemove(p) {
  if (confirmRemoveId.value === p.id) {
    projectStore.removeProject(p.id)
    editingProject.value = null
    confirmRemoveId.value = null
    clearTimeout(confirmTimer)
    showToast('🗑️ 项目已删除')
  } else {
    confirmRemoveId.value = p.id
    showToast(`再次点击「确认删除」以删除「${p.name}」`, 'warning')
    clearTimeout(confirmTimer)
    confirmTimer = setTimeout(() => { confirmRemoveId.value = null }, 5000)
  }
}

// 状态 → el-tag 类型映射
function statusTag(status) {
  if (status === '已完成') return 'success'
  if (status === '进行中') return 'primary'
  return 'info'
}

// ---------- 退出登录 ----------
function handleLogout() {
  userStore.logout()
  showToast('已退出登录', 'info')
  setTimeout(() => router.push({ name: 'login' }), 400)
}

// ---------- 轻提示（Element Plus ElMessage）----------
function showToast(msg, type = 'success') {
  ElMessage({ message: msg, type, duration: 2200 })
}
</script>

<style scoped>
.admin-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
.admin-title { font-size: 22px; }
.admin-card { text-align: left; margin-bottom: 24px; }
.admin-card-title { font-size: 18px; margin-bottom: 16px; }
.admin-hint { font-size: 13px; color: var(--muted); margin-top: -6px; }
.admin-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}
.admin-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.entry-link {
  color: var(--accent);
  font-size: 14px;
  text-decoration: none;
  font-weight: 600;
}
.entry-link:hover { text-decoration: underline; }

/* el-form 表单：表单项纵向排列（与旧布局一致） */
.profile-form .form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 16px;
}
.form-field.full { grid-column: 1 / -1; }
.full-width { width: 100%; }
.profile-form :deep(.el-form-item) { margin-bottom: 14px; }
.profile-form :deep(.el-form-item__label) {
  color: var(--muted);
  font-size: 13px;
  padding-bottom: 4px;
}

/* el-table 玻璃化覆盖：透明底 + 半透明表头 */
.ep-table {
  width: 100%;
  margin-top: 6px;
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: rgba(148, 163, 184, 0.10);
  --el-table-border-color: var(--glass-border);
  --el-table-text-color: var(--text);
  --el-table-header-text-color: var(--muted);
  border-radius: 12px;
}
.ep-table :deep(.el-table__inner-wrapper::before) { display: none; }
</style>
