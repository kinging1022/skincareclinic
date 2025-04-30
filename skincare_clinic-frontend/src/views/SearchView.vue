<template>
  <div class="min-h-screen bg-[#f0f5f1]">
    <header class="w-full bg-white shadow-sm sticky top-0 z-10 border-b border-[#d7e5dc]">
      <div class="container px-4 py-4">
        <div class="relative my-4">
          <input
            type="text"
            placeholder="Search for skincare products..."
            class="w-full px-4 py-3 pr-12 rounded-lg border border-[#d7e5dc] bg-white focus:outline-none focus:ring-2 focus:ring-[#0a5c3e] focus:border-transparent text-[#1c3a2e] placeholder-[#4a6b5d]"
            v-model="searchQuery"
            @input="handleSearchInput"
            @keyup.enter="executeSearch"
          />
          <Search 
            class="absolute right-4 top-1/2 transform -translate-y-1/2 text-[#0a5c3e] w-5 h-5" 
            @click="executeSearch"
          />
        </div>
      </div>
    </header>
    
    <main class="container px-4 py-6">
      <!-- Search Results -->
      <div v-if="searchedProducts.length" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
        <div v-for="product in paginatedProducts" :key="product.id" class="group">
          <ProductCard
              :product="product"
              :add-to-cart="() => addToCart(product)"
            />
        </div>
      </div>

      <!-- Pagination -->
      <Pagination
        v-if="searchedProducts.length > 0"
        :current-page="currentPage"
        :items-per-page="itemsPerPage"
        :total-items="searchedProducts.length"
        @page-change="handlePageChange"
        @items-per-page-change="handleItemsPerPageChange"
      />

      <!-- Empty States -->
      <div v-else-if="error" class="text-center text-red-500">
        {{ error }}
      </div>
      <div v-else-if="searchQuery && !isLoading" class="text-center text-[#4a6b5d]">
        No products found for "{{ searchQuery }}"
      </div>
      <div v-else-if="isLoading" class="flex justify-center">
        <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#0a5c3e]"></div>
      </div>
      <div v-else class="text-center text-[#4a6b5d]">
        Start typing to search our skincare collection
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, computed, onBeforeUnmount } from 'vue'
import { Search } from 'lucide-vue-next'
import { useCartStore } from '@/stores/cart'
import ProductCard from '@/components/ProductCard.vue'
import Pagination from '@/components/Pagination.vue'
import axios from 'axios'

const cartStore = useCartStore()

// Reactive state
const searchQuery = ref('')
const searchedProducts = ref([])
const error = ref(null)
const isLoading = ref(false)
const debounceTimeout = ref(null)
const currentPage = ref(1)
const itemsPerPage = ref(12)

// Computed property for paginated products
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return searchedProducts.value.slice(start, end)
})

// Methods
const getSearchedProducts = async () => {
  if (searchQuery.value.trim() === '') {
    searchedProducts.value = []
    error.value = null
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const response = await axios.get('/api/shop/search', {
      params: { query: searchQuery.value }
    })
    searchedProducts.value = response.data
    currentPage.value = 1 // Reset to first page on new search
  } catch (err) {
    console.error('Search error:', err)
    error.value = err.response?.data?.message || 'An error occurred while searching. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  window.scrollTo({
    top: document.querySelector('.container').offsetTop - 100,
    behavior: 'smooth'
  })
}

const handleItemsPerPageChange = (value) => {
  itemsPerPage.value = value
  currentPage.value = 1
}

const debounceSearch = () => {
  clearTimeout(debounceTimeout.value)
  debounceTimeout.value = setTimeout(() => {
    getSearchedProducts()
  }, 300)
}

const executeSearch = () => {
  clearTimeout(debounceTimeout.value)
  getSearchedProducts()
}

const handleSearchInput = () => {
  debounceSearch()
}

const addToCart = (product) => {
  cartStore.addItem(product)
}

// Watcher for search query changes
watch(searchQuery, (newValue) => {
  if (newValue.trim() === '') {
    searchedProducts.value = []
    error.value = null
  }
})

// Cleanup
onBeforeUnmount(() => {
  clearTimeout(debounceTimeout.value)
})
</script>

<style scoped>
.container {
  @apply max-w-7xl mx-auto;
}
</style>