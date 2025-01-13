<script setup>
import { RouterLink, RouterView } from "vue-router";
import Navbar from "@/components/common/main-navbar.vue";
import { useRoute } from 'vue-router';
import { computed} from 'vue';

const route = useRoute();

const showNavbar = computed(() => !route.meta.isAuthenticate);

</script>

<template>
  <navbar  v-show="showNavbar" />
  <RouterView />
</template>
