import { defineStore } from "pinia"
import axios from "axios"
import router from '@/router'

export const useUserStore = defineStore("user", {
  state: () => ({
    isAuthenticated: false,
    access: null,
    refresh: null,
    initialized: false,
    refreshAttempts: 0,
    maxRefreshAttempts: 3
  }),

  actions: {
    setToken(data) {
      this.isAuthenticated = true
      this.access = data.access
      this.refresh = data.refresh
      this.refreshAttempts = 0
      this.saveUserToLocalStorage()
      
      // Redirect after login
      if (router.currentRoute.value.query.redirect) {
        router.push(router.currentRoute.value.query.redirect)
      } else {
        router.push('/admin/analytics/2015')
      }
    },

    removeToken() {
      this.isAuthenticated = false
      this.access = null
      this.refresh = null
      this.refreshAttempts = 0
      localStorage.removeItem("user")
      
      // Redirect to login when logging out
      if (router.currentRoute.value.meta.requiresAuth) {
        router.push('/admin/login/2015')
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
      // Prevent excessive refresh attempts
      if (this.refreshAttempts >= this.maxRefreshAttempts) {
        console.log("Maximum refresh attempts reached. Logging out.")
        this.removeToken()
        throw new Error("Maximum refresh attempts reached")
      }

      this.refreshAttempts++
      
      try {
        const response = await axios.post("api/token/refresh/", {
          refresh: this.refresh,
        })
        this.access = response.data.access
        this.refreshAttempts = 0 // Reset counter on success
        this.saveUserToLocalStorage()
        return response.data.access
      } catch (error) {
        console.log("Refresh token failed:", error.response?.status)
        if (error.response?.status === 400 || error.response?.status === 401) {
          // Token is invalid or expired
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