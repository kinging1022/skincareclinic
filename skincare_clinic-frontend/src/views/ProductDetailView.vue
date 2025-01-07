<template>
    <div class="min-h-screen bg-gray-50">
      <main class="container mx-auto px-4 py-12">
        <button @click="goBack" class="mb-6 flex items-center text-emerald-600 hover:text-emerald-700 transition duration-300 ease-in-out">
          <ArrowLeftIcon class="h-5 w-5 mr-2" />
          Back to previous page
        </button>
        
        <div v-if="loading" class="text-center py-16">
          <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-emerald-600 mx-auto"></div>
          <p class="mt-4 text-lg text-gray-600">Loading product details...</p>
        </div>
  
        <div v-else-if="error" class="text-center py-16">
          <XCircleIcon class="mx-auto h-16 w-16 text-red-500" />
          <h2 class="mt-4 text-2xl font-semibold text-gray-900">Error Loading Product</h2>
          <p class="mt-2 text-gray-600">{{ error }}</p>
          <button @click="getProduct" class="mt-6 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition duration-300 ease-in-out">
            Try Again
          </button>
        </div>
  
        <div v-else-if="product" class="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="relative h-96 md:h-full">
              <img class="absolute inset-0 w-full h-full object-cover" :src="product.get_image" :alt="product.name" />
              <div class="absolute top-4 left-4 bg-white px-3 py-1 rounded-full text-sm font-semibold text-gray-700">
                {{ product.brand ? product.brand.name : 'Brand' }}
              </div>
            </div>
            <div class="p-8 flex flex-col justify-between">
              <div>
                <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ product.name }}</h1>
                <p class="text-gray-600 mb-6">{{ product.description }}</p>
                <div class="flex items-center mb-6">
                  <span class="text-2xl font-bold text-gray-900">${{ product.price.toLocaleString() }}</span>
                  <span :class="product.stock > 0 ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'" 
                        class="ml-4 px-3 py-1 rounded-full text-sm font-medium">
                    {{ product.stock > 0 ? `${product.stock} in stock` : 'Out of stock' }}
                  </span>
                </div>
              </div>
              <div>
                <div class="flex items-center mb-6" v-if="product.stock > 0">
                  <button @click="decreaseQuantity" 
                          class="bg-emerald-100 text-emerald-600 hover:text-emerald-700 hover:bg-emerald-200 h-10 w-10 rounded-l cursor-pointer outline-none"
                          :class="{'opacity-50 cursor-not-allowed' : cartQuantity <= 1 || !isInCart}">
                    <MinusIcon class="h-5 w-5 m-auto" />
                  </button>
                  <div class="outline-none focus:outline-none text-center w-24 bg-gray-100 font-semibold text-md md:text-base flex items-center justify-center text-gray-700">
                    {{ cartQuantity }}
                  </div>
                  <button @click="increaseQuantity"
                          class="bg-emerald-100 text-emerald-600 hover:text-emerald-700 hover:bg-emerald-200 h-10 w-10 rounded-r cursor-pointer"
                          :class="{'opacity-50 cursor-not-allowed': cartQuantity >= product.stock}">
                    <PlusIcon class="h-5 w-5 m-auto" />
                  </button>
                </div>
                <button @click="addToCart"
                        class="w-full py-3 px-6 rounded-lg transition duration-300 ease-in-out flex items-center justify-center"
                        :class="product.stock === 0 ? 'bg-red-600 text-white cursor-not-allowed' : 'bg-emerald-600 text-white hover:bg-emerald-700'"
                        :disabled="product.stock === 0 || isInCart">
                  <ShoppingCartIcon class="h-5 w-5 mr-2" />
                  {{ product.stock === 0 ? 'Out of Stock' : (isInCart ? 'Already in cart' : 'Add to Cart') }}
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <div v-else class="text-center py-16">
          <XCircleIcon class="mx-auto h-16 w-16 text-gray-400" />
          <h2 class="mt-4 text-2xl font-semibold text-gray-900">Product Not Found</h2>
          <p class="mt-2 text-gray-600">Sorry, we couldn't find the product you're looking for.</p>
          <router-link to="/" class="mt-6 inline-block px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition duration-300 ease-in-out">
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
      this.getProduct()
    },
    computed: {
      isInCart() {
        return this.product && this.cartStore.items.some(item => item.id === this.product.id);
      },
      cartQuantity() {
        if (!this.product) return 0;
        const cartItem = this.cartStore.items.find(item => item.id === this.product.id);
        return cartItem ? cartItem.quantity : 0;
      }
    },
    methods: {
      async getProduct() {
        const slug = this.$route.params.slug
        this.loading = true;
        this.error = null;
        try {
          const response = await axios.get(`/api/products/${slug}/`)
          this.product = response.data
        } catch (error) {
          console.error('Error fetching product:', error)
          this.error = "Failed to load product. Please try again."
        } finally {
          this.loading = false;
        }
      },
      addToCart() {
        if (this.product.stock > 0) {
          this.cartStore.addItem(this.product);
          const brandName = this.product.brand?.name || "No Brand"; 
          const message = this.product.brand
            ? `Added ${brandName} ${this.product.name} to cart`
            : `Added ${this.product.name} to cart`;
          this.toastStore.showToast(2000, message, "bg-emerald-500");
        }
      },
      increaseQuantity() {
        if (this.cartQuantity < this.product.stock) {
          this.cartStore.updateQuantity(this.product.id, this.cartQuantity + 1);
        }else if (this.cartQuantity >= this.product.stock){
          alert(`only ${this.product.stock} items left in stock`)
        }
      },
      decreaseQuantity() {
        if (this.cartQuantity > 1) {
          this.cartStore.updateQuantity(this.product.id, this.cartQuantity - 1);
        }else if (this.cartQuantity === 1)
        {
            this.cartStore.removeItem(this.product.id)
            this.toastStore.showToast(2000, `${this.product.name} removed from cart`, "bg-red-500");
            this.goBack()
        }
      },
      goBack() {
        this.$router.go(-1)
      }
    }
  }
  </script>