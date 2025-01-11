import "@/assets/scss/style.scss";

import { createApp } from "vue";
import { createPinia } from "pinia";
import BootstrapVue3 from "bootstrap-vue-3";
import { createVuetify } from 'vuetify'
import 'vuetify/styles'

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-3/dist/bootstrap-vue-3.css";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

const vuetify = createVuetify();

app.use(createPinia());
app.use(router);
app.use(BootstrapVue3);
app.use(vuetify);

app.mount("#app");
