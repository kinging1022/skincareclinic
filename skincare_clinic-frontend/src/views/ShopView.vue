<template>
  <div class="min-h-screen">
    <!-- Hero Banner -->
    <div v-if="bannerText" class="relative overflow-hidden">
      <div 
        class="py-12 relative z-10 text-white"
        :style="{
          backgroundImage: 'linear-gradient(rgba(10, 60, 40, 0.65), rgba(10, 60, 40, 0.65)), url(' + bannerBgImage + ')'
        }"
      >
        <div class="container mx-auto px-4 text-center">
          <h2 class="text-3xl md:text-4xl font-light tracking-wide mb-3">{{ bannerText }}</h2>
          <p class="max-w-2xl mx-auto text-base font-light md:text-lg">Discover our collection of premium skincare products</p>
        </div>
      </div>
    </div>

    <!-- Filters Section -->
    <section class="py-8 md:py-12 bg-white">
      <div class="container mx-auto px-4 md:px-6">
        <div class="mb-6 md:mb-8 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
          <h2 class="text-2xl font-medium tracking-wider text-[#1c3a2e] md:text-3xl">Discover Our Collection</h2>
          
          <div class="flex items-center gap-3 sm:ml-auto">
            <div class="hidden md:block h-10 w-[1px] bg-[#d7e5dc]"></div>
            <div class="flex items-center">
              <span class="text-[#1c3a2e] text-sm md:text-base font-light italic mr-2">Refine your selection</span>
              <button 
                class="rounded-full border border-[#d7e5dc] hover:bg-[#e3efe7] hover:border-[#0a5c3e] p-2 transition-all duration-300 group"
                @click="toggleFilters"
              >
                <filter-icon class="h-4 w-4 text-[#1c3a2e] group-hover:text-[#0a5c3e]" />
              </button>
              <span class="ml-2 text-[#0a5c3e] text-sm font-medium">
                {{ showFilters ? 'Hide' : 'Show' }} Filters
              </span>
            </div>
          </div>
        </div>

        <div 
          class="mb-6 md:mb-8 bg-[#f0f5f1] p-4 md:p-6 border border-[#d7e5dc] transition-all duration-300"
          :class="{ 'hidden': !showFilters }"
        >
          <!-- Mobile layout -->
          <div class="md:hidden">
            <div class="grid grid-cols-2 gap-3">
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium text-[#4a6b5d]">Brand</label>
                <select
                  v-model="filters.brand"
                  class="rounded-none border border-[#d7e5dc] bg-white px-2 py-2 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-xs"
                >
                  <option value="">All Brands</option>
                  <option v-for="brand in brands" :key="brand.id" :value="brand.slug">{{ brand.name }}</option>
                </select>
              </div>
              
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium text-[#4a6b5d]">Category</label>
                <select
                  v-model="filters.category"
                  class="rounded-none border border-[#d7e5dc] bg-white px-2 py-2 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-xs"
                >
                  <option value="">All Categories</option>
                  <option v-for="category in categories" :key="category.id" :value="category.slug">{{ category.name }}</option>
                </select>
              </div>
              
              <div class="flex flex-col gap-1 col-span-2">
                <label class="text-xs font-medium text-[#4a6b5d]">Price Range</label>
                <div class="flex items-center gap-1">
                  <input
                    v-model.number="filters.minPrice"
                    type="number"
                    placeholder="Min"
                    class="rounded-none border border-[#d7e5dc] bg-white px-2 py-2 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-xs w-full"
                  />
                  <span class="text-[#4a6b5d] text-xs">—</span>
                  <input
                    v-model.number="filters.maxPrice"
                    type="number"
                    placeholder="Max"
                    class="rounded-none border border-[#d7e5dc] bg-white px-2 py-2 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-xs w-full"
                  />
                </div>
              </div>
              
              <div class="flex flex-col gap-1 col-span-2">
                <label class="text-xs font-medium text-[#4a6b5d]">Sort By</label>
                <select
                  v-model="sortBy"
                  class="rounded-none border border-[#d7e5dc] bg-white px-2 py-2 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-xs"
                >
                  <option value="featured">Featured</option>
                  <option value="priceLowToHigh">Price: Low to High</option>
                  <option value="priceHighToLow">Price: High to Low</option>
                  <option value="alphabetical">Alphabetical</option>
                </select>
              </div>
            </div>
            
            <div class="mt-4 flex justify-between gap-2">
              <button 
                @click="resetFilters" 
                class="rounded-none border border-[#0a5c3e] px-3 py-2 text-[#0a5c3e] hover:bg-[#e3efe7] text-xs font-medium tracking-wider flex-1"
              >
                Reset
              </button>
              <button 
                @click="applyFilters" 
                class="rounded-none bg-[#0a5c3e] px-3 py-2 text-white hover:bg-[#0b4a33] text-xs font-medium tracking-wider flex-1"
              >
                Apply
              </button>
            </div>
          </div>
          
          <!-- Desktop layout -->
          <div class="hidden md:block">
            <div class="flex flex-wrap items-center justify-between gap-6">
              <div class="flex flex-wrap gap-4">
                <div class="flex flex-col gap-2">
                  <label class="text-sm font-medium text-[#4a6b5d]">Brand</label>
                  <select
                    v-model="filters.brand"
                    class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-sm min-w-[180px]"
                  >
                    <option value="">All Brands</option>
                    <option v-for="brand in brands" :key="brand.id" :value="brand.slug">{{ brand.name }}</option>
                  </select>
                </div>
                
                <div class="flex flex-col gap-2">
                  <label class="text-sm font-medium text-[#4a6b5d]">Category</label>
                  <select
                    v-model="filters.category"
                    class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-sm min-w-[180px]"
                  >
                    <option value="">All Categories</option>
                    <option v-for="category in categories" :key="category.id" :value="category.slug">{{ category.name }}</option>
                  </select>
                </div>
                
                <div class="flex flex-col gap-2">
                  <label class="text-sm font-medium text-[#4a6b5d]">Price Range</label>
                  <div class="flex items-center gap-2">
                    <input
                      v-model.number="filters.minPrice"
                      type="number"
                      placeholder="Min"
                      class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-sm w-24"
                    />
                    <span class="text-[#4a6b5d]">—</span>
                    <input
                      v-model.number="filters.maxPrice"
                      type="number"
                      placeholder="Max"
                      class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-sm w-24"
                    />
                  </div>
                </div>
              </div>
              
              <div class="flex flex-col gap-2">
                <label class="text-sm font-medium text-[#4a6b5d]">Sort By</label>
                <select
                  v-model="sortBy"
                  class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-sm min-w-[180px]"
                >
                  <option value="featured">Featured</option>
                  <option value="priceLowToHigh">Price: Low to High</option>
                  <option value="priceHighToLow">Price: High to Low</option>
                  <option value="alphabetical">Alphabetical</option>
                </select>
              </div>
            </div>
            
            <div class="mt-6 flex justify-end">
              <button 
                @click="resetFilters" 
                class="rounded-none border border-[#0a5c3e] px-6 py-3 text-[#0a5c3e] hover:bg-[#e3efe7] text-sm font-medium tracking-wider mr-4"
              >
                Reset
              </button>
              <button 
                @click="applyFilters" 
                class="rounded-none bg-[#0a5c3e] px-6 py-3 text-white hover:bg-[#0b4a33] text-sm font-medium tracking-wider"
              >
                Apply Filters
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Products Grid -->
    <div class="container mx-auto px-4 pb-16">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-[#0a5c3e] border-r-4 border-[#0a5c3e] border-b-4 border-[#0a5c3e] border-l-4 border-[#d7e5dc]"></div>
        <p class="mt-6 text-lg text-[#4a6b5d] font-light">Loading products...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="text-center py-16 bg-red-50 rounded-none border border-red-100">
        <div class="inline-block p-4 rounded-full bg-red-100 text-red-500 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <p class="text-red-600 font-medium">{{ error }}</p>
        <button @click="getProducts" class="mt-4 px-6 py-3 bg-red-500 text-white rounded-none hover:bg-red-600 transition-colors font-light tracking-wider">
          Try Again
        </button>
      </div>
      
      <!-- Products Grid -->
      <div v-else>
        <!-- Empty State -->
        <div v-if="sortedProducts.length === 0" class="text-center py-16">
          <div class="inline-block p-4 rounded-full mb-4">
            <ShoppingBag class="h-8 w-8" />
          </div>
          <p class="text-[#1c3a2e] font-light">No products found matching your criteria</p>
          <button @click="resetFilters" class="mt-4 px-6 py-3 bg-[#0a5c3e] text-white rounded-none hover:bg-[#0b4a33] transition-colors font-light tracking-wider">
            Reset Filters
          </button>
        </div>
        
        <!-- Products Grid -->
        <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          <div v-for="product in paginatedProducts" :key="product.id" class="product-item">
            <ProductCard
              :product="product"
              :add-to-cart="addToCart"
            />
          </div>
        </div>
        
        <!-- Pagination Component -->
        <Pagination
          v-if="sortedProducts.length > 0"
          :current-page="currentPage"
          :items-per-page="itemsPerPage"
          :total-items="sortedProducts.length"
          @page-change="handlePageChange"
          @items-per-page-change="handleItemsPerPageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  Filter as FilterIcon, 
  ShoppingBag
} from 'lucide-vue-next'
import { useCartStore } from '@/stores/cart'
import { useToastStore } from '@/stores/toast'
import ProductCard from '@/components/ProductCard.vue'
import Pagination from '@/components/Pagination.vue'
import axios from 'axios'

// Reactive state
const products = ref([])
const brands = ref([])
const categories = ref([])
const loading = ref(false)
const error = ref(null)
const showFilters = ref(true)
const currentPage = ref(1)
const itemsPerPage = ref(12)
const sortBy = ref('featured')
const bannerBgImage = ref('https://via.placeholder.com/1920x1080/0a5c3e/ffffff?text=Skincare+Hero+Image')

const filters = ref({
  brand: '',
  category: '',
  minPrice: null,
  maxPrice: null
})

// Stores
const cartStore = useCartStore()
const toastStore = useToastStore()

// Computed properties
const bannerText = computed(() => {
  if (filters.value.category && filters.value.brand) {
    const brand = brands.value.find(b => b.slug === filters.value.brand)
    const category = categories.value.find(c => c.slug === filters.value.category)
    return `${brand ? brand.name : ''} - ${category ? category.name : ''}`
  } else if (filters.value.category) {
    const category = categories.value.find(c => c.slug === filters.value.category)
    return category ? category.name : ''
  } else if (filters.value.brand) {
    const brand = brands.value.find(b => b.slug === filters.value.brand)
    return brand ? brand.name : ''
  }
  return 'Shop Our Collection'
})

const sortedProducts = computed(() => {
  let sorted = [...products.value]
  switch (sortBy.value) {
    case 'priceLowToHigh':
      sorted.sort((a, b) => a.price - b.price)
      break
    case 'priceHighToLow':
      sorted.sort((a, b) => b.price - a.price)
      break
    case 'alphabetical':
      sorted.sort((a, b) => a.name.localeCompare(b.name))
      break
    default:
      break
  }
  return sorted
})

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return sortedProducts.value.slice(start, end)
})

