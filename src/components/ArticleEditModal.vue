<template>
  <!-- ===== Element Plus 对话框组件：文章新增 / 编辑（可复用）=====
       el-dialog + el-form：标题必填校验（rules）、el-input/el-select/el-date-picker 表单控件
       #footer 插槽：删除（仅编辑）/ 取消 / 保存按钮 -->
  <el-dialog
    :model-value="true"
    :title="isNew ? '📝 新建文章' : '✏️ 编辑文章'"
    width="520px"
    align-center
    class="article-dialog"
    @close="emit('cancel')"
    @update:model-value="(v) => { if (!v) emit('cancel') }"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
      <el-form-item label="标题 *" prop="title">
        <el-input v-model="form.title" placeholder="请输入文章标题" />
      </el-form-item>

      <el-form-item label="摘要">
        <el-input v-model="form.summary" placeholder="一句话概括文章内容" />
      </el-form-item>

      <el-form-item label="正文">
        <el-input v-model="form.content" type="textarea" :rows="4" placeholder="请输入文章正文内容" />
      </el-form-item>

      <div class="form-row">
        <el-form-item label="状态">
          <el-select v-model="form.status" class="full-width">
            <el-option label="已发布" value="已发布" />
            <el-option label="草稿" value="草稿" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker
            v-model="form.date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选择日期"
            class="full-width"
          />
        </el-form-item>
      </div>
    </el-form>

    <template #footer>
      <el-button v-if="!isNew" type="danger" plain @click="emit('remove', props.article)">🗑️ 删除</el-button>
      <el-button @click="emit('cancel')">取消</el-button>
      <el-button type="primary" @click="handleSave">💾 保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
// ===== 组件通信：defineProps 收数据，defineEmits 发事件 =====
// props.article：待编辑文章（null 表示新建）；父组件通过 isNew 区分新建/编辑
import { reactive, ref, watch } from 'vue'

const props = defineProps({
  article: { type: Object, default: null },
  isNew: { type: Boolean, default: false }
})
const emit = defineEmits(['save', 'cancel', 'remove'])

// 表单独立状态：每次打开时从 props 拷贝一份，提交时才 emit 给父组件
const form = reactive({
  title: '', summary: '', content: '', status: '已发布', date: ''
})

// el-form 校验规则：标题必填
const formRef = ref(null)
const rules = {
  title: [{ required: true, message: '标题不能为空', trigger: 'blur' }]
}

// 打开弹窗时回填数据（新建给默认日期）
watch(
  () => props.article,
  (val) => {
    if (val) {
      Object.assign(form, {
        title: val.title || '',
        summary: val.summary || '',
        content: val.content || '',
        status: val.status || '已发布',
        date: val.date || ''
      })
    } else {
      Object.assign(form, {
        title: '', summary: '', content: '', status: '已发布', date: new Date().toISOString().slice(0, 10)
      })
    }
  },
  { immediate: true }
)

// 保存：先过 el-form 校验 → emit('save', 表单数据)
function handleSave() {
  formRef.value.validate((valid) => {
    if (!valid) return
    emit('save', { ...form, title: form.title.trim() })
  })
}
</script>

<style scoped>
.article-dialog {
  --el-dialog-bg-color: var(--card);
  --el-dialog-border-radius: 16px;
}
.article-dialog :deep(.el-dialog__title) { font-size: 18px; }

.full-width { width: 100%; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0 16px; }
</style>
