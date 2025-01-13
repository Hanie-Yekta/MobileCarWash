<script setup>
import { ref } from "vue";
import moment from "jalali-moment";
import BaseIcon from "@/components/common/base-icon.vue";


const m = moment();
const mountDays = ref([]);
const prevMountDays = ref([]);
const currentMountDays = ref([]);
const nextMountDays = ref([]);
const firstDayofMonth = ref();
const lastDatehofMonth = ref();
const lastDayofMonth = ref();
const lastDateofLastMonth = ref();

  m.format("jYYYY/jM/jD");
  const currYear = ref(m.jYear());
  const currMonth = ref(m.jMonth());
  const date = ref();
  const months = [
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
  ];

  const renderCalendar = () => {
    m.startOf("jMonth");
    firstDayofMonth.value = m.jDay();
    m.endOf("jMonth");
    lastDatehofMonth.value = +m.format("jD");
    lastDayofMonth.value = m.jDay();
    m.subtract(1, "jMonth");
    m.endOf("jMonth");
    lastDateofLastMonth.value = +m.format("jD");

    for (let i = firstDayofMonth.value; i > 0; i--) {
      prevMountDays.value.push(lastDateofLastMonth.value - i + 1);

    }
    m.add(1, "jMonth");
    for (let i = 1; i <= lastDatehofMonth.value; i++) {
      currentMountDays.value.push(i);

    }
    for (let i = lastDayofMonth.value; i < 6; i++) {
      nextMountDays.value.push(i - lastDayofMonth.value + 1);

    }
  };
  renderCalendar();
  const next = () => {
    prevMountDays.value = [];
    currentMountDays.value = [];
    nextMountDays.value = [];
    m.add(1, "jMonth");
    currMonth.value++;
    if (currMonth.value < 0 || currMonth.value > 11) {
      date.value = new Date(
        currYear.value,
        currMonth.value,
        new Date().getDate()
      );
      currYear.value = date.value.getFullYear();
      currMonth.value = date.value.getMonth();
    } else {
      moment();
    }
    renderCalendar();
  };
  const prev = () => {
    prevMountDays.value = [];
    currentMountDays.value = [];
    nextMountDays.value = [];
    m.subtract(1, "jMonth");
    currMonth.value--;
    if (currMonth.value < 0 || currMonth.value > 11) {
      const date = new Date(
        currYear.value,
        currMonth.value,
        new Date().getDate()
      );
      currYear.value = date.getFullYear();
      currMonth.value = date.getMonth();
    } else {
      moment();
    }
    renderCalendar();
  };
</script>

<template>
  <div class="calendar">
    <header class="calendar__head">
      <p class="calendar__month">{{ months[currMonth] }} {{ currYear }}</p>
      <div class="calendar__icons">
        <base-icon @click="prev" iconName="arrow-right"/>
        <base-icon @click="next" iconName="arrow-left"/>
      </div>
    </header>
    <div class="calendar__main">
      <ul class="calendar__weeks">
        <li class="calendar__days">ش</li>
        <li class="calendar__days">ی</li>
        <li class="calendar__days">د</li>
        <li class="calendar__days">س</li>
        <li class="calendar__days">چ</li>
        <li class="calendar__days">پ</li>
        <li class="calendar__days">ج</li>
      </ul>
      <ul class="calendar__days-container">
        <li
          class="calendar__days calendar__inactive"
          v-for="(item, index) in prevMountDays"
          :key="index"
        >
          {{ item }}
        </li>
        <li
          class="calendar__days"
          v-for="(item, index) in currentMountDays"
          :key="index"
          :class="{
            active:
              item == +moment().format('jD')-1 &&
              currMonth == +moment().format('jM') - 1 &&
              currYear == +moment().format('jYYYY'),
          }"
        >
          {{ item }}
        </li>
        <li
          class="calendar__days calendar__inactive"
          v-for="(item, index) in nextMountDays"
          :key="index"
        >
          {{ item }}
        </li>
      </ul>
    </div>
  </div>

</template>

<style lang="scss" scoped>


.active {
  box-sizing: border-box;
  text-align: center;
  background-color: #2471eb;
  border-radius: 12px;
  color: white;
}
.calendar {
  background:white;
  box-shadow: 0px 2px 20px 0px rgba(0, 67, 101, 0.05);
  height: fit-content;
  border-radius: 24px;
  padding:25px;

  &__head {
    display:flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
    color: rgb(91, 91, 91);
  }
  &__icons {
    display:flex;
    justify-content: space-between;
    width: 55px;
    cursor: pointer;
  }
  &__days-container {
    display: flex;
    flex-wrap: wrap;
    list-style: none;
    text-align: center;
    padding:0px;
  }
  &__days {
    width: calc(100% / 7);
    font-size: 13px;
    height: 25px;
  }

  &__weeks {
    color: gray;
    font-weight: 500;
    font-size: 14px;
    display: flex;
    flex-wrap: wrap;
    list-style: none;
    text-align: center;
    padding: 0px;

  }
  &__inactive {
    color: #aaa;
  }
}

header .icons span:hover {
  background: #f2f2f2;
  border-radius: 10px;
}

</style>
