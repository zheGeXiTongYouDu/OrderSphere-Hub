<template>
  <div class="layout">
    <header class="header">
      <h1>OrderSphere-Hub 在线餐厅点餐系统</h1>
      <nav>
        <router-link to="/">首页</router-link>
        <router-link to="/menu">菜单点餐</router-link>
        <router-link to="/checkout">结算</router-link>
        <router-link to="/admin">订单管理</router-link>
      </nav>
    </header>
    <main class="main">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: #1f2933;
  color: #fff;
}
nav a {
  margin-left: 12px;
  color: #fff;
  text-decoration: none;
}
nav a.router-link-active {
  font-weight: bold;
  text-decoration: underline;
}
.main {
  padding: 16px 24px;
}
</style>
