<template>
    <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-md relative">
        <button
          @click="$emit('close')"
          class="absolute right-4 top-4 text-gray-500 hover:text-gray-700 transition-colors"
          aria-label="Close modal"
        >
          <X :size="20" />
        </button>
        <div class="p-6">
          <h2 class="text-2xl font-semibold text-emerald-800 mb-2">
            Insufficient Stock
          </h2>
          <p class="text-gray-600 mb-6">
            Some items in your cart have insufficient stock. How would you like
            to proceed?
          </p>
          <div class="space-y-4 mb-6">
            <div
              v-for="product in products"
              :key="product.id"
              class="flex justify-between items-center p-3 bg-emerald-50 rounded-lg"
            >
              <span class="font-medium text-gray-800">
                {{ product.name }}
              </span>
              <span
                :class="[
                  'text-sm',
                  product.stock === 0 ? 'text-red-600 font-semibold' : 'text-emerald-600'
                ]"
              >
                {{ product.stock === 0
                  ? "Out of Stock"
                  : `${product.stock} items remaining`
                }}
              </span>
            </div>
          </div>
          <div class="flex flex-col sm:flex-row gap-3">
            <button
              @click="$emit('update-manually')"
              class="flex-1 px-4 py-2 border border-emerald-600 text-emerald-600 rounded-lg hover:bg-emerald-50 transition-colors"
            >
              Cancel & Update Manually
            </button>
            <button
              @click="$emit('update-automatically')"
              class="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
            >
              Update Cart Automatically
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { X } from 'lucide-vue-next';
  
  export default {
    name: 'InsufficientStockModal',
    components: {
      X,
    },
    props: {
      isOpen: {
        type: Boolean,
        required: true,
      },
      products: {
        type: Array,
        required: true,
        validator: (value) => {
          return value.every(product => 
            typeof product.id === 'number' &&
            typeof product.name === 'string' &&
            typeof product.stock === 'number'
          );
        },
      },
    },
    emits: ['close', 'update-manually', 'update-automatically'],
  };
  </script>
  
  