<script setup>
import { ref } from "vue";
import { store } from "@/stores";
import axios from "axios";
import report from "@/components/view/report.vue";

const authStore = store.authStore();
const activeCustomers = ref([]);
const activeWorkers = ref([]);
const inactiveWorkers = ref([]);

async function getAdminDashboardInfo() {
  try {
    const { data } = await axios({
      url: "http://127.0.0.1:8000/accounts/admin_profile/",
      method: "get",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });
    activeCustomers.value = data.active_customers;
    activeWorkers.value = data.active_workers;
    inactiveWorkers.value = data.inactive_workers;
  } catch (error) {
    console.error(error);
  }
}

getAdminDashboardInfo();
</script>

<template>
  <div class="reports-container">
    <div
      v-if="activeCustomers.length"
      class="reports-container__activation-reports activation-reports"
    >
      <h3>فعال ترین مشتریان</h3>
      <div class="activation-reports__reports reports">
        <report
          v-for="(item, index) in activeCustomers"
          :key="index"
          :item="item"
        />
      </div>
    </div>
    <div
      v-if="activeWorkers.length"
      class="reports-container__activation-reports activation-reports"
    >
      <h3>فعال ترین همیاران</h3>
      <div class="activation-reports__reports reports">
        <report
          v-for="(item, index) in activeWorkers"
          :key="index"
          :item="item"
        />
      </div>
    </div>
    <div
      v-if="inactiveWorkers.length"
      class="reports-container__activation-reports activation-reports"
    >
      <h3>کم فعالیت ترین همیاران</h3>
      <div class="activation-reports__reports reports">
        <report
          v-for="(item, index) in inactiveWorkers"
          :key="index"
          :item="item"
          class="reports__report"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.reports-container {
  background-color: #f9f9f9;
  min-height: 100vh;
  max-width: 100%;
  padding: 100px 40px;

  &__activation-reports {
    margin-top: 50px;
  }
}
.activation-reports {
  &__reports {
    margin-top: 20px;
  }
}

.reports {
  display: flex;
  width: 100%;
  overflow: auto;
  gap: 20px;

  @include scrollbars(5px, #96969690, #eee);

  &__report {
    width: 300px;
  }
}
</style>