// Methods
const toggleFilters = () => {
  showFilters.value = !showFilters.value
}

const getProducts = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('api/shop/products/')
    products.value = response.data
  } catch (err) {
    console.error(err)
    error.value = "Failed to load products. Please try again."
  } finally {
    loading.value = false
  }
}

const getBrands = async () => {
  try {
    const response = await axios.get('api/shop/brands/')
    brands.value = response.data
  } catch (err) {
    console.error(err)
  }
}

const getCategories = async () => {
  try {
    const response = await axios.get('api/shop/categories/')
    categories.value = response.data
  } catch (err) {
    console.error(err)
  }
}

const applyFilters = async () => {
  loading.value = true
  error.value = null
  currentPage.value = 1
  try {
    const response = await axios.get('api/shop/filter_products/', {
      params: {
        ...filters.value,
        minPrice: filters.value.minPrice || undefined,
        maxPrice: filters.value.maxPrice || undefined
      }
    })
    products.value = response.data
  } catch (err) {
    console.error(err)
    error.value = "Failed to update products. Please try again."
  } finally {
    loading.value = false
  }
}

const addToCart = (product) => {
  cartStore.addItem(product)
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

const resetFilters = () => {
  filters.value = {
    brand: '',
    category: '',
    minPrice: null,
    maxPrice: null
  }
  sortBy.value = 'featured'
  currentPage.value = 1
  getProducts()
}

// Lifecycle hooks
onMounted(() => {
  getProducts()
  getBrands()
  getCategories()
})
</script>

<style scoped>
.product-item {
  transition: transform 0.3s ease;
  will-change: transform;
}

.product-item:hover {
  transform: translateY(-5px);
}

/* Improve loading spinner */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* CLS improvements */
[class*="min-h-"] {
  content-visibility: auto;
}

/* Optimize transitions */
.transform {
  will-change: transform;
}

/* Performance optimizations */
.container {
  content-visibility: auto;
}
</style>