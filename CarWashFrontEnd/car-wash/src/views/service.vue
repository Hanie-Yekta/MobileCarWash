<script setup>
import { ref } from "vue";
import moment from "jalali-moment";
import axios from "axios";
import { store } from "@/stores";
import { useRoute } from "vue-router";
import router from "@/router";
import BaseButton from "@/components/common/base-button.vue";

const baseUrl = ref("http://127.0.0.1:8000");
const authStore = store.authStore();
const orderStore = store.orderStore();
const userInfo = store.userInfoStore();
const route = useRoute();
const slug = route.params.slug;
const serviceDetail = ref();

const convertTime = (time) => {
  return moment(time).locale("fa").format("YYYY/MM/DD LT");
};

const chooseService = (data) => {
  if (authStore.isAuthenticated && data.price.length == 3) {
    orderStore.setSlectedServiceInfo(data);
    router.push({ name: "order", params: { slug: data.slug } });
  }
  else if (authStore.isAuthenticated && data.price.length == 1)  {
    orderStore.setSpecialServiceInfo(data);
    router.push({ name: "order", params: { slug: data.slug } });
  } else {
    router.push({ name: "login" });
  }
};
async function getService() {
  const data = await axios({
    url: `http://127.0.0.1:8000/services/${slug}`,
    method: "get",
  });
  serviceDetail.value = data.data;
}
getService();
</script>

<template>
  <div class="container">
    <div class="service">
      <div class="service__image-conatiner" v-if="serviceDetail?.image">
        <img
          class="service__image"
          :src="baseUrl.concat(serviceDetail.image)"
        />
        <div class="service__pricees prices">
          <div
            class="prices__price-container"
            v-for="(item, index) in serviceDetail.price"
            :key="index"
          >
            <span class="prices__car" v-if="item.car_type == 'suv'"
              >سواری:</span
            >
            <span class="prices__car" v-else-if="item.car_type == 'hatchback'"
              >هاچبک:</span
            >
            <span class="prices__car" v-else-if="item.car_type == 'sedan'">شاسی بلند:</span>
            <span class="prices__price"> {{ item.price }} تومان</span>
          </div>
        </div>
      </div>
      <div class="service__content content">
        <div class="content__header" v-if="serviceDetail?.name">
          <h1 class="content__title">{{ serviceDetail.name }}</h1>
          <base-button v-if="userInfo.userInfo.role == 'customer'" @click="chooseService(serviceDetail)" size="large"
            >انتخاب سرویس</base-button
          >
        </div>
        <div class="content__description" v-if="serviceDetail?.description">
          {{ serviceDetail.description }}
        </div>
      </div>
    </div>
    <div v-if="serviceDetail?.comment" class="comments-container">
      <div class="comments">
        <div
          class="comments__comment comment"
          v-for="(item, index) in serviceDetail.comment"
          :key="index"
        >
          <p class="comment__name">
            {{ item.user.first_name }} {{ item.user.last_name }}
          </p>
          <div class="comment__body">{{ item.body }}</div>
          <hr />
          <div class="comment__footer">
            <div v-if="item.worker?.first_name">
              <span class="comment__worker-name">همیار: </span>
              <span>
                {{ item.worker.first_name }} {{ item.worker.last_name }}</span
              >
            </div>
            <span class="comment__time">{{ convertTime(item.created) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container {
  background-color: #f9f9f9;
  min-height: 100vh;
  max-width: 100%;
  padding: 50px;
}
.service {
  margin-top: 100px;
  display: flex;
  justify-content: space-between;
  gap: 40px;

  &__image {
    width: 570px;
    height: 390px;
    border-radius: 20px;
  }
}
.content {
  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  &__title {
    color: rgb(92, 91, 91);
  }
  &__description {
    background-color: white;
    color: gray;
    margin-top: 30px;
    padding: 20px;
    border-radius: 20px;
    line-height: 26px;
  }
}
.prices {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 20px;

  &__price-container {
    background-color: #bda3c5;
    padding: 12px;
    border-radius: 15px;
  }
  &__car {
    color: white;
    font-weight: bold;
    padding-left: 1px;
  }
  &__price {
    color: white;
  }
}

.comments-container {
  &__title {
    color: rgb(92, 91, 91);
  }
}
.comments {
  display: flex;
  overflow-x: auto;
  width: 100%;
  gap: 20px;
  margin-top: 20px;

  @include scrollbars(5px, #96969690, #eee);
  
  &__comment {
    padding: 20px;
  }
}

.comment {
  background-color: white;
  padding: 20px;
  border-radius: 20px;
  min-width: 800px;

  &__name {
    font-size: 15px;
    font-weight: bold;
    color: rgb(145, 151, 149);
  }

  &__footer {
    display: flex;
    justify-content: space-between;
  }

  &__worker-name {
    color: rgb(145, 151, 149);
    font-weight: bold;
  }

  &__time {
    color: #767dce;
    font-size: 15px;
    font-weight: 500;
  }
}
</style>
