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
              <input v-model="filters.minPrice" type="number" placeholder="Min Price" class="w-24 px-2 py-2 border border-gray-200 rounded-lg text-gray-600 focus:outline-none focus:border-[#2E8B57]" />
              <span>-</span>
              <input v-model="filters.maxPrice" type="number" placeholder="Max Price" class="w-24 px-2 py-2 border border-gray-200 rounded-lg text-gray-600 focus:outline-none focus:border-[#2E8B57]" />
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
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          <div v-for="product in products" :key="product.id" class="group">
            <div class="relative overflow-hidden rounded-lg mb-3">
              <img
                :src="product.get_thumbnail"
                :alt="product.name"
                class="w-full h-64 object-cover transform group-hover:scale-105 transition-transform duration-300"
              />
            </div>
            <RouterLink :to="{name:'product-detail', params:{slug:product.slug}}">
            <h3 v-if="product.brand" class="text-[#2F4F4F] font-semibold mb-1">{{ product.brand.name }}</h3>
            <p class="text-gray-500 text-sm mb-2">{{ product.name }}</p>
            </RouterLink>
            <div class="flex items-center justify-between">
              <span class="text-[#2E8B57] font-bold">${{ product.price }}</span>
              <button 
                class="text-sm px-3 py-1 bg-[#2E8B57] text-white rounded-full hover:bg-[#267346] transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
                :disabled="product.stock === 0"
              >
                {{ product.stock > 0 ? 'Add to Cart' : 'Out of Stock' }}
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
  import { Filter, ShoppingBag, Search, Menu } from 'lucide-vue-next'
  import axios from 'axios';
  
  export default {
    name: 'App',
    components: {
      Filter,
      ShoppingBag,
      Search,
      Menu
    },
    data() {
      return {
        products: [],
        brands: [],
        categories: [],
        filters: {
          brand: '',
          category: '',
          minPrice: '',
          maxPrice: ''
        },
        sortBy: 'featured'
      }
    },
    mounted() {
      this.getProducts()
      this.getBrands()
      this.getCategory()
    },
    computed: {
      bannerText() {
        if (this.filters.category && this.filters.brand) {
          return `${this.filters.brand} - ${this.filters.category}`;
        } else if (this.filters.category) {
          return this.filters.category;
        } else if (this.filters.brand) {
          return this.filters.brand;
        }
        return '';
      }
    },
    watch: {
    filters: {
      handler: 'updateProducts',
      deep: true
    },
    products: 'applySort',
    sortBy: 'applySort'
  },
    methods: {
      async getProducts() {
        try {
          const response = await axios.get('api/products/')
          this.products = response.data
          this.applySort()
        } catch (error) {
          console.error(error)
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
      async getCategory() {
        try {
          const response = await axios.get('api/categories/')
          this.categories = response.data
        } catch (error) {
          console.error(error)
        }
      },
      async updateProducts() {
        try {
            const response = await axios.get('api/filter_products/', {
                params: this.filters  
            })
          console.log(response.data)
          console.log(this.filters)
          this.products = response.data
          this.applySort()
        } catch (error) {
          console.error(error)
        }
      },
      applySort() {
        switch (this.sortBy) {
          case 'priceLowToHigh':
            this.products.sort((a, b) => a.price - b.price)
            break
          case 'priceHighToLow':
            this.products.sort((a, b) => b.price - a.price)
            break
          case 'alphabetical':
            this.products.sort((a, b) => a.name.localeCompare(b.name))
            break
          default:
            break
        }
      }
    }
  }
  </script>
  