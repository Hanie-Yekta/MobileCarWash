<template>
  <div class="step-progress">
    <div
      v-for="(item, index) in steps"
      :key="index"
      class="step-progress__step"
      @mouseover="showTooltip(index)"
      @mouseleave="hideTooltip"
    >
      <div v-if="tooltipIndex === index" class="step-progress__tooltip">
        {{ item.step }}
      </div>
      <div class="step-progress__number">{{ index + 1 }}</div>

      <base-icon class="step-progress__icon" :iconName="item.icon" />
    </div>
    <div
      v-for="index in steps.length - 1"
      :key="`line-${index}`"
      class="step-progress__line"
    ></div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import BaseIcon from "@/components/common/base-icon.vue";

const steps = ref([
  { step: "ثبت نام و وارد کردن اطلاعات", icon: "login" },
  { step: "انتخاب سرویس", icon: "car-wash" },
  { step: "انتخاب زمان", icon: "time" },
  { step: "انتخاب مکان", icon: "location" },
  { step: "ثبت نهایی", icon: "payment" },
]);
const tooltipIndex = ref(null);

const showTooltip = (index) => {
  tooltipIndex.value = index;
};

const hideTooltip = () => {
  tooltipIndex.value = null;
};
</script>

<style lang="scss" scoped>
.step-progress {
  display: flex;
  justify-content: space-between;
  position: relative;
  &__number {
    width: 40px;
    height: 40px;
    line-height: 40px;
    border-radius: 50%;
    background-color: #79cdc7;
    color: #fff;
  }

  &__icon {
    margin-top:10px;
    color: #436cff;
    width: 35px;
    height: 35px;
  }

  &__step {
    z-index: 1;
    text-align: center;
  }

  &__line {
    position: absolute;
    height: 4px;
    width: 100%;
    background-color: #bdbdbd;
    top: 20%;
  }

  &__tooltip {
    position: absolute;
    top: -50%;
    background-color: #bda3c5;
    color: #fff;
    padding: 5px 10px;
    border-radius: 4px;
    white-space: nowrap;
    font-size: 17px;
  }
}
</style>
