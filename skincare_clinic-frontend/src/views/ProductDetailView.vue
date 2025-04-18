<template>
  <div class="min-h-screen bg-gray-50">
    <main class="container mx-auto px-4 py-8 max-w-6xl">
      <button @click="goBack" class="mb-6 flex items-center text-emerald-800 hover:text-emerald-600 transition duration-300 ease-in-out">
        <ArrowLeftIcon class="h-5 w-5 mr-2" />
        Back to previous page
      </button>
      
      <div v-if="loading" class="text-center py-16">
        <div class="animate-spin rounded-full h-24 w-24 border-b-2 border-t-2 border-emerald-800 mx-auto"></div>
        <p class="mt-4 text-lg font-light text-gray-600">Loading product details...</p>
      </div>

      <div v-else-if="error" class="text-center py-16 max-w-md mx-auto">
        <XCircleIcon class="mx-auto h-16 w-16 text-red-500" />
        <h2 class="mt-4 text-2xl font-medium text-gray-900">Error Loading Product</h2>
        <p class="mt-2 text-gray-600">{{ error }}</p>
        <button @click="getProduct" class="mt-6 px-6 py-3 bg-emerald-800 text-white rounded-lg hover:bg-emerald-700 transition duration-300 ease-in-out">
          Try Again
        </button>
      </div>

      <div v-else-if="product" class="bg-white rounded-xl shadow-md overflow-hidden border border-emerald-50">
        <!-- Redesigned grid layout with better responsiveness -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-0">
          <!-- Product Image Section - Full width on mobile -->
          <div class="relative w-full">
            <!-- Removed any potential padding/margin that could create white space -->
            <div class="relative h-[300px] sm:h-[400px] md:h-[450px] lg:h-[500px] w-full">
              <img 
                class="w-full h-full object-cover" 
                :src="product.get_image" 
                :alt="product.name"
                loading="lazy"
              />
            </div>
            
            <!-- Brand Badge -->
            <div v-if="product.brand" class="absolute top-4 left-4 bg-white px-3 py-1 rounded-full text-sm font-medium text-emerald-800 shadow-sm">
              {{ product.brand.name }}
            </div>
            
            <!-- Stock Badge -->
            <div v-if="product.stock <= 5 && product.stock > 0" 
                class="absolute top-4 right-4 bg-amber-500 text-white text-xs px-2 py-1 rounded-full font-medium">
              Only {{ product.stock }} left
            </div>
            <div v-else-if="product.stock === 0" 
                class="absolute top-4 right-4 bg-red-500 text-white text-xs px-2 py-1 rounded-full font-medium">
              Out of stock
            </div>
          </div>
          
          <!-- Product Details Section -->
          <div class="p-6 md:p-8 flex flex-col">
            <div class="flex-grow">
              <h1 class="text-2xl md:text-3xl font-medium text-gray-900 mb-2">{{ product.name }}</h1>
              <p v-if="product.brand" class="text-sm font-medium text-emerald-800 uppercase tracking-wider mb-4">
                {{ product.brand.name }}
              </p>
              <p class="text-gray-600 mb-6 font-light">{{ product.description }}</p>
              <div class="flex items-center mb-6">
                <span class="text-2xl font-medium text-emerald-700">₦ {{ product.price.toLocaleString() }}</span>
              </div>
            </div>
            
            <!-- Quantity and Add to Cart Section - Always at the bottom -->
            <div class="mt-auto">
              <div class="flex items-center mb-6" v-if="product.stock > 0 && isInCart">
                <button @click="decreaseQuantity" 
                        class="bg-emerald-50 text-emerald-800 hover:bg-emerald-100 h-10 w-10 rounded-l border border-emerald-200 transition-colors"
                        :class="{'opacity-50 cursor-not-allowed' : cartQuantity <= 1}">
                  <MinusIcon class="h-5 w-5 m-auto" />
                </button>
                <div class="h-10 w-16 flex items-center justify-center border-t border-b border-emerald-200 font-medium text-gray-700">
                  {{ cartQuantity }}
                </div>
                <button @click="increaseQuantity"
                        class="bg-emerald-50 text-emerald-800 hover:bg-emerald-100 h-10 w-10 rounded-r border border-emerald-200 transition-colors"
                        :class="{'opacity-50 cursor-not-allowed': cartQuantity >= product.stock}">
                  <PlusIcon class="h-5 w-5 m-auto" />
                </button>
              </div>
              
              <button @click="addToCart"
                      class="w-full py-2.5 border transition-colors duration-300 flex items-center justify-center"
                      :class="buttonClasses"
                      :disabled="product.stock === 0 || isInCart">
                <ShoppingCartIcon class="h-5 w-5 mr-2" />
                {{ cartButtonText }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-16 max-w-md mx-auto">
        <XCircleIcon class="mx-auto h-16 w-16 text-gray-400" />
        <h2 class="mt-4 text-2xl font-medium text-gray-900">Product Not Found</h2>
        <p class="mt-2 text-gray-600 font-light">Sorry, we couldn't find the product you're looking for.</p>
        <router-link to="/" class="mt-6 inline-block px-6 py-3 bg-emerald-800 text-white rounded-lg hover:bg-emerald-700 transition duration-300 ease-in-out">
          Return to Shop
        </router-link>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import { useCartStore } from '@/stores/cart';
import { useToastStore } from '@/stores/toast';
import { ShoppingCartIcon, MinusIcon, PlusIcon, XCircleIcon, ArrowLeftIcon } from 'lucide-vue-next'

export default {
  name: 'ProductDetail',
  components: {
    ShoppingCartIcon,
    MinusIcon,
    PlusIcon,
    XCircleIcon,
    ArrowLeftIcon
  },
  data() {
    return {
      product: null,
      loading: true,
      error: null,
      cartStore: useCartStore(),
      toastStore: useToastStore()
    }
  },
  mounted() {
    this.getProduct();
    // Add event listener for image loading
    window.addEventListener('load', this.handleImagesLoaded);
  },
  beforeUnmount() {
    // Clean up event listener
    window.removeEventListener('load', this.handleImagesLoaded);
  },
  computed: {
    isInCart() {
      return this.product && this.cartStore.items.some(item => item.id === this.product.id);
    },
    cartQuantity() {
      if (!this.product) return 0;
      const cartItem = this.cartStore.items.find(item => item.id === this.product.id);
      return cartItem ? cartItem.quantity : 0;
    },
    buttonClasses() {
      if (this.product?.stock === 0) {
        return 'border-gray-300 text-gray-400 cursor-not-allowed';
      } else if (this.isInCart) {
        return 'border-emerald-300 bg-emerald-50 text-emerald-800 cursor-default';
      } else {
        return 'border-emerald-800 text-emerald-800 hover:bg-emerald-800 hover:text-white';
      }
    },
    cartButtonText() {
      if (this.product?.stock === 0) {
        return 'Out of Stock';
      } else if (this.isInCart) {
        return 'Added to Cart';
      } else {
        return 'Add to Cart';
      }
    }
  },
  methods: {
    async getProduct() {
      const slug = this.$route.params.slug;
      this.loading = true;
      this.error = null;
      
      try {
        // Use a timeout to prevent multiple rapid requests
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
        
        const response = await axios.get(`/api/shop/products/${slug}/`, {
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        this.product = response.data;
      } catch (error) {
        console.error('Error fetching product:', error);
        this.error = error.name === 'AbortError' 
          ? "Request timed out. Please check your connection and try again." 
          : "Failed to load product. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    addToCart() {
      if (this.product.stock > 0 && !this.isInCart) {
        this.cartStore.addItem(this.product);
      }
    },
    increaseQuantity() {
      if (this.cartQuantity < this.product.stock) {
        this.cartStore.updateQuantity(this.product.id, this.cartQuantity + 1);
      } else if (this.cartQuantity >= this.product.stock) {
        this.toastStore.showToast(2000, `Only ${this.product.stock} items available in stock`, "bg-amber-500");
      }
    },
    decreaseQuantity() {
      if (this.cartQuantity > 1) {
        this.cartStore.updateQuantity(this.product.id, this.cartQuantity - 1);
      } else if (this.cartQuantity === 1) {
        this.cartStore.removeItem(this.product.id);
        this.toastStore.showToast(2000, `${this.product.name} removed from cart`, "bg-red-500");
      }
    },
    goBack() {
      this.$router.go(-1);
    },
    handleImagesLoaded() {
      // This helps with layout shifts after images load
      const images = document.querySelectorAll('img');
      images.forEach(img => {
        if (img.complete) {
          img.classList.add('loaded');
        } else {
          img.addEventListener('load', () => {
            img.classList.add('loaded');
          });
        }
      });
    }
  }
}
</script>

<style scoped>
/* Optimize rendering performance */
img {
  backface-visibility: hidden;
  will-change: transform;
  transform: translateZ(0);
}

/* Smooth transitions for loaded images */
img.loaded {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0.8; }
  to { opacity: 1; }
}

/* Improve text rendering */
h1, h2, p, span, button {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Optimize button transitions */
button {
  will-change: background-color, color;
  transform: translateZ(0);
}

/* Optimize animations */
.animate-spin {
  will-change: transform;
}

/* Remove any potential white space on smaller screens */
@media (max-width: 768px) {
  .rounded-xl {
    border-radius: 0.75rem;
    overflow: hidden;
  }
  
  /* Ensure image container takes full width */
  .relative.w-full {
    width: 100%;
    padding: 0;
    margin: 0;
  }
  
  /* Ensure image fills container completely */
  .relative.w-full img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}
</style>