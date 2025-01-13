import { defineStore } from "pinia";

export const useServicesStore = defineStore("store", {
  state: () => {
    return {
      services: [],
    };
  },
  actions: {
    setService(data) {
      this.services = data;
    },
  },
});
