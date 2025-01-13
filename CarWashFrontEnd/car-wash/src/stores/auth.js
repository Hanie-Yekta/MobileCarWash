// stores/auth.js
import { defineStore } from 'pinia';
import Cookies from 'js-cookie';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: Cookies.get('token') || null,
    refreshToken: Cookies.get('refresh') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    setToken(token) {
      this.token = token;
      Cookies.set('token', token);
    },
    setRefreshToken(token) {
      this.refreshToken = token;
      Cookies.set('refresh', token);
    },
    clearToken() {
      this.token = null;
      this.refreshToken = null;
      Cookies.remove('refresh');
      Cookies.remove('token');
    },
  },
});

