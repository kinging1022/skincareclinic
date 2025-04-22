<template>
  <main class="flex-1">
    <!-- Enhanced Animated Hero Section without Images -->
    <section class="relative overflow-hidden">
      <!-- Gradient Background with Animation -->
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
            class="absolute inset-0 h-full w-full transition-opacity duration-1000"
            :class="slide.gradient"
          >
            <!-- SVG Pattern Overlay -->
            <div class="absolute inset-0 opacity-10">
              <component :is="slide.pattern" class="h-full w-full text-white"></component>
            </div>
          </div>
        </transition-group>
        
        <!-- Elegant Moving Line Decoration -->
        <div class="absolute inset-0">
          <div class="elegant-line-top"></div>
          <div class="elegant-line-bottom"></div>
        </div>
        
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
        
        <!-- Animated Decorative Element -->
        <div class="mb-4 flex justify-center overflow-hidden">
          <div class="luxury-divider" :class="{'animate-expand': animationStarted}">
            <SparklesIcon class="h-5 w-5 text-white opacity-80" />
          </div>
        </div>
        
        <!-- Animated Headline -->
        <div class="overflow-hidden mb-4">
          <transition 
            name="slide-up" 
            mode="out-in"
          >
            <h1 
              :key="currentHeadline" 
              class="max-w-3xl text-4xl font-light tracking-wide md:text-5xl lg:text-6xl drop-shadow-sm luxury-font"
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
        
        <!-- Fixed CTA Button (Always Visible) -->
        <RouterLink 
          to="/shop" 
          class="rounded-none bg-transparent border border-white px-8 text-white hover:bg-white hover:text-[#0a5c3e] text-base py-4 transition-all duration-300 opacity-0 flex items-center group"
          :class="{'animate-fade-in-delay': animationStarted}"
        >
          <span>Shop Collection</span>
          <ArrowRightIcon class="ml-2 h-5 w-5 transform transition-transform duration-300 group-hover:translate-x-1" />
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
            <div class="mb-4 h-16 w-16 rounded-full border border-[#d7e5dc] bg-white p-4 transform transition-transform hover:scale-105">
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
            <button class="rounded-none bg-[#0a5c3e] hover:bg-[#0b4a33] text-base text-white px-6 py-2 flex items-center">
              <span>Subscribe</span>
              <ArrowRightIcon class="ml-2 h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { Leaf, Heart, Recycle, ArrowRight, Sparkles } from 'lucide-vue-next'
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
    ArrowRightIcon: ArrowRight,
    SparklesIcon: Sparkles,
    CirclePattern: {
      template: `
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <pattern id="circlePattern" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
            <circle cx="20" cy="20" r="1" fill="currentColor" />
          </pattern>
          <rect x="0" y="0" width="100%" height="100%" fill="url(#circlePattern)" />
        </svg>
      `
    },
    WavePattern: {
      template: `
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <pattern id="wavePattern" x="0" y="0" width="100" height="30" patternUnits="userSpaceOnUse">
            <path d="M0,15 C20,5 35,25 50,15 C65,5 80,25 100,15 L100,30 L0,30 Z" fill="currentColor" opacity="0.3" />
          </pattern>
          <rect x="0" y="0" width="100%" height="100%" fill="url(#wavePattern)" />
        </svg>
      `
    },
    GridPattern: {
      template: `
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <pattern id="gridPattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M20,0 L0,0 L0,20" stroke="currentColor" stroke-width="0.5" fill="none" />
          </pattern>
          <rect x="0" y="0" width="100%" height="100%" fill="url(#gridPattern)" />
        </svg>
      `
    },
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
          gradient: 'bg-gradient-to-r from-[#0a5c3e] to-[#1c3a2e]',
          pattern: 'CirclePattern'
        },
        {
          id: 2,
          gradient: 'bg-gradient-to-r from-[#0c4a33] to-[#0a3c28]',
          pattern: 'WavePattern'
        },
        {
          id: 3,
          gradient: 'bg-gradient-to-tr from-[#0a3c28] via-[#0b4a33] to-[#0c5c3e]',
          pattern: 'GridPattern'
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
        console.error('Error fetching new arrivals:', error)
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
    }
  },
  mounted() {
    this.getCollections()
    this.getFeaturedProducts()
    this.getNewArrivals()
    
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
/* Import luxury font */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Playfair+Display:wght@400;500&display=swap');

/* Applying luxury font */
.luxury-font {
  font-family: 'Playfair Display', serif;
}

.brand-name {
  font-family: 'Cormorant Garamond', serif;
  letter-spacing: 0.3em;
}

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

/* Elegant moving line decorations */
.elegant-line-top {
  position: absolute;
  top: 40px;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.3) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  animation: slideLeft 20s infinite linear;
}

.elegant-line-bottom {
  position: absolute;
  bottom: 40px;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.3) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  animation: slideRight 20s infinite linear;
}

@keyframes slideLeft {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(-100%);
  }
}

@keyframes slideRight {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Luxury divider */
.luxury-divider {
  position: relative;
  width: 0;
  height: 2px;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.8) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
}

.animate-expand {
  animation: expandWidth 1.2s forwards ease-out 0.8s;
}

@keyframes expandWidth {
  0% {
    width: 0;
  }
  100% {
    width: 100px;
  }
}
</style>