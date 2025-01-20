<script setup>
import { ref } from "vue";
import axios from "axios";
import { store } from "@/stores";
const authStore = store.authStore();
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";
import BaseButton from "@/components/common/base-button.vue";
import BaseIcon from "@/components/common/base-icon.vue";
import { responseList } from "../../responses/responses";
const emit = defineEmits(["nextProcess","hideDetail"]);
const baseUrl = ref("http://127.0.0.1:8000");
const $toast = useToast();

const selectedWorker = ref();
const comment = ref();
const workerStatus = ref();

const props = defineProps({
  order: {
    type: Object,
    required: true,
  },
  workers: {
    type: Array,
  },
  wokerRole: {
    type: Boolean,
  },
});

async function changeWorkerStatus() {
  if (props.order?.worker_status == null) {
    workerStatus.value = "in_way";
  } else if (props.order?.worker_status == "in_way") {
    workerStatus.value = "doing";
  }
  try {
    await axios({
      url: `http://127.0.0.1:8000/orders/change_wstatus/${props.order.id}/`,
      method: "PUT",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
      data: {
        worker_status: workerStatus.value,
      },
    });
    $toast.open({
      message: responseList.order["success-change-worker-status"],
      position: "top-left",
      type: "success",
    });
    emit("nextProcess", "success-change");
  } catch (error) {
    $toast.open({
      message: responseList.order["failed-change-worker-status"],
      position: "top-left",
      type: "error",
    });
    emit("nextProcess","failed-change");
  }
}

async function selectWorker() {
  try {
    await axios({
      url: `http://127.0.0.1:8000/orders/order_detail/${props.order.id}/${selectedWorker.value}/`,
      method: "PUT",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });
    $toast.open({
      message: responseList.order["success-select-worker"],
      position: "top-left",
      type: "success",
    });
    emit("nextProcess", "success");
  } catch (error) {
    $toast.open({
      message: responseList.order["failed-select-worker"],
      position: "top-left",
      type: "error",
    });
    emit("nextProcess");
  }
}

async function submitFeedback() {
  try {
    await axios({
      url: `http://127.0.0.1:8000/orders/comment/${props.order.id}/`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
      data: {
        body: comment.value,
      },
    });
    $toast.open({
      message: responseList.order["success-submit-comment"],
      position: "top-left",
      type: "success",
    });
    comment.value = "";
    emit("nextProcess");
  } catch (error) {
    $toast.open({
      message: responseList.order["failed-submit-comment"],
      position: "top-left",
      type: "error",
    });
    comment.value = "";
    emit("nextProcess");
  }
}

async function payment() {
  try {
    await axios({
      url: `http://127.0.0.1:8000/orders/pay/${props.order.id}/`,
      method: "PUT",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });
    $toast.open({
      message: responseList.order["success-pay"],
      position: "top-left",
      type: "success",
    });
    emit("nextProcess", "success");
  } catch (error) {
    $toast.open({
      message: responseList.order["failed-pay"],
      position: "top-left",
      type: "error",
    });
    emit("nextProcess", "failed");
  }
}
</script>

