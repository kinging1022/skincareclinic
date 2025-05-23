<template>
  <div class="flex min-h-screen flex-col bg-[#f0f5f1]">
    <!-- Header -->
    <header v-if="!$route.meta.hideNavigation" class="sticky top-0 z-50 w-full border-b border-[#d7e5dc] bg-[#f0f5f1] h-16 lg:h-20">
      <div class="container flex h-full items-center justify-between px-4">
        <RouterLink to="/" class="flex items-center gap-2">
          <span class="text-lg font-semibold tracking-wider text-[#1c3a2e] lg:text-xl">OZIMA SKIN SHOP</span>
        </RouterLink>
        
        <nav class="hidden gap-4 lg:flex lg:gap-6">
          <RouterLink to="/products" class="text-base font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Shop</RouterLink>
          <RouterLink to="/track-order" class="text-base font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Track Order</RouterLink>
          <RouterLink to="/about" class="text-base font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">About</RouterLink>
          <RouterLink v-if="!isAuthenticated" to="/blog" class="text-base font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Blog</RouterLink>
          <button v-if="isAuthenticated" @click="logout" class="text-base font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Logout</button>
        </nav>
        
        <nav class="hidden gap-3 md:flex lg:hidden">
          <RouterLink to="/products" class="text-sm font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Shop</RouterLink>
          <RouterLink to="/track-order" class="text-sm font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">Track</RouterLink>
          <RouterLink to="/about" class="text-sm font-medium tracking-wide text-[#1c3a2e] hover:text-[#0a5c3e]">About</RouterLink>
        </nav>
        
        <div class="flex items-center gap-3 md:gap-4">
          <RouterLink 
            to="/search" 
            class="flex items-center gap-1 text-sm font-medium text-[#1c3a2e] hover:text-[#0a5c3e]"
          >
            <Search class="h-5 w-5" />
            <span class="hidden md:inline">Search</span>
          </RouterLink>
          
          <RouterLink to="/cart" class="relative">
            <ShoppingBag class="h-5 w-5 text-[#1c3a2e]" />
            <span v-if="cartItemCount > 0" class="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-[#0a5c3e] text-[10px] font-medium text-white">
              {{ cartItemCount }}
            </span>
          </RouterLink>
          
          <RouterLink v-if="!isAuthenticated" to="/track-order" class="md:hidden flex items-center justify-center h-8 w-8 rounded-full hover:bg-[#d7e5dc]/50">
            <Truck class="h-5 w-5 text-[#1c3a2e]" />
          </RouterLink>
          
          <button v-if="isAuthenticated" @click="logout" class="md:hidden flex items-center justify-center h-8 w-8 rounded-full hover:bg-[#d7e5dc]/50">
            <LogOut class="h-5 w-5 text-[#1c3a2e]" />
          </button>
        </div>
      </div>
    </header>

    <main class="flex-1">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="border-t border-[#d7e5dc] bg-white w-full">
      <div class="container mx-auto px-4">
        <div class="py-6 md:py-8">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
            <!-- Shop Column -->
            <div class="flex flex-col space-y-2">
              <h3 class="text-sm font-medium text-[#1c3a2e] h-6">Shop</h3>
              <RouterLink to="/products" class="flex items-center text-[#4a6b5d] hover:text-[#0a5c3e] h-6">
                <ShoppingBag class="h-4 w-4 mr-2 flex-shrink-0" />
                <span class="text-sm">All Products</span>
              </RouterLink>
              <RouterLink to="/privacy-policy" class="flex items-center text-[#4a6b5d] hover:text-[#0a5c3e] h-6">
                <Lock class="h-4 w-4 mr-2 flex-shrink-0" />
                <span class="text-sm">Privacy policy</span>
              </RouterLink>
            </div>

            <!-- About Column -->
            <div class="flex flex-col space-y-2">
              <h3 class="text-sm font-medium text-[#1c3a2e] h-6">About</h3>
              <RouterLink to="/about" class="flex items-center text-[#4a6b5d] hover:text-[#0a5c3e] h-6">
                <Info class="h-4 w-4 mr-2 flex-shrink-0" />
                <span class="text-sm">About Us</span>
              </RouterLink>
              <RouterLink v-if="!isAuthenticated" to="/blog" class="flex items-center text-[#4a6b5d] hover:text-[#0a5c3e] h-6">
                <Newspaper class="h-4 w-4 mr-2 flex-shrink-0" />
                <span class="text-sm">Blog</span>
              </RouterLink>
            </div>

            <!-- Shipping Column -->
            <div class="flex flex-col space-y-2">
              <h3 class="text-sm font-medium text-[#1c3a2e] h-6">Shipping</h3>
              <RouterLink to="/track-order" class="flex items-center text-[#4a6b5d] hover:text-[#0a5c3e] h-6">
                <Truck class="h-4 w-4 mr-2 flex-shrink-0" />
                <span class="text-sm">Track Order</span>
              </RouterLink>
              <RouterLink to="/shipping-policy" class="flex items-center text-[#4a6b5d] hover:text-[#0a5c3e] h-6">
                <PackageCheck class="h-4 w-4 mr-2 flex-shrink-0" />
                <span class="text-sm">Shipping Policy</span>
              </RouterLink>
            </div>

            <!-- Connect Column -->
            <div class="flex flex-col space-y-2">
              <h3 class="text-sm font-medium text-[#1c3a2e] h-6">Connect</h3>
              <div class="flex flex-col space-y-2">
                <a href="https://www.instagram.com/online_skincare_store_ibadan?igsh=MTU5c2trOWtrYmhkOA==" class="flex items-center text-[#4a6b5d] hover:text-[#0a5c3e] h-6" aria-label="Instagram">
                  <Instagram class="h-4 w-4 mr-2 flex-shrink-0" />
                  <span class="text-sm">Instagram</span>
                </a>
                <a href="https://linktr.ee/The_skincare_clinic" class="flex items-center text-[#4a6b5d] hover:text-[#0a5c3e] h-6">
                  <Mail class="h-4 w-4 mr-2 flex-shrink-0" />
                  <span class="text-sm">Contact Us</span>
                </a>
              </div>
            </div>
          </div>
          
          <div class="h-10 flex items-center justify-center border-t border-[#d7e5dc] mt-6">
            <p class="text-xs text-[#4a6b5d] text-center">
              © {{ currentYear }} OZIMA SKIN SHOP. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>

    <Toast />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'
