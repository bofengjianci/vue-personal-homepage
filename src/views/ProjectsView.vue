<template>
  <!-- ===== 项目页（嵌套路由父容器）=====
       /projects        → 渲染子路由"项目列表"
       /projects/:id    → 渲染子路由"项目详情"
       RouterView 会根据 URL 自动切换渲染哪个子路由 -->
  <div class="projects-page">
    <RouterView />
  </div>
</template>

<script setup>
// 父路由组件：只提供页面容器与子路由出口，具体内容由子路由组件渲染
</script>

<style scoped>
.projects-page { min-height: 40vh; }
</style>
