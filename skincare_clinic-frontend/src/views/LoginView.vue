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
      
      <div class="text-center">
        <button 
          @click="openResetModal"
          class="text-sm text-emerald-600 hover:text-emerald-700 hover:underline"
        >
          Forgot password?
        </button>
      </div>
    </div>

    <!-- Reset Password Modal -->
    <div v-if="showResetModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-emerald-950">Reset Password</h3>
          <button @click="closeResetModal" class="text-gray-500 hover:text-gray-700">
            <X class="h-6 w-6" />
          </button>
        </div>
        
        <form @submit.prevent="handleResetPassword" class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input
              id="email"
              v-model="resetEmail"
              type="email"
              required
              class="block w-full rounded-lg border border-gray-200 p-3 text-sm focus:border-emerald-500 focus:ring-emerald-500"
              placeholder="Enter your email"
            />
            <p v-if="resetError" class="text-sm text-red-500 mt-1">{{ resetError }}</p>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="closeResetModal"
              class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isResetting"
              class="px-4 py-2 bg-emerald-600 rounded-lg text-sm font-medium text-white hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="!isResetting">Reset Password</span>
              <span v-else class="flex items-center justify-center">
                <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4" />
                Processing...
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { User, Lock, ArrowRight, X, Loader2 } from 'lucide-vue-next'
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
  name: 'AdminLoginForm',
  components: {
    User,
    Lock,
    ArrowRight,
    X,
    Loader2
  },
  data() {
    return {
      formData: {
        username: "",
        password: "",
      },
      errors: {},
      userStore: useUserStore(),
      toastStore: useToastStore(),
      showResetModal: false,
      resetEmail: '',
      resetError: '',
      isResetting: false
    }
  },
  methods: {
    async handleSubmit() {
      this.errors = {};

      if (!this.formData.username) this.errors.username = "Username is required";
      if (!this.formData.password) this.errors.password = "Password is required";
      
      if (Object.keys(this.errors).length === 0) {
        try {
          await this.userStore.login(this.formData);

          Object.keys(this.formData).forEach((key) => {
            this.formData[key] = "";
          });

          this.$router.push('/admin/analytics/2015');
          this.toastStore.showToast(5000, 'Welcome boss', "bg-emerald-500");

        } catch (error) {
          console.error('Login error:', error);
          this.toastStore.showToast(5000, 'Login failed. Please try again.', "bg-red-500");
        }
      }
    },
    openResetModal() {
      this.showResetModal = true;
      this.resetEmail = '';
      this.resetError = '';
    },
    closeResetModal() {
      this.showResetModal = false;
    },
    async handleResetPassword() {
      this.resetError = '';
      this.isResetting = true;
      
      if (!this.resetEmail) {
        this.resetError = 'Email is required';
        this.isResetting = false;
        return;
      }

      try {
        const response = await axios.post('api/request/password/reset/', {
          email: this.resetEmail
        });

        this.toastStore.showToast(5000, 'Password reset link sent to your email', "bg-emerald-500");
        this.closeResetModal();
      } catch (error) {
        console.error('Reset password error:', error);
        if (error.response && error.response.data && error.response.data.error) {
          this.resetError = error.response.data.error;
        } else {
          this.resetError = 'An error occurred. Please try again.';
        }
      } finally {
        this.isResetting = false;
      }
    }
  }
}
</script>