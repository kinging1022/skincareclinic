<template>
    <div class="min-h-screen bg-white">
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
        <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          <div v-for="product in sortedProducts" :key="product.id" class="group">
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
              <span class="text-[#2E8B57] font-bold">${{ product.price.toFixed(2) }}</span>
              <button @click="addToCart(product)" 
                class="text-sm px-3 py-1 bg-[#2E8B57] text-white rounded-full hover:bg-[#267346] transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed md:flex md:items-center md:space-x-1"
                :disabled="product.stock === 0"
              >
                <span class="hidden md:inline">{{ product.stock > 0 ? 'Add to Cart' : 'Out of Stock' }}</span>
                <ShoppingCartIcon class="h-4 w-4 md:ml-1" />
              </button>
            </div>
            <p class="text-sm text-gray-600 mt-2">
              {{ product.stock > 0 ? `${product.stock} left in stock` : 'Out of stock' }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { useCartStore } from '@/stores/cart';
  import { useToastStore } from '@/stores/toast';
  import { Filter, ShoppingBag, Search, Menu, ShoppingCart } from 'lucide-vue-next'
  import axios from 'axios';
  
  export default {
    name: 'ShopPage',
    components: {
      Filter,
      ShoppingBag,
      Search,
      Menu,
      ShoppingCartIcon: ShoppingCart
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
        error: null
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
      }
    },
    watch: {
      filters: {
        handler: 'updateProducts',
        deep: true
      }
    },
    methods: {
      async getProducts() {
        this.loading = true;
        this.error = null;
        try {
          const response = await axios.get('api/products/')
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
          const response = await axios.get('api/brands/')
          this.brands = response.data
        } catch (error) {
          console.error(error)
        }
      },
      async getCategories() {
        try {
          const response = await axios.get('api/categories/')
          this.categories = response.data
        } catch (error) {
          console.error(error)
        }
      },
      async updateProducts() {
        this.loading = true;
        this.error = null;
        try {
          const response = await axios.get('api/filter_products/', {
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
      }
    }
  }
  </script>
  
  