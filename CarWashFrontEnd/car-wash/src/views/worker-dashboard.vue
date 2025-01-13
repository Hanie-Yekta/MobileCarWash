<script setup>
import { ref } from "vue";
import { store } from "@/stores";
import moment from "jalali-moment";
import Order from "@/components/view/order.vue";
import OrderDetail from "@/components/view/order-detail.vue";
import BlankDashboard from "@/components/view/blank-dashboard.vue";
import axios from "axios";

const authStore = store.authStore();

const orders = ref([]);
const comments = ref([]);
const showOrderDetail = ref([]);
const resetArray = (arr) => arr.map(() => false);
const showDark = ref(false);

const resetDeatail = () => {
  showOrderDetail.value = resetArray(showOrderDetail.value);
};

const convertTime = (time) => {
  return moment(time).locale("fa").format("YYYY/MM/DD LT");
};

const nextProcess = (status) => {
  if (status == "success-finish-cancel") {
    getWorkerDashboardInfo();
  }
  if (status == "success-change") {
    showDark.value = !showDark.value;
    resetDeatail();
    getWorkerDashboardInfo();
  } else if (status == "failed-change") {
    showDark.value = !showDark.value;
  }
};

const updateOrderDetailVisibility = (item, id) => {
  showDark.value = !showDark.value;

  if (item === "in_progress") {
    showOrderDetail.value = resetArray(showOrderDetail.value).map(
      (_, index) => index === id
    );
  } else if (item === "clean") {
    resetDeatail();
  }
};

async function getWorkerDashboardInfo() {
  try {
    const { data } = await axios({
      url: "http://127.0.0.1:8000/accounts/worker_profile/",
      method: "get",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });
    console.log(data);
    orders.value = data.orders;
    comments.value = data.comments;
    showOrderDetail.value = new Array(orders.value?.length).fill(false);
  } catch (error) {
    console.error("Error fetching dashboard info:", error);
  }
}

getWorkerDashboardInfo();
</script>

<template>
  <div class="dashboard-container">
    <div
      v-show="showDark"
      class="dark"
      @click="updateOrderDetailVisibility('clean')"
    ></div>
    <blank-dashboard v-if="orders.length == 0" />
    <div class="order" v-else>
      <p class="order__status">سفارشات</p>
      <div class="order__container">
        <div v-for="(item, index) in orders" :key="index">
          <order
            @showOrderDetail="updateOrderDetailVisibility(item.status, index)"
            @nextProcess="nextProcess"
            :order="item"
            :wokerRole="item?.worker?.is_worker"
          />
          <order-detail
            v-show="showOrderDetail[index]"
            @nextProcess="nextProcess"
            :wokerRole="item?.worker?.is_worker"
            :order="item"
            class="order-detail"
          />
        </div>
      </div>
    </div>
    <div v-if="comments.length !== 0" class="dashboard-container__comments-container">
      <p class="comments-container__title">نظرات</p>
      <div class="comments">
        <div
          class="comments__comment comment"
          v-for="(item, index) in comments"
          :key="index"
        >
          <p class="comment__name">
            {{ item.user.first_name }} {{ item.user.last_name }}
          </p>
          <div class="comment__body">{{ item.body }}</div>
          <hr />
          <div class="comment__footer">
            <div v-if="item.worker?.first_name">
              <span class="comment__worker-name">همیار: </span>
              <span>
                {{ item.worker.first_name }} {{ item.worker.last_name }}</span
              >
            </div>
            <span class="comment__time">{{ convertTime(item.created) }}</span>
          </div>
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

  &__comments-container {
    margin-top: 30px;
  }
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
.comments-container{
  &__title{
    font-size: 20px;
    font-weight: bold;
    color: rgb(81, 81, 81);
  }
}
.comments {
  display: flex;
  overflow-x: auto;
  @include scrollbars(5px, #96969690, #eee);
  width: 100%;
  gap: 20px;
  margin-top: 20px;
  &__comment {
    padding: 10px;
  }
}

.comment {
  background-color: rgb(242, 236, 254);
  box-shadow: 0px 2px 20px 0px rgba(0, 67, 101, 0.05);
  padding: 10px;
  border-radius: 20px;
  min-width: 350px;

  &__name {
    font-size: 15px;
    font-weight: bold;
    color: rgb(145, 151, 149);
  }

  &__footer {
    display: flex;
    justify-content: space-between;
  }

  &__worker-name {
    color: rgb(145, 151, 149);
    font-weight: bold;
  }

  &__time {
    color: #767dce;
    font-size: 15px;
    font-weight: 500;
  }
}
</style>
