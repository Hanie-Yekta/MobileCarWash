import { defineStore } from "pinia";

export const useOrder = defineStore("order", {
  state: () => ({
    order: {
      service: "",
      image: "",
      prices: [],
      price:"",
      car: "",
      time: "",
      address: null,
    },
  }),

  actions: {
    setSlectedServiceInfo(data) {
      this.order.service = data.name;
      this.order.image = data.image;
      this.order.prices = data.price;
      this.cleanOrder();
    },

    setSpecialServiceInfo(data) {
      this.order.service = data.name;
      this.order.image = data.image;
      this.order.price = data.price[0].price;
      this.order.car = data.price[0].car_type;
      this.cleanSpecialOrder();
    },

    cleanOrder() {
      this.order.time = "";
      this.order.address = "";
      this.order.car = "";
      this.order.price = "";
    },

    cleanSpecialOrder(){
      this.order.time = "";
      this.order.address = "";
    },

    setOrderTime(data) {
      this.order.time = data;
    },

    setOrderAddress(data) {
      this.order.address = data;
    },

    setOrderCar(data) {
      this.order.car = data;
    },

    setOrderPrice(data) {
      this.order.price = data;
    },
  },
});
