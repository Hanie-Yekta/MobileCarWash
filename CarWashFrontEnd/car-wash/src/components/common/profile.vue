<script setup>
import { store } from "@/stores";
import BaseIcon from "@/components/common/base-icon.vue";
import BaseButton from "@/components/common/base-button.vue";
const userInfo = store.userInfoStore();
</script>

<template>
  <div class="profile">
    <div class="profile__image-container">
      <img v-if="userInfo.userInfo.gender == 'female'" class="profile__image" src="../../assets/images/female.jpg" />
      <img v-else class="profile__image" src="../../assets/images/male.jpg" />
    </div>
    <div class="profile__name">
      {{ userInfo.userInfo.firstName }} {{ userInfo.userInfo.lastName }}
    </div>
    <div class="profile__information information">
      <div class="information__content">
        <div class="information__box">
          <base-icon
            class="information__icon information__email-icon"
            iconName="dashboard-email"
          />
          <span>ایمیل</span>
          <base-icon class="information__icon-arrow" iconName="arrow-left" />
        </div>
        <span>{{ userInfo.userInfo.email }}</span>
      </div>
      <div class="information__content">
        <div class="information__box">
          <base-icon
            class="information__icon information__phone-icon"
            iconName="dashboard-phone"
          />
          <span>تلفن</span>
          <base-icon class="information__icon-arrow" iconName="arrow-left" />
        </div>
        <span>{{userInfo.userInfo.phone}}</span>
      </div>
    </div>
  </div>
  <div class="reports">
    <base-button v-if="userInfo.userInfo.role == 'admin'" size="x-large" @click="$router.push({ name: 'reports' })">گزارشات</base-button>
  </div>
</template>

<style lang="scss" scoped>
.profile {
  background: white;
  box-shadow: 0px 2px 20px 0px rgba(0, 67, 101, 0.05);
  height: fit-content;
  border-radius: 24px;
  padding: 25px;

  &__name {
    text-align: center;
    font-weight: bold;
    font-size: 20px;
  }

  &__image-container {
    margin: auto;
    width: 200px;
    height: 200px;
    border-radius: 50%;
  }
  &__image {
    width: 100%;
    background-size: contain;
  }
}

.information {
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  &__icon {
    width: 25px;
    height: 25px;
  }

  &__icon-arrow {
    width: 15px;
    height: 15px;
  }

  &__email-icon {
    color: red;
  }

  &__phone {
    color: green;
  }

  &__content {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  &__box {
    display: flex;
    align-items: center;
    gap: 3px;
  }
}
.reports{
  margin-top:20px;
}
</style>
