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
        <div class="grid grid-cols-1 md:grid-cols-2 gap-0">
          <!-- Product Image Section -->
          <div class="relative w-full">
            <div class="relative h-[300px] sm:h-[400px] md:h-[450px] lg:h-[500px] w-full">
              <img 
                class="w-full h-full object-cover" 
                :src="product.get_image" 
                :alt="product.name"
                loading="lazy"
                @load="imageLoaded"
                @error="handleImageError"
              />
            </div>
            
            <div v-if="product.brand" class="absolute top-4 left-4 bg-white px-3 py-1 rounded-full text-sm font-medium text-emerald-800 shadow-sm">
              {{ product.brand.name }}
            </div>
            
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

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ShoppingCartIcon, MinusIcon, PlusIcon, XCircleIcon, ArrowLeftIcon } from 'lucide-vue-next'
import axios from 'axios'
import { useCartStore } from '@/stores/cart'
import { useToastStore } from '@/stores/toast'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const toastStore = useToastStore()

const product = ref(null)
const loading = ref(true)
const error = ref(null)

const getProduct = async () => {
  const slug = route.params.slug
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get(`/api/shop/products/${slug}/`)
    product.value = response.data
  } catch (err) {
    console.error('Error fetching product:', err)
    error.value = err.response?.status === 404 
      ? "Product not found" 
      : "Failed to load product. Please try again."
  } finally {
    loading.value = false
  }
}

const imageLoaded = (event) => {
  event.target.classList.add('loaded')
}

const handleImageError = (event) => {
  console.error('Image failed to load:', product.value?.get_image)
  // Optional: Set a fallback image
  // event.target.src = '/images/placeholder-product.jpg'
}

const isInCart = computed(() => {
  return product.value && cartStore.items.some(item => item.id === product.value.id)
})

const cartQuantity = computed(() => {
  if (!product.value) return 0
  const cartItem = cartStore.items.find(item => item.id === product.value.id)
  return cartItem ? cartItem.quantity : 0
})

const buttonClasses = computed(() => {
  if (product.value?.stock === 0) {
    return 'border-gray-300 text-gray-400 cursor-not-allowed'
  } else if (isInCart.value) {
    return 'border-emerald-300 bg-emerald-50 text-emerald-800 cursor-default'
  } else {
    return 'border-emerald-800 text-emerald-800 hover:bg-emerald-800 hover:text-white'
  }
})

const cartButtonText = computed(() => {
  if (product.value?.stock === 0) {
    return 'Out of Stock'
  } else if (isInCart.value) {
    return 'Added to Cart'
  } else {
    return 'Add to Cart'
  }
})

const addToCart = () => {
  if (product.value.stock > 0 && !isInCart.value) {
    cartStore.addItem(product.value)
  }
}

const increaseQuantity = () => {
  if (cartQuantity.value < product.value.stock) {
    cartStore.updateQuantity(product.value.id, cartQuantity.value + 1)
  } else if (cartQuantity.value >= product.value.stock) {
    toastStore.showToast(2000, `Only ${product.value.stock} items available in stock`, "bg-amber-500")
  }
}

const decreaseQuantity = () => {
  if (cartQuantity.value > 1) {
    cartStore.updateQuantity(product.value.id, cartQuantity.value - 1)
  } else if (cartQuantity.value === 1) {
    cartStore.removeItem(product.value.id)
    toastStore.showToast(2000, `${product.value.name} removed from cart`, "bg-red-500")
  }
}

const goBack = () => {
  router.go(-1)
}

onMounted(() => {
  getProduct()
})
</script>

<style scoped>
img {
  opacity: 0;
  transition: opacity 0.3s ease;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

img.loaded {
  opacity: 1;
}

.animate-spin {
  will-change: transform;
}

button {
  will-change: background-color, color;
}

h1, h2, p, span, button {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

@media (max-width: 768px) {
  .rounded-xl {
    border-radius: 0.75rem;
    overflow: hidden;
  }
  
  .relative.w-full {
    width: 100%;
    padding: 0;
    margin: 0;
  }
  
  .relative.w-full img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}
</style>