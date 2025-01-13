<script setup>
import {ref } from "vue";
import router from "@/router";
import Navbar from "@/components/common/main-navbar.vue";
import axios from "axios";
import { store} from '@/stores';
import IntroductionVideo from "../components/view/introduction-video.vue";
import BaseButton from "@/components/common/base-button.vue";
import ProgressBar from "@/components/view/progress-bar.vue";
import carouselWrapper from "@/components/view/carousel-wrapper.vue";
import carouselItem from "@/components/view/carousel-item.vue";

const authStore = store.authStore();
const serviceStore = store.servicesStore();
const services = ref([]);

const order = () => {
  if (authStore.isAuthenticated) {
    router.push({ name: "services" });
  } else {
    router.push({ name: "login" });
  }
};

async function getServices() {
  const data = await axios({
    url: "http://127.0.0.1:8000/services/",
  });
  services.value = data.data;
  serviceStore.setService(services.value);

}
getServices();
</script>

<template>
  <div class="container">
    <navbar />
    <div class="introduction">
      <div class="introduction__content content">
        <h1 class="content__title">کوییک واش</h1>
        <p class="content__summary">
          تجربه‌ی تمیزی و درخشندگی بی‌نظیر در هر زمان و هر مکان!
        </p>
        <div class="content__description">
          ما معتقدیم که هر خودرو نیاز به مراقبت ویژه‌ای دارد و به همین دلیل
          خدمات ما متنوع و منحصربه‌فرد هستند. با تجهیزات پیشرفته و تیمی متخصص،
          ما به شما اطمینان می‌دهیم که خودروی شما همیشه در بهترین وضعیت خود
          باشد. ما به جزئیات اهمیت می‌دهیم و هدف ما راحتی و رضایت شماست.
        </div>
        <base-button
          @click="order"
          class="content__button"
          varient="confirm"
          size="large"
        >
      خدمات کوییک واش
        </base-button>
      </div>
      <div class="introduction__video">
        <introduction-video />
      </div>
    </div>
    <div class="step-progress-bar">
      <h3 class="step-progress-bar__title">مراحل ثبت سفارش</h3>
      <progress-bar class="step-progress-bar__bar" />
    </div>
    <div class="carousel">
      <h3 class="carousel__title">خدمات</h3>
      <carousel-wrapper class="carousel__carousel-wrapper" :carouselItems="serviceStore.services" v-slot="{ item }">
        <div class="carousel__item">
          <carouselItem @click="$router.push({ name: 'service', params: { slug: item.slug } })" :service="item" />
        </div>
      </carousel-wrapper>
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
.introduction {
  display: flex;
  justify-content: space-between;
  padding: 50px;
  margin-top: 30px;
  background-color: white;
  border-radius: 20px;
}
.content {
  padding-left: 50px;
  &__title {
    color: gray;
  }
  &__summary {
    color: rgb(198, 197, 197);
    margin-top: 15px;
  }
  &__description {
    margin-top: 25px;
    color: gray;
    font-size: 20px;
    line-height: 1.8;
  }
  &__button {
    margin-top: 30px;
  }
}
.step-progress-bar {
  &__title {
    margin-top: 100px;
    color: gray;
  }
  &__bar {
    margin-top: 80px;
  }
}
.carousel {
  &__item {
    padding-left: 15px;
  }
  &__title {
    margin-top: 100px;
    color: gray;
  }
  &__carousel-wrapper{
    margin-top: 30px;

  }
}
</style>
