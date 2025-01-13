<script setup>
import { ref, watch } from "vue";
import router from "@/router";
import axios from "axios";
import BaseInput from "@/components/common/base-input.vue";
import BaseButton from "@/components/common/base-button.vue";
import BaseIcon from "@/components/common/base-icon.vue";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";
import { responseList } from "../responses/responses";

const emit = defineEmits(["update:modelValue"]);
const $toast = useToast();

const email = ref();
const password = ref();
const phoneNumber = ref();
const gender = ref();
const firstName = ref();
const lastName = ref();
const hidePass = ref(true);
const disable = ref(true);
const passwordField = ref("password");
const emailValidation = ref("");
const phoneValidation = ref("");
const emailError = ref(false);
const phoneError = ref(false);
const emailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
const phoneformat = /^(\+98|0)?9\d{9}$/;

const hide = () => {
  hidePass.value = !hidePass.value;
  if (passwordField.value == "password") passwordField.value = "text";
  else passwordField.value = "password";
};

const onUpdateValue = (value, type) => {
  if (type == "email") {
    if (value.match(emailformat) == null && value != "") {
      emailValidation.value = responseList.authentication["email-validation"];
      emailError.value = true;
    } else {
      emailValidation.value = "";
      emailError.value = false;
    }
  }
  if (type == "phoneNumber") {
    if (value.match(phoneformat) == null && value != "") {
      phoneValidation.value = responseList.authentication["phone-validation"];
      phoneError.value = true;
    } else {
      phoneValidation.value = "";
      phoneError.value = false;
    }
  }
};

async function signup() {
  try {
    const response = await axios({
      url: "http://127.0.0.1:8000/accounts/register/",
      method: "post",
      data: {
        email: email.value,
        password: password.value,
        first_name: firstName.value,
        last_name: lastName.value,
        phone_number: phoneNumber.value,
        gender: gender.value
      },
    });
    $toast.open({
      message: responseList.authentication["success-signup"],
      position: "top-left",
      type: "success",
    });
    router.push({ name: "login" });
  } catch (errors) {
    for (const error in errors.response.data) {
      $toast.open({
        message: errors.response.data[error][0],
        position: "top-left",
        type: "error",
      });
    }
  }
}

watch(
  () => [
    email.value,
    gender.value,
    password.value,
    firstName.value,
    lastName.value,
    phoneNumber.value,
    emailValidation.value,
    phoneValidation.value,
  ],
  () => {
    if (
      email.value &&
      password.value &&
      gender.value &&
      firstName.value &&
      lastName.value &&
      phoneNumber.value &&
      !phoneValidation.value &&
      !emailValidation.value
    ) {
      disable.value = false;
    } else disable.value = true;
  }
);
</script>

<template>
  <div class="signup-container">
    <base-icon
      @click="$router.go(-1)"
      class="signup-container__back"
      iconName="back"
    />
    <h2>ثبت نام کاربر</h2>
    <form class="signup-form" @submit.prevent="signup">
      <base-input
        @update:modelValue="(value, type) => onUpdateValue(value, type)"
        class="signup-form__input"
        v-model:modelValue="email"
        :inputValue="email"
        label="ایمیل"
        icon="email"
        type="email"
        typeCheck="email"
        :error="emailError"
      />
      <p class="signup-form__invalid-input">
        {{ emailValidation }}
      </p>
      <base-input
        @update:modelValue="(value, type) => onUpdateValue(value, type)"
        class="signup-form__input"
        v-model:modelValue="phoneNumber"
        :inputValue="phoneNumber"
        label="تلفن همراه"
        icon="phone"
        type="text"
        typeCheck="phoneNumber"
        :error="phoneError"
      />
      <p class="signup-form__invalid-input">
        {{ phoneValidation }}
      </p>
      <base-input
        class="signup-form__input"
        v-model:modelValue="firstName"
        :inputValue="firstName"
        label="نام"
        icon="user"
        type="text"
      />
      <base-input
        class="signup-form__input"
        v-model:modelValue="lastName"
        :inputValue="lastName"
        label="نام خانوادگی"
        icon="user"
        type="text"
      />
      <base-input
        class="signup-form__input"
        v-model:modelValue="password"
        :inputValue="password"
        label="رمز عبور"
        icon="password"
        :type="passwordField"
      >
        <template #eye>
          <base-icon
              class="signup-form__eye"
              iconName="closed-eye"
              v-if="hidePass"
              @click="hide"
            />
            <base-icon
              class="signup-form__eye"
              iconName="eye"
              v-else
              @click="hide"
            /></template
      ></base-input>
      <div class="signup-form__gender gender">
        <div class="gender__title">جنسیت:</div>
        <div class="gender__input-box">
          <label>زن</label>
          <input class="gender__input" v-model="gender" name="gender" value="female" type="radio"/>
        </div>
        <div class="gender__input-box">
          <label>مرد</label>
          <input class="gender__input" v-model="gender" name="gender" value="male" type="radio"/>
        </div>
      </div>
      <base-button
        class="signup-form__button"
        :disabled="disable"
        varient="confirm"
        size="x-large"
      >
        ورود
      </base-button>
    </form>
  </div>
</template>

<style scoped lang="scss">
.signup-container {
  padding: 50px;
  &__back {
    width: 35px;
    height: 35px;
  }
}

.signup-form {
  &__input {
    margin-top: 20px;
  }

  &__eye {
    width: 30px;
    height: 30px;
  }

  &__button {
    margin-top: 30px;
  }

  &__invalid-input {
    color: red;
    font-size: 12px;
    margin-top: 5px;
  }

  &__gender{
    margin-top: 20px;
    padding-right:18px;
  }
}

.signup-links {
  margin-top: 40px;
  display: flex;
  align-items: center;
  gap: 7px;

  &__link {
    text-decoration: none;
  }
}

.forget-password-link {
  margin-top: 10px;
  &__link {
    text-decoration: none;
  }
}

.gender{
  display:flex;
  align-items: center;
  gap:10px;
  font-size: 15px;
  color: #818181;

  &__input-box{
    display: flex;
    align-items: center;
  }

  &__input{
    accent-color: rgb(111, 80, 133);
  }
}
</style>
