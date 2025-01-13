import { useAuthStore } from "./auth";
import { useServicesStore } from "./services";
import { useUserInfoStore } from "./user";
import { useOrder } from "./order";
import {useForgetPass} from "./forget-pass";

export const store = {
  authStore: useAuthStore,
  servicesStore: useServicesStore,
  userInfoStore: useUserInfoStore,
  orderStore: useOrder,
  forgetPassStore : useForgetPass,
};
