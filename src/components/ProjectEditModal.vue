<template>
  <!-- ===== Element Plus 对话框组件：项目新增 / 编辑 =====
       el-dialog：对话框容器；el-form + el-input / el-select / el-checkbox 组合表单
       rules 校验项目名称必填；#footer 插槽放操作按钮 -->
  <el-dialog
    :model-value="true"
    :title="isNew ? '🚀 添加项目' : '✏️ 编辑项目'"
    width="600px"
    align-center
    class="project-dialog"
    @close="emit('cancel')"
    @update:model-value="(v) => { if (!v) emit('cancel') }"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
      <el-form-item label="项目名称 *" prop="name">
        <el-input v-model="form.name" placeholder="例如：个人主页" />
      </el-form-item>

      <el-form-item label="项目简介">
        <el-input v-model="form.description" type="textarea" :rows="3" placeholder="用一两句话介绍这个项目…" />
      </el-form-item>

      <div class="form-row">
        <el-form-item label="状态">
          <el-select v-model="form.status" class="full-width">
            <el-option label="已完成" value="已完成" />
            <el-option label="进行中" value="进行中" />
            <el-option label="规划中" value="规划中" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签（用逗号分隔）">
          <el-input v-model="tagsText" placeholder="Vue 3, Vite" />
        </el-form-item>
      </div>

      <el-form-item label="封面图片">
        <div class="image-input-row">
          <el-input v-model="form.image" placeholder="粘贴图片 URL，或上传本地图片" />
          <el-button type="success" plain @click="fileInput?.click()">📁 上传本地图片</el-button>
          <input ref="fileInput" type="file" accept="image/*" hidden @change="onFileChange">
        </div>
        <div v-if="form.image" class="image-preview">
          <img v-if="previewOk" :src="form.image" alt="封面预览">
          <span v-else class="preview-fallback">⚠️ 图片加载失败，请检查地址或换一张</span>
          <el-button class="remove-img" size="small" @click="form.image = ''">✕ 移除图片</el-button>
        </div>
      </el-form-item>

      <el-form-item>
        <el-checkbox v-model="form.featured">⭐ 设为着重项目（在板块中占据更大、更醒目的位置）</el-checkbox>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button v-if="!isNew" type="danger" plain @click="emit('remove', form.id)">🗑️ 删除项目</el-button>
      <el-button @click="emit('cancel')">取消</el-button>
      <el-button type="primary" @click="save">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

// ===== props：project=null 表示新建，传对象表示编辑 =====
const props = defineProps({
  project: { type: Object, default: null },
  isNew: { type: Boolean, default: false }
})

// ===== emits：保存 / 取消 / 删除，都交给父组件处理 =====
const emit = defineEmits(['save', 'cancel', 'remove'])

// 表单初始化：编辑 = 拷贝传入项目；新建 = 空模板
function emptyForm() {
  return { id: null, name: '', description: '', status: '进行中', tags: [], image: '', featured: false }
}
const form = ref({ ...emptyForm(), ...(props.project || {}) })
const tagsText = ref((props.project?.tags || []).join('，'))

// el-form 校验规则
const formRef = ref(null)
const rules = {
  name: [{ required: true, message: '请填写项目名称', trigger: 'blur' }]
}

// 预览图加载失败提示
const previewOk = ref(true)
watch(() => props.project?.image, () => { previewOk.value = true })

const fileInput = ref(null)

// ===== 本地图片上传：转 base64 存入表单（限制 800KB，防止撑爆 localStorage）=====
function onFileChange(e) {
  const file = e.target.files?.[0]
  if (!file) return
  if (file.size > 800 * 1024) {
    ElMessage.warning('图片超过 800KB，请改用图片 URL 方式，或压缩后再上传')
    e.target.value = ''
    return
  }
  const reader = new FileReader()
  reader.onload = () => {
    form.value.image = reader.result
    previewOk.value = true
  }
  reader.readAsDataURL(file)
  e.target.value = ''
}

// 保存：先过表单校验；标签文本 → 数组
function save() {
  formRef.value.validate((valid) => {
    if (!valid) return
    emit('save', {
      ...form.value,
      name: form.value.name.trim(),
      tags: tagsText.value.split(/[,，]/).map(t => t.trim()).filter(Boolean)
    })
  })
}
</script>

<style scoped>
/* el-dialog 玻璃化覆盖 */
.project-dialog {
  --el-dialog-bg-color: var(--card);
  --el-dialog-border-radius: 16px;
}
.project-dialog :deep(.el-dialog__title) { font-size: 18px; }

.full-width { width: 100%; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0 16px; }

.image-input-row { display: flex; gap: 10px; width: 100%; }
.image-input-row .el-input { flex: 1; min-width: 0; }

.image-preview {
  position: relative;
  margin-top: 10px;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}
.image-preview img {
  width: 100%;
  max-height: 220px;
  object-fit: cover;
  display: block;
}
.preview-fallback {
  display: block;
  padding: 30px;
  text-align: center;
  color: var(--muted);
  font-size: 13px;
}
.remove-img { position: absolute; top: 8px; right: 8px; }
</style>
