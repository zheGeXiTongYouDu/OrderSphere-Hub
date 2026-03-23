<template>
  <section>
    <h2>欢迎来到 OrderSphere-Hub</h2>
    <p>这是一个基于 Python + Vue + SQLite 的在线餐厅点餐系统示例。</p>
    <router-link to="/menu">
      <button>开始点餐</button>
    </router-link>
  </section>
</template>

<style scoped>
section {
  text-align: center;
  margin-top: 40px;
}
button {
  margin-top: 16px;
  padding: 8px 16px;
}
</style>
