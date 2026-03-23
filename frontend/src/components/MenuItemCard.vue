<template>
  <div class="card">
    <h3>{{ item.name }}</h3>
    <p class="desc">{{ item.description }}</p>
    <p class="meta">
      <span>价格：{{ item.price }}</span>
      <span v-if="item.region">地区：{{ item.region }}</span>
    </p>
    <button @click="addToCart">加入购物车</button>
  </div>
</template>

<script setup>
const props = defineProps({
  item: { type: Object, required: true }
})
const emits = defineEmits(['add'])

const addToCart = () => {
  emits('add', props.item)
}
</script>

<style scoped>
.card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
}
.desc {
  font-size: 14px;
  color: #4b5563;
}
.meta {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  margin: 8px 0;
}
button {
  padding: 6px 12px;
  background: #2563eb;
  color: #fff;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}
</style>
