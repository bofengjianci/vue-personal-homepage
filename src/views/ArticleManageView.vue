<template>
  <div class="admin-page">
    <!-- ===== 顶部栏：返回后台 + 标题 ===== -->
    <div class="admin-top">
      <h2 class="admin-title">📝 文章管理</h2>
      <el-button @click="router.push({ name: 'admin' })">← 返回后台</el-button>
    </div>

    <!-- ===== 文章列表（Element Plus 表格：增 / 删 / 改）=====
         el-table / el-table-column：展示文章；#default 插槽定制状态标签与操作按钮 -->
    <section class="card admin-card">
      <div class="admin-head">
        <h3 class="admin-card-title">📚 文章列表（{{ articleStore.articleCount }}）</h3>
        <el-button type="primary" @click="openAdd">＋ 添加文章</el-button>
      </div>

      <el-table :data="articles" class="ep-table">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="row.status === '已发布' ? 'success' : 'info'" effect="plain" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="日期" width="130" />
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
          <el-empty description="暂无文章，点击「添加文章」创建" :image-size="70" />
        </template>
      </el-table>
    </section>

    <!-- ===== 文章编辑弹窗（el-dialog 对话框 + 表单，复用组件）===== -->
    <ArticleEditModal
      v-if="editingArticle !== null"
      :article="editingArticle === 'new' ? null : editingArticle"
      :is-new="editingArticle === 'new'"
      @save="saveArticle"
      @cancel="closeArticleEdit"
      @remove="removeArticle"
    />
  </div>
</template>

<script setup>
// ===== 文章管理页（/admin/articles，路由守卫 requiresAuth 保护）=====
// storeToRefs：解构 Store 数据保持响应式；actions 通过 store 实例调用
// Element Plus：el-table 列表、el-tag 状态、el-button 操作、ElMessage 轻提示
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useArticleStore } from '../stores/articleStore'
import ArticleEditModal from '../components/ArticleEditModal.vue'

const articleStore = useArticleStore()
const router = useRouter()

// storeToRefs 解构 state（保持响应式，增删改后表格自动更新）
const { articles } = storeToRefs(articleStore)

// ---------- 文章管理 ----------
const editingArticle = ref(null)
// 二次点击确认删除（不依赖原生 confirm 弹窗）
const confirmRemoveId = ref(null)
let confirmTimer = 0

function openAdd() {
  editingArticle.value = 'new'
}

function openEdit(article) {
  editingArticle.value = article
}

function closeArticleEdit() {
  editingArticle.value = null
}

// 保存：调用 articleStore 的 actions（新建 addArticle / 编辑 updateArticle）
function saveArticle(form) {
  if (editingArticle.value === 'new') {
    articleStore.addArticle(form)
    showToast('✓ 文章已添加')
  } else {
    articleStore.updateArticle(form)
    showToast('✓ 文章已更新')
  }
  editingArticle.value = null
}

// 删除：调用 articleStore.removeArticle（二次点击确认防误删）
function askRemove(a) {
  if (confirmRemoveId.value === a.id) {
    articleStore.removeArticle(a.id)
    editingArticle.value = null
    confirmRemoveId.value = null
    clearTimeout(confirmTimer)
    showToast('🗑️ 文章已删除')
  } else {
    confirmRemoveId.value = a.id
    showToast(`再次点击「确认删除」以删除「${a.title}」`, 'warning')
    clearTimeout(confirmTimer)
    confirmTimer = setTimeout(() => { confirmRemoveId.value = null }, 5000)
  }
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
.admin-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

/* el-table 玻璃化覆盖 */
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
