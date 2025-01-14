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

const forgetPassStore = store.forgetPassStore();
const emit = defineEmits(["update:modelValue"]);
const $toast = useToast();

const password = ref();
const hidePass = ref(true);
const hideConfirmPass = ref(true);
const passwordField = ref("password");
const passwordMatch = ref("");
const passwordMatchError = ref(false);
const passwordFieldConfirm = ref("password");
const passwordConfirmation = ref();
const disable = ref(true);

const hide = (type) => {
  if (type == "pass") {
    hidePass.value = !hidePass.value;
    if (passwordField.value == "password") passwordField.value = "text";
    else passwordField.value = "password";
  } else {
    hideConfirmPass.value = !hideConfirmPass.value;
    if (passwordFieldConfirm.value == "password")
      passwordFieldConfirm.value = "text";
    else passwordFieldConfirm.value = "password";
  }
};

const onUpdateValue = (confirmPass) => {
  if (confirmPass != password.value && confirmPass != "") {
    passwordMatchError.value = true;
    passwordMatch.value = responseList.authentication["password-match"];
  } else {
    passwordMatchError.value = false;
    passwordMatch.value = "";
  }
};

watch(
  () => [password.value, passwordConfirmation.value],
  () => {
    if (password.value == passwordConfirmation.value) {
      disable.value = false;
    } else {
      disable.value = true;
    }
  }
);

async function changePassword() {
  try {
    const response = await axios({
      url: `http://127.0.0.1:8000/accounts/change_pass/${forgetPassStore.phoneNumber}/`,
      method: "post",
      data: {
        password1: password.value,
        password2: passwordConfirmation.value,
      },
    });
    $toast.open({
      message: responseList.authentication["success-change-password"],
      position: "top-left",
      type: "success",
    });
    router.push({ name: "login" });
  } catch (error) {
    $toast.open({
      message: responseList.authentication["failed-change-password"],
      position: "top-left",
      type: "error",
    });
    router.push({ name: "login" });
  }
}
</script>

<template>
  <div class="change-password-container">
    <base-icon
      @click="$router.go(-1)"
      class="change-password-container__back"
      iconName="back"
    />
    <h2 class="change-password-container__title">تغییر رمز عبور</h2>
    <form
      @submit.prevent="changePassword"
      class="change-password-container__change-password-form change-password-form"
    >
      <p class="change-password-form__title">
        لطفا رمز عبور جدید خود را وارد کنید.
      </p>
      <base-input
        class="change-password-form__input"
        v-model:modelValue="password"
        :inputValue="password"
        label="رمز عبور"
        icon="password"
        :type="passwordField"
      >
        <template #eye>
          <base-icon
            class="change-password-form__eye"
            iconName="closed-eye"
            v-if="hidePass"
            @click="hide('pass')" />
          <base-icon
            class="change-password-form__eye"
            iconName="eye"
            v-else
            @click="hide('pass')" /></template
      ></base-input>
      <base-input
        @update:modelValue="(value) => onUpdateValue(value)"
        class="change-password-form__input"
        v-model:modelValue="passwordConfirmation"
        :inputValue="passwordConfirmation"
        label="تکرار رمز"
        icon="password"
        :type="passwordFieldConfirm"
        :error="passwordMatchError"
      >
        <template #eye>
          <base-icon
            class="change-password-form__eye"
            iconName="closed-eye"
            v-if="hideConfirmPass"
            @click="hide('confirm')" />
          <base-icon
            class="change-password-form__eye"
            iconName="eye"
            v-else
            @click="hide('confirm')" /></template
      ></base-input>
      <p class="change-password-form__invalid-input">
        {{ passwordMatch }}
      </p>
      <base-button
        class="change-password-form__button"
        :disabled="disable"
        varient="confirm"
        size="x-large"
      >
        تغییر رمز
      </base-button>
    </form>
  </div>
</template>

<style scoped lang="scss">
.change-password-container {
  padding: 50px;

  &__back {
    width: 35px;
    height: 35px;
  }

  &__change-password-form {
    margin-top: 80px;
  }
}

.change-password-form {
  &__title {
    font-size: 14px;
  }

  &__button {
    margin-top: 40px;
  }

  &__input {
    margin-top: 25px;
  }

  &__eye {
    width: 30px;
    height: 30px;
  }

  &__invalid-input {
    color: red;
    font-size: 12px;
    margin-top: 5px;
  }
}
</style>
