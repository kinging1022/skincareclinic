<template>
  <div class="w-full min-h-screen bg-white">
    <header>
      <nav class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16 items-center">
            <div class="flex-shrink-0 flex items-center">
              <RouterLink to="/"><span class="text-2xl font-bold text-emerald-800">Skincare Clinic</span></RouterLink>
            </div>
            <div class="hidden md:flex items-center space-x-8">
              <RouterLink to="/" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Home</RouterLink>
              <RouterLink to="/shop" class="text-gray-600 hover:text-emerald-700">Shop</RouterLink>
              <RouterLink to="/track-order" class="text-gray-600 hover:text-emerald-700">Track Order</RouterLink>
              <RouterLink to="/blog" class="text-gray-600 hover:text-emerald-700">Blog</RouterLink>
              <RouterLink v-if="userStore.isAuthenticated" to="/analytics" class="text-gray-600 hover:text-emerald-700">Analytics</RouterLink>
              <button v-if="userStore.isAuthenticated" @click="LogOut()" class="text-red-600 hover:text-red-700">Log out</button>

            </div>
            <div class="hidden md:flex items-center space-x-4">
              <RouterLink to="/search" class="p-2 text-gray-600 hover:text-emerald-700">
                <search-icon :size="20" />
              </RouterLink>
              <RouterLink to="/cart" class="p-2 text-gray-600 hover:text-emerald-700 relative">
                <shopping-cart-icon :size="20" />
                <span v-if="cartItemCount > 0" class="absolute -top-1 -right-1 bg-emerald-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                  {{ cartItemCount }}
                </span>
              </RouterLink>
              
            
              
            </div>
            
            <div class="md:hidden flex items-center space-x-4">
              <RouterLink to="/search" class="p-2 text-gray-600 hover:text-emerald-700">
                <search-icon :size="20" />
              </RouterLink>
              <RouterLink to="/cart" class="p-2 text-gray-600 hover:text-emerald-700 relative">
                <shopping-cart-icon :size="20" />
                <span v-if="cartItemCount > 0" class="absolute -top-1 -right-1 bg-emerald-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                  {{ cartItemCount }}
                </span>
              </RouterLink>
              <button @click="toggleMenu" class="p-2 text-gray-600 hover:text-emerald-700">
                <x-icon v-if="isOpen" :size="24" />
                <menu-icon v-else :size="24" />
              </button>
            </div>
          </div>
        </div>
        <div v-if="isOpen" class="md:hidden">
          <div class="px-2 pt-2 pb-3 space-y-1">
            <RouterLink to="/" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Home</RouterLink>
            <RouterLink to="/shop" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Shop</RouterLink>
            <RouterLink  to="/track-order" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Track Order</RouterLink>
            <RouterLink to="/blog" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Blog</RouterLink>
            <RouterLink v-if="userStore.isAuthenticated" to="/analytics" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Analytics</RouterLink>
            <button v-if="userStore.isAuthenticated" @click="LogOut()" class="block px-3 py-2 text-red-600 hover:text-red-700">Log out</button>

          </div>
        </div>
      </nav>

      <div class="w-full bg-cover bg-center py-3" :style="announcementStyle">
        <div class="max-w-7xl mx-auto px-4">
          <p class="text-center text-white text-sm md:text-base font-medium animate-fade-in">
            {{ announcements[currentAnnouncement] }}
          </p>
        </div>
      </div>
    </header>

    <RouterView />

    <Toast />

    <footer class="bg-emerald-900 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 class="text-lg font-semibold mb-4">About Us</h3>
            <p class="text-emerald-100">
              Emerald Essence is dedicated to providing premium skincare products that enhance your natural beauty.
            </p>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Quick Links</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-emerald-100 hover:text-white">Shop</a></li>
              <li><a href="#" class="text-emerald-100 hover:text-white">About</a></li>
              <li><a href="#" class="text-emerald-100 hover:text-white">Contact</a></li>
              <li><a href="#" class="text-emerald-100 hover:text-white">FAQs</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Contact</h3>
            <ul class="space-y-2">
              <li class="text-emerald-100">Email: info@emeraldessence.com</li>
              <li class="text-emerald-100">Phone: (555) 123-4567</li>
              <li class="text-emerald-100">Address: 123 Beauty Lane</li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Follow Us</h3>
            <div class="flex space-x-4">
              <a href="#" class="text-emerald-100 hover:text-white">
                <facebook-icon :size="24" />
              </a>
              <a href="#" class="text-emerald-100 hover:text-white">
                <twitter-icon :size="24" />
              </a>
              <a href="#" class="text-emerald-100 hover:text-white">
                <instagram-icon :size="24" />
              </a>
            </div>
          </div>
        </div>
        <div class="border-t border-emerald-800 mt-8 pt-8 text-center text-emerald-100">
          <p>&copy; 2024 Emerald Essence. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router'
import { useCartStore } from './stores/cart';
import Toast from './components/Toast.vue'
import { Menu, X, ChevronDown, ShoppingCart, Search, User, Facebook, Twitter, Instagram, Route , LogOut } from 'lucide-vue-next'
import { useUserStore } from './stores/user';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    MenuIcon: Menu,
    XIcon: X,
    ChevronDownIcon: ChevronDown,
    ShoppingCartIcon: ShoppingCart,
    SearchIcon: Search,
    UserIcon: User,
    FacebookIcon: Facebook,
    TwitterIcon: Twitter,
    InstagramIcon: Instagram,
    Toast,
    LogOut
  },
  data() {
    return {
      isOpen: false,
      openCategory: null,
      currentAnnouncement: 0,
      announcementInterval: null,
      cartStore : useCartStore(),
      userStore: useUserStore(),
      announcements: [],
    }
  },
  computed: {
    announcementStyle() {
      return {
        backgroundImage: 'url("https://images.unsplash.com/photo-1550859492-d5da9d8e45f3?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3")',
        backgroundColor: "rgba(45, 148, 116, 0.9)",
        backgroundBlendMode: "overlay",
      }
    },
    cartItemCount() {
      return this.cartStore.totalItems;
    },
    
    
  },
  methods: {
    async getAnnoucements(){
      try{

        const response = await axios.get('api/annoucements/')
        
        this.announcements = response.data.map(announcement => announcement.title.replace(/['"]+/g, ''));

      }catch(error){

      }

    },
    toggleMenu() {
      this.isOpen = !this.isOpen
    },
    LogOut(){
      this.userStore.removeToken()
      this.$router.push('/shop')
    }
  },
  mounted() {      
    // Announcement rotation logic
    this.getAnnoucements()
    this.userStore.initStore();
    this.cartStore.initializeCart
    this.announcementInterval = setInterval(() => {
      this.currentAnnouncement = (this.currentAnnouncement + 1) % this.announcements.length
    }, 5000)
  },
  beforeUnmount() {
  clearInterval(this.announcementInterval);
}
}
</script>

<style scoped>
/* Add any scoped styles here if needed */
</style>
