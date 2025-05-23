<template>
  <main class="flex-1">
    <!-- Brand Marquee at Top -->
    <div class="bg-[#0a5c3e] py-3 overflow-hidden border-b border-[#0a5c3e]/20">
      <div class="marquee-container relative h-12 flex items-center">
        <div class="marquee-track flex items-center whitespace-nowrap">
          <div v-for="(brand, index) in brands" :key="index" class="marquee-item mx-6">
            <span class="text-xl font-light tracking-wider text-white/90 hover:text-white transition-colors duration-300">
              {{ brand }}
            </span>
          </div>
          <!-- Duplicate for seamless looping -->
          <div v-for="(brand, index) in brands" :key="'copy-'+index" class="marquee-item mx-6">
            <span class="text-xl font-light tracking-wider text-white/90 hover:text-white transition-colors duration-300">
              {{ brand }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="container px-4 py-8 text-red-600">
      {{ error }}
    </div>

    <!-- Hero Section -->
    <section class="relative min-h-[80vh] flex items-center overflow-hidden bg-[#0a5c3e]">
      <div class="absolute inset-0 bg-[#0a5c3e]/80 md:bg-[#0a5c3e]/50 z-10"></div>
      <div class="absolute inset-0 bg-gradient-to-b md:bg-gradient-to-r from-[#0a5c3e]/90 via-[#0a5c3e]/70 to-transparent z-10"></div>
      
      <div class="container px-4 md:px-8 relative z-20 text-left md:ml-12 lg:ml-24">
        <div class="max-w-xl">
          <span class="inline-block mb-4 text-sm tracking-widest uppercase text-[#e3efe7] font-light">
            Curated Healthy Skincare
          </span>
          
          <!-- New Luxury Brand Name -->
          <div class="mb-6 group">
            <div class="overflow-hidden">
              <h1 class="hero-title text-white font-light tracking-[0.15em] leading-[0.9] transform transition-all duration-500 group-hover:tracking-[0.18em]">
                <span class="block text-[1.1em] mb-1">OZIMA</span>
                <span class="block text-[0.85em] font-thin tracking-[0.3em] opacity-90 border-t border-[#e3efe7]/30 pt-2 w-max">
                  SKIN SHOP
                </span>
              </h1>
            </div>
            <div class="h-px bg-[#e3efe7]/20 w-0 group-hover:w-full transition-all duration-700 delay-100 mt-3"></div>
          </div>
          
          <p class="mb-8 text-[#e3efe7] max-w-md leading-relaxed">
            Discover exquisite skincare curation from the world's most prestigious dermatological brands.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4">
            <RouterLink 
              to="/products" 
              class="inline-flex items-center justify-center rounded-none bg-[#e3efe7] backdrop-blur-sm px-8 text-[#0a5c3e] hover:bg-white text-base py-4 transition-all duration-300 group shadow-lg"
              aria-label="Shop our collection"
            >
              <span class="font-light tracking-wider">SHOP PRODUCTS</span>
              <ArrowRightIcon class="ml-2 h-5 w-5 transform transition-transform duration-300 group-hover:translate-x-1" />
            </RouterLink>
            
            <RouterLink
              to="/about" 
              class="inline-flex items-center justify-center rounded-none bg-transparent border border-[#e3efe7] px-8 text-[#e3efe7] hover:bg-[#e3efe7]/10 text-base py-4 transition-all duration-300 group"
              aria-label="Learn about our story"
            >
              <span class="font-light tracking-wider">ABOUT US</span>
            </RouterLink>
          </div>
        </div>
      </div>
      
      <div class="absolute bottom-8 right-8 hidden md:block z-20">
        <div class="w-24 h-24 border border-[#e3efe7]/50 rounded-full flex items-center justify-center">
          <div class="w-20 h-20 border border-[#e3efe7]/70 rounded-full flex items-center justify-center">
            <div class="w-16 h-16 bg-[#e3efe7]/20 backdrop-blur-sm rounded-full"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Skeleton Loaders -->
    <template v-if="loading">
      <div class="py-12 container px-4">
        <div class="flex space-x-4 overflow-x-auto pb-4">
          <div v-for="i in 4" :key="'category-' + i" class="min-w-[200px] h-[150px] bg-gray-200 animate-pulse rounded"></div>
        </div>
      </div>
      <div class="py-12 container px-4">
        <div class="h-8 w-48 bg-gray-200 animate-pulse mb-6"></div>
        <div class="flex space-x-4 overflow-x-auto pb-4">
          <div v-for="i in 4" :key="'product-' + i" class="min-w-[250px] h-[350px] bg-gray-200 animate-pulse rounded"></div>
        </div>
      </div>
    </template>
    
    <template v-else>
      <ScrollableCategories :categories="collections" />
      <ScrollableProducts 
        :products="newArrivals" 
        title="New Arrivals" 
        @add-to-cart="addToCart"
      />
      <ScrollableProducts
        :products="popularProducts"
        title="Bestsellers"
        @add-to-cart="addToCart"
      />
    </template>

    <!-- About Us Section -->
    <section class="py-16 bg-[#f0f5f1]">
      <div class="container px-4 md:px-6">
        <div class="max-w-4xl mx-auto text-center mb-12">
          <h2 class="text-3xl font-light tracking-wider text-[#1c3a2e] mb-6">
            THE OZIMA EXPERIENCE
          </h2>
          <div class="w-24 h-px bg-[#0a5c3e]/30 mx-auto mb-8"></div>
        </div>

        <div class="grid grid-cols-1 gap-12 md:grid-cols-2">
          <!-- Our Story -->
          <div class="flex flex-col items-center text-center">
            <div class="mb-6 h-20 w-20 min-w-[80px] rounded-full border border-[#d7e5dc] bg-white p-4 flex items-center justify-center">
              <Leaf class="h-10 w-10 text-[#0a5c3e]" />
            </div>
            <h3 class="mb-4 text-xl font-light tracking-wider text-[#1c3a2e]">
              Our Philosophy
            </h3>
            <p class="text-sm text-[#4a6b5d] leading-relaxed">
              At Ozima Skin Shop, we believe true beauty begins with healthy skin. 
              Our authentic skincare boutique brings you meticulously curated 
              products from the world's most trusted brands. Each item is hand-selected 
              by our team of aestheticians for its purity, efficacy, and commitment to 
              sustainable beauty.
            </p>
          </div>

          <!-- Our Products -->
          <div class="flex flex-col items-center text-center">
            <div class="mb-6 h-20 w-20 min-w-[80px] rounded-full border border-[#d7e5dc] bg-white p-4 flex items-center justify-center">
              <Heart class="h-10 w-10 text-[#0a5c3e]" />
            </div>
            <h3 class="mb-4 text-xl font-light tracking-wider text-[#1c3a2e]">
              Authentic Excellence
            </h3>
            <p class="text-sm text-[#4a6b5d] leading-relaxed">
              We partner exclusively with dermatologist-recommended healthy brands to guarantee 
              authenticity. Every product in our collection meets our rigorous standards for 
              clinical results without compromise. Discover why skincare professionals trust 
              us as their source for premium formulations.
            </p>
          </div>

          <!-- Our Location -->
          <div class="flex flex-col items-center text-center">
            <div class="mb-6 h-20 w-20 min-w-[80px] rounded-full border border-[#d7e5dc] bg-white p-4 flex items-center justify-center">
              <Recycle class="h-10 w-10 text-[#0a5c3e]" />
            </div>
            <h3 class="mb-4 text-xl font-light tracking-wider text-[#1c3a2e]">
              Nigeria's Premier Skincare Destination
            </h3>
            <p class="text-sm text-[#4a6b5d] leading-relaxed">
              Ozima Skin Shop is your premier destination for healthy skincare in Lagos, Abuja, 
              Ibadan and across Nigeria. Our experts provide personalized guidance through 
              our exclusive range of products, ensuring you find the perfect match for your 
              unique skin needs. Experience white-glove service and expert advice.
            </p>
          </div>

          <!-- Our Promise -->
          <div class="flex flex-col items-center text-center">
            <div class="mb-6 h-20 w-20 min-w-[80px] rounded-full border border-[#d7e5dc] bg-white p-4 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-10 w-10 text-[#0a5c3e]">
                <path d="M12 2L4 7v10l8 5 8-5V7l-8-5z"></path>
                <path d="M7.5 4.5l9 5M7.5 19.5l9-5"></path>
              </svg>
            </div>
            <h3 class="mb-4 text-xl font-light tracking-wider text-[#1c3a2e]">
              The Ozima Standard
            </h3>
            <p class="text-sm text-[#4a6b5d] leading-relaxed">
              We stand behind every product with our 100% satisfaction guarantee. 
              Enjoy complimentary luxury packaging and expedited shipping across Nigeria.
              Should any product not meet your expectations, our concierge team will 
              ensure a seamless resolution.
            </p>
          </div>
        </div>

        <!-- Signature -->
        <div class="max-w-md mx-auto mt-16 pt-8 border-t border-[#d7e5dc] text-center">
          <p class="text-sm text-[#4a6b5d] italic mb-2">
            "Radiant skin begins with uncompromising quality."
          </p>
          <p class="text-xs text-[#4a6b5d]/80 tracking-widest">
            — OZIMA SKIN SHOP
          </p>
        </div>
      </div>
    </section>

    <!-- Newsletter -->
    <section class="bg-[#e3efe7] py-16">
      <div class="container px-4 md:px-6">
        <div class="mx-auto max-w-md text-center">
          <h2 class="mb-4 text-2xl font-light tracking-wider text-[#1c3a2e] min-h-[40px]">
            Join Our Community
          </h2>
          <p class="mb-6 text-base text-[#4a6b5d] min-h-[60px] flex items-center justify-center">
            Subscribe to receive exclusive offers, skincare tips, and early access to new collections.
          </p>
          <form @submit.prevent="subscribeToNewsletter" class="flex">
            <input
              type="email"
              v-model="email"
              placeholder="Your email address"
              class="flex-1 rounded-none border-[#d7e5dc] bg-white focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none border text-base py-2 px-4 min-w-0"
              required
              aria-label="Email address for newsletter"
            />
            <button 
              type="submit" 
              class="rounded-none bg-[#0a5c3e] hover:bg-[#0b4a33] text-base text-white px-6 py-2 flex items-center min-w-[120px]"
              aria-label="Subscribe to newsletter"
            >
              <span>Subscribe</span>
              <ArrowRightIcon class="ml-2 h-4 w-4" />
            </button>
          </form>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, defineAsyncComponent } from 'vue';
