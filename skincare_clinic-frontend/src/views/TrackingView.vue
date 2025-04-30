<template>
  <div class="min-h-screen bg-[#f8faf8]">
    <main class="container mx-auto px-4 py-12 md:py-16">
      <!-- Tracking Card -->
      <div class="bg-white rounded-lg shadow-sm border border-[#e0eae3] p-6 md:p-8 max-w-md mx-auto">
        <!-- Header -->
        <div class="mb-8 text-center">
          <h1 class="text-2xl md:text-3xl font-light text-[#1c3a2e] mb-2 tracking-wide">Track Your Order</h1>
          <p class="text-[#4a6b5d] text-sm">Enter your tracking number below</p>
        </div>

        <!-- Tracking Form -->
        <form @submit.prevent="trackOrder" class="mb-8">
          <div class="relative">
            <input
              v-model="trackingNumber"
              type="text"
              placeholder="TRK-12345678"
              class="w-full px-5 py-3 border-b border-[#d7e5dc] focus:border-[#0a5c3e] text-[#1c3a2e] placeholder-[#9ab5a7] focus:outline-none bg-transparent transition-colors duration-300"
              required
            />
            <button
              type="submit"
              class="absolute right-0 top-0 h-full px-4 text-[#0a5c3e] hover:text-[#0b4a33] focus:outline-none"
              aria-label="Track order"
            >
              <Search class="w-6 h-6" />
            </button>
          </div>
        </form>

        <!-- Tracking Progress -->
        <div v-if="order" class="mb-8">
          <div class="relative">
            <!-- Progress line -->
            <div class="absolute left-4 top-0 h-full w-0.5 bg-[#e3efe7] z-0"></div>
            
            <div class="space-y-8 relative z-10">
              <div
                v-for="(stage, index) in stages"
                :key="index"
                class="flex items-start"
              >
                <div
                  :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center mr-4 mt-0.5 flex-shrink-0 border-2',
                    order.status >= index
                      ? 'bg-[#0a5c3e] border-[#0a5c3e]'
                      : 'bg-white border-[#d7e5dc]'
                  ]"
                >
                  <span v-if="order.status < index" class="text-xs text-[#9ab5a7]">{{ index + 1 }}</span>
                  <Check v-else class="w-4 h-4 text-white" stroke-width="3" />
                </div>
                <div>
                  <span class="block text-sm font-medium text-[#1c3a2e]">
                    {{ stage.label }}
                  </span>
                  <span v-if="order.status === index && stage.dateField && order[stage.dateField]" 
                        class="block text-xs text-[#7a9b8a] mt-1">
                    {{ formatDate(order[stage.dateField]) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Details -->
        <div v-if="order" class="mb-8">
          <div class="p-5 bg-[#f5f9f6] rounded-lg">
            <h3 class="text-sm font-medium text-[#4a6b5d] uppercase tracking-wider mb-3">Order Summary</h3>
            <div class="grid grid-cols-2 gap-y-2 text-sm">
              <div class="text-[#7a9b8a]">Order Number:</div>
              <div class="text-[#1c3a2e] font-medium">{{ order.id }}</div>
              
              <div class="text-[#7a9b8a]">Customer:</div>
              <div class="text-[#1c3a2e] font-medium">{{ order.full_name }}</div>
              
              <div class="text-[#7a9b8a]">Order Amount:</div>
              <div class="text-[#1c3a2e] font-medium">₦{{ order.order_amount.toLocaleString() }}</div>
              
              <div class="text-[#7a9b8a]">Status:</div>
              <div class="text-[#1c3a2e] font-medium capitalize">{{ stages[order.status].label }}</div>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mb-6 p-4 bg-[#fff5f5] rounded-lg border border-[#fed7d7]">
          <div class="flex items-start">
            <div class="flex-shrink-0 text-[#f56565] mr-3">
              <AlertCircle class="w-5 h-5" />
            </div>
            <div class="text-sm text-[#9b2c2c]">{{ error }}</div>
          </div>
        </div>

        <!-- Shipping Policy Link -->
        <div class="pt-5 border-t border-[#e3efe7] text-center">
          <router-link 
            to="/shipping-policy" 
            class="inline-flex items-center text-xs text-[#7a9b8a] hover:text-[#0a5c3e] transition-colors duration-200 group"
          >
            <span>Shipping Policy</span>
            <ChevronRight class="w-4 h-4 ml-1 transform transition-transform duration-200 group-hover:translate-x-1" />
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { Search, Check, AlertCircle, ChevronRight } from 'lucide-vue-next';
import axios from 'axios';

export default {
  name: 'OrderTracking',
  components: {
    Search,
    Check,
    AlertCircle,
    ChevronRight
  },
  data() {
    return {
      trackingNumber: '',
      order: null,
      error: '',
      stages: [
        { label: 'Order Received', dateField: 'created_at' },
        { label: 'Processing', dateField: null },
        { label: 'Shipped', dateField: 'shipped_date' },
      ],
    };
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
      });
    },
    async trackOrder() {
      this.error = '';
      this.order = null;

      if (this.trackingNumber) {
        try {
          const response = await axios.post('api/track_order/', {
            tracking: this.trackingNumber,
          });
          this.order = response.data;
        } catch (error) {
          this.error = 'Invalid tracking number. Please try again.';
          console.error('Tracking error:', error);
        }
      }
    },
  },
};
</script>

<style scoped>
/* Custom input focus effect */
input:focus {
  box-shadow: 0 1px 0 0 #0a5c3e;
}

/* Smooth number appearance in progress circles */
span {
  transition: opacity 0.3s ease;
}
</style>