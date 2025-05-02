<template>
  <main class="flex-1">
    <!-- Hero Section -->
    <section class="relative">
      <div class="flex h-[70vh] w-full flex-col items-center justify-center bg-gradient-to-b from-[#0a5c3e] to-[#1c7d56] px-4 text-center text-white">
        <h1 class="mb-4 max-w-3xl text-4xl font-light tracking-wide md:text-5xl lg:text-6xl drop-shadow-sm">
          The Skincare Clinic - Nigeria's Trusted Skincare Retailer
        </h1>
        <p class="mb-8 max-w-md text-base font-light md:text-lg drop-shadow-sm">
          Authentic products from global brands with expert guidance for every skin type
        </p>
        <RouterLink 
          to="/products" 
          class="rounded-none bg-white/20 hover:bg-white/30 px-8 py-3 text-sm backdrop-blur-sm border border-white/30 transition-all font-medium"
          aria-label="Browse all skincare products"
        >
          Shop Authentic Products
        </RouterLink>
      </div>
    </section>

    <!-- Brand Story Section -->
    <section class="py-16 bg-white">
      <div class="container px-4 md:px-6 mx-auto max-w-4xl">
        <h2 class="text-3xl font-medium text-[#1c3a2e] mb-6 text-center">About The Skincare Clinic</h2>
        
        <div class="prose text-[#4a6b5d]">
          <p class="text-lg mb-6">
            Welcome to The Skincare Clinic, Nigeria's leading online skincare retail shop dedicated to providing authentic 
            skincare products from trusted global brands. We understand that healthy, radiant skin starts with the right 
            products and we're here to help you find them.
          </p>

          <h3 class="text-2xl font-medium text-[#1c3a2e] mb-4">Your Destination for Genuine Skincare Brands</h3>
          <p class="mb-6">
            At The Skincare Clinic, we are committed to offering 100% original skincare products sourced directly from 
            reputable manufacturers and authorized distributors. We stock a wide range of dermatologist-recommended brands 
            including:
          </p>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div 
              v-for="(brand, index) in featuredBrands" 
              :key="index" 
              class="bg-[#f8faf9] p-4 rounded-lg text-center"
            >
              <h4 class="font-medium text-[#1c3a2e]">{{ brand }}</h4>
            </div>
          </div>

          <h3 class="text-2xl font-medium text-[#1c3a2e] mb-4">Why Shop With Us?</h3>
          <div class="grid md:grid-cols-2 gap-6 mb-8">
            <div v-for="(benefit, index) in benefits" :key="index" class="flex items-start">
              <div class="mr-4 mt-1 flex-shrink-0">
                <CheckCircle class="h-6 w-6 text-[#0a5c3e]" />
              </div>
              <div>
                <h4 class="font-medium text-[#1c3a2e] mb-1">{{ benefit.title }}</h4>
                <p class="text-[#4a6b5d]">{{ benefit.description }}</p>
              </div>
            </div>
          </div>

          <h3 class="text-2xl font-medium text-[#1c3a2e] mb-4">A Mission Rooted in Skin Health</h3>
          <p class="mb-6">
            At The Skincare Clinic, we believe skincare is self-care. Our mission is to empower Nigerians with access to 
            affordable, high-quality skincare solutions that actually work. Every product we offer is selected with care, 
            backed by science, and trusted by skin professionals worldwide.
          </p>

          <div class="bg-[#f0f5f1] p-6 rounded-lg">
            <h4 class="text-xl font-medium text-[#1c3a2e] mb-3">Join Thousands of Happy Customers</h4>
            <p>
              From Lagos to Abuja, Port Harcourt to Kaduna, thousands of Nigerians trust The Skincare Clinic for their 
              daily skincare needs. Join our growing community and enjoy a clearer, brighter, and healthier complexion one 
              product at a time.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Skin Conditions Section - Original Routing Maintained -->
    <section class="py-16 bg-[#f0f5f1]">
      <div class="container px-4 md:px-6">
        <h2 class="mb-12 text-center text-2xl font-medium tracking-wider text-[#1c3a2e]">Solutions For Your Skin Concerns</h2>
        <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div 
            v-for="(condition, index) in skinConditions" 
            :key="index" 
            class="bg-white p-8 text-center rounded-none border border-[#d7e5dc] hover:shadow-lg transition-shadow"
          >
            <h3 class="mb-4 text-xl font-medium text-[#1c3a2e]">{{ condition.name }}</h3>
            <p class="mb-4 text-[#4a6b5d] font-light">
              {{ condition.description }}
            </p>
            <RouterLink 
              :to="{ name: 'collections', params: { slug: condition.slug } }"
              class="inline-block text-sm text-[#0a5c3e] hover:underline font-medium"
              :aria-label="'View products for ' + condition.name"
            >
              View Recommended Products →
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="py-16 bg-white">
      <div class="container px-4 md:px-6">
        <h2 class="mb-12 text-center text-2xl font-medium tracking-wider text-[#1c3a2e]">What Our Customers Say</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div 
            v-for="(testimonial, index) in testimonials" 
            :key="index" 
            class="bg-white p-6 rounded-lg border border-[#d7e5dc]"
          >
            <div class="flex items-center mb-4">
              <div class="h-12 w-12 rounded-full mr-4 bg-[#e3efe7] flex items-center justify-center text-[#0a5c3e]">
                <component :is="testimonial.icon" class="h-6 w-6" />
              </div>
              <div>
                <h4 class="font-medium text-[#1c3a2e]">{{ testimonial.name }}</h4>
                <div class="flex">
                  <Star v-for="i in 5" :key="i" class="h-4 w-4 text-yellow-400" />
                </div>
                <div class="text-xs text-[#4a6b5d] mt-1">{{ testimonial.location }}</div>
              </div>
            </div>
            <p class="text-[#4a6b5d]">
              "{{ testimonial.text }}"
            </p>
            <div class="mt-3 text-sm text-[#4a6b5d]">
              Used: <span class="font-medium">{{ testimonial.product }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Final CTA -->
    <section class="bg-[#e3efe7] py-16">
      <div class="container px-4 md:px-6">
        <div class="mx-auto max-w-3xl text-center">
          <h2 class="mb-4 text-2xl font-light tracking-wider text-[#1c3a2e]">Ready for Healthier Skin?</h2>
          <p class="mb-8 text-base text-[#4a6b5d] font-light">
            Join thousands of Nigerians who trust us for authentic skincare products and expert advice.
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <RouterLink 
              to="/products" 
              class="inline-block rounded-none bg-[#0a5c3e] hover:bg-[#0b4a33] text-base text-white px-8 py-3 transition-colors"
            >
              Shop Now
            </RouterLink>
            <a
              href="https://linktr.ee/The_skincare_clinic" 
              class="inline-block rounded-none border border-[#0a5c3e] text-[#0a5c3e] hover:bg-[#0a5c3e]/10 text-base px-8 py-3 transition-colors"
            >
              Chat with Our Experts
            </a>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router'
import { 
  Star, CheckCircle, ShieldCheck, Heart, 
  User, User2, UserCircle, Truck
} from 'lucide-vue-next'

export default {
  name: 'AboutView',
  components: {
    RouterLink,
    Star,
    CheckCircle,
    ShieldCheck,
    Heart,
    User,
    User2,
    UserCircle,
    Truck
  },
  data() {
    return {
      featuredBrands: [
        "CeraVe",
        "The Ordinary", 
        "Neutrogena",
        "La Roche-Posay",
        "Cetaphil",
        "Skinceuticals",
        "Paula's Choice",
        "Eucerin"
      ],
      benefits: [
        {
          title: "Authenticity Guaranteed",
          description: "We only sell genuine skincare products, no counterfeits, no imitations."
        },
        {
          title: "Expert Support",
          description: "Get personalized recommendations from our skincare experts."
        },
        {
          title: "Fast Nationwide Delivery",
          description: "We deliver across all 36 states in Nigeria."
        },
        {
          title: "Safe Online Shopping",
          description: "Secure payment gateways and easy-to-use website."
        }
      ],
      skinConditions: [
        {
          name: "Hyperpigmentation",
          description: "Our dermatologist-recommended products reduce dark spots and even skin tone with proven ingredients like vitamin C and niacinamide.",
          slug: "hyper-pigmentation"
        },
        {
          name: "Acne & Breakouts",
          description: "Gentle yet effective acne solutions that combat breakouts without irritation. We carry treatments for all acne severity levels.",
          slug: "acne-and-breakout"
        },
        {
          name: "Dry/Dehydrated Skin",
          description: "Intensive hydration solutions with ceramides and hyaluronic acid to restore your skin's moisture barrier and prevent water loss.",
          slug: "dry-and-dehydrated-skin"
        }
      ],
      testimonials: [
        {
          name: "Amina K.",
          location: "Lagos",
          text: "Finally found authentic CeraVe products in Nigeria! My skin has never been better.",
          product: "CeraVe Moisturizing Cream",
          icon: User
        },
        {
          name: "Chinedu O.",
          location: "Abuja",
          text: "The Ordinary products arrived perfectly packaged. Customer service helped me choose the right products.",
          product: "The Ordinary Niacinamide",
          icon: User2
        },
        {
          name: "Folake S.",
          location: "Port Harcourt",
          text: "La Roche-Posay cleared my acne in weeks. Will never buy skincare from anywhere else.",
          product: "La Roche-Posay Effaclar",
          icon: UserCircle
        }
      ]
    }
  }
}
</script>

<style scoped>
.prose {
  line-height: 1.75;
}

.prose h2, .prose h3, .prose h4 {
  color: #1c3a2e;
  margin-bottom: 1rem;
  font-weight: 500;
}

.prose p {
  margin-bottom: 1.5rem;
}

/* Smooth transitions */
a, button {
  transition: all 0.3s ease;
}

/* Focus states for accessibility */
a:focus, button:focus {
  @apply outline-none ring-2 ring-[#0a5c3e] ring-opacity-50;
}
</style>