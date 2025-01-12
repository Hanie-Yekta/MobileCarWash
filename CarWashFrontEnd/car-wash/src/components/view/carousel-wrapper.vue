<script setup>
import { computed, ref } from "vue";
import IconButton from "@/components/common/icon-button.vue";


const currentShiftAmount = ref(0);
const carouselItem = ref();
let carouselItemIndex = ref(0);

const props = defineProps({
  carouselItems: {
    type: Array,
    required: true,
  },
});

const canMoveForward = computed(() => {
  return !(carouselItemIndex.value + 1 === props.carouselItems.length);
});

const canMoveBackward = computed(() => !(currentShiftAmount.value === 0));

const transformAmount = computed(() => `${currentShiftAmount.value}px`);

const moveCarousel = (direction) => {
  if (direction === "backward" && canMoveBackward.value) {
    carouselItemIndex.value--;
    currentShiftAmount.value -=
      carouselItem.value[carouselItemIndex.value]?.offsetWidth;
  } else if (direction === "forward" && canMoveForward.value) {
    currentShiftAmount.value += carouselItem.value[carouselItemIndex.value]?.offsetWidth;
    carouselItemIndex.value++;
  }
};
</script>

<template>
  <div class="carousel">
    <div class="carousel__container">
      <ul class="carousel__items">
        <li
          class="carousel__item"
          v-for="(item, index) in carouselItems"
          :key="index"
          ref="carouselItem"
        >
          <slot :item="item"></slot>
        </li>
      </ul>
    </div>
    <icon-button
      :disabled="!canMoveBackward"
      @click="moveCarousel('backward')"
      icon-name="arrow-right"
      class="carousel__backward carousel__icon"
      variant="text"
    />
    <icon-button
      :disabled="!canMoveForward"
      @click="moveCarousel('forward')"
      icon-name="arrow-left"
      class="carousel__forward carousel__icon"
      variant="text"
    />
  </div>
</template>


<style scoped lang="scss">
.carousel {
  position: relative;
  margin: 0 20px;

  &__container {
    overflow: hidden;
    margin: 0 20px;
  }

  &__items {
    display: flex;
    align-items: center;
    transform: translateX(v-bind(transformAmount));
    transition: transform 0.5s ease-in-out;
  }

  &__icon {
    position: absolute;
    transform: translate(0, -50%);
    top: 50%;
  }

  &__forward {
    left: 0;
  }

  &__backward {
    right: 0;
  }
}
</style>
