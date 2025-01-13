<template>
    <div class="min-h-screen ">
      <header class="w-full bg-white shadow-sm sticky top-0 z-10">
        <div class="max-w-7xl mx-auto px-4 py-4">
          <div class="relative my-4">
            <input
              type="text"
              placeholder="Search for skincare products..."
              class="w-full px-4 py-3 pr-12 rounded-lg border border-emerald-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              v-model="searchQuery"
              @input="debounceSearch"
            />
            <Search class="absolute right-4 top-1/2 transform -translate-y-1/2 text-emerald-500 w-5 h-5" />
          </div>
        </div>
      </header>
      <main class="max-w-7xl mx-auto px-4 py-6">
        <div v-if="searchedProducts.length" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
            <div v-for="product in searchedProducts" :key="product.id" class="group">
                <ProductCard
                :product="product"
                />
            </div>

        </div>
        <div v-else-if="error" class="text-center text-red-500">
          {{ error }}
        </div>
        <div v-else-if="searchQuery && !isLoading" class="text-center text-gray-500">
          No products found for "{{ searchQuery }}"
        </div>
        <div v-else-if="isLoading" class="text-center text-gray-500">
          Searching...
        </div>
      </main>
    </div>
  </template>
  
  <script>
  import { Search } from 'lucide-vue-next'
  import ProductCard from '@/components/ProductCard.vue'
  import axios from 'axios'
  
  export default {
    components: {
      Search,
      ProductCard
    },
    data() {
      return {
        searchQuery: '',
        searchedProducts: [],
        error: null,
        isLoading: false,
        debounceTimeout: null
      }
    },
    methods: {
      async getSearchedProducts() {
        if (this.searchQuery.trim() === '') {
          this.searchedProducts = []
          this.error = null
          return
        }
  
        this.isLoading = true
        this.error = null
  
        try {
          const response = await axios.get('api/shop/search', {
            params: {
              query: this.searchQuery
            }
          })
          this.searchedProducts = response.data
        } catch (err) {
          console.error(err)
          this.error = 'An error occurred while searching. Please try again.'
        } finally {
          this.isLoading = false
        }
      },
      debounceSearch() {
        clearTimeout(this.debounceTimeout)
        this.debounceTimeout = setTimeout(() => {
          this.getSearchedProducts()
        }, 300)
      }
    },
    watch: {
      searchQuery(newValue) {
        if (newValue.trim() === '') {
          this.searchedProducts = []
          this.error = null
        }
      }
    },
    beforeUnmount() {
      clearTimeout(this.debounceTimeout)
    }
  }
  </script>