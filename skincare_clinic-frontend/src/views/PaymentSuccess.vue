<template>
    <main class="min-h-screen w-full bg-emerald-50 flex items-center justify-center p-4">
      <div class="max-w-md w-full bg-white rounded-2xl shadow-lg p-6 md:p-8">
        <div class="text-center">
          <CheckCircle class="w-16 h-16 text-emerald-500 mx-auto mb-4" />
          <h1 class="text-2xl font-bold text-gray-800 mb-2">
            Payment Successful!
          </h1>
          <p class="text-gray-600 mb-8">
            Your transaction has been completed
          </p>
        </div>
        <div class="space-y-4 mb-8">
          <div class="flex justify-between py-3 border-b border-gray-100">
            <span class="text-gray-600">Order Id</span>
            <span class="font-semibold text-gray-800">{{ transactionId }}</span>
          </div>
          <div class="flex justify-between py-3 border-b border-gray-100">
            <span class="text-gray-600">Amount Paid</span>
            <span class="font-semibold text-gray-800">₦ {{ cartStore.total.toLocaleString() }}</span>
          </div>
          <p class="font-small text-gray-800">Kindly note that the delivery price paid was not included here</p>

          <div class="flex justify-between py-3 border-b border-gray-100">
            <span class="text-gray-600">Time</span>
            <span class="font-semibold text-gray-800">
              {{ formattedDate }}
            </span>
          </div>
        </div>
        <button
          @click="navigateToShop"
          class="w-full flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white py-3 px-4 rounded-lg transition-colors duration-200"
        >
          <ArrowLeft class="w-4 h-4" />
          Clear Cart and Go Back to Shop
        </button>
      </div>
    </main>
  </template>
  
  <script>
  import { CheckCircle, ArrowLeft } from 'lucide-vue-next';
  import { format } from 'date-fns';
  import { useCartStore } from '@/stores/cart';
  
  export default {
    name: 'PaymentSuccess',
    components: {
      CheckCircle,
      ArrowLeft,
    },
    data() {
      return {
        confettiActive: true,
        windowDimension: {
          width: window.innerWidth,
          height: window.innerHeight,
        },
        cartStore: useCartStore(),
        transactionId: this.$route.params.id,
        timestamp: new Date().toLocaleString(),
      };
    },
    computed: {
      formattedDate() {
        return format(new Date(), 'MMM d, yyyy HH:mm');
      },
    },
    mounted() {
      this.startConfetti();
      window.addEventListener('resize', this.handleResize);
      this.confettiTimer = setTimeout(() => {
        this.confettiActive = false;
        this.stopConfetti();
      }, 5000);
    },
    beforeUnmount() {
      window.removeEventListener('resize', this.handleResize);
      clearTimeout(this.confettiTimer);
      this.stopConfetti();
    },
    methods: {
      handleResize() {
        this.windowDimension = {
          width: window.innerWidth,
          height: window.innerHeight,
        };
      },
      navigateToShop() {
        this.cartStore.clearCart();
        this.$router.push('/');
      },
      startConfetti() {
        this.$confetti.start({
          particles: [
            {
              type: 'circle',
              colors: ['#059669', '#34d399', '#6ee7b7', '#a7f3d0']
            }
          ],
          defaultType: 'circle',
          defaultSize: 10,
          defaultDuration: 5 * 1000
        });
      },
      stopConfetti() {
        this.$confetti.stop();
      },
    },
  };
  </script>
  
  