import { useCartStore } from '@/stores/cart';
import { useToastStore } from '@/stores/toast';
import { Leaf, Heart, Recycle, ArrowRight as ArrowRightIcon } from 'lucide-vue-next';
import axios from 'axios';

// Lazy load components
const ScrollableCategories = defineAsyncComponent({
  loader: () => import('@/components/ScrollableCategory.vue'),
  loadingComponent: {
    template: `<div class="flex space-x-4 overflow-x-auto pb-4">
      <div v-for="i in 4" :key="i" class="min-w-[200px] h-[150px] bg-gray-200 animate-pulse rounded"></div>
    </div>`
  }
});

const ScrollableProducts = defineAsyncComponent({
  loader: () => import('@/components/ScrollableProduct.vue'),
  loadingComponent: {
    template: `<div class="flex space-x-4 overflow-x-auto pb-4">
      <div v-for="i in 4" :key="i" class="min-w-[250px] h-[350px] bg-gray-200 animate-pulse rounded"></div>
    </div>`
  }
});

const cartStore = useCartStore();
const toastStore = useToastStore();
const collections = ref([]);
const newArrivals = ref([]);
const popularProducts = ref([]);
const loading = ref(true);
const email = ref('');
const error = ref(null);

// Luxury skincare brands for marquee
const brands = ref([
  "CeraVe", "La Roche-Posay", "The Ordinary", "Dr. Rashel", 
  "Olay", "Neutrogena", "Paula's Choice", "Cetaphil",
  "Eucerin", "Dermalogica", "Kiehl's", "Vichy","Face Fact",
  "Beauty Formula", "Estellin"
]);

