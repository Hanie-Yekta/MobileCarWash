<script setup>
import { ref } from "vue";
import { store } from "@/stores";
import axios from "axios";
import router from "@/router";
import BaseButton from "@/components/common/base-button.vue";
import BaseIcon from "@/components/common/base-icon.vue";
const authStore = store.authStore();
const userInfo = store.userInfoStore();

const navItems = ref([
  { name: "خانه", link: "home", icon: "home" },
  { name: "درباره ما", link: "about-us", icon: "about-us" },
  { name: "تماس با ما", link: "contact-us", icon: "phone" },
  { name: "خدمات", link: "services", type: "normal", icon: "services" },
]);

const notLoggedInItems = ref([
  { name: "ورود", link: "login" },
  { name: "ثبت نام کاربر", link: "user-signup" },
  { name: "ثبت نام همیار", link: "worker-signup" },
]);

async function logout() {
  try {
    const response = await axios({
      url: "http://127.0.0.1:8000/accounts/logout/",
      method: "get",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });
    authStore.clearToken();
    router.push({ name: "login" });
  } catch (error) {
    console.log(error);
  }
}

async function getProfile() {
  try {
    const response = await axios({
      url: "http://127.0.0.1:8000/accounts/get_info/",
      method: "get",
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });
    userInfo.setInfo(response.data);
    console.log(response.data);
  } catch (error) {
    console.log(error);
  }
}
if(authStore.token){
  getProfile();
}

</script>

<template>
  <nav class="navbar">
    <ul>
      <li v-for="item in navItems" :key="item.name">
        <base-icon class="navbar__icon" :iconName="item.icon" />
        <router-link class="navbar__link" :to="{ name: item.link }">{{
          item.name
        }}</router-link>
      </li>
    </ul>
    <ul v-if="!authStore.isAuthenticated">
      <li v-for="item in notLoggedInItems" :key="item.name">
        <router-link class="navbar__link" :to="{ name: item.link }">{{
          item.name
        }}</router-link>
      </li>
    </ul>
    <ul v-else>
      <li>
        <router-link class="navbar__link" :to="{ name: 'dashboard' }"
          >داشبورد</router-link
        >
      </li>
      <li>
        {{ userInfo.userInfo.firstName }} {{ userInfo.userInfo.lastName }}
      </li>
      <li>
        <base-button
          class="navbar__logout"
          @click="logout"
          size="normal"
          variant="cancel"
          >خروج</base-button
        >
      </li>
    </ul>
  </nav>
</template>

<style scoped lang="scss">
.navbar {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  height: 100px;
  background-color: white;
  padding: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 3;

  &__icon {
    width: 45px;
    height: 45px;
    padding: 5px;
    color: rgb(232, 207, 255);
  }

  &__link {
    text-decoration: none;
    color: rgb(152, 151, 151);

    &:hover {
      color: rgb(106, 105, 107);
      font-weight: bold;
    }
  }
}

.navbar ul {
  display: flex;
  align-items: center;
  gap: 40px;
}
</style>
