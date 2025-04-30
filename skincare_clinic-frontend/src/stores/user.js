import { defineStore } from "pinia"
import axios from "axios"
import router from '@/router'

export const useUserStore = defineStore("user", {
  state: () => ({
    isAuthenticated: false,
    access: null,
    refresh: null,
    initialized: false
  }),

  actions: {
    setToken(data) {
      this.isAuthenticated = true
      this.access = data.access
      this.refresh = data.refresh
      this.saveUserToLocalStorage()
      
      // Redirect after login
      if (router.currentRoute.value.query.redirect) {
        router.push(router.currentRoute.value.query.redirect)
      } else {
        router.push('/analytics')
      }
    },

    removeToken() {
      this.isAuthenticated = false
      this.access = null
      this.refresh = null
      localStorage.removeItem("user")
      
      // Redirect to login when logging out
      if (router.currentRoute.value.meta.requiresAuth) {
        router.push('/admin/login')
      }
    },

    async initStore() {
      const storedUser = localStorage.getItem("user")
      if (storedUser) {
        const parsedUser = JSON.parse(storedUser)
        this.isAuthenticated = parsedUser.isAuthenticated || false
        this.access = parsedUser.access || null
        this.refresh = parsedUser.refresh || null
      }
      this.initialized = true
    },

    async refreshToken() {
      try {
        const response = await axios.post("api/token/refresh/", {
          refresh: this.refresh,
        })
        this.access = response.data.access
        this.saveUserToLocalStorage()
        return response.data.access
      } catch (error) {
        if (error.response?.status === 400) {
          console.log("Refresh token expired or invalid. Logging out.")
          this.removeToken()
        }
        throw error
      }
    },

    saveUserToLocalStorage() {
      const userData = {
        isAuthenticated: this.isAuthenticated,
        access: this.access,
        refresh: this.refresh,
      }
      localStorage.setItem("user", JSON.stringify(userData))
    },
    
    async login(credentials) {
      try {
        const response = await axios.post('api/token/', credentials)
        this.setToken(response.data)
        return response.data
      } catch (error) {
        throw error.response?.data || error
      }
    },
    
    async logout() {
      try {
        await axios.post('/api/auth/logout/', { refresh: this.refresh })
      } finally {
        this.removeToken()
      }
    }
  }
})