<template>
    <div class="min-h-screen bg-gray-50">
      <main class="container mx-auto px-4 py-12">
        <button @click="goBack" class="mb-6 flex items-center text-emerald-600 hover:text-emerald-700 transition duration-300 ease-in-out">
          <ArrowLeftIcon class="h-5 w-5 mr-2" />
          Back to previous page
        </button>
        
        <div v-if="product" class="bg-white rounded-2xl shadow-lg overflow-hidden">
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
                  <span class="text-2xl font-bold text-gray-900">${{ product.price }}</span>
                  <span :class="product.stock > 0 ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'" 
                        class="ml-4 px-3 py-1 rounded-full text-sm font-medium">
                    {{ product.stock > 0 ? `${product.stock} in stock` : 'Out of stock' }}
                  </span>
                </div>
              </div>
              <div>
                <div class="flex items-center mb-6">
                  <button @click="decreaseQuantity" 
                          class="bg-emerald-100 text-emerald-600 hover:text-emerald-700 hover:bg-emerald-200 h-10 w-10 rounded-l cursor-pointer outline-none">
                    <MinusIcon class="h-5 w-5 m-auto" />
                  </button>
                  <input v-model.number="quantity" 
                         type="number" 
                         class="outline-none focus:outline-none text-center w-24 bg-gray-100 font-semibold text-md hover:text-black focus:text-black md:text-base cursor-default flex items-center text-gray-700 outline-none"
                         :disabled="product.stock === 0"
                         min="1"
                         :max="product.stock" />
                  <button @click="increaseQuantity"
                          class="bg-emerald-100 text-emerald-600 hover:text-emerald-700 hover:bg-emerald-200 h-10 w-10 rounded-r cursor-pointer">
                    <PlusIcon class="h-5 w-5 m-auto" />
                  </button>
                </div>
                <button @click="addToCart"
                        class="w-full bg-emerald-600 text-white py-3 px-6 rounded-lg hover:bg-emerald-700 transition duration-300 ease-in-out flex items-center justify-center"
                        :disabled="product.stock === 0 || quantity < 1">
                  <ShoppingCartIcon class="h-5 w-5 mr-2" />
                  Add to Cart
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
        quantity: 1,
        product: null
      }
    },
    mounted() {
      this.getProduct()
    },
    methods: {
      async getProduct() {
        const slug = this.$route.params.slug
        try {
          const response = await axios.get(`/api/products/${slug}/`)
          this.product = response.data
        } catch (error) {
          console.error('Error fetching product:', error)
        }
      },
      addToCart() {
        if (this.quantity > 0 && this.quantity <= this.product.stock) {
          console.log(`Added ${this.quantity} of ${this.product.name} to cart`)
          alert(`Added ${this.quantity} of ${this.product.name} to cart`)
          
          this.product.stock -= this.quantity
          this.quantity = 1
        }
      },
      increaseQuantity() {
        if (this.quantity < this.product.stock) {
          this.quantity++
        }
      },
      decreaseQuantity() {
        if (this.quantity > 1) {
          this.quantity--
        }
      },
      goBack() {
        this.$router.go(-1)
      }
    }
  }
  </script>