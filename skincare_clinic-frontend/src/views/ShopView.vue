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
          
          <!-- Restyled filter explanation -->
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

    <!-- Rest of the component remains unchanged -->
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
        
        <!-- Pagination Section -->
        <section class="py-12" v-if="sortedProducts.length > 0">
          <div class="flex flex-col items-center justify-between gap-6 sm:flex-row">
            <div class="text-sm font-light text-[#4a6b5d]">
              Showing {{ paginationStart }} - {{ paginationEnd }} of {{ sortedProducts.length }} products
            </div>
            
            <div class="flex items-center gap-3">
              <button
                @click="changePage(1)"
                :disabled="currentPage === 1"
                class="rounded-none border border-[#d7e5dc] p-2 text-[#1c3a2e] hover:bg-[#e3efe7] hover:border-[#0a5c3e] disabled:opacity-50 disabled:cursor-not-allowed"
                aria-label="First page"
              >
                <chevrons-left-icon class="h-4 w-4" />
              </button>
              
              <button
                @click="changePage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="rounded-none border border-[#d7e5dc] p-2 text-[#1c3a2e] hover:bg-[#e3efe7] hover:border-[#0a5c3e] disabled:opacity-50 disabled:cursor-not-allowed"
                aria-label="Previous page"
              >
                <chevron-left-icon class="h-4 w-4" />
              </button>
              
              <div class="flex items-center gap-2">
                <div v-for="page in visiblePageNumbers" :key="page" class="flex items-center">
                  <button
                    v-if="page !== '...'"
                    @click="changePage(page)"
                    :class="[
                      'h-8 w-8 flex items-center justify-center text-sm font-light',
                      currentPage === page 
                        ? 'bg-[#0a5c3e] text-white' 
                        : 'border border-[#d7e5dc] text-[#1c3a2e] hover:bg-[#e3efe7] hover:border-[#0a5c3e]'
                    ]"
                  >
                    {{ page }}
                  </button>
                  <span v-else class="px-1 text-[#4a6b5d]">{{ page }}</span>
                </div>
              </div>
              
              <button
                @click="changePage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="rounded-none border border-[#d7e5dc] p-2 text-[#1c3a2e] hover:bg-[#e3efe7] hover:border-[#0a5c3e] disabled:opacity-50 disabled:cursor-not-allowed"
                aria-label="Next page"
              >
                <chevron-right-icon class="h-4 w-4" />
              </button>
              
              <button
                @click="changePage(totalPages)"
                :disabled="currentPage === totalPages"
                class="rounded-none border border-[#d7e5dc] p-2 text-[#1c3a2e] hover:bg-[#e3efe7] hover:border-[#0a5c3e] disabled:opacity-50 disabled:cursor-not-allowed"
                aria-label="Last page"
              >
                <chevrons-right-icon class="h-4 w-4" />
              </button>
            </div>
            
            <div class="flex items-center gap-3">
              <span class="text-sm font-light text-[#4a6b5d]">View</span>
              <select
                v-model="itemsPerPage"
                @change="currentPage = 1"
                class="rounded-none border border-[#d7e5dc] bg-white px-3 py-2 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-sm"
              >
                <option :value="12">12</option>
                <option :value="24">24</option>
                <option :value="36">36</option>
                <option :value="48">48</option>
              </select>
              <span class="text-sm font-light text-[#4a6b5d]">per page</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import { useCartStore } from '@/stores/cart';
import { useToastStore } from '@/stores/toast';
import { 
  Filter as FilterIcon, 
  ShoppingBag, 
  ChevronRight as ChevronRightIcon, 
  ChevronLeft as ChevronLeftIcon, 
  ChevronsLeft as ChevronsLeftIcon, 
  ChevronsRight as ChevronsRightIcon 
} from 'lucide-vue-next'
import ProductCard from '@/components/ProductCard.vue';
import axios from 'axios';

export default {
  name: 'ShopPage',
  components: {
    FilterIcon,
    ShoppingBag,
    ProductCard,
    ChevronRightIcon,
    ChevronLeftIcon,
    ChevronsLeftIcon,
    ChevronsRightIcon
  },
  data() {
    return {
      products: [],
      brands: [],
      categories: [],
      filters: {
        brand: '',
        category: '',
        minPrice: null,
        maxPrice: null
      },
      sortBy: 'featured',
      cartStore: useCartStore(),
      toastStore: useToastStore(),
      loading: false,
      error: null,
      currentPage: 1,
      itemsPerPage: 12,
      showFilters: true,
      bannerBgImage: 'https://via.placeholder.com/1920x1080/0a5c3e/ffffff?text=Skincare+Hero+Image'
    }
  },
  mounted() {
    this.getProducts();
    this.getBrands();
    this.getCategories();
  },
  computed: {
    bannerText() {
      if (this.filters.category && this.filters.brand) {
        const brand = this.brands.find(b => b.slug === this.filters.brand);
        const category = this.categories.find(c => c.slug === this.filters.category);
        return `${brand ? brand.name : ''} - ${category ? category.name : ''}`;
      } else if (this.filters.category) {
        const category = this.categories.find(c => c.slug === this.filters.category);
        return category ? category.name : '';
      } else if (this.filters.brand) {
        const brand = this.brands.find(b => b.slug === this.filters.brand);
        return brand ? brand.name : '';
      }
      return 'Shop Our Collection';
    },
    sortedProducts() {
      let sorted = [...this.products];
      switch (this.sortBy) {
        case 'priceLowToHigh':
          sorted.sort((a, b) => a.price - b.price);
          break;
        case 'priceHighToLow':
          sorted.sort((a, b) => b.price - a.price);
          break;
        case 'alphabetical':
          sorted.sort((a, b) => a.name.localeCompare(b.name));
          break;
        default:
          break;
      }
      return sorted;
    },
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedProducts.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.sortedProducts.length / this.itemsPerPage);
    },
    paginationStart() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    paginationEnd() {
      return Math.min(this.currentPage * this.itemsPerPage, this.sortedProducts.length);
    },
    visiblePageNumbers() {
      const pages = [];
      const totalDisplayPages = 5; // Number of page numbers to show
      
      if (this.totalPages <= totalDisplayPages) {
        // If total pages is less than or equal to total display pages, show all pages
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i);
        }
      } else {
        // Always show first page
        pages.push(1);
        
        let startPage = Math.max(2, this.currentPage - 1);
        let endPage = Math.min(this.totalPages - 1, this.currentPage + 1);
        
        // Adjust if at boundaries
        if (this.currentPage <= 2) {
          endPage = 4;
        } else if (this.currentPage >= this.totalPages - 1) {
          startPage = this.totalPages - 3;
        }
        
        // Add ellipsis after first page if needed
        if (startPage > 2) {
          pages.push('...');
        }
        
        // Add internal pages
        for (let i = startPage; i <= endPage; i++) {
          pages.push(i);
        }
        
        // Add ellipsis before last page if needed
        if (endPage < this.totalPages - 1) {
          pages.push('...');
        }
        
        // Always show last page
        pages.push(this.totalPages);
      }
      
      return pages;
    }
  },
  watch: {
    sortBy() {
      this.currentPage = 1;
    },
    itemsPerPage() {
      this.currentPage = 1;
    }
  },
  methods: {
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    async getProducts() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get('api/shop/products/');
        this.products = response.data;
      } catch (error) {
        console.error(error);
        this.error = "Failed to load products. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    async getBrands() {
      try {
        const response = await axios.get('api/shop/brands/');
        this.brands = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async getCategories() {
      try {
        const response = await axios.get('api/shop/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async applyFilters() {
      this.loading = true;
      this.error = null;
      this.currentPage = 1;
      try {
        const response = await axios.get('api/shop/filter_products/', {
          params: {
            ...this.filters,
            minPrice: this.filters.minPrice || undefined,
            maxPrice: this.filters.maxPrice || undefined
          }
        });
        this.products = response.data;
      } catch (error) {
        console.error(error);
        this.error = "Failed to update products. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    addToCart(product) {
      this.cartStore.addItem(product);
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        // Scroll to top of products section
        window.scrollTo({
          top: document.querySelector('.container').offsetTop - 100,
          behavior: 'smooth'
        });
      }
    },
    resetFilters() {
      this.filters = {
        brand: '',
        category: '',
        minPrice: null,
        maxPrice: null
      };
      this.sortBy = 'featured';
      this.currentPage = 1;
      this.getProducts();
    }
  }
}
</script>

<style scoped>
.product-item {
  transition: transform 0.3s ease;
}

.product-item:hover {
  transform: translateY(-5px);
}

/* Improve scrolling behavior */
html {
  scroll-behavior: smooth;
}

/* Custom focus styles */
button:focus, select:focus, input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(10, 92, 62, 0.4);
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
</style>