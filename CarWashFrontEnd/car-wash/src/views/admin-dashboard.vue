<script setup>
import { ref } from "vue";
import { store } from "@/stores";
import Order from "@/components/view/order.vue";
import OrderDetail from "@/components/view/order-detail.vue";
import BlankDashboard from "@/components/view/blank-dashboard.vue";
import axios from "axios";

const authStore = store.authStore();

const orders = ref([]);
const workers = ref([]);
const waitingOrders = ref([]);
const inProgressOrders = ref([]);
const showWaitingOrderDetail = ref([]);
const showInProgressOrderDetail = ref([]);

const resetArray = (arr) => arr.map(() => false);

const showDark = ref(false);
const waitingFlag = ref(false);
const inProgressFlag = ref(false);

const resetDeatail = () => {
  showWaitingOrderDetail.value = resetArray(showWaitingOrderDetail.value);
  showInProgressOrderDetail.value = resetArray(showInProgressOrderDetail.value);
};

const nextProcess = (status) => {
  showDark.value = !showDark.value;
  resetDeatail();
  if (status == "success") {
    waitingFlag.value = false;
    inProgressFlag.value = false;
    getAdminDashboardInfo();
  }
};

const updateOrderDetailVisibility = (item, id) => {
  showDark.value = !showDark.value;

  if (item === "waiting") {
    showWaitingOrderDetail.value = resetArray(showWaitingOrderDetail.value).map(
      (_, index) => index === id
    );
  } else if (item === "in_progress") {
    showInProgressOrderDetail.value = resetArray(
      showInProgressOrderDetail.value
    ).map((_, index) => index === id);
  } else if (item === "clean") {
    resetDeatail();
  }
};

async function getAdminDashboardInfo() {
  try {
    const { data } = await axios({
      url: "http://127.0.0.1:8000/accounts/admin_profile/",
      method: "get",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });
    console.log(data);
    workers.value = data.available_workers;
    orders.value = data.orders;
    waitingOrders.value = [];
    inProgressOrders.value = [];

    orders.value.forEach((element) => {
      if (element.status === "waiting") {
        waitingFlag.value = true;
        waitingOrders.value.push(element);
      } else if (element.status === "in_progress") {
        inProgressFlag.value = true;
        inProgressOrders.value.push(element);
      }
    });

    showWaitingOrderDetail.value = new Array(waitingOrders.value.length).fill(
      false
    );
    showInProgressOrderDetail.value = new Array(
      inProgressOrders.value.length
    ).fill(false);
  } catch (error) {
    console.error("Error fetching dashboard info:", error);
  }
}

getAdminDashboardInfo();
</script>

<template>
  <div class="dashboard-container">
    <div
      v-show="showDark"
      class="dark"
      @click="updateOrderDetailVisibility('clean')"
    ></div>
    <blank-dashboard v-if="orders?.length === 0" />
    <div v-else>
      <p class="order__status" v-show="waitingFlag">در انتظار تایید</p>
      <div class="order__container" >
        <div v-for="(item, index) in waitingOrders" :key="index">
          <order
            @showOrderDetail="updateOrderDetailVisibility(item.status, index)"
            :order="item"
          />
          <order-detail
            v-show="showWaitingOrderDetail[index]"
            :order="item"
            :workers="workers"
            @nextProcess="nextProcess"
            class="order-detail"
          />
        </div>
      </div>

      <p class="order__status" v-show="inProgressFlag">در حال انجام</p>
      <div class="order__container">
        <div v-for="(item, index) in inProgressOrders" :key="index">
          <order
            @showOrderDetail="updateOrderDetailVisibility(item.status, index)"
            :order="item"
          />
          <order-detail
            v-show="showInProgressOrderDetail[index]"
            :order="item"
            class="order-detail"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.dashboard-container {
  background-color: rgb(255, 255, 255);
  padding: 10px 50px 50px 50px;
  border-radius: 20px;
}

.order {
  &__status {
    font-size: 20px;
    font-weight: bold;
    color: rgb(81, 81, 81);
    margin-top: 30px;
  }

  &__container {
    display: flex;
    gap: 15px;
    overflow: auto;
    @include scrollbars(5px, #96969690, #eee);
  }
}

.dark {
  background: rgba(0, 0, 0, 0.6);
  z-index: 3;
  position: fixed;
  width: 100%;
  height: 100vh;
  bottom: 0;
  left: 0;
  right: 0;
  top: 0;
}
</style>
