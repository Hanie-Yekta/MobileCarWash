<script setup>
import { ref, onMounted, watch } from "vue";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";
import { store } from "@/stores";
const orderStore = store.orderStore();
import BaseButton from "@/components/common/base-button.vue";
import { responseList } from "@/responses/responses";
import L from "leaflet";
const emit = defineEmits(["locationNext"]);

const $toast = useToast();
const lat = ref(0);
const lng = ref(0);
const address = ref();
const disableNext = ref(true);
const map = ref();
const mapContainer = ref();
const marker = ref();

const Next = () => {
  orderStore.setOrderAddress(address.value);
  emit("locationNext");
};
watch(
  () => [address.value],
  () => {
    if (address.value) {
      disableNext.value = false;
    } else disableNext.value = true;
  }
);

onMounted(() => {
  map.value = L.map(mapContainer.value).setView([36.2972, 59.6067], 13);
  marker.value = L.marker([36.2972, 59.6067], { draggable: true })
    .addTo(map.value)
    .on("dragend", (event) => {
      const { lat, lng } = event.target.getLatLng();
      geocode({ latitude: lat, longitude: lng });
    });

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map.value);
});

const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(
      (position) => {
        lat.value = position.coords.latitude;
        lng.value = position.coords.longitude;
        map.value.setView([lat.value, lng.value], 13);
        marker.value.setLatLng([lat.value, lng.value]);
        geocode({ latitude: lat.value, longitude: lng.value });
      },
      (error) => {
        console.log(error);
      }
    );
  } else {
    console.error("Geolocation is not supported by this browser.");
  }
};

const geocode = async ({ latitude, longitude, query }) => {
  let url;

  if (latitude && longitude) {
    url = `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json&accept-language=fa`;
  } else if (query) {
    url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
      query
    )}&format=json&addressdetails=1&limit=1&accept-language=fa`;
  } else {
    console.error("Either latitude/longitude or query must be provided.");
    return;
  }

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (latitude && longitude) {
      address.value = formatAddress(data.display_name || "آدرس یافت نشد");
    } else if (query && data.length > 0) {
      const result = data[0];
      lat.value = result.lat;
      lng.value = result.lon;
      address.value = formatAddress(result.display_name);

      map.value.setView([lat.value, lng.value], 13);
      marker.value.setLatLng([lat.value, lng.value]);
    } else {
      address.value = "نتیجه‌ای یافت نشد.";
    }
  } catch (error) {
    console.error("Error fetching geocoding data:", error);
    address.value = "خطا در دریافت داده‌ها.";
  }
};

const formatAddress = (fullAddress) => {
  const parts = fullAddress.split(", ");
  const rearrangedParts = parts.reverse().join("، ");
  return rearrangedParts;
};
</script>

<template>
  <div class="select-location">
    <div>
      <p class="select-location__title">
        لطفا موقعیت مکانی خود را انتخاب نمایید.
      </p>
      <div class="select-location__input-box">
        <input
          class="select-location__input"
          v-model="address"
          placeholder="آدرس:"
        />
        <base-button
          class="select-location__button"
          @click="getLocation"
          size="normal"
          >دریافت موقعیت فعلی</base-button
        >
      </div>
    </div>

    <div ref="mapContainer" class="map-container"></div>
    <div class="select-location__button-next">
      <base-button @click="$router.go(-1)" size="normal">مرحله قبل</base-button>
      <base-button @click="Next" size="normal" :disabled="disableNext"
        >مرحله بعد</base-button
      >
    </div>
  </div>
</template>

<style scoped lang="scss">
.select-location {
  padding-right: 60px;

  &__header {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  &__title {
    color: rgb(164, 164, 164);
  }

  &__input-box {
    display: flex;
    margin-top: 20px;
    gap: 20px;
  }

  &__input {
    background-color: white;
    flex-grow: 3;
    padding: 12px;
    border-radius: 20px;
  }

  &__button-next {
    margin-top: 25px;
    display: flex;
    gap: 5px;
    justify-content: end;
  }
}
.map-container {
  border-radius: 20px;
  height: 250px;
  width: 100%;
  margin-top: 20px;
}
</style>
