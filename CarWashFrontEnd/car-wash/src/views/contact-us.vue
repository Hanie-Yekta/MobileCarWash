<script setup>
import BaseIcon from "@/components/common/base-icon.vue";
</script>
<template>
  <div class="container">
    <div class="contact-us">
      <div class="contact-us__image-container">
        <img class="contact-us__image" src="../assets/images/location.jpg" />
      </div>
      <div class="contact-us__information information">
        <h2>تماس با ما</h2>
        <div class="information__box">
          <base-icon class="information__icon" iconName="contact-us-address"/>
          <span class="information__text">آدرس دفتر مرکزی: مشهد، بلوار وکیل آباد، بین وکیل آباد 7 و 9</span>
        </div>
        <div class="information__box">
          <base-icon class="information__icon" iconName="contact-us-telephone"/>
          <span class="information__text">تلفن: 09157061290</span>
        </div>
        <div class="information__box">
          <base-icon class="information__icon" iconName="contact-us-email"/>
          <span class="information__text">ایمیل: quickwash@gmail.com</span>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped lang="scss">
.container {
  background-color: #f9f9f9;
  height: 100vh;
  max-width: 100%;
  padding: 150px 100px;
}
.contact-us {
  background-color: white;
  display:flex;
  gap:30px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  padding: 30px;

  &__image {
    width: 100%;
    height: 100%;
    border-radius: 10px;
  }

  &__image-container {
    width: 45%;
    height: 400px;
  }
}
.information{
  &__icon{
    width:30px;
    height: 30px;
    color:rgb(51, 146, 160);
  }
  &__box{
    margin-top:20px;
  }
  &__text{
    padding:10px;
    
  }
}
</style>