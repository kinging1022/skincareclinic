<template>
  <div class="min-h-screen bg-[#f0f5f1]">
    <!-- Checkout Header -->
    <div class="bg-white border-b border-[#d7e5dc] py-6">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <h1 class="text-2xl sm:text-3xl font-light tracking-wider text-[#1c3a2e] text-center">
          SKINCARÈ CLINIC CHECKOUT
        </h1>
      </div>
    </div>

    <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
      <div class="grid lg:grid-cols-3 gap-6 sm:gap-8">
        <!-- Left Column - Checkout Steps -->
        <div class="lg:col-span-2 space-y-6 sm:space-y-8">
          <!-- Personal Details Card -->
          <div class="bg-white rounded-lg border border-[#d7e5dc] overflow-hidden">
            <div class="bg-[#f0f5f1] px-4 sm:px-6 py-3 sm:py-4 border-b border-[#d7e5dc]">
              <h2 class="text-base sm:text-lg font-medium text-[#1c3a2e] tracking-wider">
                <span class="text-[#0a5c3e] mr-2">01</span> Contact Information
              </h2>
            </div>
            <div class="p-4 sm:p-6">
              <form class="space-y-4 sm:space-y-6">
                <div>
                  <label class="block text-sm font-medium text-[#4a6b5d] mb-2">Full Name</label>
                  <input
                    type="text"
                    class="w-full px-3 sm:px-4 py-2 sm:py-3 border border-[#d7e5dc] rounded-none focus:ring-1 focus:ring-[#0a5c3e] focus:border-[#0a5c3e] text-[#1c3a2e] placeholder-[#9ab0a6]"
                    placeholder="Enter your full name"
                    v-model="fullName"
                  />
                  <span v-if="errors.fullName" class="text-red-500 text-xs mt-1">{{ errors.fullName }}</span>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-[#4a6b5d] mb-2">Email</label>
                  <input
                    type="email"
                    class="w-full px-3 sm:px-4 py-2 sm:py-3 border border-[#d7e5dc] rounded-none focus:ring-1 focus:ring-[#0a5c3e] focus:border-[#0a5c3e] text-[#1c3a2e] placeholder-[#9ab0a6]"
                    placeholder="your@email.com"
                    v-model="email"
                  />
                  <span v-if="errors.email" class="text-red-500 text-xs mt-1">{{ errors.email }}</span>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-[#4a6b5d] mb-2">Phone Number</label>
                  <input
                    type="tel"
                    class="w-full px-3 sm:px-4 py-2 sm:py-3 border border-[#d7e5dc] rounded-none focus:ring-1 focus:ring-[#0a5c3e] focus:border-[#0a5c3e] text-[#1c3a2e] placeholder-[#9ab0a6]"
                    placeholder="+234 800 000 0000"
                    v-model="phoneNumber"
                  />
                  <span v-if="errors.phoneNumber" class="text-red-500 text-xs mt-1">{{ errors.phoneNumber }}</span>
                </div>
              </form>
            </div>
          </div>

          <!-- Delivery Method Card - Vertical Layout -->
          <div class="bg-white rounded-lg border border-[#d7e5dc] overflow-hidden">
            <div class="bg-[#f0f5f1] px-4 sm:px-6 py-3 sm:py-4 border-b border-[#d7e5dc]">
              <h2 class="text-base sm:text-lg font-medium text-[#1c3a2e] tracking-wider">
                <span class="text-[#0a5c3e] mr-2">02</span> Delivery Method
              </h2>
            </div>
            <div class="p-4 sm:p-6 space-y-4">
              <!-- Vertical Radio Buttons -->
              <div class="space-y-3 sm:space-y-4">
                <label class="block cursor-pointer">
                  <input
                    type="radio"
                    name="delivery"
                    value="pickup"
                    v-model="deliveryOption"
                    class="sr-only peer"
                  />
                  <div class="p-3 sm:p-4 border border-[#d7e5dc] rounded-none peer-checked:border-[#0a5c3e] peer-checked:bg-[#f0f5f1] transition-colors">
                    <div class="flex items-center">
                      <div class="h-5 w-5 rounded-full border-2 border-[#d7e5dc] flex items-center justify-center mr-3">
                        <div class="h-3 w-3 rounded-full bg-[#0a5c3e]" :class="[deliveryOption === 'pickup' ? 'opacity-100' : 'opacity-0']"></div>
                      </div>
                      <div>
                        <span class="text-[#1c3a2e] font-medium">Pickup</span>
                        <p class="text-xs sm:text-sm text-[#4a6b5d] mt-1">Send your payment receipt to our IG for pick up details</p>
                      </div>
                    </div>
                  </div>
                </label>
                
                <label class="block cursor-pointer">
                  <input
                    type="radio"
                    name="delivery"
                    value="delivery"
                    v-model="deliveryOption"
                    class="sr-only peer"
                  />
                  <div class="p-3 sm:p-4 border border-[#d7e5dc] rounded-none peer-checked:border-[#0a5c3e] peer-checked:bg-[#f0f5f1] transition-colors">
                    <div class="flex items-center">
                      <div class="h-5 w-5 rounded-full border-2 border-[#d7e5dc] flex items-center justify-center mr-3">
                        <div class="h-3 w-3 rounded-full bg-[#0a5c3e]" :class="[deliveryOption === 'delivery' ? 'opacity-100' : 'opacity-0']"></div>
                      </div>
                      <div>
                        <span class="text-[#1c3a2e] font-medium">Home Delivery</span>
                        <p class="text-xs sm:text-sm text-[#4a6b5d] mt-1">Delivered to your doorstep</p>
                      </div>
                    </div>
                  </div>
                </label>
              </div>

              <!-- Delivery Address Section - Reordered with address last -->
              <div v-if="deliveryOption === 'delivery'" class="space-y-4 sm:space-y-6 pt-4">
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-[#4a6b5d] mb-2">Location Category</label>
                    <select
                      v-model="selectedLocation"
                      class="w-full px-3 sm:px-4 py-2 sm:py-3 border border-[#d7e5dc] rounded-none focus:ring-1 focus:ring-[#0a5c3e] focus:border-[#0a5c3e] text-[#1c3a2e] appearance-none bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM0YTZiNWQiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1jaGV2cm9uLWRvd24iPjxwYXRoIGQ9Im03IDE1IDUgNSA1LTUiLz48L3N2Zz4=')] bg-[position:right_0.5rem_center] bg-no-repeat bg-[length:1.5rem]"
                    >
                      <option value="" disabled selected>Select your area</option>
                      <option v-for="location in locationsCategory" :key="location.id" :value="location.slug">{{ location.name }}</option>
                    </select>
                    <span v-if="errors.selectedLocation" class="text-red-500 text-xs mt-1">{{ errors.selectedLocation }}</span>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-[#4a6b5d] mb-2">Prices</label>
                    <select
                      v-model="selectedArea"
                      class="w-full px-3 sm:px-4 py-2 sm:py-3 border border-[#d7e5dc] rounded-none focus:ring-1 focus:ring-[#0a5c3e] focus:border-[#0a5c3e] text-[#1c3a2e] appearance-none bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM0YTZiNWQiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1jaGV2cm9uLWRvd24iPjxwYXRoIGQ9Im03IDE1IDUgNSA1LTUiLz48L3N2Zz4=')] bg-[position:right_0.5rem_center] bg-no-repeat bg-[length:1.5rem]"
                    >
                      <option value="" disabled selected>Select delivery option</option>
                      <option v-for="location in locations" :key="location.id" :value="location.name">
                        {{ location.name }} (₦{{ location.price.toLocaleString() }})
                      </option>
                    </select>
                    <span v-if="errors.selectedArea" class="text-red-500 text-xs mt-1">{{ errors.selectedArea }}</span>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-[#4a6b5d] mb-2">Delivery Address / Park Address</label>
                  <input
                    type="text"
                    class="w-full px-3 sm:px-4 py-2 sm:py-3 border border-[#d7e5dc] rounded-none focus:ring-1 focus:ring-[#0a5c3e] focus:border-[#0a5c3e] text-[#1c3a2e] placeholder-[#9ab0a6]"
                    placeholder="Your full address"
                    v-model="address"
                    :disabled="deliveryOption === 'pickup'"
                  />
                  <span v-if="errors.address" class="text-red-500 text-xs mt-1">{{ errors.address }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Order Summary - Made same width as left column on mobile -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg border border-[#d7e5dc] lg:sticky lg:top-6">
            <div class="bg-[#f0f5f1] px-4 sm:px-6 py-3 sm:py-4 border-b border-[#d7e5dc]">
              <h2 class="text-base sm:text-lg font-medium text-[#1c3a2e] tracking-wider">
                Order Total
              </h2>
            </div>
            
            <div class="p-4 sm:p-6">
              <!-- Order Totals - Adjusted spacing for mobile -->
              <div class="space-y-2 sm:space-y-3">
                <div class="flex justify-between text-sm text-[#4a6b5d]">
                  <span>Weight</span>
                  <span>{{totalWeight}} KG</span>
                </div>
                
                <div class="flex justify-between text-sm text-[#4a6b5d]">
                  <span>Subtotal</span>
                  <span>₦{{ total.toLocaleString() }}</span>
                </div>
                
                <div class="flex justify-between text-sm text-[#4a6b5d]">
                  <span>Delivery Fee</span>
                  <span v-if="deliveryOption === 'pickup'">₦0</span>
                  <span v-else-if="selectedArea">₦{{ deliveryFee.toLocaleString() }}</span>
                  <span v-else class="text-xs">Select area</span>
                </div>

                <div class="border-t border-[#d7e5dc] pt-2 sm:pt-3 mt-2 sm:mt-3">
                  <div class="flex justify-between text-sm sm:text-base font-medium text-[#1c3a2e]">
                    <span>Total</span>
                    <span>₦{{ totalPlusDelivery.toLocaleString() }}</span>
                  </div>
                </div>
              </div>

              <!-- Payment Button - Made full width and responsive -->
              <button
                @click="makePayment"
                class="mt-4 sm:mt-6 w-full bg-[#0a5c3e] hover:bg-[#0b4a33] text-white py-2 sm:py-3 px-4 sm:px-6 rounded-none transition-colors duration-200 flex items-center justify-center text-sm sm:text-base whitespace-nowrap"
              >
                <span>Complete Purchase</span>
                <ArrowRight class="ml-2 w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
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
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowRight } from 'lucide-vue-next';
import { useCartStore } from "@/stores/cart";
import { useToastStore } from "@/stores/toast";
import CheckoutModal from "@/components/CheckoutModal.vue";
import axios from "axios";

// Setup stores and router
const cartStore = useCartStore();
const toastStore = useToastStore();
const router = useRouter();

// Form state
const fullName = ref("");
const email = ref("");
const address = ref("");
const phoneNumber = ref("");
const deliveryOption = ref("pickup");
const selectedLocation = ref("");
const selectedArea = ref("");
const locationsCategory = ref([]);
const locations = ref([]);
const errors = ref({});
const insufficient_products = ref([]);
const showInsufficientStockModal = ref(false);

// Computed properties
const totalWeight = computed(() => cartStore.totalWeight);

const deliveryFee = computed(() => {
  if (deliveryOption.value === "pickup") return 0;
  const location = locations.value.find((loc) => loc.name === selectedArea.value);
  return location ? location.price : 0;
});

const total = computed(() => cartStore.total);

const totalPlusDelivery = computed(() => total.value + deliveryFee.value);

// API methods
const getLocationsCategory = async () => {
  try {
    // Use AbortController for cancellable requests
    const controller = new AbortController();
    const signal = controller.signal;
    
    const response = await axios.get("api/delivery_category/", { signal });
    locationsCategory.value = response.data;
  } catch (error) {
    if (error.name !== 'AbortError') {
      toastStore.showToast(3000, "Failed to load delivery categories. Please try again.", "bg-red-500");
    }
  }
};

const getLocationAndPrice = async () => {
  if (!selectedLocation.value) {
    locations.value = [];
    return;
  }
  
  try {
    // Use AbortController for cancellable requests
    const controller = new AbortController();
    const signal = controller.signal;
    
    const response = await axios.get("api/delivery_prices/", {
      params: {
        category: selectedLocation.value,
        weight: totalWeight.value,
      },
      signal
    });
    locations.value = response.data;
  } catch (error) {
    if (error.name !== 'AbortError') {
      toastStore.showToast(3000, "Failed to load delivery prices. Please try again.", "bg-red-500");
    }
  }
};

// Validation function
const isValidEmail = (email) => {
  const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return regex.test(email);
};

// Checkout methods
const makePayment = async () => {
  errors.value = {};

  // Validate Full Name
  if (!fullName.value) errors.value.fullName = "Full Name is required.";
  
  // Validate Email
  if (!email.value) {
    errors.value.email = "Email is required.";
  } else if (!isValidEmail(email.value)) {
    errors.value.email = "Please enter a valid email address.";
  }

  // Validate other fields
  if (!phoneNumber.value) errors.value.phoneNumber = "Phone Number is required.";
  if (deliveryOption.value === "delivery") {
    if (!address.value) errors.value.address = "Address is required.";
    if (!selectedLocation.value) errors.value.selectedLocation = "Location is required.";
    if (!selectedArea.value) errors.value.selectedArea = "Delivery option is required.";
  }

  if (Object.keys(errors.value).length > 0) return;

  const payload = {
    full_name: fullName.value,
    email: email.value,
    address: address.value,
    phone_number: phoneNumber.value,
    delivery_option: deliveryOption.value,
    delivery_location: selectedArea.value,
    total_weight: totalWeight.value,
    shipping_fee: deliveryFee.value,
    total: total.value,
    total_plus_delivery: totalPlusDelivery.value,
    items: cartStore.items.map((item) => ({
      product: item.id,
      quantity: item.quantity,
    })),
  };

  try {
    const response = await axios.post("api/checkout/", payload);
    window.location.href = response.data.redirect_url;
  } catch (error) {
    if (error.response && error.response.status === 400 && error.response.data.insufficient_products) {
      insufficient_products.value = error.response.data.insufficient_products;
      showInsufficientStockModal.value = true;
      
      // Update cart items with current stock info
      insufficient_products.value.forEach(product => {
        const cartItem = cartStore.items.find(item => item.name === product.name);
        if (cartItem) {
          cartStore.updateStock(cartItem.id, product.stock);
        }
      });

      toastStore.showToast(5000, "Some products are out of stock. Please remove them from your cart.", 'bg-red-500');
    } else {
      const errorMessage = error.response?.data?.error || "An error occurred. Please try again.";
      toastStore.showToast(3000, errorMessage, "bg-red-500 text-white");
    }
  }
};

const updateCartAutomatically = () => {
  insufficient_products.value.forEach(product => {
    const cartItem = cartStore.items.find(item => item.name === product.name);

    if (cartItem) {
      if (product.stock === 0) {
        cartStore.removeItem(cartItem.id);
      } else {
        cartStore.updateQuantity(cartItem.id, Math.min(cartItem.quantity, product.stock));
      }
    }
  });

  showInsufficientStockModal.value = false;
  insufficient_products.value = [];
  
  toastStore.showToast(
    3000,
    "Cart updated based on available stock.",
    'bg-blue-500'
  );
};

const cancelCheckout = () => {
  showInsufficientStockModal.value = false;
  toastStore.showToast(3000, "Please update your cart manually before proceeding.", 'bg-yellow-500');
  router.push('/cart');
};

// Watchers
watch(selectedLocation, () => {
  getLocationAndPrice();
});

watch(deliveryOption, (newOption) => {
  if (newOption === "pickup") {
    selectedLocation.value = "";
    selectedArea.value = "";
    address.value = ""; 
    
    // Clear related errors
    const newErrors = { ...errors.value };
    delete newErrors.selectedLocation;
    delete newErrors.selectedArea;
    delete newErrors.address;
    errors.value = newErrors;
  }
});

// Initialize component
onMounted(() => {
  getLocationsCategory();
});
</script>

<style scoped>
/* Use will-change for optimized animations */
button, select, input {
  will-change: transform, opacity;
}

/* Use hardware acceleration for transitions */
.transition-colors {
  backface-visibility: hidden;
  -webkit-font-smoothing: subpixel-antialiased;
}

/* Responsive adjustments */
@media (max-width: 1023px) {
  .lg\:col-span-2, .lg\:col-span-1 {
    grid-column: span 1;
    width: 100%;
  }
  
  .lg\:sticky {
    position: static;
    margin-top: 1.5rem;
  }
}
</style>