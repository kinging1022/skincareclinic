<template>
    <main class="min-h-screen w-full bg-red-50 flex items-center justify-center p-4">
      <div class="max-w-md w-full bg-white rounded-2xl shadow-lg p-6 md:p-8">
        <div class="text-center">
          <XCircle class="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h1 class="text-2xl font-bold text-gray-800 mb-2">
            Payment Failed
          </h1>
          <p class="text-gray-600 mb-8">
            We're sorry, but your payment could not be processed.
          </p>
        </div>
        <div class="space-y-4 mb-8">
          <div class="flex justify-between py-3 border-b border-gray-100">
            <span class="text-gray-600">Order Amount</span>
            <span class="font-semibold text-gray-800">NGN {{ cartStore.total }}</span>
          </div>
          <div class="flex justify-between py-3 border-b border-gray-100">
            <span class="text-gray-600">Error</span>
            <span class="font-semibold text-gray-800">PAYMENT_FAILED</span>
          </div>
          <div class="flex justify-between py-3 border-b border-gray-100">
            <span class="text-gray-600">Time</span>
            <span class="font-semibold text-gray-800">
              {{ formattedDate }}
            </span>
          </div>
        </div>
        <div class="space-y-4">
          <button
            @click="retryPayment"
            class="w-full flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white py-3 px-4 rounded-lg transition-colors duration-200"
          >
            <RefreshCw class="w-4 h-4" />
            Try Again
          </button>
        </div>
      </div>
    </main>
  </template>
  
  <script>
  import { XCircle, RefreshCw, LifeBuoy } from 'lucide-vue-next';
  import { format } from 'date-fns';
  import { useCartStore } from '@/stores/cart';

  
  export default {
    name: 'PaymentFailed',
    components: {
      XCircle,
      RefreshCw,
      LifeBuoy,
    },
    computed: {
      formattedDate() {
        return format(new Date(), 'MMM d, yyyy HH:mm');
      },
    },
    data() {
      return {
        cartStore: useCartStore(),
        timestamp: new Date().toLocaleString(),
      };
    },
    methods: {
      retryPayment() {
        this.$router.push('/checkout');
      },
      
    },
  };
  </script>
  
  