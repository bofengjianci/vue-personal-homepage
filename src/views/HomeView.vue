<template>
  <div>
    <!-- ===== 个人简介卡片 ===== -->
    <section class="card profile-card" @mousemove="handleTilt" @mouseleave="resetTilt">
      <div class="avatar-wrap">
        <img v-if="userStore.profile.avatar" :src="userStore.profile.avatar" alt="头像" @error="userStore.profile.avatar = ''">
        <span v-else class="avatar-fallback">{{ userStore.profile.name.charAt(0) }}</span>
      </div>

      <h2 class="name">{{ userStore.profile.name }}</h2>
      <p class="major">{{ userStore.profile.major }}</p>
      <p class="motto">“{{ userStore.profile.motto }}”</p>
      <p class="bio">{{ userStore.profile.bio }}</p>

      <div class="detail" v-show="showDetail">
        <div class="detail-item"><span>学号</span><p>{{ userStore.profile.studentId }}</p></div>
        <div class="detail-item"><span>学院</span><p>{{ userStore.profile.college }}</p></div>
        <div class="detail-item"><span>📧 邮箱</span><p>{{ userStore.profile.email }}</p></div>
        <div class="detail-item"><span>📱 电话</span><p>{{ userStore.profile.phone }}</p></div>
        <div class="detail-item"><span>📍 所在城市</span><p>{{ userStore.profile.location }}</p></div>
        <div class="detail-item"><span>🎂 生日</span><p>{{ userStore.profile.birthday }}</p></div>
      </div>

      <div class="btn-row">
        <button class="btn" @click="toggleDetail">{{ showDetail ? '收起详情 ▲' : '展开详情 ▼' }}</button>
        <!-- 内容修改入口统一放到后台管理页（需要登录），与访客浏览功能区分 -->
        <button class="btn primary" @click="goAdmin">🔒 后台管理</button>
      </div>
    </section>

    <!-- ===== 技能与兴趣卡片 ===== -->
    <section class="card skills-card">
      <h3 class="section-title">🎯 技能与兴趣</h3>

      <input class="search-input" v-model="searchKeyword" type="text"
             placeholder="🔍 输入关键词搜索技能（支持名称 / 分类）">

      <p class="result-count">共 {{ filteredSkills.length }} 项技能</p>

      <div class="skill-grid" v-if="filteredSkills.length">
        <div class="skill-item" v-for="skill in filteredSkills" :key="skill.id"
             @mousemove="handleTilt" @mouseleave="resetTilt">
          <div class="skill-icon">{{ skill.icon }}</div>
          <div class="skill-info">
            <h4>{{ skill.name }}</h4>
            <p class="skill-meta">{{ skill.category }} · {{ skill.level }}</p>
            <div class="level-bar">
              <div class="level-fill" :style="{ width: skill.percent + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="empty-state" v-else>😕 没有找到与“{{ searchKeyword }}”匹配的技能</div>
    </section>

    <!-- ===== 项目预览板块（复用 ProjectsSection）
         访客点击卡片 → 跳项目详情页；点击添加 → 进入后台管理（守卫拦截未登录）===== -->
    <ProjectsSection
      :projects="projects"
      @add="goAdmin"
      @edit="goDetail"
    />
  </div>
</template>

<script setup>
// ===== 首页视图 =====
// Pinia：userStore 提供个人简介/技能，projectStore 提供项目预览数据
// storeToRefs 解构 state/getters 保持响应式；跳转使用 useRouter() 编程式导航
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import { useProjectStore } from '../stores/projectStore'
import ProjectsSection from '../components/ProjectsSection.vue'

const userStore = useUserStore()
const projectStore = useProjectStore()
const router = useRouter()

// storeToRefs 解构：skills 响应式可搜索；projects 传给项目预览板块
const { skills } = storeToRefs(userStore)
const { projects } = storeToRefs(projectStore)

const searchKeyword = ref('')
const showDetail = ref(false)

// 技能筛选（名称 / 分类）
const filteredSkills = computed(() => {
  const kw = searchKeyword.value.trim().toLowerCase()
  if (!kw) return skills.value
  return skills.value.filter(s =>
    s.name.toLowerCase().includes(kw) ||
    s.category.toLowerCase().includes(kw)
  )
})

function toggleDetail() {
  showDetail.value = !showDetail.value
}

// 编程式跳转：进入后台管理（未登录会被路由守卫引导到登录页）
function goAdmin() {
  router.push({ name: 'admin' })
}

// 编程式跳转：点击项目卡片 → 动态路由详情页 /projects/:id
function goDetail(project) {
  router.push({ name: 'project-detail', params: { id: project.id } })
}

// ===== 卡片 3D 倾斜交互特效 =====
function handleTilt(e) {
  const el = e.currentTarget
  const rect = el.getBoundingClientRect()
  const px = (e.clientX - rect.left) / rect.width
  const py = (e.clientY - rect.top) / rect.height
  const rx = (0.5 - py) * 10
  const ry = (px - 0.5) * 12
  el.style.transform = `perspective(700px) rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg) translateY(-4px)`
}

function resetTilt(e) {
  e.currentTarget.style.transform = ''
}
</script>
