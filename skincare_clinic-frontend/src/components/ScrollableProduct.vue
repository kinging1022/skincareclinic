<template>
  <section class="bg-white">
    <div class="container px-4 md:px-6 py-16">
      <div class="mb-8 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center min-h-[40px]">
        <h2 class="text-2xl font-light tracking-wider text-[#1c3a2e] md:text-3xl">{{ title }}</h2>
        <div class="flex w-full flex-col gap-4 sm:w-auto sm:flex-row sm:items-center">
          <div class="flex gap-2 self-end sm:self-auto">
            <button
              class="rounded-full border border-[#d7e5dc] hover:bg-[#e3efe7] hover:border-[#0a5c3e] p-2 transition-colors duration-200"
              @click="scroll('left')"
              aria-label="Scroll left"
            >
              <ChevronLeftIcon class="h-4 w-4 text-[#1c3a2e]" />
            </button>
            <button
              class="rounded-full border border-[#d7e5dc] hover:bg-[#e3efe7] hover:border-[#0a5c3e] p-2 transition-colors duration-200"
              @click="scroll('right')"
              aria-label="Scroll right"
            >
              <ChevronRightIcon class="h-4 w-4 text-[#1c3a2e]" />
            </button>
          </div>
        </div>
      </div>

      <div class="relative">
        <div
          ref="scrollContainer"
          class="overflow-x-auto scrollbar-hide pb-4"
          style="scrollbar-width: none; -ms-overflow-style: none"
        >
          <div class="flex gap-4 w-max">
            <div
              v-for="product in products"
              :key="product.id"
              class="w-[160px] sm:w-[200px] md:w-[240px] flex-shrink-0"
            >
              <div class="aspect-square mb-4 bg-[#e3efe7] overflow-hidden relative">
                <img
                  :src="product.get_thumbnail"
                  :alt="product.name"
                  loading="lazy"
                  width="240"
                  height="240"
                  class="w-full h-full object-cover transition-opacity duration-300"
                  :class="{ 'opacity-0': !loadedImages[product.id] }"
                  @load="loadedImages[product.id] = true"
                />
                <div v-if="!loadedImages[product.id]" class="absolute inset-0 bg-[#e3efe7] animate-pulse"></div>
              </div>

              <RouterLink 
                :to="{ name: 'product-detail', params: { slug: product.slug } }"
                class="block"
              >
                <h3 class="mb-1 text-base font-medium text-[#1c3a2e] line-clamp-1">{{ product.brand?.name || 'Brand' }}</h3>
                <p class="mb-2 text-sm text-[#0a5c3e] line-clamp-2">{{ product.name }}</p>
                <p class="text-base font-medium text-[#1c3a2e]">₦ {{ product.price.toLocaleString() }}</p>
              </RouterLink>

              <div class="mt-4">
                <button 
                  v-if="product.stock > 0"
                  @click="addToCart(product)"
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
        </div>
      </div>

      <div class="mt-8 flex justify-center" v-if="showViewAll">
        <RouterLink 
          to="/products" 
          class="rounded-none border border-[#0a5c3e] bg-transparent px-8 text-[#0a5c3e] hover:bg-[#e3efe7] text-base py-6 transition-colors duration-300"
        >
          View All Products
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ChevronRight as ChevronRightIcon, ChevronLeft as ChevronLeftIcon, ShoppingCart as ShoppingCartIcon } from 'lucide-vue-next'
import { ref } from 'vue'

const props = defineProps({
  products: {
    type: Array,
    required: true,
    default: () => []
  },
  title: {
    type: String,
    default: 'Bestsellers'
  },
  showViewAll: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['add-to-cart'])
const scrollContainer = ref(null)
const loadedImages = ref({})

// Initialize image loaded states
props.products.forEach(product => {
  loadedImages.value[product.id] = false
})

const scroll = (direction) => {
  if (!scrollContainer.value) return
  const scrollAmount = direction === 'left' ? -300 : 300
  scrollContainer.value.scrollBy({ left: scrollAmount, behavior: 'smooth' })
}

const addToCart = (product) => {
  emit('add-to-cart', product)
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.animate-pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

section {
  contain: content;
}
</style>