<template>
  <main class="flex-1">
    <!-- Enhanced Animated Hero Section -->
    <section class="relative overflow-hidden">
      <!-- Background Image Carousel -->
      <div class="absolute inset-0 w-full h-full">
        <transition-group 
          name="fade" 
          tag="div" 
          class="h-full w-full"
        >
          <div 
            v-for="(slide, index) in heroSlides" 
            :key="slide.id"
            v-show="currentSlide === index"
            class="absolute inset-0 h-full w-full bg-cover bg-center transition-opacity duration-1000"
            :style="{
              backgroundImage: `linear-gradient(rgba(10, 60, 40, 0.55), rgba(10, 60, 40, 0.65)), url(${slide.image})`
            }"
          ></div>
        </transition-group>
        
        <!-- Subtle Animated Overlay -->
        <div class="absolute inset-0 opacity-20">
          <div class="shimmer-effect"></div>
        </div>
      </div>
      
      <!-- Content -->
      <div class="relative flex h-[80vh] w-full flex-col items-center justify-center px-4 text-center text-white">
        <!-- Animated Brand Logo -->
        <div class="mb-6 overflow-hidden">
          <h2 
            class="brand-name text-lg font-light tracking-[0.25em] md:text-xl"
            :class="{'animate-reveal': animationStarted}"
          >
            <span class="inline-block">S</span>
            <span class="inline-block">K</span>
            <span class="inline-block">I</span>
            <span class="inline-block">N</span>
            <span class="inline-block">C</span>
            <span class="inline-block">A</span>
            <span class="inline-block">R</span>
            <span class="inline-block">È</span>
            <span class="inline-block mx-2">•</span>
            <span class="inline-block">C</span>
            <span class="inline-block">L</span>
            <span class="inline-block">I</span>
            <span class="inline-block">N</span>
            <span class="inline-block">I</span>
            <span class="inline-block">C</span>
          </h2>
        </div>
        
        <!-- Animated Headline -->
        <div class="overflow-hidden mb-4">
          <transition 
            name="slide-up" 
            mode="out-in"
          >
            <h1 
              :key="currentHeadline" 
              class="max-w-3xl text-4xl font-light tracking-wide md:text-5xl lg:text-6xl drop-shadow-sm"
            >
              {{ headlines[currentHeadline] }}
            </h1>
          </transition>
        </div>
        
        <!-- Animated Tagline -->
        <div class="overflow-hidden mb-8">
          <p 
            class="max-w-md text-base font-light md:text-lg drop-shadow-sm opacity-0"
            :class="{'animate-fade-in': animationStarted}"
          >
            Luxurious formulations crafted with the finest ingredients for timeless beauty
          </p>
        </div>
        
        <!-- Animated Button -->
        <RouterLink 
          to="/shop" 
          class="rounded-none bg-transparent border border-white px-8 text-white hover:bg-white hover:text-[#0a5c3e] text-base py-4 transition-all duration-300 opacity-0"
          :class="{'animate-fade-in-delay': animationStarted}"
        >
          Shop Collection
        </RouterLink>
        
        <!-- Slide Indicators -->
        <div class="absolute bottom-8 left-0 right-0 flex justify-center space-x-2">
          <button 
            v-for="(slide, index) in heroSlides" 
            :key="slide.id"
            @click="setSlide(index)"
            class="h-1 w-12 transition-all duration-300"
            :class="currentSlide === index ? 'bg-white' : 'bg-white/40'"
            aria-label="Change slide"
          ></button>
        </div>
      </div>
    </section>

    <!-- Product Categories - Scrollable -->
    <ScrollableCategories :categories="collections" />

    <!-- New arrival - Scrollable -->
    <ScrollableProducts 
      :products="NewArrivals" 
      title="New Arrivals" 
      @add-to-cart="addToCart" 
    />

    <!-- Featured Products - Scrollable -->
    <ScrollableProducts 
      :products="FeaturedProducts" 
      title="Bestsellers" 
      @add-to-cart="addToCart" 
    />

    <!-- Benefits Section -->
    <section class="py-16 bg-[#f0f5f1]">
      <div class="container px-4 md:px-6">
        <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div v-for="(benefit, index) in benefits" :key="index" class="flex flex-col items-center text-center">
            <div class="mb-4 h-16 w-16 rounded-full border border-[#d7e5dc] bg-white p-4">
              <component :is="benefit.icon" class="h-full w-full text-[#0a5c3e]"></component>
            </div>
            <h3 class="mb-2 text-base font-medium text-[#1c3a2e]">{{ benefit.title }}</h3>
            <p class="text-sm text-[#4a6b5d]">
              {{ benefit.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Newsletter -->
    <section class="bg-[#e3efe7] py-16">
      <div class="container px-4 md:px-6">
        <div class="mx-auto max-w-md text-center">
          <h2 class="mb-4 text-2xl font-light tracking-wider text-[#1c3a2e]">Join Our Community</h2>
          <p class="mb-6 text-base text-[#4a6b5d]">
            Subscribe to receive exclusive offers, skincare tips, and early access to new products.
          </p>
          <div class="flex">
            <input
              type="email"
              placeholder="Your email address"
              class="rounded-none border-[#d7e5dc] bg-white focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none border text-base w-full py-2 px-4"
            />
            <button class="rounded-none bg-[#0a5c3e] hover:bg-[#0b4a33] text-base text-white px-6 py-2">Subscribe</button>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { Leaf, Heart, Recycle } from 'lucide-vue-next'
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import ScrollableCategories from '@/components/ScrollableCategory.vue'
import ScrollableProducts from '@/components/ScrollableProduct.vue'

export default {
  name: 'HomeView',
  components: {
    Leaf,
    Heart,
    Recycle,
    RouterLink,
    ScrollableCategories,
    ScrollableProducts
  },
  data() {
    return {
      cartStore: useCartStore(),
      collections: [],
      NewArrivals:[],
      FeaturedProducts: [],
      animationStarted: false,
      currentSlide: 0,
      currentHeadline: 0,
      slideInterval: null,
      headlineInterval: null,
      heroSlides: [
        {
          id: 1,
          image: 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?q=80&w=1920&auto=format&fit=crop',
        },
        {
          id: 2,
          image: 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?q=80&w=1920&auto=format&fit=crop',
        },
        {
          id: 3,
          image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?q=80&w=1920&auto=format&fit=crop',
        }
      ],
      headlines: [
        "Discover the Art of Radiant Skin",
        "Elevate Your Skincare Ritual",
        "Unveil Your Natural Luminosity"
      ],
      benefits: [
        {
          title: "Natural Ingredients",
          description: "Ethically sourced botanicals and active ingredients for gentle yet effective results.",
          icon: Leaf
        },
        {
          title: "Cruelty Free",
          description: "Products never tested on animals and are committed to ethical beauty practices.",
          icon: Heart
        },
        {
          title: "Sustainable Packaging",
          description: "Eco-friendly packaging designed to minimize environmental impact.",
          icon: Recycle
        }
      ]
    }
  },
  methods: {
    async getFeaturedProducts() {
      try {
        const response = await axios.get('api/shop/featured_products/')
        this.FeaturedProducts = response.data
      } catch (error) {
        console.error('Error fetching featured products:', error)
      }
    },
    async getNewArrivals() {
      try {
        const response = await axios.get('api/shop/new_arrivals/')
        this.NewArrivals = response.data
      } catch (error) {
        console.error('Error fetching featured products:', error)
      }
    },
    async getCollections() {
      try {
        const response = await axios.get('api/shop/collections/')
        this.collections = response.data
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    },
    addToCart(product) {
      this.cartStore.addItem(product)
    },
    startSlideshow() {
      this.slideInterval = setInterval(() => {
        this.currentSlide = (this.currentSlide + 1) % this.heroSlides.length
      }, 6000)
    },
    startHeadlineRotation() {
      this.headlineInterval = setInterval(() => {
        this.currentHeadline = (this.currentHeadline + 1) % this.headlines.length
      }, 4000)
    },
    setSlide(index) {
      this.currentSlide = index
      // Reset the slideshow timer when manually changing slides
      clearInterval(this.slideInterval)
      this.startSlideshow()
    },
    preloadImages() {
      this.heroSlides.forEach(slide => {
        const img = new Image()
        img.src = slide.image
      })
    }
  },
  mounted() {
    this.getCollections()
    this.getFeaturedProducts()
    this.getNewArrivals()
    
    // Preload images for better performance
    this.preloadImages()
    
    // Start animations after a short delay
    setTimeout(() => {
      this.animationStarted = true
    }, 300)
    
    // Start the slideshow and headline rotation
    this.startSlideshow()
    this.startHeadlineRotation()
  },
  beforeUnmount() {
    // Clear intervals when component is destroyed
    clearInterval(this.slideInterval)
    clearInterval(this.headlineInterval)
  }
}
</script>

<style scoped>
/* Fade transition for slides */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Slide up animation for headlines */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.8s ease, opacity 0.8s ease;
}
.slide-up-enter-from {
  transform: translateY(20px);
  opacity: 0;
}
.slide-up-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}

/* Brand name animation */
.brand-name span {
  display: inline-block;
  opacity: 0;
  transform: translateY(20px);
}

.animate-reveal span {
  animation: revealLetter 0.5s forwards;
}

.animate-reveal span:nth-child(1) { animation-delay: 0.1s; }
.animate-reveal span:nth-child(2) { animation-delay: 0.15s; }
.animate-reveal span:nth-child(3) { animation-delay: 0.2s; }
.animate-reveal span:nth-child(4) { animation-delay: 0.25s; }
.animate-reveal span:nth-child(5) { animation-delay: 0.3s; }
.animate-reveal span:nth-child(6) { animation-delay: 0.35s; }
.animate-reveal span:nth-child(7) { animation-delay: 0.4s; }
.animate-reveal span:nth-child(8) { animation-delay: 0.45s; }
.animate-reveal span:nth-child(9) { animation-delay: 0.5s; }
.animate-reveal span:nth-child(10) { animation-delay: 0.55s; }
.animate-reveal span:nth-child(11) { animation-delay: 0.6s; }
.animate-reveal span:nth-child(12) { animation-delay: 0.65s; }
.animate-reveal span:nth-child(13) { animation-delay: 0.7s; }
.animate-reveal span:nth-child(14) { animation-delay: 0.75s; }
.animate-reveal span:nth-child(15) { animation-delay: 0.8s; }

@keyframes revealLetter {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Fade in animations */
.animate-fade-in {
  animation: fadeIn 1s ease 1s forwards;
}

.animate-fade-in-delay {
  animation: fadeIn 1s ease 1.5s forwards;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

/* Shimmer effect for luxury feel */
.shimmer-effect {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  animation: shimmer 8s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}
</style>