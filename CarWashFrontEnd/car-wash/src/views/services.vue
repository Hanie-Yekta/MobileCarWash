<script setup>
import {ref} from 'vue';
import { store } from "@/stores";
import axios from "axios";
import ServiceCard from "../components/view/service-card.vue";

const serviceStore = store.servicesStore();
const services = ref([]);


async function getServices() {
  const data = await axios({
    url: "http://127.0.0.1:8000/services/",
    method: "get",
  });
  services.value = data.data;
  console.log(data)
  serviceStore.setService(services.value);
}
getServices();

</script>

<template>
  <div class="container">
    <div class="services">
      <service-card
        v-for="(item, index) in serviceStore.services"
        :key="index"
        :service="item"
      />
    </div>
  </div>
</template>
<style scoped lang="scss">
.container {
  background-color: #f9f9f9;
  min-height: 100vh;
  max-width: 100%;
  padding: 100px;
}
.services {
  display: flex;
  margin-top:50px;
  flex-wrap: wrap;
  gap:50px;
}

</style>
