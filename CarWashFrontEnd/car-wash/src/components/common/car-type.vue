<script setup>
import {computed} from 'vue';
const props = defineProps({
  selected: {
    default:false
  },
  price: {
    type: Number,
  },
  carType: {
    type: String,
    validator(value) {
      return ["hatchback", "suv", "sedan"].includes(value);
    },
  },
});

const carTypeClasses = computed(() => {
  return {
    'car': true,
    'car__selected': props.selected,
  };
});
</script>

<template>
  <div class="car" :class="carTypeClasses">
    <div class="car__image-container">
      <img
        class="car__image"
        v-if="props.carType == 'suv'"
        src="../../assets/images/suv.webp"
      />
      <img
        class="car__image"
        v-if="props.carType == 'sedan'"
        src="../../assets/images/sedan.webp"
      />
      <img
        class="car__image"
        v-if="props.carType == 'hatchback'"
        src="../../assets/images/hatchback.webp"
      />
    </div>
    <div class="car__car-detail car-detail">
      <span class="car-detail__price"> {{ price }}تومان </span>
      <span class="car-detail__type" v-if="carType == 'sedan'">سواری</span>
      <span class="car-detail__type" v-else-if="carType == 'suv'"
        >شاسی بلند</span
      >
      <span class="car-detail__type" v-else>هاچبک</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.car {
  background-color: white;
  box-shadow: 0px 0px 30px 0px rgba(24, 24, 24, 0.1);
  padding: 20px;
  height: 250px;
  border-radius: 20px;

  &__selected{
    background-color: rgb(242, 251, 255);

  }

  &__image {
    width: 100%;
  }
}
.car-detail {
  display: flex;
  margin-top: 20px;
  gap: 5px;

  &__price {
    background-color: rgb(252, 212, 255);
    color: white;
    padding: 10px;
    border-radius: 20px;
  }

  &__type {
    background-color: rgb(255, 225, 150);
    color: white;
    padding: 10px;
    border-radius: 20px;
  }
}
</style>
