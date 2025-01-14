<script setup>
import BaseButton from "@/components/common/base-button.vue";
import { store } from "@/stores";
const orderStore = store.orderStore();
</script>

<template>
  <div class="container">
    <div class="order">
      <h3 class="order__title">سفارش شما:</h3>
      <div class="order__item">
        <span class="order__name">سرویس: </span>
        <span>{{ orderStore.order.service }}</span>
      </div>
      <div class="order__item">
        <span class="order__name">زمان: </span>
        <span>{{ orderStore.order.time }}</span>
      </div>
      <div class="order__item" v-if="orderStore.order.car != 'all_types'">
        <span class="order__name">اتومبیل: </span>
        <span v-if="orderStore.order.car == 'sedan'">سواری</span>
        <span v-else-if="orderStore.order.car == 'hatchback'">هاچبک</span>
        <span v-else>شاسی بلند</span>
      </div>
      <div class="order__item">
        <span class="order__name">قیمت: </span>
        <span>{{ orderStore.order.price }} تومان</span>
      </div>
      <div class="order__item">
        <span class="order__name">آدرس: </span>
        <span>{{ orderStore.order.address }}</span>
      </div>
    </div>
    <div class="container__button-next">
      <base-button @click="$router.push({ name: 'dashboard' })" size="normal"
        >داشبورد</base-button
      >
    </div>
  </div>
</template>

<style scoped lang="scss">
.container {
  padding-right: 60px;

  &__button-next {
    display: flex;
    justify-content: end;
    margin-top: 30px;
    gap: 10px;
  }
}

.order {
  background-color: white;
  box-shadow: 0px 2px 20px 0px rgba(0, 67, 101, 0.05);
  padding: 40px;
  border-radius: 20px;

  &__title {
    color: rgb(252, 212, 255);
  }

  &__item {
    margin-top: 20px;
    font-size: 18px;
  }

  &__name {
    color: rgb(192, 192, 192);
    font-weight: bold;
  }
}
</style>
