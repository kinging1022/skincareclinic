<template>
    <div class="min-h-screen bg-emerald-50 w-full">
      <div class="max-w-6xl mx-auto p-6">
        <h1 class="text-3xl font-bold text-emerald-800 mb-8 text-center">
          Checkout
        </h1>
        <div class="grid md:grid-cols-2 gap-8">
          <div class="bg-white p-6 rounded-lg shadow-sm">
            <h2 class="text-xl font-semibold text-emerald-700 mb-6">
              Personal Details
            </h2>
            <form class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  placeholder="Enter your full name"
                  v-model="fullName"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  placeholder="Enter your email"
                  v-model="email"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Address
                </label>
                <input
                  type="text"
                  class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  placeholder="Enter your Address"
                  v-model="address"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Phone Number
                </label>
                <input
                  type="tel"
                  class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  placeholder="Enter your phone number"
                  v-model="phoneNumber"
                />
              </div>
            </form>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-sm">
            <h2 class="text-xl font-semibold text-emerald-700 mb-6">
              Delivery Details
            </h2>
            <div class="space-y-6">
              <div class="space-y-4">
                <div class="flex space-x-6">
                  <label class="flex items-center space-x-2">
                    <input
                      type="radio"
                      name="delivery"
                      value="pickup"
                      v-model="deliveryOption"
                      class="text-emerald-600 focus:ring-emerald-500"
                    />
                    <span class="text-gray-700">Pick Up</span>
                  </label>
                  <label class="flex items-center space-x-2">
                    <input
                      type="radio"
                      name="delivery"
                      value="delivery"
                      v-model="deliveryOption"
                      class="text-emerald-600 focus:ring-emerald-500"
                    />
                    <span class="text-gray-700">Delivery</span>
                  </label>
                </div>
                <div v-if="deliveryOption === 'pickup'" class="bg-emerald-50 p-4 rounded-md">
                  <p class="text-emerald-800 text-sm">
                    Pick up details will be communicated to you immediately
                    after your order has been confirmed and paid.
                  </p>
                </div>
                <div v-else class="space-y-4">
                  <select
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                    v-model="selectedLocation"
                  >
                    <option value="">Select Location</option>
                    <option value="within">Within City</option>
                    <option value="outside">Outside City</option>
                  </select>
                  <select
                    v-if="selectedLocation"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                    v-model="selectedArea"
                  >
                    <option value="">Select Area and Price</option>
                    <option
                      v-for="loc in currentLocationList"
                      :key="loc.name"
                      :value="loc.name"
                    >
                      {{ loc.name }} - ${{ loc.price }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-8 bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-xl font-semibold text-emerald-700 mb-4">
            Order Summary
          </h2>
          <div class="space-y-3">
            <div class="flex justify-between text-gray-600">
              <span>Subtotal</span>
              <span>{{ total.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between text-gray-600">
              <span>Delivery Fee</span>
              <span>${{ deliveryFee.toFixed(2) }}</span>
            </div>
            <div class="border-t pt-3 mt-3">
              <div class="flex justify-between font-semibold text-gray-800">
                <span>Total</span>
                <span>${{ totalPlusDelivery.toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-8 text-center">
          <button class="bg-emerald-600 text-white px-8 py-3 rounded-md hover:bg-emerald-700 transition-colors duration-200">
            Proceed to Payment
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { useCartStore } from '@/stores/cart';
  export default {
    data() {
      return {
        deliveryOption: 'pickup',
        selectedLocation: '',
        selectedArea: '',
        fullName: '',
        email: '',
        address:'',
        cartStore: useCartStore(),
        phoneNumber: '',
        locations: {
          within: [
            { name: "Downtown", price: 5 },
            { name: "Suburb Area", price: 8 },
            { name: "Business District", price: 6 },
          ],
          outside: [
            { name: "Neighboring City A", price: 15 },
            { name: "Neighboring City B", price: 18 },
            { name: "Rural Area", price: 20 },
          ],
        },
      };
    },
    computed: {
      currentLocationList() {
        return this.selectedLocation === 'within' ? this.locations.within : this.locations.outside;
      },
      deliveryFee() {
        if (this.deliveryOption === 'pickup') return 0;
        const locationList = this.currentLocationList;
        return locationList.find(loc => loc.name === this.selectedArea)?.price || 0;
      },
      total() {
        return this.cartStore.total
      },
      totalPlusDelivery() {
        return this.total + this.deliveryFee;
      },
    },
    watch: {
      deliveryOption() {
        this.selectedLocation = '';
        this.selectedArea = '';
      },
      selectedLocation() {
        this.selectedArea = '';
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add any component-specific styles here */
  </style>
  
  