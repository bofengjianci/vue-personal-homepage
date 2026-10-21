<template>
  <!-- ===== Element Plus 布局组件重构整体结构 =====
       el-container：外层容器（垂直方向）
       el-header  ：顶部区域（具名插槽 #header 注入导航）
       el-main    ：主体内容区（默认插槽注入路由页面）
       el-footer  ：底部区域（具名插槽 #footer，带默认回退内容） -->
  <el-container class="page" :class="isDark ? 'dark' : ''" direction="vertical">
    <!-- 光标跟随光斑（交互特效）：跟随鼠标的柔和光晕 -->
    <div ref="spotlightEl" class="spotlight" aria-hidden="true"></div>

    <el-header class="layout-header" height="auto">
      <slot name="header" />
    </el-header>

    <el-main class="layout-main">
      <div class="container">
        <slot />
      </div>
    </el-main>

    <el-footer class="layout-footer" height="auto">
      <slot name="footer">
        <footer class="app-footer">
          <div class="footer-inner">
            <p>© 2026 我的个人主页 · Powered by Vue 3</p>
          </div>
        </footer>
      </slot>
    </el-footer>
  </el-container>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

// isDark 由父组件 App.vue 传入（:is-dark="isDark"），用于切换 .dark 样式
defineProps({
  isDark: { type: Boolean, default: false }
})

// ===== 光标跟随光斑（spotlight）交互特效 =====
// 鼠标移动时，一层柔和光晕以 lerp（缓动插值）平滑跟随光标
const spotlightEl = ref(null)
let tx = 0  // 鼠标目标位置
let ty = 0
let cx = 0  // 光斑当前位置（向目标缓动）
let cy = 0
let raf = 0

function onMouseMove(e) {
  tx = e.clientX
  ty = e.clientY
}

function animateSpotlight() {
  cx += (tx - cx) * 0.12  // 缓动系数 0.12：数值越小跟随越"黏"
  cy += (ty - cy) * 0.12
  if (spotlightEl.value) {
    // 光斑 600×600，translate 偏移 -300 使其中心对准光标
    spotlightEl.value.style.transform = `translate(${cx - 300}px, ${cy - 300}px)`
  }
  raf = requestAnimationFrame(animateSpotlight)
}

onMounted(() => {
  window.addEventListener('mousemove', onMouseMove)
  raf = requestAnimationFrame(animateSpotlight)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', onMouseMove)
  cancelAnimationFrame(raf)
})
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

body { margin: 0; background: #eef2f7; }

.page {
  --bg: #eef2f7;
  --card: #ffffff;
  --text: #1f2937;
  --muted: #64748b;
  --border: #e2e8f0;
  --input-bg: #f1f5f9;
  --accent: #65a30d;
  --accent2: #a3e635;
  --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);

  /* 玻璃拟态变量：半透明磨砂卡片，亮/暗主题统一切换 */
  --glass: rgba(255, 255, 255, 0.6);
  --glass-strong: rgba(255, 255, 255, 0.72);
  --glass-border: rgba(255, 255, 255, 0.55);
  --glass-item: rgba(255, 255, 255, 0.5);
  --glass-shadow: 0 10px 30px rgba(15, 23, 42, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.6);

  min-height: 100vh;
  background:
    radial-gradient(ellipse 900px 550px at 8% 12%, rgba(163, 230, 53, 0.18), transparent 60%),
    radial-gradient(ellipse 750px 480px at 92% 6%, rgba(34, 197, 94, 0.13), transparent 60%),
    radial-gradient(ellipse 1000px 650px at 78% 92%, rgba(14, 165, 233, 0.10), transparent 60%),
    linear-gradient(180deg, #f2f7ea 0%, #eef2f7 45%, #e8eef4 100%);
  background-attachment: fixed;
  color: var(--text);
  font-family: "PingFang SC", "Microsoft YaHei", "Segoe UI", system-ui, sans-serif;
  padding-bottom: 48px;
}

.page.dark {
  --bg: #0b1220;
  --card: #151e30;
  --text: #e5eaf2;
  --muted: #8fa0b8;
  --border: #25324a;
  --input-bg: #1c2840;
  --shadow: 0 10px 30px rgba(0, 0, 0, 0.45);

  --glass: rgba(21, 30, 48, 0.6);
  --glass-strong: rgba(21, 30, 48, 0.72);
  --glass-border: rgba(255, 255, 255, 0.08);
  --glass-item: rgba(28, 40, 64, 0.5);
  --glass-shadow: 0 10px 30px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06);

  background:
    radial-gradient(ellipse 900px 550px at 8% 12%, rgba(163, 230, 53, 0.10), transparent 60%),
    radial-gradient(ellipse 750px 480px at 92% 6%, rgba(34, 197, 94, 0.07), transparent 60%),
    radial-gradient(ellipse 1000px 650px at 80% 92%, rgba(37, 99, 235, 0.14), transparent 60%),
    linear-gradient(180deg, #0e1728 0%, #0b1220 50%, #0a101d 100%);
  background-attachment: fixed;
}

/* 光标跟随光斑：半透明柔光，覆盖在内容之上，pointer-events 穿透
   暖金色系（避免与主题绿撞色） */
.spotlight {
  position: fixed;
  left: 0;
  top: 0;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  pointer-events: none;
  z-index: 2;
  background: radial-gradient(circle, rgba(251, 191, 36, 0.16) 0%, rgba(251, 191, 36, 0.05) 35%, transparent 65%);
  will-change: transform;
}
.page.dark .spotlight {
  background: radial-gradient(circle, rgba(251, 191, 36, 0.10) 0%, rgba(180, 83, 9, 0.04) 35%, transparent 65%);
}

.container { max-width: 860px; margin: 0 auto; padding: 32px 20px 0; }

/* ===== Element Plus 布局组件样式对齐（覆盖默认 padding/height）===== */
.layout-header { padding: 0; }
.layout-main { padding: 0; }
.layout-footer { padding: 0; }

/* 插槽默认内容（footer fallback）的样式 */
.app-footer {
  margin-top: 48px;
  border-top: 1px solid var(--glass-border);
  background: var(--glass-strong);
  backdrop-filter: blur(16px) saturate(1.4);
  -webkit-backdrop-filter: blur(16px) saturate(1.4);
}
.footer-inner {
  max-width: 860px;
  margin: 0 auto;
  padding: 20px;
  color: var(--muted);
  font-size: 13px;
}
</style>
