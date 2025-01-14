<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import { store } from "@/stores";
import router from "@/router";
import BaseInput from "@/components/common/base-input.vue";
import BaseButton from "@/components/common/base-button.vue";
import BaseIcon from "@/components/common/base-icon.vue";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";
import { responseList } from "../responses/responses";

const emit = defineEmits(["update:modelValue"]);
const $toast = useToast();
const forgetPassStore = store.forgetPassStore();

const phoneNumber = ref();
const phoneformat = /^(\+98|0)?9\d{9}$/;
const phoneValidation = ref();
const phoneError = ref(false);
const disable = ref(true);

const onUpdateValue = (value) => {
  if (value.match(phoneformat) == null && value != "") {
    phoneValidation.value = responseList.authentication["phone-validation"];
    phoneError.value = true;
  } else {
    phoneValidation.value = "";
    phoneError.value = false;
  }
};

watch(
  () => [phoneNumber.value],
  () => {
    if (phoneNumber.value && phoneError.value == false) {
      disable.value = false;
    } else disable.value = true;
  }
);

async function verifyPhone() {
  try {
    const response = await axios({
      url: "http://127.0.0.1:8000/accounts/forget_pass/",
      method: "post",
      data: {
        phone_number: phoneNumber.value,
      },
    });
    $toast.open({
      message: responseList.authentication["success-verify-phone"],
      position: "top-left",
      type: "success",
    });
    forgetPassStore.setPhone(phoneNumber.value);
    router.push({ name: "verifycode" });

  } catch (error) {
    $toast.open({
      message: responseList.authentication["failed-verify-phone"],
      position: "top-left",
      type: "error",
    });
  }
}
</script>

<template>
  <div class="enter-phone-container">
    <base-icon
      @click="$router.go(-1)"
      class="enter-phone-container__back"
      iconName="back"
    />
    <h2 class="enter-phone-container__title">تایید شماره تلفن</h2>
    <form
      class="enter-phone-container__enter-phone-form enter-phone-form"
      @submit.prevent="verifyPhone"
    >
      <p class="enter-phone-form__title">
        لطفا تلفن همراه خود را برای ارسال کد وارد کنید.
      </p>
      <base-input
        @update:modelValue="(value, type) => onUpdateValue(value, type)"
        class="enter-phone-form__input"
        v-model:modelValue="phoneNumber"
        :inputValue="phoneNumber"
        label="تلفن همراه"
        icon="phone"
        type="text"
        typeCheck="phoneNumber"
        :error="phoneError"
      />
      <p class="enter-phone-form__invalid-email">
        {{ phoneValidation }}
      </p>
      <base-button
        class="enter-phone-form__button"
        :disabled="disable"
        varient="confirm"
        size="x-large"
      >
        ارسال کد
      </base-button>
    </form>
  </div>
</template>

<style scoped lang="scss">
.enter-phone-container {
  padding: 50px;

  &__back {
    width: 35px;
    height: 35px;
  }

  &__enter-phone-form {
    margin-top: 80px;
  }
}

.enter-phone-form {
  &__title {
    font-size: 14px;
  }

  &__button {
    margin-top: 40px;
  }

  &__invalid-email {
    color: red;
    font-size: 12px;
    margin-top: 5px;
  }
}
</style>
