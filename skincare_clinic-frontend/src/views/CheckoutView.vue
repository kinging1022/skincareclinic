<template>
    <div class="min-h-screen bg-emerald-50 w-full">
      <div class="max-w-6xl mx-auto p-6">
        <h1 class="text-3xl font-bold text-emerald-800 mb-8 text-center">
          Checkout
        </h1>
        <div class="grid md:grid-cols-2 gap-8">
          <!-- Personal Details -->
          <div class="bg-white p-6 rounded-lg shadow-sm">
            <h2 class="text-xl font-semibold text-emerald-700 mb-6">
              Personal Details
            </h2>
            <form class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                <input
                  type="text"
                  class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  placeholder="Enter your full name"
                  v-model="fullName"
                />
                <span v-if="errors.fullName" class="text-red-500 text-sm">{{ errors.fullName }}</span>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  placeholder="Enter your email"
                  v-model="email"
                />
                <span v-if="errors.email" class="text-red-500 text-sm">{{ errors.email }}</span>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
                <input
                  type="text"
                  class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  placeholder="Enter your address"
                  v-model="address"
                />
                <span v-if="errors.address" class="text-red-500 text-sm">{{ errors.address }}</span>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                <input
                  type="tel"
                  class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  placeholder="Enter your phone number"
                  v-model="phoneNumber"
                />
                <span v-if="errors.phoneNumber" class="text-red-500 text-sm">{{ errors.phoneNumber }}</span>
              </div>
            </form>
          </div>
  
          <!-- Delivery Details -->
          <div class="bg-white p-6 rounded-lg shadow-sm">
            <h2 class="text-xl font-semibold text-emerald-700 mb-6">Delivery Details</h2>
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
                    <option v-for="location in locationsCategory" :key="location.id" :value="location.slug">{{ location.name }}</option>
                  </select>
                  <span v-if="errors.selectedLocation" class="text-red-500 text-sm">{{ errors.selectedLocation }}</span>
                  <select
                    v-if="selectedLocation"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                    v-model="selectedArea"
                  >
                    <option value="">Select Area and Price</option>
                    <option
                      v-for="location in locations"
                      :key="location.id"
                      :value="location.name"
                    >
                      {{ location.name }} - ${{ location.price.toLocaleString() }}
                    </option>
                  </select>
                  <span v-if="errors.selectedArea" class="text-red-500 text-sm">{{ errors.selectedArea }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Order Summary -->
        <div class="mt-8 bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-xl font-semibold text-emerald-700 mb-4">Order Summary</h2>
          <div class="space-y-3">
            <div class="flex justify-between text-gray-600">
              <span>Subtotal</span>
              <span>${{ total.toLocaleString() }}</span>
            </div>
            <div class="flex justify-between text-gray-600">
              <span>Package Weight</span>
              <span>{{ totalWeight }}</span>
            </div>
            <div class="flex justify-between text-gray-600">
              <span>Delivery Fee</span>
              <span>${{ deliveryFee.toLocaleString() }}</span>
            </div>
            <div class="border-t pt-3 mt-3">
              <div class="flex justify-between font-semibold text-gray-800">
                <span>Total</span>
                <span>${{ totalPlusDelivery.toLocaleString() }}</span>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Payment Button -->
        <div class="mt-8 text-center">
          <button
            @click="makePayment"
            class="bg-emerald-600 text-white px-8 py-3 rounded-md hover:bg-emerald-700 transition-colors duration-200"
          >
            Proceed to Payment
          </button>
        </div>

        <!-- Insufficient Stock Modal -->
        <CheckoutModal 
            :is-open="showInsufficientStockModal"
            :products="insufficient_products"
            @update-manually="cancelCheckout"
            @update-automatically="updateCartAutomatically"
            @close="cancelCheckout"
        />
      </div>
    </div>
  </template>
  
  <script>
  import { useCartStore } from "@/stores/cart";
  import { useToastStore } from "@/stores/toast";
  import CheckoutModal from "@/components/CheckoutModal.vue";
  import axios from "axios";
  
  export default {
    data() {
      return {
        cartStore: useCartStore(),
        toastStore: useToastStore(),
        fullName: "",
        email: "",
        address: "",
        phoneNumber: "",
        deliveryOption: "pickup",
        selectedLocation: "",
        selectedArea: "",
        locationsCategory: [],
        locations: [],
        errors: {},
        insufficient_products:[],
        showInsufficientStockModal: false,
      };
    },
    components: {
    CheckoutModal
  },
    mounted() {
      this.getLocationsCategory();
    },
    computed: {
      totalWeight() {
        return this.cartStore.totalWeight;
      },
      deliveryFee() {
        if (this.deliveryOption === "pickup") return 0;
        const location = this.locations.find((loc) => loc.name === this.selectedArea);
        return location ? location.price : 0;
      },
      total() {
        return this.cartStore.total;
      },
      totalPlusDelivery() {
        return this.total + this.deliveryFee;
      },
    },
    methods: {
      async getLocationsCategory() {
        try {
          const response = await axios.get("api/delivery_category/");
          this.locationsCategory = response.data;
        } catch (error) {
          this.$toast.error("Failed to load delivery categories. Please try again.");
        }
      },
      async getLocationAndPrice() {
        if (!this.selectedLocation) {
          this.locations = [];
          return;
        }
        try {
          const response = await axios.get("api/delivery_prices/", {
            params: {
              category: this.selectedLocation,
              weight: this.totalWeight,
            },
          });
          this.locations = response.data;
        } catch (error) {
          this.$toast.error("Failed to load delivery prices. Please try again.");
        }
      },
      async makePayment() {
        this.errors = {};
  
        if (!this.fullName) this.errors.fullName = "Full Name is required.";
        if (!this.email) this.errors.email = "Email is required.";
        if (!this.address) this.errors.address = "Address is required.";
        if (!this.phoneNumber) this.errors.phoneNumber = "Phone Number is required.";
        if (this.deliveryOption === "delivery" && !this.selectedLocation) {
          this.errors.selectedLocation = "Delivery Location is required.";
        }
        if (this.deliveryOption === "delivery" && !this.selectedArea) {
          this.errors.selectedArea = "Delivery Area is required.";
        }
  
        if (Object.keys(this.errors).length > 0) return;
  
        const payload = {
          full_name: this.fullName,
          email: this.email,
          address: this.address,
          phone_number: this.phoneNumber,
          delivery_option: this.deliveryOption,
          delivery_location: this.selectedArea,
          total_weight: this.totalWeight,
          shipping_fee: this.deliveryFee,
          total: this.total,
          total_plus_delivery: this.totalPlusDelivery,
          items: this.cartStore.items.map((item) => ({
            product: item.id,
            quantity: item.quantity,
          })),
        };
  
        // Proceed with payment logic
        console.log("Payload for payment:", payload);
        try{
            const response = await axios.post("api/checkout/", payload);
            console.log(response.data);
            window.location.href = response.data.redirect_url;

        }catch(error){
            if(error.response && error.response.status === 400 && error.response.data.insufficient_products){
                const errorData = error.response.data;
                if(errorData.insufficient_products){
                    this.insufficient_products = errorData.insufficient_products;
                    this.showInsufficientStockModal = true;
                    this.insufficient_products.forEach(product => {
                        const cartItem = this.cartStore.items.find(item => item.name === product.name);

                            if (cartItem) {
                                this.cartStore.updateStock(cartItem.id, product.stock)
                            }
                    });
                            

                    this.toastStore.showToast(5000,"Some products are out of stock. Please remove them from your cart.", 'bg-red-500');
                }
            }else {
                this.$toast.error("An error occurred during checkout. Please try again.");
            }
            
        }

      },
      updateCartAutomatically() {
        this.insufficient_products.forEach(product => {
            const cartItem = this.cartStore.items.find(item => item.name === product.name);

            if (cartItem) {
            if (product.stock === 0) {
                this.cartStore.removeItem(cartItem.id);
            } else {
                this.cartStore.updateQuantity(cartItem.id, Math.min(cartItem.quantity, product.stock));
            }
            }
        });

        this.showInsufficientStockModal = false;
        this.insufficient_products = [];
        
        this.toastStore.showToast(
            5000,
            "Cart updated based on available stock.",
            'bg-blue-500'
        );
        },


    cancelCheckout() {
      this.showInsufficientStockModal = false;
      this.toastStore.showToast(5000, "Please update your cart manually before proceeding.", 'bg-yellow-500');
      this.$router.push('/cart');
    }
    },
    watch: {
      selectedLocation: "getLocationAndPrice",
      deliveryOption(newOption) {
        if (newOption === "pickup") {
          this.selectedLocation = "";
          this.selectedArea = "";
          delete this.errors.selectedLocation;
          delete this.errors.selectedArea;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add any component-specific styles here */
  </style>
  