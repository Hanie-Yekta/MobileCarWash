import { defineStore } from "pinia";

export const  useUserInfoStore = defineStore("userInfo", {
  state: () => ({
    userInfo: {
      firstName: "",
      lastName: "",
      email: "",
      role: "",
      phone: "",
      gender: "",
    },
  }),

  actions: {
    setInfo(data) {
      this.userInfo.firstName = data.first_name;
      this.userInfo.lastName = data.last_name;
      this.userInfo.email = data.email;
      this.userInfo.gender = data.gender;
      this.userInfo.phone = data.phone_number;
      this.userInfo.role = this.setRole(data.is_worker, data.is_admin);
    },

    setRole(isWorker, isAdmin) {
      if (isWorker) {
        return "worker";
      } else if (isAdmin) {
        return "admin";
      } else return "customer";
    },
  },
});