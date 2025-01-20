<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import router from "@/router";
import BaseInput from "@/components/common/base-input.vue";
import BaseButton from "@/components/common/base-button.vue";
import BaseIcon from "@/components/common/base-icon.vue";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";
import { responseList } from "../responses/responses";
import { store } from "@/stores";

const authStore = store.authStore();
const emit = defineEmits(["update:modelValue"]);
const $toast = useToast();

const email = ref();
const password = ref();
const emailError = ref(false);
const hidePass = ref(true);
const disable = ref(true);
const passwordField = ref("password");
const emailValidation = ref("");
const emailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

const hide = () => {
  hidePass.value = !hidePass.value;
  if (passwordField.value == "password") passwordField.value = "text";
  else passwordField.value = "password";
};

const onUpdateValue = (emailValue) => {
  if (emailValue.match(emailformat) == null && emailValue != "") {
    emailValidation.value = responseList.authentication["email-validation"];
    emailError.value = true;
  } else {
    emailValidation.value = "";
    emailError.value = false;
  }
};

const startInterval = () => {
  setInterval(() => {
    refreshToken();
  }, 60 * 1000 * 60);
};

async function refreshToken() {
  try {
    const response = await axios({
      url: "http://127.0.0.1:8000/accounts/login/refresh/",
      method: "post",
      data: {
        refresh: authStore.refreshToken,
      },
    });
    authStore.setToken(response.data.access);
  } catch (error) {
    console.log(error);
  }
}

async function login() {
  try {
    const response = await axios({
      url: "http://127.0.0.1:8000/accounts/login/",
      method: "post",
      data: {
        email: email.value,
        password: password.value,
      },
    });
    authStore.setToken(response.data.access);
    authStore.setRefreshToken(response.data.refresh);
    $toast.open({
      message: responseList.authentication["success-login"],
      position: "top-left",
      type: "success",
    });
    router.push({ name: "home" });
    startInterval();
  } catch (error) {
    $toast.open({
      message: responseList.authentication["failed-login"],
      position: "top-left",
      type: "error",
    });
  }
}

watch(
  () => [email.value, password.value],
  () => {
    if (email.value && password.value && emailError.value == false) {
      disable.value = false;
    } else disable.value = true;
  }
);
</script>

<template>
  <div class="login-container">
    <base-icon
      @click="$router.go(-1)"
      class="login-container__back"
      iconName="back"
    />
    <h1>ورود</h1>
    <form class="login-form" @submit.prevent="login">
      <base-input
        @update:modelValue="(value) => onUpdateValue(value)"
        class="login-form__input"
        v-model:modelValue="email"
        :inputValue="email"
        label="ایمیل"
        icon="email"
        type="email"
        :error="emailError"
      />
      <p class="login-form_invalid-email">
        {{ emailValidation }}
      </p>
      <base-input
        class="login-form__input"
        v-model:modelValue="password"
        :inputValue="password"
        label="رمز عبور"
        icon="password"
        :type="passwordField"
      >
        <template #eye>
          <base-icon
            class="login-form__eye"
            iconName="closed-eye"
            v-if="hidePass"
            @click="hide"
          />
          <base-icon
            class="login-form__eye"
            iconName="eye"
            v-else
            @click="hide"
          /> </template
      ></base-input>
      <base-button
        class="login-form__button"
        :disabled="disable"
        varient="confirm"
        size="x-large"
      >
        ورود
      </base-button>
    </form>
    <div class="login-container__signup-links">
      <span>حساب کاربری ندارید؟</span>
      <base-button size="small" variant="link">
        <router-link
          class="login-container__signup-link"
          :to="{ name: 'worker-signup' }"
          >ثبت نام همیار</router-link
        >
      </base-button>
      <base-button size="small" variant="link">
        <router-link
          class="login-container__signup-link"
          :to="{ name: 'user-signup' }"
          >ثبت نام کاربر</router-link
        >
      </base-button>
    </div>
    <div class="login-container__forget-password">
      <router-link
        class="login-container__forget-password-link"
        :to="{ name: 'verifyphone' }"
        >رمز عبور خود را فراموش کرده اید؟</router-link
      >
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-container {
  padding: 50px;
  &__back {
    width: 35px;
    height: 35px;
  }
  &__signup-links {
    margin-top: 40px;
    display: flex;
    align-items: center;
    gap: 7px;
  }
  &__signup-link {
    text-decoration: none;
  }
  &__forget-password{
    margin-top: 10px;
  }
  &__forget-password-link{
    text-decoration:none;
    
  }
}

.login-form {
  &__input {
    margin-top: 30px;
  }

  &__eye {
    width: 30px;
    height: 30px;
  }

  &__button {
    margin-top: 50px;
  }

  &_invalid-email {
    color: red;
    font-size: 12px;
    margin-top: 5px;
  }
}

</style>
