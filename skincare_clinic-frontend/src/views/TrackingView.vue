<template>
  <div class="min-h-screen bg-gray-100">
    <main class="container mx-auto px-4 py-8">
      <div class="bg-white rounded-lg shadow-md p-6 max-w-md mx-auto">
        <form @submit.prevent="trackOrder" class="mb-8">
          <div class="flex flex-col">
            <input
              v-model="trackingNumber"
              type="text"
              placeholder="Enter your tracking number"
              class="w-full px-4 py-2 mb-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#2E8B57] focus:border-transparent"
              required
            />
            <button
              type="submit"
              class="w-full px-6 py-2 bg-[#2E8B57] text-white rounded-md hover:bg-[#267346] focus:outline-none focus:ring-2 focus:ring-[#2E8B57] focus:ring-opacity-50"
            >
              Track
            </button>
          </div>
        </form>

        <div v-if="orderStatus !== null" class="mb-8">
          <div class="space-y-6">
            <div
              v-for="(stage, index) in stages"
              :key="index"
              class="flex items-center"
            >
              <div
                :class="[
                  'w-8 h-8 rounded-full border-4 flex items-center justify-center mr-4',
                  orderStatus >= index
                    ? 'bg-[#2E8B57] border-[#2E8B57]'
                    : 'bg-white border-gray-300'
                ]"
              >
                <Check
                  v-if="orderStatus >= index"
                  class="w-5 h-5 text-white"
                />
              </div>
              <span class="text-sm font-medium text-gray-700">
                {{ stage }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="orderStatus !== null" class="mb-8">
          <h2 class="text-xl font-semibold mb-4">Order Details</h2>
          <div class="bg-gray-50 p-4 rounded-md">
            <p class="mb-2">
              <strong>Order Number:</strong> #{{ trackingNumber }}
            </p>
            <p class="mb-2">
              <strong>Status:</strong> {{ stages[orderStatus] }}
            </p>
          </div>
        </div>

        <div v-if="error" class="mb-8 text-red-600">
          {{ error }}
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import { ArrowLeft, Check } from 'lucide-vue-next';

export default {
  name: 'OrderTracking',
  components: {
    ArrowLeft,
    Check,
  },
  data() {
    return {
      trackingNumber: '',
      orderStatus: null,
      error: '',
      stages: ['Order Received', 'Order Processed', 'Order Sent'],
    };
  },
  methods: {
    async trackOrder() {
      this.error = '';

      if (this.trackingNumber) {
        try {
          const order = await axios.post('api/track_order/', {
            tracking: this.trackingNumber,
          });
          this.orderStatus = order.data.status;
        } catch (error) {
          this.error = 'Invalid tracking number. Please try again.';
          this.orderStatus = null;
        }
      }
    },
  },
};
</script>

