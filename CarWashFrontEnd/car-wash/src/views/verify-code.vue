<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import { store } from "@/stores";
import router from "@/router";
import BaseButton from "@/components/common/base-button.vue";
import BaseIcon from "@/components/common/base-icon.vue";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";
import { responseList } from "../responses/responses";
const forgetPassStore = store.forgetPassStore();

const emit = defineEmits(["update:modelValue"]);
const $toast = useToast();

const code = ref([]);
const disable = ref(true);
const keysAllowed = ref(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]);
code.value = new Array(4).fill("");

watch(
  () => code.value,
  () => {
    disable.value = code.value.includes("");
  },
  { deep: true }
);

async function verifyCode() {
  try {
    const response = await axios({
      url: `http://127.0.0.1:8000/accounts/verify_code/${forgetPassStore.phoneNumber}/`,
      method: "post",
      data: {
        code: code.value.join(""),
      },
    });
    $toast.open({
      message: responseList.authentication["success-verify-code"],
      position: "top-left",
      type: "success",
    });
    router.push({ name: "newpassword" });

  } catch (error) {
    console.log(error);
    $toast.open({
      message: responseList.authentication["failed-verify-code"],
      position: "top-left",
      type: "error",
    });
  }
}

const isNumber = (event) => {
  const keyPressed = event.key;
  if (
    !keysAllowed.value.includes(keyPressed) ||
    (code.value.length == 4 && !code.value.includes(""))
  ) {
    event.preventDefault();
  }
};

const handleInput = (event) => {
  const inputType = event.inputType;
  let currentActiveElement = event.target;
  if (inputType === "insertText")
    currentActiveElement.nextElementSibling?.focus();
};

const handleDelete = (event) => {
  let value = event.target.value;
  let currentActiveElement = event.target;
  if (!value) currentActiveElement.previousElementSibling?.focus();
};

const onPaste = (event) => {
  event.preventDefault();
  const pastedData = event.clipboardData?.getData("text").trim().split("");

  if (pastedData) {
    const filteredData = pastedData.filter((num) =>
      keysAllowed.value.includes(num)
    );


    for (let i = 0; i < filteredData.length; i++) {
      if (i < code.value.length) {
        code.value[i] = filteredData[i];
      }
    }

    let currentActiveElement = event.target;
    for (let i = 0; i < filteredData.length; i++) {
      if (currentActiveElement.nextElementSibling) {
        currentActiveElement.nextElementSibling.focus();
        currentActiveElement = currentActiveElement.nextElementSibling;
      }
    }
  }
};
</script>

<template>
  <div class="verify-code-container">
    <base-icon
      @click="$router.go(-1)"
      class="verify-code-container__back"
      iconName="back"
    />
    <h2 class="verify-code-container__title">کد تایید</h2>

    <form class="verify-code-container__verify-code-form verify-code-form" @submit.prevent="verifyCode">
      <p class="verify-code-form__title">لطفا کد پیامک شده را وارد کنید.</p>
      <div class="verify-code-form__input-container">
        <input
          v-for="(n, index) in code"
          :key="index"
          min="0"
          max="9"
          pattern="\d*"
          :id="'input_' + index"
          maxlength="1"
          v-model="code[index]"
          @input="handleInput"
          @keypress="isNumber"
          @keydown.delete="handleDelete"
          @paste="onPaste"
          class="verify-code-form__verify-input"
        />
      </div>
      <p class="verify-code-form__invalid-email"></p>
      <base-button
        class="verify-code-form__button"
        varient="confirm"
        size="x-large"
        :disabled="disable"
      >
        تایید کد
      </base-button>
    </form>
  </div>
</template>

<style scoped lang="scss">

.verify-code-container {
  padding: 50px;

  &__back {
    width: 35px;
    height: 35px;
  }

  &__verify-code-form {
    margin-top: 80px;
  }
}

.verify-code-form {
  &__input-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    direction: ltr;
  }

  &__title {
    font-size: 14px;
  }

  &__verify-input {
    direction: ltr;
    width: 50px;
    height: 50px;
    background-color: #f4f9fd;
    border: 1px solid #dbe8f2;
    border-radius: 16px;
    text-align: center;
    font-size: 20px;
    font-weight: 900;
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
