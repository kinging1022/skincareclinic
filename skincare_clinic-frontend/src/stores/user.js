import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    isAuthenticated: false,
    access: null,
    refresh: null,
  }),

  actions: {
    setToken(data) {
      this.access = data.access;
      this.refresh = data.refresh;
      this.isAuthenticated = true;
      this.saveUserToLocalStorage();
    },

    removeToken() {
      this.isAuthenticated = false;
      this.access = null;
      this.refresh = null;
      localStorage.removeItem("user");
    },

    initStore() {
      const storedUser = localStorage.getItem("user");
      if (storedUser) {
        const parsedUser = JSON.parse(storedUser);
        this.isAuthenticated = parsedUser.isAuthenticated || false;
        this.access = parsedUser.access || null;
        this.refresh = parsedUser.refresh || null;
      }
    },

    async refreshToken() {
      try {
        const response = await axios.post("api/auth/token/refresh", {
          refresh: this.refresh,
        });
        this.access = response.data.access;
        this.saveUserToLocalStorage();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          console.log("Refresh token expired or invalid. Logging out.");
          this.removeToken();
        } else {
          throw new Error("Token refresh failed");
        }
      }
    },

    saveUserToLocalStorage() {
      const userData = {
        isAuthenticated: this.isAuthenticated,
        access: this.access,
        refresh: this.refresh,
      };
      localStorage.setItem("user", JSON.stringify(userData));
    },
  },
});
