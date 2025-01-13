<template>
    <main class="w-full">
      <section class="relative bg-emerald-50 py-16 md:py-24">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center">
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-emerald-800 mb-6">
              Your Skin Deserves the Best
            </h1>
            <p class="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Discover our carefully curated collection of premium skincare products designed to nourish, protect, and enhance your natural beauty.
            </p>
            <RouterLink to="/shop" class="bg-emerald-700 text-white px-8 py-3 rounded-md hover:bg-emerald-800 transition-colors duration-300">
              Shop Now
            </RouterLink>
          </div>
        </div>
      </section>

      <product-slider title="Popular Products" :products="popularProducts" />
      <product-slider title="Featured Products" :products="featuredProducts" />
      <product-slider title="New Arrivals" :products="newArrivals" />
    </main>

    
</template>




<script>
import axios from 'axios';
import ProductSlider from '@/components/ProductSlider.vue';
export default {
  name: 'App',
  components: {
    ProductSlider
  },
  mounted() {
    this.getPopularProducts()
    this.getFeaturedProduct()
    this.getNewArrivals()
    
  },
  data() {
    return {
      isOpen: false,
      openCategory: null,
      currentAnnouncement: 0,
       announcements : [
    "Free shipping on orders over $50! 🚚",
    "New Summer Collection is here! ✨",
    "Get 20% off on your first purchase! 🎉",
  ],
  popularProducts : [],
  featuredProducts : [],
  newArrivals : []
    }
  },
  computed: {
    
  },
  methods: {
    async getPopularProducts() {
      try {
        const response = await axios.get('api/shop/popular_products/')
        this.popularProducts = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async getFeaturedProduct(){
      try {
        const response = await axios.get('api/shop/featured_products/')
        this.featuredProducts = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async getNewArrivals(){
      try {
        const response = await axios.get('api/shop/new_arrivals/')
        this.newArrivals = response.data
      } catch (error) {
        console.error(error)
      }
    }
  
  },
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
