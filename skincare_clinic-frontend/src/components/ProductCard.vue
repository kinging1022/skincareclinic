<template>
  <div>
    <div class="relative overflow-hidden rounded-lg mb-3">
        <img
        :src="product.get_thumbnail"
        :alt="product.name"
        class="w-full h-64 object-cover transform group-hover:scale-105 transition-transform duration-300"
        />
    </div>
    <RouterLink :to="{name:'product-detail', params:{slug:product.slug}}">
        <h3 class="text-[#2F4F4F] font-semibold mb-1 h-6">
        {{ product.brand ? product.brand.name : ' ' }}
        </h3>
        <p class="text-gray-500 text-sm mb-2">{{ product.name }}</p>
    </RouterLink>
    <div class="flex items-center justify-between">
        <span class="text-[#2E8B57] font-bold">${{ product.price.toLocaleString() }}</span>
        <button @click="addToCart(product)" 
        class="text-sm px-3 py-1 bg-[#2E8B57] text-white rounded-full hover:bg-[#267346] transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed md:flex md:items-center md:space-x-1"
        :disabled="product.stock === 0"
        >
        <span class="hidden md:inline">{{ product.stock > 0 ? 'Add to Cart' : 'Out of Stock' }}</span>
        <ShoppingCartIcon class="h-4 w-4 md:ml-1" />
        </button>
    </div>
   <!-- <p class="text-sm text-gray-600 mt-2">
        {{ product.stock > 0 ? `${product.stock} left in stock` : 'Out of stock' }}
    </p>-->
  </div>
</template>
  
  <script>
  import { Star,ShoppingCartIcon } from 'lucide-vue-next'
  
  export default {
    name: 'ProductCard',
    components: {
      Star,
      ShoppingCartIcon
    },
    props: {
      product: {
        type: Object, 
        required: true
      },
      addToCart: {
        type: Function,
        required: true
      },
      
    }
  }
  </script>
  
  