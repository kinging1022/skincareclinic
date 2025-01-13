<template>
  <div class="min-h-screen bg-emerald-50">
    <div v-if="bannerText" class="bg-[#F5FFFA] py-8">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold text-[#2F4F4F] mb-2">{{ bannerText }}</h2>
        <p class="text-gray-600">Discover our collection of premium skincare products</p>
      </div>
    </div>
    <div class="container mx-auto px-4 py-6">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div class="flex flex-wrap gap-4">
          <select v-model="filters.brand" class="px-4 py-2 border border-gray-200 rounded-lg text-gray-600 focus:outline-none focus:border-[#2E8B57]">
            <option value="">All Brands</option>
            <option v-for="brand in brands" :key="brand.id" :value="brand.slug">{{ brand.name }}</option>
          </select>
          <select v-model="filters.category" class="px-4 py-2 border border-gray-200 rounded-lg text-gray-600 focus:outline-none focus:border-[#2E8B57]">
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category.id" :value="category.slug">{{ category.name }}</option>
          </select>
          <div class="flex items-center space-x-2">
            <input v-model.number="filters.minPrice" type="number" placeholder="Min Price" class="w-24 px-2 py-2 border border-gray-200 rounded-lg text-gray-600 focus:outline-none focus:border-[#2E8B57]" />
            <span>-</span>
            <input v-model.number="filters.maxPrice" type="number" placeholder="Max Price" class="w-24 px-2 py-2 border border-gray-200 rounded-lg text-gray-600 focus:outline-none focus:border-[#2E8B57]" />
          </div>
        </div>
        <select v-model="sortBy" class="px-4 py-2 border border-gray-200 rounded-lg text-gray-600 focus:outline-none focus:border-[#2E8B57]">
          <option value="featured">Sort by: Featured</option>
          <option value="priceLowToHigh">Price: Low to High</option>
          <option value="priceHighToLow">Price: High to Low</option>
          <option value="alphabetical">Alphabetical Order</option>
        </select>
      </div>
    </div>
    <div class="container mx-auto px-4 py-8">
      <div v-if="loading" class="text-center py-16">
        <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-emerald-600 mx-auto"></div>
        <p class="mt-4 text-lg text-gray-600">Loading products...</p>
      </div>
      <div v-else-if="error" class="text-center py-16">
        <p class="text-red-500">{{ error }}</p>
      </div>
      <div v-else>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          <div v-for="product in paginatedProducts" :key="product.id" class="group">
            <ProductCard
              :product="product"
              :add-to-cart="addToCart"
            />
          </div>
        </div>
        
        <!-- Pagination controls -->
        <div class="mt-8 flex justify-center items-center space-x-4">
          <button 
            @click="changePage(currentPage - 1)" 
            :disabled="currentPage === 1"
            class="px-4 py-2 bg-emerald-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Previous page"
          >
            Previous
          </button>
          <span class="text-gray-600">Page {{ currentPage }} of {{ totalPages }}</span>
          <button 
            @click="changePage(currentPage + 1)" 
            :disabled="currentPage === totalPages"
            class="px-4 py-2 bg-emerald-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Next page"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useCartStore } from '@/stores/cart';
import { useToastStore } from '@/stores/toast';
import { Filter, ShoppingBag, Search, Menu } from 'lucide-vue-next'
import ProductCard from '@/components/ProductCard.vue';
import axios from 'axios';

export default {
  name: 'ShopPage',
  components: {
    Filter,
    ShoppingBag,
    Search,
    Menu,
    ProductCard
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
      itemsPerPage: 12
    }
  },
  mounted() {
    this.getProducts()
    this.getBrands()
    this.getCategories()
  },
  computed: {
    bannerText() {
      if (this.filters.category && this.filters.brand) {
        const brand = this.brands.find(b => b.slug === this.filters.brand)
        const category = this.categories.find(c => c.slug === this.filters.category)
        return `${brand ? brand.name : ''} - ${category ? category.name : ''}`;
      } else if (this.filters.category) {
        const category = this.categories.find(c => c.slug === this.filters.category)
        return category ? category.name : '';
      } else if (this.filters.brand) {
        const brand = this.brands.find(b => b.slug === this.filters.brand)
        return brand ? brand.name : '';
      }
      return '';
    },
    sortedProducts() {
      let sorted = [...this.products];
      switch (this.sortBy) {
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
      return sorted;
    },
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedProducts.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.sortedProducts.length / this.itemsPerPage);
    }
  },
  watch: {
    filters: {
      handler: 'updateProducts',
      deep: true
    },
    sortBy() {
      this.currentPage = 1;
    }
  },
  methods: {
    async getProducts() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get('api/shop/products/')
        this.products = response.data
      } catch (error) {
        console.error(error)
        this.error = "Failed to load products. Please try again."
      } finally {
        this.loading = false;
      }
    },
    async getBrands() {
      try {
        const response = await axios.get('api/shop/brands/')
        this.brands = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async getCategories() {
      try {
        const response = await axios.get('api/shop/categories/')
        this.categories = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async updateProducts() {
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
        })
        this.products = response.data
      } catch (error) {
        console.error(error)
        this.error = "Failed to update products. Please try again."
      } finally {
        this.loading = false;
      }
    },
    addToCart(product) {
      this.cartStore.addItem(product);
      const brandName = product.brand?.name || " "; 
      const message = `Added ${brandName} ${product.name} to cart`;
      this.toastStore.showToast(5000, message, "bg-emerald-500");
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    }
  }
}
</script>