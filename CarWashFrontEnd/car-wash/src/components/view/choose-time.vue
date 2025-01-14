<script setup>
import { ref, watch } from "vue";
import { useRoute } from 'vue-router';
import axios from "axios";
import { VTimePicker } from "vuetify/labs/VTimePicker";
import BaseButton from "@/components/common/base-button.vue";
import { responseList } from "@/responses/responses";
import "vue-toast-notification/dist/theme-sugar.css";
import { useToast } from "vue-toast-notification";
const authStore = store.authStore();


import { store } from "@/stores";
const $toast = useToast();
const emit = defineEmits(["timeNext"]);

const orderStore = store.orderStore();
const route = useRoute();


const time = ref();
const disableNext = ref(true);
const slug = route.params.slug;


async function orderBooking() {
  orderStore.setOrderTime(time.value);
  try {
    const response = await axios({
      url: `http://127.0.0.1:8000/orders/${slug}/`,
      method: "post",
      data: {
        car_type: orderStore.order.car,
        address: orderStore.order.address ,
        time: time.value,
      },
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });
    $toast.open({
      message: responseList.order["success-order"],
      position: "top-left",
      type: "success",
    });
    emit("timeNext");
  } catch (error) {
    $toast.open({
      message: responseList.order["failed-order"],
      position: "top-left",
      type: "error",
    });
  }
}
watch(
  () => [time.value],
  () => {
    if (time.value) {
      disableNext.value = false;
    } else disableNext.value = true;
  }
);
</script>

<template>
  <div class="container">
    <p class="container__title">لطفا زمان موردنظر خود را انتخاب نمایید.</p>
    <div class="container__select-time select-time">
      <v-time-picker
        class="time-picker"
        v-model="time"
        color="blue"
        header-color="blue"
      ></v-time-picker>
      <div class="select-time__button-next">
        <base-button @click="$emit('timePrevious')" size="normal"
          >مرحله قبل</base-button
        >
        <base-button @click="orderBooking" size="normal" :disabled="disableNext"
          >ثبت سفارش</base-button
        >
      </div>
    </div>
  </div>
</template>
<style scoped lang="scss">
.container {
  padding-right: 60px;

  &__title {
    color: rgb(164, 164, 164);
  }
}
.select-time {
  display: flex;
  justify-content: space-between;

  &__button-next {
    display: flex;
    justify-content: end;
    margin-top: auto;
    gap: 10px;
  }
}
.time-picker {
  border: 1px solid rgb(219, 219, 219);
  border-radius: 20px;
  width: 650px;
}
</style>