import {
  Search,
  ShoppingBag,
  Truck,
  Info,
  Newspaper,
  PackageCheck,
  Instagram,
  Mail,
  LogOut,
  Lock,
} from 'lucide-vue-next'
import Toast from '@/components/Toast.vue'

const userStore = useUserStore()
const cartStore = useCartStore()
const router = useRouter()

const currentYear = ref(new Date().getFullYear())
const isMobile = ref(false)
const isAuthenticated = computed(() => userStore.isAuthenticated)
const cartItemCount = computed(() => cartStore.totalItems || 0)

const logout = () => {
  userStore.removeToken()
  router.push('/products')
}

onMounted(() => {
  const handleResize = () => {
    isMobile.value = window.innerWidth < 768
  }
  
  handleResize()
  userStore.initStore()
  cartStore.initializeCart()
  
  let resizeTimer
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer)
    resizeTimer = setTimeout(handleResize, 100)
  }, { passive: true })
})
</script>

<style>
/* Container styles */
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
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

.router-link-active {
  color: #0a5c3e;
  font-weight: 600;
}

.router-link-exact-active {
  color: #0a5c3e;
  font-weight: 600;
}

header {
  contain: layout style paint;
}

.cls-footer {
  contain: layout style paint;
  content-visibility: auto;
  contain-intrinsic-size: 0 140px;
}

.footer-wrapper {
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.footer-links-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  grid-auto-rows: minmax(90px, auto);
}

.footer-column {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  height: 100%;
}

.footer-heading {
  font-size: 0.875rem;
  font-weight: 500;
  color: #1c3a2e;
  line-height: 1.25;
  margin-bottom: 0.5rem;
  height: 1.25rem;
}

.footer-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4a6b5d;
  transition: color 0.15s ease;
  height: 1.5rem;
  margin-bottom: 0.25rem;
}

.footer-link:hover {
  color: #0a5c3e;
}

.footer-icon {
  height: 1rem;
  width: 1rem;
  flex-shrink: 0;
}

.footer-icon-lg {
  height: 1.25rem;
  width: 1.25rem;
  flex-shrink: 0;
}

.footer-text {
  font-size: 0.875rem;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.footer-connect {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  color: #4a6b5d;
  transition: color 0.15s ease;
  border-radius: 9999px;
}

.social-icon:hover {
  color: #0a5c3e;
  background-color: #f0f5f1;
}

.copyright-container {
  border-top: 1px solid #d7e5dc;
  padding-top: 1rem;
  height: 2.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.copyright-text {
  font-size: 0.75rem;
  color: #4a6b5d;
  text-align: center;
  line-height: 1.5;
}

@media (min-width: 768px) {
  .cls-footer {
    contain-intrinsic-size: 0 120px;
  }

  .footer-links-container {
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
    grid-auto-rows: minmax(80px, auto);
  }
  
  .footer-heading {
    font-size: 1rem;
    height: 1.5rem;
  }
  
  .copyright-text {
    font-size: 0.875rem;
  }
}

.aspect-ratio-box {
  position: relative;
  width: 100%;
  padding-top: 133.33%;
  overflow: hidden;
}

.aspect-ratio-box img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>