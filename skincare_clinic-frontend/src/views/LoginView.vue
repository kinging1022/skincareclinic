<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-emerald-50 to-white flex items-start sm:items-center justify-center p-4 pt-8 sm:p-4">
    <div class="w-full max-w-md space-y-8 bg-white p-8 rounded-2xl shadow-sm">
      <div class="text-center">
        <h2 class="text-3xl font-semibold text-emerald-950">ADMIN</h2>
        <p class="mt-2 text-sm text-gray-500">
          Welcome back to office boss
        </p>
      </div>
      <form @submit.prevent="handleSubmit" class="mt-8 space-y-6">
        <div class="space-y-4">
          <div class="relative">
            <label for="username" class="sr-only">
              Username
            </label>
            <User class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              id="username"
              name="username"
              type="text"
              required
              v-model="formData.username"
              class="block w-full rounded-lg border border-gray-200 pl-12 p-3 text-sm focus:border-emerald-500 focus:ring-emerald-500"
              placeholder="Username"
            />
            <p v-if="errors.username" class="text-sm text-red-500">{{ errors.username }}</p>
          </div>
          <div class="relative">
            <label for="password" class="sr-only">
              Password
            </label>
            <Lock class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              id="password"
              name="password"
              type="password"
              required
              v-model="formData.password"
              class="block w-full rounded-lg border border-gray-200 pl-12 p-3 text-sm focus:border-emerald-500 focus:ring-emerald-500"
              placeholder="Password"
            />
            <p v-if="errors.password" class="text-sm text-red-500">{{ errors.password }}</p>
          </div>
        </div>
        <button
          type="submit"
          class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
        >
          Sign in
          <ArrowRight class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { User, Lock, ArrowRight } from 'lucide-vue-next'
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
  name: 'AdminLoginForm',
  components: {
    User,
    Lock,
    ArrowRight
  },
  data() {
    return {
      formData: {
        username: "",
        password: "",
      },
      errors: {},
      userStore: useUserStore(),
      toastStore: useToastStore()
    }
  },
  methods: {
    async handleSubmit() {
      this.errors = {};

      if (!this.formData.username) this.errors.username = "Username is required";
      if (!this.formData.password) this.errors.password = "Password is required";
      
      if (Object.keys(this.errors).length === 0) {
        try {
          const response = await axios.post('api/auth/admin/login/', this.formData);

          this.userStore.setToken(response.data);

          Object.keys(this.formData).forEach((key) => {
            this.formData[key] = "";
          });

          this.$router.push('/analytics');
          this.toastStore.showToast(5000, 'Welcome boss', "bg-emerald-500");

        } catch (error) {
          console.error('Login error:', error);
          this.toastStore.showToast(5000, 'Login failed. Please try again.', "bg-red-500");
        }
      }
    }
  }
}
</script>