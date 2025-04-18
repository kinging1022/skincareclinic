<template>
    <div class="min-h-screen ">
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
  
      <!-- Products Grid -->
      <div class="container mx-auto py-8 px-4 pb-16">
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
          <div v-if="products.length === 0" class="text-center py-16 ">
            <div class="inline-block p-4 rounded-full mb-4">
              <ShoppingBag class="h-8 w-8" />
            </div>
            <p class="text-[#1c3a2e] font-light">No products available in this collections</p>
            
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
          <section class="py-12" v-if="products.length > 0">
            <div class="flex flex-col items-center justify-between gap-6 sm:flex-row">
              <div class="text-sm font-light text-[#4a6b5d]">
                Showing {{ paginationStart }} - {{ paginationEnd }} of {{ products.length }} products
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
    ShoppingBag, 
    Search, 
    Menu, 
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
      ShoppingBag,
      Search,
      Menu,
      ProductCard,
      ChevronRightIcon,
      ChevronLeftIcon,
      ChevronsLeftIcon,
      ChevronsRightIcon
    },
    data() {
      return {
        products: [],
        cartStore: useCartStore(),
        toastStore: useToastStore(),
        loading: false,
        error: null,
        currentPage: 1,
        itemsPerPage: 12,
        bannerBgImage: 'https://via.placeholder.com/1920x1080/0a5c3e/ffffff?text=Skincare+Hero+Image'
      }
    },
    mounted() {
      this.getProducts()
    },
    computed: {
      bannerText() {
        const collectionName = this.$route.params.collections_name;
        return collectionName;
      },
      paginatedProducts() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.products.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.products.length / this.itemsPerPage);
      },
      paginationStart() {
        return (this.currentPage - 1) * this.itemsPerPage + 1;
      },
      paginationEnd() {
        return Math.min(this.currentPage * this.itemsPerPage, this.products.length);
      },
      visiblePageNumbers() {
        const pages = []
        const totalDisplayPages = 5 // Number of page numbers to show
        
        if (this.totalPages <= totalDisplayPages) {
          // If total pages is less than or equal to total display pages, show all pages
          for (let i = 1; i <= this.totalPages; i++) {
            pages.push(i)
          }
        } else {
          // Always show first page
          pages.push(1)
          
          let startPage = Math.max(2, this.currentPage - 1)
          let endPage = Math.min(this.totalPages - 1, this.currentPage + 1)
          
          // Adjust if at boundaries
          if (this.currentPage <= 2) {
            endPage = 4
          } else if (this.currentPage >= this.totalPages - 1) {
            startPage = this.totalPages - 3
          }
          
          // Add ellipsis after first page if needed
          if (startPage > 2) {
            pages.push('...')
          }
          
          // Add internal pages
          for (let i = startPage; i <= endPage; i++) {
            pages.push(i)
          }
          
          // Add ellipsis before last page if needed
          if (endPage < this.totalPages - 1) {
            pages.push('...')
          }
          
          // Always show last page
          pages.push(this.totalPages)
        }
        
        return pages
      }
    },
    methods: {
      async getProducts() {
        this.loading = true;
        this.error = null;
        try {
          const response = await axios.get('api/shop/products/', {
            params: {
              collection: this.$route.params.slug
            }
          })
        this.products = response.data
        } catch (error) {
          console.error(error)
          this.error = "Failed to load products. Please try again."
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