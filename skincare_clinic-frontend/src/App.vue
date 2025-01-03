
<template>
  <div class="w-full min-h-screen bg-white">
  <header>
    <nav class="bg-white shadow-sm">
      <!-- Navigation content -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex-shrink-0 flex items-center">
            <RouterLink to="/"><span class="text-2xl font-bold text-emerald-800">Skincare Clinic</span></RouterLink>
          </div>
          <div class="hidden md:flex items-center space-x-8">
            <RouterLink to="/" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Home</RouterLink>
            <RouterLink to="/shop" class="text-gray-600 hover:text-emerald-700">Shop</RouterLink>
            <RouterLink to="/track-order" class="text-gray-600 hover:text-emerald-700">Track Order</RouterLink>
            <a href="#" class="text-gray-600 hover:text-emerald-700">Blog</a>
          </div>
          <div class="hidden md:flex items-center space-x-4">
            <button class="p-2 text-gray-600 hover:text-emerald-700">
              <search-icon :size="20" />
            </button>
            <RouterLink to="/cart" class="p-2 text-gray-600 hover:text-emerald-700">
              <shopping-cart-icon :size="20" />
            </RouterLink>
          </div>
          
        <div class="md:hidden flex items-center space-x-4">
            <button class="p-2 text-gray-600 hover:text-emerald-700">
              <search-icon :size="20" />
            </button>
            <RouterLink to="/cart" class="p-2 text-gray-600 hover:text-emerald-700">
              <shopping-cart-icon :size="20" />
            </RouterLink>
            <button @click="toggleMenu" class="p-2 text-gray-600 hover:text-emerald-700">
              <x-icon v-if="isOpen" :size="24" />
              <menu-icon v-else :size="24" />
            </button>
        </div>

        </div>
      </div>
      <div v-if="isOpen" class="md:hidden">
        <!-- Mobile menu content -->
        <div class="px-2 pt-2 pb-3 space-y-1">
          <RouterLink to="/" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Home</RouterLink>
          <RouterLink to="/shop" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Shop</RouterLink>
          <RouterLink  to="/track-order" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Track Order</RouterLink>
          <a href="#" class="block px-3 py-2 text-gray-600 hover:text-emerald-700">Blog</a>
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

  <footer class="bg-emerald-900 text-white">
      <!-- Footer content -->
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
import { Menu, X, ChevronDown, ShoppingCart, Search, User, Facebook, Twitter, Instagram } from 'lucide-vue-next'
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
   
    }
  },
  computed: {
    announcementStyle() {
      return {
        backgroundImage: 'url("https://images.unsplash.com/photo-1550859492-d5da9d8e45f3?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3")',
        backgroundColor: "rgba(45, 148, 116, 0.9)",
        backgroundBlendMode: "overlay",
      }
    }
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen
      console.log(this.isOpen)
    },
    
  },
  mounted() {
    // Announcement rotation logic
    setInterval(() => {
      this.currentAnnouncement = (this.currentAnnouncement + 1) % this.announcements.length
    }, 5000)
  }
}
</script>

<style scoped>

</style>


