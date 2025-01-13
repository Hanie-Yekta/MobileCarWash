<script setup>
import BaseIcon from "@/components/common/base-icon.vue";
</script>

<template>
  <div class="blank-dashboard">
    <div class="blank-dashboard__text" >سفارشی وجود ندارد.</div>
  </div>
</template>

<style scoped lang="scss">
.blank-dashboard {
  height: 400px;
  border-radius: 50px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
  justify-content: center;

  &__text{
    color:rgb(183, 183, 183);
    font-size:20px;
  }
}
</style>
