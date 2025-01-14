<script setup>
import { ref } from "vue";
import router from "@/router";

const props = defineProps(["service"]);

const baseUrl = ref("http://127.0.0.1:8000");
</script>
<template>
  <div class="card" @click="router.push({name:'service',params:{slug:props.service.slug}})">
    <div>
      <div>
        <img v-if="props.service.image" class="card__image" :src="baseUrl.concat(props.service.image)" />
      </div>
      <div class="card__title">{{ props.service.name }}</div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.card {
  width: 30%;
  border-radius: 20px;
  &:hover{
    background-color: rgb(254, 241, 255);
  }

  &__image {
    width: 100%;
    height: 250px;
    border-radius: 20px 20px 0px 0px;
  }

  &__title {
    padding: 25px;
    font-size: large;
    font-weight: bold;
    color: gray;
  }
}
</style>
