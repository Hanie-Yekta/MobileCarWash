import { defineStore } from "pinia";

export const useForgetPass = defineStore("forgetPass", {
  state: () => ({
    phoneNumber: "",
  }),

  actions: {
    setPhone(data) {
      this.phoneNumber = data;
    },
  },
});
