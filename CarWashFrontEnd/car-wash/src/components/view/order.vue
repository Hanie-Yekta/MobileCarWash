<script setup>
import axios from "axios";
import { store } from "@/stores";
const authStore = store.authStore();
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";
import BaseButton from "@/components/common/base-button.vue";
import { responseList } from "../../responses/responses.js";
const emit = defineEmits(["nextProcess","showOrderDetail"]);

const $toast = useToast();

const props = defineProps({
  order: {
    type: Object,
    required: true,
  },
  wokerRole: {
    type: Boolean,
  },
});

async function cancelOrder() {
  try {
   const response =  await axios({
      url: `http://127.0.0.1:8000/orders/cancel/${props.order.id}/`,
      method: "PUT",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });
    emit("nextProcess","success-finish-cancel");
    $toast.open({
      message: responseList.order["success-cancel"],
      position: "top-left",
      type: "success",
    });

  } catch (error) {
    $toast.open({
      message: responseList.order["failed-cancel"],
      position: "top-left",
      type: "error",
    });

  }
}

async function finishedOrder() {
  try {
   const response =  await axios({
      url: `http://127.0.0.1:8000/orders/finish/${props.order.id}/`,
      method: "PUT",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });
    emit("nextProcess","success-finish-cancel");
    $toast.open({
      message: responseList.order["success-finish"],
      position: "top-left",
      type: "success",
    });

  } catch (error) {
    $toast.open({
      message: responseList.order["failed-finish"],
      position: "top-left",
      type: "error",
    });

  }
}

</script>

<template>
  <div class="order" @click="$emit('showOrderDetail')">
    <p class="order__name">{{ order.service.name }}</p>
    <hr />
    <div class="order__footer">
      <p class="order__price">{{ order.price }} تومان</p>
      <p class="order__time">{{ order.time }}</p>
    </div>
    <div class="order__button" v-if="wokerRole">
      <base-button @click.stop="finishedOrder"  variant="confirm" size="normal"> اتمام سفارش</base-button>
      <base-button @click.stop="cancelOrder" variant="cancel" size="normal"> لغو سفارش</base-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.order {
  width: 200px;
  background-color: rgb(242, 236, 254);
  box-shadow: 0px 2px 20px 0px rgba(0, 67, 101, 0.05);
  border-radius: 20px;
  padding: 15px;

  &__footer {
    display: flex;
    justify-content: space-between;
  }

  &__name {
    font-weight: bold;
    color:rgb(110, 110, 110);
  }

  &__price{
    color:rgb(110, 110, 110);
  }

  &__time {
    color: #767dce;
  }

  &__button{
    display:flex;
    gap:10px;
  }
}
</style>
