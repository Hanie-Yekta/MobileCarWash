<script setup>
import { ref, watch } from "vue";
import { store } from "@/stores";
import { useRoute } from "vue-router";
import BaseButton from "@/components/common/base-button.vue";
import CarType from "@/components/common/car-type.vue";

const route = useRoute();

const orderStore = store.orderStore();
const selectedCarIndex = ref();
const disableNext = ref(true);
const selectedCarPrice = ref();
const selectedCarType = ref();
const slug = route.params.slug;

watch(
  () => [selectedCarPrice.value, selectedCarType.value],
  () => {
    if (selectedCarPrice.value && selectedCarType.value) {
      disableNext.value = false;
    } else disableNext.value = true;
  }
);

const selectCar = (index, item) => {
  console.log(item.car_type)
  selectedCarIndex.value = index;
  selectedCarPrice.value = item.price;
  selectedCarType.value = item.car_type;
  orderStore.setOrderPrice(item.price);
  orderStore.setOrderCar(item.car_type);
};
</script>

<template>
  <div class="container">
    <p class="container__title">لطفا نوع اتومبیل خود را مشخص نمایید.</p>
    <div class="select-car">
      <car-type
        v-for="(item, index) in orderStore.order.prices"
        :key="item.id"
        class="select-car__car-type"
        :price="item.price"
        :carType="item.car_type"
        :selected="selectedCarIndex === index"
        @click="selectCar(index, item)"
      />
    </div>
    <div class="container__button-next">
      <base-button @click="$emit('carPrevious')" size="normal"
        >مرحله قبل</base-button
      >
      <base-button
        @click="$emit('carNext')"
        size="normal"
        :disabled="disableNext"
        >مرحله بعد</base-button
      >
    </div>
  </div>
</template>

<style scoped lang="scss">
.container {
  padding-right: 60px;

  &__title {
    color: rgb(164, 164, 164);
  }

  &__button-next {
    margin-top: 60px;
    display: flex;
    justify-content: end;
    gap: 5px;
  }
}

.select-car {
  border-radius: 20px;
  margin-top: 40px;
  display: flex;
  gap: 20px;
}
</style>
