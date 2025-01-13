<script setup>
import { computed } from "vue";
import { store } from "@/stores";
import router from "@/router";
const userInfo = store.userInfoStore();
import AdminDashboard from "./admin-dashboard.vue";
import CustomerDashboard from "./customer-dashboard.vue";
import WorkerDahboard from "./worker-dashboard.vue";
import Calendar from "@/components/common/calendar.vue";
import Profile from "@/components/common/profile.vue";
import BaseButton from "@/components/common/base-button.vue";

const dashboardComponent = computed(() => {
  const role = userInfo.userInfo.role;
  switch (role) {
    case "customer":
      return CustomerDashboard;
    case "admin":
      return AdminDashboard;
    case "worker":
      return WorkerDahboard;
  }
});
</script>

<template>
  <div class="container">
    <div class="profile">
      <profile />
      <base-button
        class="profile__button"
        v-if="userInfo.userInfo.role == 'customer'"
        @click="$router.push({ name: 'services' })"
        size="x-large"
        >ثبت سفارش</base-button
      >
    </div>
    <component class="dashboard" :is="dashboardComponent" />
    <calendar class="calendar" />
  </div>
</template>
<style scoped lang="scss">
.container {
  background-color: #f9f9f9;
  display: flex;
  justify-content: space-between;
  flex-direction: row;
  min-height: 100vh;
  max-width: 100%;
  padding: 130px 40px;
}
.profile {
  position: fixed;
  width:20%;
  right:25px;
  &__button {
    margin-top: 30px;
  }
}
.calendar {
  width: 20%;
  position: fixed;
  left:25px;
}
.dashboard {
  width: 56%;
  margin-right:auto;
  margin-left: auto;

}
</style>
