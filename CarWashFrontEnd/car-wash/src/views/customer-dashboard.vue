<script setup>
import { ref } from "vue";
import { store } from "@/stores";
import Order from "@/components/view/order.vue";
import OrderDetail from "@/components/view/order-detail.vue";
import BlankDashboard from "@/components/view/blank-dashboard.vue";
import axios from "axios";
const authStore = store.authStore();

const orders = ref([]);
const waitingOrders = ref([]);
const finishedOrders = ref([]);
const notPaidOrders = ref([]);
const inProgressOrders = ref([]);

const showWaitingOrderDetail = ref([]);
const showFinishedOrderDetail = ref([]);
const showNotPaidOrderDetail = ref([]);
const showInProgressOrderDetail = ref([]);

const resetArray = (arr) => arr.map(() => false);

const showDark = ref(false);
const finishedFlag = ref(false);
const waitingFlag = ref(false);
const notPaiedFlag = ref(false);
const inProgressFlag = ref(false);

const nextProcess = (status) => {
  showDark.value = !showDark.value;
  resetDeatail();
  if (status == "success") {
    finishedFlag.value = false;
    waitingFlag.value = false;
    notPaiedFlag.value = false;
    inProgressFlag.value = false;
    getCustomerDashboardInfo();
  }
};

const resetDeatail = () => {
  showWaitingOrderDetail.value = resetArray(showWaitingOrderDetail.value);
  showFinishedOrderDetail.value = resetArray(showFinishedOrderDetail.value);
  showNotPaidOrderDetail.value = resetArray(showNotPaidOrderDetail.value);
  showInProgressOrderDetail.value = resetArray(showInProgressOrderDetail.value);
};
const updateOrderDetailVisibility = (item, id) => {
  showDark.value = !showDark.value;

  if (item === "finished") {
    showFinishedOrderDetail.value = resetArray(
      showFinishedOrderDetail.value
    ).map((_, index) => index === id);
  } else if (item === "waiting") {
    showWaitingOrderDetail.value = resetArray(showWaitingOrderDetail.value).map(
      (_, index) => index === id
    );
  } else if (item === null) {
    showNotPaidOrderDetail.value = resetArray(showNotPaidOrderDetail.value).map(
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

async function getCustomerDashboardInfo() {
  try {
    const { data } = await axios({
      url: "http://127.0.0.1:8000/accounts/customer_profile/",
      method: "get",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });

    orders.value = data.orders;
    waitingOrders.value = [];
    finishedOrders.value = [];
    notPaidOrders.value = [];
    inProgressOrders.value = [];

    orders.value.forEach((element) => {
      if (element.status === "finished") {
        finishedFlag.value = true;
        finishedOrders.value.push(element);
      } else if (element.status === "waiting") {
        waitingFlag.value = true;
        waitingOrders.value.push(element);
      } else if (element.status === null) {
        notPaiedFlag.value = true;
        notPaidOrders.value.push(element);
      } else if (element.status === "in_progress") {
        inProgressFlag.value = true;
        inProgressOrders.value.push(element);
      }
    });

    showWaitingOrderDetail.value = new Array(waitingOrders.value.length).fill(
      false
    );
    showFinishedOrderDetail.value = new Array(finishedOrders.value.length).fill(
      false
    );
    showNotPaidOrderDetail.value = new Array(notPaidOrders.value.length).fill(
      false
    );
    showInProgressOrderDetail.value = new Array(
      inProgressOrders.value.length
    ).fill(false);
  } catch (error) {
    console.error("Error fetching dashboard info:", error);
  }
}

getCustomerDashboardInfo();
</script>

<template>
  <div class="dashboard-container">
    <div
      v-show="showDark"
      class="dark"
      @click="updateOrderDetailVisibility('clean')"
    ></div>
    <blank-dashboard v-if="orders?.length == 0" />
    <div v-else>
      <p v-show="waitingFlag" class="order__status">در انتظار تایید</p>
      <div class="order__container" >
        <div v-for="(item, index) in waitingOrders" :key="index">
          <order
            @showOrderDetail="updateOrderDetailVisibility(item.status, index)"
            :order="item"
          />
          <order-detail
            v-show="showWaitingOrderDetail[index]"
            @nextProcess="nextProcess"
            :order="item"
            class="order-detail"
          />
        </div>
      </div>

      <p class="order__status" v-show="notPaiedFlag">در انتظار پرداخت</p>
      <div class="order__container">
        <div v-for="(item, index) in notPaidOrders" :key="index">
          <order
            @showOrderDetail="updateOrderDetailVisibility(item.status, index)"
            :order="item"
          />
          <order-detail
            @nextProcess="nextProcess"
            v-show="showNotPaidOrderDetail[index]"
            :order="item"
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
            @nextProcess="nextProcess"
            :order="item"
            class="order-detail"
          />
        </div>
      </div>

      <p class="order__status" v-show="finishedFlag">به پایان رسیده</p>
      <div class="order__container">
        <div v-for="(item, index) in finishedOrders" :key="index">
          <order
            @showOrderDetail="updateOrderDetailVisibility(item.status, index)"
            :order="item"
          />
          <order-detail
            v-show="showFinishedOrderDetail[index]"
            @nextProcess="nextProcess"
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