<template>

  <div class="order-detail">
    <base-icon @click="$emit('hideDetail')" class="order-detail__close-icon" iconName="close"/>
    <div class="oreder-detail__image-container">
      <img
        class="order-detail__image"
        :src="baseUrl.concat(order.service.image)"
      />
    </div>
    <div class="order-detail__item" v-if="order?.service?.name">
      <span class="order-detail__title">نام سفارش:</span>
      <span>{{ order.service.name }}</span>
    </div>
    <div class="order-detail__item" v-if="order?.time">
      <span class="order-detail__title">زمان سفارش:</span>
      <span>{{ order.time }}</span>
    </div>
    <div class="order-detail__item" v-if="order?.address">
      <span class="order-detail__title">آدرس:</span>
      <span>{{ order.address }}</span>
    </div>
    <div class="order-detail__item" v-if="order?.car_type">
      <span class="order-detail__title">نوع اتومبیل:</span>
      <span v-if="order.car_type == 'suv'">شاسی بلند</span>
      <span v-else-if="order.car_type == 'hatchback'">هاچبک</span>
      <span v-else>سواری</span>
    </div>
    <div class="order-detail__item" v-if="order?.status">
      <span class="order-detail__title">وضعیت سفارش:</span>
      <span v-if="order.status == 'none'">پرداخت نشده</span>
      <span v-else-if="order.status == 'waiting'">در انتظار تایید</span>
      <span v-else-if="order.status == 'finished'">به اتمام رسیده</span>
      <span v-else>در حال انجام</span>
    </div>
    <div class="order-detail__item" v-if="order?.price">
      <span class="order-detail__title">هزینه سفارش:</span>
      <span>{{ order.price }} تومان</span>
    </div>
    <div class="order-detail__item" v-if="'worker_status' in order && order.status =='in_progress'">
      <span class="order-detail__title">وضعیت همیار:</span>
      <span v-if="order.worker_status == null">نیاز به تایید سفارش</span>
      <span v-if="order.worker_status == 'doing'">در حال انجام سفارش</span>
      <span v-if="order.worker_status == 'in_way'"> در مسیر</span>
    </div>
    <div class="order-detail__item" v-if="order.worker?.first_name">
      <span class="order-detail__title">نام همیار:</span>
      <span>{{ order.worker.first_name }} </span>
    </div>
    <div class="order-detail__item" v-if="order.worker?.last_name">
      <span class="order-detail__title">نام خانوادگی همیار:</span>
      <span>{{ order.worker.last_name }}</span>
    </div>
    <div class="order-detail__pay" v-if="order.status == null">
      <base-button @click="payment" size="x-large">پرداخت</base-button>
    </div>
    <div
      class="order-detail__comment comment"
      v-if="order.status == 'finished'"
    >
      <label class="comment__label"
        >نظر خود را درمورد این سرویس با ما درمیان بگذارید.</label
      >
      <textarea v-model="comment" class="comment__text"></textarea>
      <base-button class="comment__submit" @click="submitFeedback" size="small"
        >ثبت نظر</base-button
      >
    </div>
    <div v-if="props.workers" class="order-deatil__select-worker select-worker">
      <div
        v-if="props.workers?.length != 0"
        class="select-worker__available-worker"
      >
        <label for="workers" class="select-worker__label"
          >لطفا همیار موردنظر برای این سرویس را انتخاب کنید.</label
        >
        <select
          name="workers"
          v-model="selectedWorker"
          class="select-worker__selector"
        >
          <option
            class="select-worker__option"
            :value="item.email"
            v-for="(item, index) in workers"
            :key="index"
          >
            <p>{{ item.phone_number }} -</p>
            <p>{{ item.first_name }} {{ item.last_name }}</p>
          </option>
        </select>
        <base-button
          @click="selectWorker"
          class="select-worker__submit"
          size="small"
          >ثبت همیار</base-button
        >
      </div>
      <div v-else class="select-worker__not-available-worker">
        متاسفانه در حال حاضر همیار دردسترس وجود ندارد.
      </div>
    </div>
    <base-button
      class="order-detail__change-worker-status"
      v-if="wokerRole && order.worker_status != 'doing'"
      size="x-large"
      @click="changeWorkerStatus"
    >
      <span v-if="order.worker_status == null">پذیرش سفارش</span>
      <span v-if="order.worker_status == 'in_way'"> شروع کار</span>
    </base-button>
  </div>
</template>

<style scoped lang="scss">
.order-detail {
  width: inherit;
  padding: 15px;
  background: white;
  border-radius: 20px;
  z-index: 10;
  position: fixed;
  top: 4%;
  left: 35%;
  width: 27%;

  &__close-icon{
    width:30px;
    height: 30px;
    color:gray;
  }

  &__image {
    width: 100%;
    height: 220px;
    border-radius: 24px;
  }

  &__item {
    margin-top: 7px;
    font-size:14px;
  }

  &__title {
    color: rgb(162, 155, 173);
    padding-left: 5px;
    font-size:14px;
  }

  &__pay {
    margin-top: 20px;
  }

  &__change-worker-status {
    margin-top: 10px;
  }
}
.comment {
  margin-top: 20px;
  &__label {
    color: rgb(162, 155, 173);
  }
  &__text {
    margin-top: 10px;
    padding: 5px;
    border-radius: 5px;
    border: 1px solid rgb(220, 230, 255);
    width: 100%;
    height: 60px;
  }
  &__submit {
    margin-right: auto;
  }
}

.select-worker {
  &__selector {
    margin-top: 10px;
    outline-color: rgb(233, 172, 244);
    border: 1px solid rgb(233, 172, 244);
    border-radius: 10px;
    width: 100%;
    padding: 10px;
    display: flex;
  }

  &__phone {
    margin: 70px;
  }

  &__label {
    margin-top: 20px;
    color: rgb(162, 155, 173);
  }

  &__submit {
    margin-right: auto;
    margin-top: 10px;
  }

  &__not-available-worker {
    margin-top: 20px;
    color: rgb(162, 155, 173);
  }
}
</style>
