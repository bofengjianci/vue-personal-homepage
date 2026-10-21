<template>
  <!-- ===== 登录页（身份认证）===== -->
  <section class="card login-card">
    <div class="login-icon">🔐</div>
    <h2 class="login-title">后台管理登录</h2>
    <p class="login-tip">登录后可进入后台管理页面，修改个人简介与项目信息</p>

    <form class="login-form" @submit.prevent="handleLogin">
      <div class="form-field">
        <label>用户名</label>
        <input v-model="username" type="text" placeholder="请输入用户名" autocomplete="username">
      </div>
      <div class="form-field">
        <label>密码</label>
        <input v-model="password" type="password" placeholder="请输入密码" autocomplete="current-password">
      </div>

      <p v-if="errorMsg" class="login-error">⚠️ {{ errorMsg }}</p>

      <button type="submit" class="btn primary login-btn" :disabled="loading">
        {{ loading ? '登录中…' : '登 录' }}
      </button>
    </form>

    <p class="login-hint">演示账号：admin　密码：123456</p>
    <button class="btn back-btn" @click="router.push({ name: 'home' })">← 返回首页</button>
  </section>
</template>

<script setup>
// ===== 登录页：表单校验 → userStore.login() → 跳转 redirect 目标或后台 =====
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'

const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)

function handleLogin() {
  // 表单校验
  if (!username.value.trim() || !password.value) {
    errorMsg.value = '请输入用户名和密码'
    return
  }
  loading.value = true
  // 模拟登录请求：稍作延迟后校验账号
  setTimeout(() => {
    if (username.value.trim() === 'admin' && password.value === '123456') {
      userStore.login()
      errorMsg.value = ''
      // 登录成功后跳回原目标（路由守卫携带的 redirect），否则进后台管理
      const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : ''
      router.push(redirect || { name: 'admin' })
    } else {
      errorMsg.value = '用户名或密码错误'
      loading.value = false
    }
  }, 400)
}
</script>

<style scoped>
.login-card {
  max-width: 420px;
  margin: 24px auto 0;
  text-align: center;
}
.login-icon { font-size: 44px; margin-bottom: 10px; }
.login-title { font-size: 22px; margin-bottom: 8px; }
.login-tip { font-size: 13px; color: var(--muted); margin-bottom: 22px; }
.login-form { display: flex; flex-direction: column; gap: 14px; text-align: left; }
.login-error { color: #ef4444; font-size: 13px; }
.login-btn { width: 100%; margin-top: 4px; }
.login-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.login-hint {
  margin-top: 18px;
  font-size: 12px;
  color: var(--muted);
  background: var(--input-bg);
  padding: 8px;
  border-radius: 8px;
}
.back-btn { margin-top: 16px; }
</style>
