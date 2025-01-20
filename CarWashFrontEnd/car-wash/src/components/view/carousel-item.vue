<script setup>
import { computed } from "vue";

  const props = defineProps({
    service: {
      type: Object,
      required: true,
    },
  });

const backgroundImage = computed(() => {
  const baseUrl = "http://127.0.0.1:8000";
  const x = baseUrl.concat(props.service.image);
  return `url(${x})`;
});
</script>

<template>
  <div @click="$router.push({ name: 'service', params: { slug: props.service.slug } })"  class="layer">
    <div class="service">
      <div class="service__service-content service-content">
        <span class="service-content__name">{{ service.name }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">

.service {
  padding: 30px;
  z-index:10;
  border-radius: 12px;
  background-color: rgb(218, 212, 212);
  background-size: cover;
  background-image: v-bind(backgroundImage);
  overflow: hidden;
  width: 249px;
  height: 195px;
  transition: {
    property: width, height;
    timing-function: ease-out;
    duration: 0.25s;
  }

  &:hover {
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.5); 
    width: 320px;
    height: 250px;
    font-size:20px;
  }
}

.service-content {
  z-index: 1;
  padding: 10px;
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.6);
  width:fit-content;
  margin-top: 50%;

  &__name {
    color: rgb(107, 80, 115);
    font-weight: bolder;
  }
}
</style>
