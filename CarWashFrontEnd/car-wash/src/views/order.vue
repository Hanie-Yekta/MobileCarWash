<script setup>
import { ref } from "vue";
import { store } from "@/stores";
import ChooseLocation from "@/components/view/choose-location.vue";
import ChooseCar from "@/components/view/choose-car.vue";
import ChooseTime from "@/components/view/choose-time.vue";
import Receipt from "@/views/receipt.vue";
const orderStore = store.orderStore();
const baseUrl = ref("http://127.0.0.1:8000");

const props = defineProps({
  slug: {
    required: true,
  },
});

const showLocation = ref(true);
const showTime = ref(false);
const showCar = ref(false);
const showReceipt = ref(false);

const showCarSelection = () => {
  if (props.slug == "ceramic-coating-car" || props.slug =="engine-wash") {
    showLocation.value = !showLocation.value;
    showTime.value = !showTime.value;
  } else {
    showLocation.value = !showLocation.value;
    showCar.value = !showCar.value;
  }
};
const showTimeSelection = () => {
  if (props.slug == "ceramic-coating-car" || props.slug == "engine-wash") {
    showLocation.value = !showLocation.value;
    showTime.value = !showTime.value;
  } else {
    showCar.value = !showCar.value;
    showTime.value = !showTime.value;
  }
};

const showPaymentPage =()=>{
  showTime.value = !showTime.value;
  showReceipt.value = !showReceipt.value;
}
</script>

<template>
  <div class="order-container">
    <h2 class="order-container__title">ثبت سفارش</h2>
    <div class="order-container__content">
      <div class="order-container__order-information order-information">
        <div>
          <img
            class="order-information__image"
            :src="baseUrl.concat(orderStore.order.image)"
          />
        </div>
        <p class="order-information__title">{{ orderStore.order.service }}</p>
      </div>
      <div class="order-container__complete-order complete-order">
        <choose-location
          @locationNext="showCarSelection"
          v-show="showLocation"
        />
        <choose-car
          @carNext="showTimeSelection"
          @carPrevious="showCarSelection"
          v-show="showCar"
        />
        <choose-time @timePrevious="showTimeSelection" @timeNext="showPaymentPage" v-show="showTime" />
        <Receipt @paymentPrevious="showPaymentPage" v-show="showReceipt"/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.order-container {
  background-color: #f9f9f9;
  height: 100vh;
  max-width: 100%;
  padding: 100px;

  &__content {
    display: flex;
    margin-top: 30px;
  }

  &__title {
    color: rgb(92, 91, 91);
    margin-top: 30px;
  }
}
.complete-order {
  width: 75%;
}
.order-information {
  width: 25%;
  background-color: white;
  box-shadow: 0px 0px 30px 0px rgba(24, 24, 24, 0.1);
  border-radius: 20px;
  padding: 20px;

  &__image {
    width: 100%;
    height: 320px;
    border-radius: 10px;
  }

  &__title {
    font-size: 23px;
    font-weight: bolder;
    margin-top: 25px;
  }
}
.order-steps {
  width: 80%;
  background-color: white;
}
</style>
