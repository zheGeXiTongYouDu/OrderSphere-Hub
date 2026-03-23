<template>
  <div class="cart">
    <h3>购物车</h3>
    <div v-if="items.length === 0">购物车为空</div>
    <ul v-else>
      <li v-for="item in items" :key="item.id">
        <span>{{ item.name }} x {{ item.quantity }}</span>
        <span>¥ {{ (item.price * item.quantity).toFixed(2) }}</span>
      </li>
    </ul>
    <p class="total">合计：¥ {{ total.toFixed(2) }}</p>
    <router-link to="/checkout">
      <button :disabled="items.length === 0">去结算</button>
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: { type: Array, required: true }
})

const total = computed(() =>
  props.items.reduce((sum, i) => sum + i.price * i.quantity, 0)
)
</script>

<style scoped>
.cart {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
}
li {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}
.total {
  margin-top: 8px;
  font-weight: bold;
}
button {
  margin-top: 8px;
  padding: 6px 12px;
}
</style>
