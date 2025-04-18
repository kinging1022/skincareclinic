<template>
  <div class="product-card group transition-all duration-300 hover:shadow-lg rounded-none overflow-hidden bg-white border border-[#d7e5dc]">
    <!-- Image container -->
    <div class="relative overflow-hidden aspect-square">
      <img
        :src="product.get_thumbnail"
        :alt="product.name"
        class="w-full h-full object-cover transform transition-transform duration-500 group-hover:scale-105"
        loading="lazy"
      />
      
      <!-- Quick View Button -->
      <div class="absolute inset-0 bg-black bg-opacity-20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
        <RouterLink 
          :to="{name:'product-detail', params:{slug:product.slug}}"
          class="bg-white text-[#0a5c3e] px-4 py-2 transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300 text-sm font-medium tracking-wider"
        >
          QUICK VIEW
        </RouterLink>
      </div>
      
      <!-- Stock badge -->
      <div v-if="product.stock <= 5 && product.stock > 0" 
           class="absolute top-2 right-2 bg-amber-500 text-white text-xs px-2 py-1 rounded-none font-medium tracking-wider">
        ONLY {{ product.stock }} LEFT
      </div>
      <div v-else-if="product.stock === 0" 
           class="absolute top-2 right-2 bg-red-500 text-white text-xs px-2 py-1 rounded-none font-medium tracking-wider">
        OUT OF STOCK
      </div>
    </div>
    
    <!-- Content container -->
    <div class="p-4">
      <RouterLink :to="{name:'product-detail', params:{slug:product.slug}}" class="block">
        <h3 v-if="product.brand" class="text-xs font-medium text-[#1c3a2e] uppercase tracking-[0.15em] mb-2">
          {{ product.brand.name }}
        </h3>
        <p class="text-[#1c3a2e] font-medium text-[15px] leading-snug mb-3 line-clamp-2 h-[2.8em]">
          {{ product.name }}
        </p>
        <p class="text-[#0a5c3e] font-medium tracking-wider">₦ {{ product.price.toLocaleString() }}</p>
      </RouterLink>
      
      <div class="mt-4">
        <button 
          @click="addToCart(product)" 
          v-if="product.stock > 0"
          class="w-full py-2.5 border border-[#0a5c3e] text-[#0a5c3e] hover:bg-[#0a5c3e] hover:text-white transition-colors duration-300 text-sm font-medium tracking-wider flex items-center justify-center"
        >
          <ShoppingCartIcon class="h-4 w-4 mr-2" />
          ADD TO CART
        </button>
        <button 
          v-else
          disabled
          class="w-full py-2.5 border border-[#d7e5dc] text-[#4a6b5d] cursor-not-allowed text-sm font-medium tracking-wider flex items-center justify-center"
        >
          OUT OF STOCK
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ShoppingCartIcon } from 'lucide-vue-next'
  
export default {
  name: 'ProductCard',
  components: {
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
    }
  }
}
</script>

<style scoped>
.product-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  will-change: transform;
  contain: content;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(10, 92, 62, 0.08);
}

/* Line clamp for product names */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Text rendering improvements */
h3, p, span, button {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-weight: 500;
}

/* Color classes */
.text-dark-green {
  color: #1c3a2e;
}

.text-primary-green {
  color: #0a5c3e;
}

/* Optimize image loading */
.product-card img {
  backface-visibility: hidden;
  image-rendering: -webkit-optimize-contrast;
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .product-card {
    border-width: 1px;
  }
  
  .product-card p {
    font-size: 15px;
  }
  
  .product-card button {
    font-size: 14px;
    padding: 10px 0;
  }
}
</style>