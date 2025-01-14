<script setup>
const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <div class="report">
    <div>
      <span class="report__title">نام: </span>
      <span> {{ item.first_name }} {{ item.last_name }}</span>
    </div>
    <div>
      <span class="report__title">تلفن: </span>
      <span> {{ item.phone_number }}</span>
    </div>
    <div>
      <span class="report__title">ایمیل: </span>
      <span> {{ item.email }}</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.report {
  background-color: white;
  display:flex;
  flex-direction: column;
  gap:10px;
  padding: 15px;
  border-radius: 20px;
  min-width: 300px;

  &__title{
    color:rgb(67, 128, 154);
    font-size:17px;
  }
}
</style>
