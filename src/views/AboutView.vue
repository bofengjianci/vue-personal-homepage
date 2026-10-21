<template>
  <div>
    <!-- ===== 关于页：个人简介展示 ===== -->
    <section class="card profile-card">
      <div class="avatar-wrap">
        <img v-if="profile.avatar" :src="profile.avatar" alt="头像" @error="profile.avatar = ''">
        <span v-else class="avatar-fallback">{{ profile.name.charAt(0) }}</span>
      </div>
      <h2 class="name">{{ profile.name }}</h2>
      <p class="major">{{ profile.major }}</p>
      <p class="motto">“{{ profile.motto }}”</p>
      <p class="bio">{{ profile.bio }}</p>
    </section>

    <section class="card about-card">
      <h3 class="section-title">🧑‍🎓 基本信息</h3>
      <div class="about-grid">
        <div class="about-item"><span>学号</span><p>{{ profile.studentId }}</p></div>
        <div class="about-item"><span>学院</span><p>{{ profile.college }}</p></div>
        <div class="about-item"><span>所在城市</span><p>{{ profile.location }}</p></div>
        <div class="about-item"><span>生日</span><p>{{ profile.birthday }}</p></div>
        <div class="about-item full"><span>📧 邮箱</span><p>{{ profile.email }}</p></div>
        <div class="about-item full"><span>📱 电话</span><p>{{ profile.phone }}</p></div>
      </div>
    </section>

    <section class="card about-card">
      <h3 class="section-title">🎯 技能概览</h3>
      <div class="skills-summary">
        <span v-for="s in skills" :key="s.id" class="skill-chip">{{ s.icon }} {{ s.name }} · {{ s.level }}</span>
      </div>
    </section>

    <!-- ===== Element Plus 时间线组件：个人成长经历 =====
         el-timeline / el-timeline-item：带时间节点的纵向时间线，
         timestamp 显示时间，type 控制节点颜色 -->
    <section class="card about-card">
      <h3 class="section-title">🧭 个人经历</h3>
      <el-timeline class="exp-timeline">
        <el-timeline-item
          v-for="e in experiences"
          :key="e.id"
          :timestamp="e.time"
          :type="e.color"
          placement="top"
        >
          <div class="exp-card">
            <h4 class="exp-title">{{ e.title }}</h4>
            <p class="exp-desc">{{ e.desc }}</p>
          </div>
        </el-timeline-item>
      </el-timeline>
    </section>
  </div>
</template>

<script setup>
// ===== 关于页：只读展示个人资料（数据来自 Pinia userStore）=====
// storeToRefs 解构 profile / skills / experiences，保持响应式
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'

const userStore = useUserStore()
const { profile, skills, experiences } = storeToRefs(userStore)
</script>

<style scoped>
.about-card { margin-top: 24px; text-align: left; }
.about-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.about-item {
  /* 玻璃拟态格子：与首页技能卡片/文章卡片统一风格 */
  background: var(--glass-item);
  backdrop-filter: blur(12px) saturate(1.3);
  -webkit-backdrop-filter: blur(12px) saturate(1.3);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 12px 14px;
  transition: box-shadow 0.25s, transform 0.1s ease-out;
}
.about-item:hover {
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.14);
  transform: translateY(-1px);
}
.about-item.full { grid-column: 1 / -1; }
.about-item span { display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; }
.about-item p { font-size: 14px; word-break: break-all; }

.skills-summary { display: flex; flex-wrap: wrap; gap: 10px; }
.skill-chip {
  padding: 8px 16px;
  border-radius: 999px;
  background: var(--glass-item);
  border: 1px solid var(--glass-border);
  font-size: 13px;
}

/* 时间线卡片（el-timeline 内嵌内容） */
.exp-timeline { margin-top: 6px; }
.exp-card {
  background: var(--glass-item);
  backdrop-filter: blur(12px) saturate(1.3);
  -webkit-backdrop-filter: blur(12px) saturate(1.3);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 4px;
}
.exp-title { font-size: 15px; margin-bottom: 4px; }
.exp-desc { font-size: 13px; color: var(--muted); line-height: 1.7; }
</style>
