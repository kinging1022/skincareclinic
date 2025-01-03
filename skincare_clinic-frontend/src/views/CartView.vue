<template>
    <div class="min-h-screen bg-gray-100">
      <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold text-[#2E8B57] mb-8">Your Cart</h1>
        <div v-if="cart.length === 0" class="text-center py-16">
          <ShoppingCart class="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p class="text-xl text-gray-600">Your cart is empty</p>
          <router-link to="/" class="mt-4 inline-block px-6 py-2 bg-[#2E8B57] text-white rounded-full hover:bg-[#267346] transition-colors">
            Continue Shopping
          </router-link>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="md:col-span-2">
            <div v-for="item in cart" :key="item.id" class="bg-white rounded-lg shadow-md p-6 mb-4">
              <div class="flex items-center">
                <img :src="item.image" :alt="item.name" class="w-20 h-20 object-cover rounded-md mr-4" />
                <div class="flex-grow">
                  <h2 class="text-lg font-semibold text-[#2F4F4F]">{{ item.name }}</h2>
                  <p class="text-gray-600">{{ item.description }}</p>
                  <div class="mt-2 flex items-center">
                    <button @click="decreaseQuantity(item)" class="text-gray-500 hover:text-[#2E8B57] focus:outline-none">
                      <Minus class="w-5 h-5" />
                    </button>
                    <span class="mx-2 w-8 text-center">{{ item.quantity }}</span>
                    <button @click="increaseQuantity(item)" class="text-gray-500 hover:text-[#2E8B57] focus:outline-none">
                      <Plus class="w-5 h-5" />
                    </button>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-lg font-bold text-[#2E8B57]">${{ (item.price * item.quantity).toFixed(2) }}</p>
                  <button @click="removeItem(item)" class="mt-2 text-red-500 hover:text-red-700 focus:outline-none">
                    <Trash2 class="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="md:col-span-1">
            <div class="bg-white rounded-lg shadow-md p-6">
              <h2 class="text-xl font-semibold text-[#2F4F4F] mb-4">Order Summary</h2>
              <div class="flex justify-between mb-2">
                <span>Subtotal</span>
                <span>${{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between mb-2">
                <span>Shipping</span>
                <span>$5.00</span>
              </div>
              <div class="flex justify-between mb-2">
                <span>Tax</span>
                <span>${{ tax.toFixed(2) }}</span>
              </div>
              <div class="border-t pt-2 mt-2">
                <div class="flex justify-between">
                  <span class="font-semibold">Total</span>
                  <span class="font-semibold">${{ total.toFixed(2) }}</span>
                </div>
              </div>
              <button @click="checkout" class="w-full mt-6 px-6 py-3 bg-[#2E8B57] text-white rounded-full hover:bg-[#267346] transition-colors">
                Proceed to Checkout
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ShoppingCart, Minus, Plus, Trash2 } from 'lucide-vue-next'
  
  export default {
    name: 'Cart',
    components: {
      ShoppingCart,
      Minus,
      Plus,
      Trash2
    },
    data() {
      return {
        cart: [
          {
            id: 1,
            name: "Hydrating Serum",
            price: 49.99,
            image: "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3",
            description: "Deep hydration for all skin types",
            quantity: 2
          },
          {
            id: 2,
            name: "Vitamin C Cream",
            price: 39.99,
            image: "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3",
            description: "Brightening daily moisturizer",
            quantity: 1
          }
        ]
      }
    },
    computed: {
      subtotal() {
        return this.cart.reduce((total, item) => total + item.price * item.quantity, 0)
      },
      tax() {
        return this.subtotal * 0.08 // Assuming 8% tax rate
      },
      total() {
        return this.subtotal + this.tax + 5 // Adding $5 for shipping
      }
    },
    methods: {
      increaseQuantity(item) {
        item.quantity++
      },
      decreaseQuantity(item) {
        if (item.quantity > 1) {
          item.quantity--
        }
      },
      removeItem(item) {
        const index = this.cart.findIndex(cartItem => cartItem.id === item.id)
        if (index !== -1) {
          this.cart.splice(index, 1)
        }
      },
      checkout() {
        // Implement checkout logic here
        alert('Proceeding to checkout...')
      }
    }
  }
  </script>