<template>
    <div class="min-h-screen w-full bg-gradient-to-br from-emerald-50 to-white flex items-center justify-center p-4">
      <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-sm">
        <div class="text-center mb-6">
          <h2 class="text-2xl font-semibold text-emerald-950">Reset Your Password</h2>
          <p class="mt-2 text-sm text-gray-500">
            Enter your new password below
          </p>
        </div>
  
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <input type="hidden" v-model="token">
          
          <div>
            <label for="new_password" class="block text-sm font-medium text-gray-700 mb-1">New Password</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                id="new_password"
                v-model="formData.new_password"
                type="password"
                required
                class="block w-full rounded-lg border border-gray-200 pl-12 p-3 text-sm focus:border-emerald-500 focus:ring-emerald-500"
                placeholder="Enter new password"
              />
            </div>
            <p v-if="errors.new_password" class="text-sm text-red-500 mt-1">{{ errors.new_password }}</p>
          </div>
  
          <div>
            <label for="confirm_password" class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                id="confirm_password"
                v-model="formData.confirm_password"
                type="password"
                required
                class="block w-full rounded-lg border border-gray-200 pl-12 p-3 text-sm focus:border-emerald-500 focus:ring-emerald-500"
                placeholder="Confirm new password"
              />
            </div>
            <p v-if="errors.confirm_password" class="text-sm text-red-500 mt-1">{{ errors.confirm_password }}</p>
          </div>
  
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!isSubmitting" class="flex items-center justify-center">
              <RefreshCw class="mr-2 h-4 w-4" />
              Reset Password
            </span>
            <span v-else class="flex items-center justify-center">
              <Loader2 class="animate-spin mr-2 h-4 w-4" />
              Processing...
            </span>
          </button>
        </form>
  
        <p v-if="successMessage" class="mt-4 text-sm text-emerald-600 text-center">{{ successMessage }}</p>
        <p v-if="errorMessage" class="mt-4 text-sm text-red-500 text-center">{{ errorMessage }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import { Lock, RefreshCw, Loader2 } from 'lucide-vue-next'
  import { useToastStore } from '@/stores/toast';
  import { useRoute, useRouter } from 'vue-router';
  import axios from 'axios'; // Make sure to import axios
  
  export default {
    name: 'ResetPassword',
    components: {
      Lock,
      RefreshCw,
      Loader2
    },
    setup() {
      const route = useRoute();
      const router = useRouter();
      const toastStore = useToastStore();
      
      return { route, router, toastStore };
    },
    data() {
      return {
        token: this.route.params.token,
        formData: {
          new_password: '',
          confirm_password: '',
        },
        errors: {},
        isSubmitting: false,
        successMessage: '',
        errorMessage: ''
      };
    },
    methods: {
      validateForm() {
        this.errors = {};
        let isValid = true;
  
        if (!this.formData.new_password) {
          this.errors.new_password = 'New password is required';
          isValid = false;
        } else if (this.formData.new_password.length < 8) {
          this.errors.new_password = 'Password must be at least 8 characters';
          isValid = false;
        }
  
        if (!this.formData.confirm_password) {
          this.errors.confirm_password = 'Please confirm your password';
          isValid = false;
        } else if (this.formData.new_password !== this.formData.confirm_password) {
          this.errors.confirm_password = 'Passwords do not match';
          isValid = false;
        }
  
        return isValid;
      },
      async handleSubmit() {
        if (!this.validateForm()) return;
  
        this.isSubmitting = true;
        this.errorMessage = '';
        this.successMessage = '';
  
        try {
          // Make sure the endpoint is correct and includes your base URL if needed
          const response = await axios.post('/api/reset/password/', {
            token: this.token,
            new_password: this.formData.new_password,
            confirm_password: this.formData.confirm_password
          }, {
            headers: {
              'Content-Type': 'application/json'
            }
          });
  
          if (response.data && response.status === 200) {
            this.successMessage = 'Password reset successfully!';
            this.toastStore.showToast(5000, 'Password reset successfully!', "bg-emerald-500");
            
            setTimeout(() => {
              this.router.push('/shop/admin/login/2015');
            }, 2000);
          } else {
            this.errorMessage = response.data.message || 'Password reset failed';
          }
        } catch (error) {
          console.error('Reset password error:', error);
          if (error.response) {
            // The request was made and the server responded with a status code
            if (error.response.data) {
              this.errorMessage = error.response.data.error || 
                                error.response.data.message || 
                                'An error occurred. Please try again.';
            } else {
              this.errorMessage = `Server error: ${error.response.status}`;
            }
          } else if (error.request) {
            // The request was made but no response was received
            this.errorMessage = 'No response from server. Please check your connection.';
          } else {
            // Something happened in setting up the request
            this.errorMessage = 'Request error. Please try again.';
          }
        } finally {
          this.isSubmitting = false;
        }
      }
    }
  };
  </script>