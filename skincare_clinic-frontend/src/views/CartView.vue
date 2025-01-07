<template>
    <div class="min-h-screen w-full bg-white">
      <div class="max-w-6xl mx-auto px-4 py-8">
        <div class="flex items-center gap-2 mb-8">
          <ShoppingBag class="text-emerald-600" :size="24" />
          <h1 class="text-2xl font-medium">Your Cart</h1>
        </div>
        <div v-if="cartStore.items.length === 0" class="text-center py-16">
          <p class="text-gray-500">Your cart is empty</p>
          <router-link to="/shop" class="mt-4 inline-block px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors">
            Continue Shopping
          </router-link>
        </div>
        <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div class="lg:col-span-2">
            <div class="bg-white rounded-lg border border-emerald-100">
              <div
                v-for="item in cartStore.items"
                :key="item.id"
                class="flex items-center gap-4 p-4 border-b border-emerald-100 last:border-b-0"
              >
                <img :src="item.get_thumbnail" :alt="item.name" class="w-16 h-16 object-cover rounded" />
                <div class="flex-grow">
                  <RouterLink
                  :to="{name:'product-detail', params:{slug:item.slug}}"> 
                    <h3 v-if="item.brand" class="font-medium">{{ item.brand.name }}</h3>
                  <p class="text-gray-700">{{ item.name }}</p></RouterLink>
                  <p class="text-black-500">${{ item.price.toLocaleString() }}</p>
                </div>
                <div class="flex items-center gap-2">
                  <button
                    @click="decreaseQuantity(item)"
                    class="w-8 h-8 flex items-center justify-center bg-emerald-100 rounded-full hover:bg-emerald-200 transition-colors"
                  >
                    <Minus class="w-4 h-4" />
                  </button>
                  <span class="w-8 text-center">{{ item.quantity }}</span>
                  <button
                    @click="increaseQuantity(item)"
                    class="w-8 h-8 flex items-center justify-center bg-emerald-100 rounded-full hover:bg-emerald-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    :class="{'opacity-50 cursor-not-allowed': item.quantity >= item.stock}"

                    >
                    <Plus class="w-4 h-4" />
                  </button>
                </div>
                <button
                  @click="removeItem(item)"
                  class="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <XIcon :size="20" />
                </button>
              </div>
            </div>
          </div>
          <div class="lg:col-span-1">
            <div class="bg-white rounded-lg border border-emerald-100 p-6">
              <h2 class="text-lg font-medium mb-4">Order Summary</h2>
              <div class="space-y-3 mb-4">
                <div class="flex justify-between">
                  <span class="text-gray-600">Subtotal</span>
                  <span>${{ subtotal.toLocaleString() }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Tax</span>
                  <span>${{ tax.toLocaleString() }}</span>
                </div>
                <div class="h-px bg-emerald-100"></div>
                <div class="flex justify-between font-medium">
                  <span>Total</span>
                  <span>${{ total.toLocaleString() }}</span>
                </div>
              </div>
              <RouterLink to="/checkout"  class="w-full bg-emerald-600 text-white py-3 px-4 rounded-lg hover:bg-emerald-700 transition-colors">
                Proceed to Checkout
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ShoppingBag, XIcon, Minus, Plus } from 'lucide-vue-next';
  import { useCartStore } from '@/stores/cart'
  
  export default {
    name: 'CartPage',
    components: {
      ShoppingBag,
      XIcon,
      Minus,
      Plus
    },
    data() {
      return {
        cartStore: useCartStore()
      }
    },
    computed: {
      subtotal() {
        return this.cartStore.subtotal
      },
      tax() {
        return this.cartStore.tax
      },
      total() {
        return this.cartStore.total
      }
    },
    methods: {
      increaseQuantity(item) {
        if (item.quantity < item.stock) {
          this.cartStore.updateQuantity(item.id, item.quantity + 1)
        } else {
            
            alert(`only ${item.stock} items left in stock`)
        }
      },
      decreaseQuantity(item) {
        if (item.quantity > 1) {
          this.cartStore.updateQuantity(item.id, item.quantity - 1)
        }
      },
      removeItem(item) {
        this.cartStore.removeItem(item.id)
      },
    }
  }
  </script>