const addToCart = (product) => {
  cartStore.addItem(product);
  toastStore.showToast(3000, "Added to cart", "bg-[#0a5c3e] text-white");
};

const subscribeToNewsletter = async () => {
  try {
    if (!email.value) {
      toastStore.showToast(5000, "Please enter a valid email address", "bg-red-500 text-white");
      return;
    }
    toastStore.showToast(5000, `${email.value} successfully subscribed`, "bg-[#0a5c3e] text-white")
    email.value = '';
  } catch (err) {
    console.error('Subscription error:', err);
  }
};

const fetchData = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const [collectionsRes, newArrivalsRes, popularRes] = await Promise.all([
      axios.get('/api/shop/collections/'),
      axios.get('/api/shop/new_arrivals/'),
      axios.get('/api/shop/popular_products/')
    ]);
    
    collections.value = collectionsRes.data || [];
    newArrivals.value = newArrivalsRes.data || [];
    popularProducts.value = popularRes.data || [];
  } catch (err) {
    error.value = 'Failed to load products. Please try again later.';
    console.error('API Error:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  // Inject critical CSS
  const style = document.createElement('style');
  style.textContent = `
    /* Marquee animation */
    .marquee-container {
      overflow: hidden;
    }
    .marquee-track {
      animation: marquee 25s linear infinite;
      display: inline-block;
    }
    .marquee-item {
      display: inline-block;
    }
    @keyframes marquee {
      0% {
        transform: translateX(0);
      }
      100% {
        transform: translateX(-50%);
      }
    }
    
    /* Hero title animations */
    .hero-title {
      font-family: "Cormorant Garamond", "Times New Roman", serif;
      text-shadow: 0 2px 12px rgba(0, 0, 0, 0.25);
      letter-spacing: 0.05em;
      font-weight: 300;
      line-height: 1;
      font-size: clamp(2.8rem, 7vw, 5.5rem);
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    @supports (background-clip: text) or (-webkit-background-clip: text) {
      .hero-title:hover span:first-child {
        background: linear-gradient(90deg, #e3efe7 10%, #d4a373 50%, #e3efe7 90%);
        background-size: 200% auto;
        color: transparent;
        background-clip: text;
        -webkit-background-clip: text;
        animation: shine 3s linear infinite;
      }
    }
    
    @keyframes shine {
      to {
        background-position: 200% center;
      }
    }
  `;
  document.head.appendChild(style);
  
  if ('requestIdleCallback' in window) {
    requestIdleCallback(fetchData, { timeout: 2000 });
  } else {
    setTimeout(fetchData, 100);
  }
});
</script>

<style scoped>
/* Optimized animations */
.animate-pulse {
  will-change: opacity;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

/* CLS improvements */
[class*="min-h-"] {
  content-visibility: auto;
}

/* Optimize transitions */
.transform {
  will-change: transform;
}

/* Mobile-specific contrast improvements */
@media (max-width: 767px) {
  .hero-title {
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  }
  [class*="text-[#e3efe7]"] {
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  }
}
</style>