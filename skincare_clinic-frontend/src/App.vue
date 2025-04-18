<template>
  <div class="flex min-h-screen flex-col bg-[#f0f5f1]">
    <!-- Header -->
    <header class="sticky top-0 z-50 w-full border-b border-[#d7e5dc] bg-[#f0f5f1]/80 backdrop-blur-sm">
      <div class="container flex h-16 items-center justify-between px-4 lg:h-20">
        <a href="/" class="flex items-center gap-2">
          <span class="text-lg font-semibold tracking-wider text-[#1c3a2e] lg:text-xl">SKINCARÈ CLINIC</span>
        </a>
        
        <!-- Desktop Navigation -->
        <nav class="hidden gap-4 lg:flex lg:gap-6">
          <RouterLink to="/shop" class="text-base font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Shop</RouterLink>
          <RouterLink to="/track-order" class="text-base font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Track Order</RouterLink>
          <RouterLink to="/about" class="text-base font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">About</RouterLink>
          <RouterLink to="/blog" class="text-base font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Blog</RouterLink>
        </nav>
        
        <!-- Tablet Navigation -->
        <nav class="hidden gap-3 md:flex lg:hidden">
          <RouterLink to="/shop" class="text-sm font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Shop</RouterLink>
          <RouterLink to="/track-order" class="text-sm font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Track</RouterLink>
          <RouterLink to="/about" class="text-sm font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">About</RouterLink>
        </nav>
        
        <div class="flex items-center gap-3 md:gap-4">
          <!-- Desktop Search -->
          <div class="relative hidden lg:block">
            <search-icon class="absolute left-2.5 top-2.5 h-4 w-4 text-[#0a5c3e]" />
            <input
              type="search"
              placeholder="Search products..."
              class="h-10 w-64 rounded-full border border-[#d7e5dc] bg-transparent pl-9 pr-4 text-sm text-[#1c3a2e] placeholder-[#4a6b5d] focus:border-[#0a5c3e] focus:outline-none focus:ring-1 focus:ring-[#0a5c3e]"
            />
          </div>
          
          <!-- Tablet Search -->
          <div class="relative hidden md:block lg:hidden">
            <search-icon class="absolute left-2.5 top-2.5 h-4 w-4 text-[#0a5c3e]" />
            <input
              type="search"
              placeholder="Search..."
              class="h-9 w-40 rounded-full border border-[#d7e5dc] bg-transparent pl-9 pr-3 text-sm text-[#1c3a2e] placeholder-[#4a6b5d] focus:border-[#0a5c3e] focus:outline-none focus:ring-1 focus:ring-[#0a5c3e]"
            />
          </div>
          
          <!-- Cart Icon (all views) -->
          <RouterLink to="/cart" class="relative">
            <shopping-bag-icon class="h-5 w-5 text-[#1c3a2e]" />
            <span class="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-[#0a5c3e] text-[10px] font-medium text-white">
              {{ cartItemCount }}
            </span>
          </RouterLink>
          
          <!-- Mobile-only icons -->
          <RouterLink to="/search" class="md:hidden">
            <search-icon class="h-5 w-5 text-[#1c3a2e]" />
          </RouterLink>
          
          <!-- Mobile Track Order -->
          <RouterLink to="/track-order" class="md:hidden flex items-center justify-center h-8 w-8 rounded-full hover:bg-[#d7e5dc]/50">
            <truck-icon class="h-5 w-5 text-[#1c3a2e]" />
          </RouterLink>
        </div>
      </div>
    </header>

    <RouterView />
    <Toast />

    <!-- Footer -->
    <footer class="border-t border-[#d7e5dc] bg-white py-8 lg:py-12">
      <div class="container px-4">
        <div class="grid grid-cols-2 gap-6 md:grid-cols-4 md:gap-8">
          <div v-for="(footerSection, index) in footerSections" :key="index">
            <h3 class="mb-3 text-sm font-medium text-[#1c3a2e] lg:mb-4 lg:text-base">{{ footerSection.title }}</h3>
            
            <!-- Render links if available -->
            <ul v-if="footerSection.links" class="space-y-2 text-xs text-[#4a6b5d] lg:text-sm">
              <li v-for="(link, linkIndex) in footerSection.links" :key="linkIndex">
                <RouterLink :to="link.url" class="hover:text-[#0a5c3e]">
                  {{ link.label }}
                </RouterLink>
              </li>
            </ul>

            <!-- Render social icons -->
            <div v-if="footerSection.social" class="mb-3 flex gap-4 lg:mb-4">
              <a href="#" class="text-[#4a6b5d] hover:text-[#0a5c3e]">
                <instagram-icon class="h-5 w-5" />
              </a>
              <a href="#" class="text-[#4a6b5d] hover:text-[#0a5c3e]">
                <facebook-icon class="h-5 w-5" />
              </a>
              <a href="#" class="text-[#4a6b5d] hover:text-[#0a5c3e]">
                <twitter-icon class="h-5 w-5" />
              </a>
            </div>

            <!-- Copyright -->
            <p v-if="footerSection.copyright" class="text-xs text-[#4a6b5d] lg:text-sm">
              © {{ currentYear }} SKINCARÈ CLINIC. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router'
import { useCartStore } from './stores/cart'
import Toast from './components/Toast.vue'
import {
  Search as SearchIcon,
  ShoppingBag as ShoppingBagIcon,
  Instagram as InstagramIcon,
  Facebook as FacebookIcon,
  Twitter as TwitterIcon,
  Truck as TruckIcon
} from 'lucide-vue-next'
import { useUserStore } from './stores/user'

export default {
  name: 'App',
  components: {
    SearchIcon,
    ShoppingBagIcon,
    InstagramIcon,
    FacebookIcon,
    TwitterIcon,
    TruckIcon,
    Toast,
    RouterView
  },
  data() {
    return {
      cartStore: useCartStore(),
      userStore: useUserStore(),
      currentYear: new Date().getFullYear(),
      footerSections: [
        {
          title: "Shop",
          links: [{ label: "All Products", url: "/shop" }]
        },
        {
          title: "About",
          links: [{ label: "About Us", url: "/about", }, { label: "Blog", url: "/blog" }]
        },
        {
          title: "Shipping & Tracking",
          links: [
            { label: "Track Order", url: "/track-order" }
          ]
        },
        {
          title: "Connect",
          social: true,
          copyright: true
        }
      ]
    }
  },
  computed: {
    cartItemCount() {
      return this.cartStore?.totalItems || 0
    }
  },
  methods: {
    LogOut() {
      this.userStore.removeToken()
      this.$router.push('/shop')
    }
  },
  mounted() {
    this.userStore.initStore()
    this.cartStore.initializeCart()
  }
}
</script>

<style>
/* Hide scrollbar for Chrome, Safari and Opera */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

/* Global styles */
body {
  font-family: 'Inter', sans-serif;
}

.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  max-width: 1280px;
}

@media (min-width: 640px) {
  .container {
    max-width: 640px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}

@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}

/* Line clamp utilities */
.line-clamp-1 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
</style>