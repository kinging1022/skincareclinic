<template>
  <div class="min-h-screen bg-[#f0f5f1]">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
      <!-- Cart Header -->
      <div class="flex items-center gap-3 mb-8">
        <ShoppingBag class="text-[#0a5c3e] w-6 h-6" />
        <h1 class="text-2xl sm:text-3xl font-light tracking-wider text-[#1c3a2e]">
          YOUR CART
        </h1>
      </div>

      <!-- Empty Cart State -->
      <div v-if="cartStore.items.length === 0" class="text-center py-16">
        <p class="text-[#4a6b5d] mb-6">Your cart is currently empty</p>
        <router-link 
          to="/products" 
          class="inline-block bg-[#0a5c3e] hover:bg-[#0b4a33] text-white py-2 sm:py-3 px-6 sm:px-8 rounded-none transition-colors duration-200 text-sm sm:text-base"
        >
          CONTINUE SHOPPING
        </router-link>
      </div>

      <!-- Cart with Items -->
      <div v-else class="grid lg:grid-cols-3 gap-6 sm:gap-8">
        <!-- Left Column - Cart Items -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg border border-[#d7e5dc] overflow-hidden">
            <!-- Cart Items List -->
            <div
              v-for="item in cartStore.items"
              :key="item.id"
              class="flex items-start sm:items-center gap-4 p-4 sm:p-6 border-b border-[#d7e5dc] last:border-b-0"
            >
              <!-- Product Image -->
              <RouterLink 
                :to="{name:'product-detail', params:{slug:item.slug}}"
                class="flex-shrink-0"
              >
                <img 
                  :src="item.get_thumbnail" 
                  :alt="item.name" 
                  class="w-16 h-16 sm:w-20 sm:h-20 object-cover"
                  loading="lazy"
                />
              </RouterLink>

              <!-- Product Details -->
              <div class="flex-grow">
                <RouterLink :to="{name:'product-detail', params:{slug:item.slug}}">
                  <h3 v-if="item.brand" class="text-xs font-medium text-[#0a5c3e] uppercase tracking-wider mb-1">
                    {{ item.brand.name }}
                  </h3>
                  <p class="text-sm sm:text-base text-[#1c3a2e] font-light">{{ item.name }}</p>
                </RouterLink>
                <p class="text-[#0a5c3e] font-medium mt-1 sm:mt-2">
                  ₦{{ item.price.toLocaleString() }}
                </p>
              </div>

              <!-- Quantity Controls -->
              <div class="flex items-center gap-2">
                <button
                  @click="decreaseQuantity(item)"
                  class="w-6 h-6 sm:w-8 sm:h-8 flex items-center justify-center border border-[#d7e5dc] text-[#0a5c3e] hover:bg-[#f0f5f1] transition-colors"
                >
                  <Minus class="w-3 h-3 sm:w-4 sm:h-4" />
                </button>
                <span class="w-6 text-center text-sm sm:text-base">{{ item.quantity }}</span>
                <button
                  @click="increaseQuantity(item)"
                  class="w-6 h-6 sm:w-8 sm:h-8 flex items-center justify-center border border-[#d7e5dc] text-[#0a5c3e] hover:bg-[#f0f5f1] transition-colors"
                  :class="{'opacity-50 cursor-not-allowed': item.quantity >= item.stock}"
                >
                  <Plus class="w-3 h-3 sm:w-4 sm:h-4" />
                </button>
              </div>

              <!-- Remove Item -->
              <button
                @click="removeItem(item)"
                class="text-[#9ab0a6] hover:text-[#0a5c3e] transition-colors ml-2"
                aria-label="Remove item"
              >
                <X class="w-4 h-4 sm:w-5 sm:h-5" />
              </button>
            </div>
          </div>
        </div>

        <!-- Right Column - Order Summary -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg border border-[#d7e5dc] lg:sticky lg:top-6">
            <div class="bg-[#f0f5f1] px-4 sm:px-6 py-3 sm:py-4 border-b border-[#d7e5dc]">
              <h2 class="text-base sm:text-lg font-medium text-[#1c3a2e] tracking-wider">
                ORDER SUMMARY
              </h2>
            </div>
            
            <div class="p-4 sm:p-6">
              <!-- Order Totals -->
              <div class="space-y-3">
                <div class="flex justify-between text-sm text-[#4a6b5d]">
                  <span>Subtotal</span>
                  <span>₦{{ subtotal.toLocaleString() }}</span>
                </div>
                
                
                <div class="border-t border-[#d7e5dc] pt-3 mt-3">
                  <div class="flex justify-between text-sm sm:text-base font-medium text-[#1c3a2e]">
                    <span>Total</span>
                    <span>₦{{ total.toLocaleString() }}</span>
                  </div>
                </div>
              </div>

              <!-- Checkout Button -->
              <RouterLink 
                to="/checkout" 
                class="mt-4 sm:mt-6 w-full bg-[#0a5c3e] hover:bg-[#0b4a33] text-white py-2 sm:py-3 px-4 sm:px-6 rounded-none transition-colors duration-200 flex items-center justify-center text-sm sm:text-base"
              >
                <span>PROCEED TO CHECKOUT</span>
                <ArrowRight class="ml-2 w-4 h-4" />
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ShoppingBag, X, Minus, Plus, ArrowRight } from 'lucide-vue-next';
import { useToastStore } from '@/stores/toast';
import { useCartStore } from '@/stores/cart';

export default {
  name: 'CartPage',
  components: {
    ShoppingBag,
    X,
    Minus,
    Plus,
    ArrowRight
  },
  data() {
    return {
      cartStore: useCartStore(),
      toastStore: useToastStore()
    }
  },
  computed: {
    subtotal() {
      return this.cartStore.subtotal;
    },

    total() {
      return this.cartStore.total;
    }
  },
  methods: {
    increaseQuantity(item) {
      if (item.quantity < item.stock) {
        this.cartStore.updateQuantity(item.id, item.quantity + 1);
      } else {
        this.toastStore.showToast(2000, `Only ${item.stock} items available in stock`, "bg-amber-500");
      }
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        this.cartStore.updateQuantity(item.id, item.quantity - 1);
      } else {
        this.removeItem(item);
      }
    },
    removeItem(item) {
      this.cartStore.removeItem(item.id);
      this.toastStore.showToast(2000, `${item.name} removed from cart`, "bg-red-500 text-white");
    }
  }
}
</script>

<style scoped>
/* Optimize image loading */
img {
  backface-visibility: hidden;
  will-change: transform;
}

/* Improve text rendering */
h1, h2, h3, p, span, button {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Optimize button transitions */
button {
  will-change: background-color;
  transform: translateZ(0);
}

/* Responsive adjustments */
@media (max-width: 1023px) {
  .lg\:sticky {
    position: static;
    margin-top: 1.5rem;
  }
}
</style>