<template>
  <main class="flex-1">
    <!-- Hero Section with Schema Markup -->
    <section class="relative" itemscope itemtype="https://schema.org/WebPage">
      <div class="flex h-[70vh] w-full flex-col items-center justify-center bg-gradient-to-b from-[#0a5c3e] to-[#1c7d56] px-4 text-center text-white">
        <h1 class="mb-4 max-w-3xl text-4xl font-light tracking-wide md:text-5xl lg:text-6xl drop-shadow-sm" itemprop="headline">
          Best Skin Care Products in Nigeria
        </h1>
        <p class="mb-8 max-w-md text-base font-light md:text-lg drop-shadow-sm" itemprop="description">
          Clinically effective skincare products formulated for healthy, glowing skin. Shop authentic brands with expert guidance.
        </p>
      </div>
    </section>

    <!-- Our Story Section with Organization Schema -->
    <section class="py-16 bg-white" itemscope itemtype="https://schema.org/Organization">
      <div class="container px-4 md:px-6">
        <div class="mx-auto max-w-4xl text-center">
          <h2 class="mb-4 text-2xl font-medium tracking-wider text-[#1c3a2e]">Redefining Skin Care in Nigeria</h2>
          <div class="mb-12 h-px w-24 bg-[#d7e5dc] mx-auto"></div>
          <p class="mb-8 text-lg text-[#4a6b5d] font-light leading-relaxed" itemprop="description">
            Welcome to <span itemprop="name">Skin Care Clinic</span>, Nigeria's trusted online destination for dermatologist recommended skincare. 
            We combine scientific formulations with personalized advice to help you achieve your healthiest skin. 
            Our carefully curated collection features only authentic products from world leading brands.
          </p>
          <p class="text-lg text-[#4a6b5d] font-light leading-relaxed">
            Specializing in treating <span itemprop="medicalSpecialty">hyperpigmentation</span>, <span itemprop="medicalSpecialty">acne</span>, 
            and <span itemprop="medicalSpecialty">dry skin</span>, we offer:
          </p>
          <ul class="mt-4 text-left inline-block text-[#4a6b5d]">
            <li class="mb-2 flex items-start">
              <svg class="h-5 w-5 text-[#0a5c3e] mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Affordable skincare consultations
            </li>
            <li class="mb-2 flex items-start">
              <svg class="h-5 w-5 text-[#0a5c3e] mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Nationwide delivery
            </li>
            <li class="flex items-start">
              <svg class="h-5 w-5 text-[#0a5c3e] mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              100% authentic products guarantee
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Expertise Section with MedicalBusiness Schema -->
    <section class="py-16 bg-[#f0f5f1]" itemscope itemtype="https://schema.org/MedicalBusiness">
      <div class="container px-4 md:px-6">
        <h2 class="mb-12 text-center text-2xl font-medium tracking-wider text-[#1c3a2e]">View special Collections</h2>
        <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div 
            v-for="(condition, index) in skinConditions" 
            :key="index" 
            class="bg-white p-8 text-center rounded-none border border-[#d7e5dc] hover:shadow-lg transition-shadow"
            itemprop="medicalSpecialty"
          >
            <h3 class="mb-4 text-xl font-medium text-[#1c3a2e]">{{ condition.name }}</h3>
            <p class="mb-4 text-[#4a6b5d] font-light">
              {{ condition.description }}
            </p>
            <RouterLink 
              :to="{ name: 'collections', params: {slug: condition.slug} }"
              class="inline-block text-sm text-[#0a5c3e] hover:underline font-medium"
              :aria-label="'View products for ' + condition.name"
            >
              View Recommended Products →
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Choose Us -->
    <section class="py-16 bg-white">
      <div class="container px-4 md:px-6">
        <div class="mx-auto max-w-4xl">
          <h2 class="mb-12 text-center text-2xl font-medium tracking-wider text-[#1c3a2e]">Why Choose Skin Care Clinic?</h2>
          <div class="space-y-8">
            <div 
              v-for="(reason, index) in reasons" 
              :key="index" 
              class="flex items-start bg-[#f8faf9] p-6 rounded-lg"
            >
              <div class="mr-6 mt-1 flex h-12 w-12 items-center justify-center rounded-full bg-[#0a5c3e] text-white flex-shrink-0">
                <component :is="reason.icon" class="h-6 w-6" />
              </div>
              <div>
                <h3 class="mb-2 text-lg font-medium text-[#1c3a2e]">{{ reason.title }}</h3>
                <p class="text-[#4a6b5d] font-light">
                  {{ reason.description }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="py-16 bg-[#f0f5f1]">
      <div class="container px-4 md:px-6">
        <h2 class="mb-12 text-center text-2xl font-medium tracking-wider text-[#1c3a2e]">What Our Customers Say</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div 
            v-for="(testimonial, index) in testimonials" 
            :key="index" 
            class="bg-white p-6 rounded-lg shadow-sm"
            itemscope itemtype="https://schema.org/Review"
          >
            <div class="flex items-center mb-4">
              <div class="h-12 w-12 rounded-full mr-4 bg-[#e3efe7] flex items-center justify-center text-[#0a5c3e]">
                <component :is="testimonial.icon" class="h-6 w-6" />
              </div>
              <div>
                <h4 class="font-medium text-[#1c3a2e]" itemprop="author">{{ testimonial.name }}</h4>
                <div class="flex">
                  <Star v-for="i in 5" :key="i" class="h-4 w-4 text-yellow-400" />
                </div>
              </div>
            </div>
            <p class="text-[#4a6b5d]" itemprop="reviewBody">
              "{{ testimonial.text }}"
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="bg-[#e3efe7] py-16">
      <div class="container px-4 md:px-6">
        <div class="mx-auto max-w-3xl text-center">
          <h2 class="mb-4 text-2xl font-light tracking-wider text-[#1c3a2e]">Start Your Journey to Healthier Skin Today</h2>
          <p class="mb-8 text-base text-[#4a6b5d] font-light">
            Join thousands of satisfied customers who trust Skin Care Clinic for their skincare needs.
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <RouterLink 
              to="/shop" 
              class="inline-block rounded-none bg-[#0a5c3e] hover:bg-[#0b4a33] text-base text-white px-8 py-3 transition-colors"
              aria-label="Shop our skincare products"
            >
              Shop Now
            </RouterLink>
            <a
              href="https://linktr.ee/The_skincare_clinic" 
              class="inline-block rounded-none border border-[#0a5c3e] text-[#0a5c3e] hover:bg-[#0a5c3e]/10 text-base px-8 py-3 transition-colors"
              aria-label="Book a skincare consultation"
            >
              Get Personalized Advice
            </a>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router'
import { Star, CheckCircle, ShieldCheck, Heart, User, User2, UserCircle } from 'lucide-vue-next'

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
    UserCircle
  },
  data() {
    return {
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
      reasons: [
        {
          title: "Expert-Recommended Products",
          description: "Every product in our collection is vetted by skincare professionals for efficacy and safety across all skin types.",
          icon: CheckCircle
        },
        {
          title: "100% Authentic Guarantee",
          description: "We source directly from brands and authorized distributors to ensure you receive only genuine products.",
          icon: ShieldCheck
        },
        {
          title: "Personalized Skincare Guidance",
          description: "Our team provides customized routine recommendations based on your specific skin concerns and goals.",
          icon: Heart
        }
      ],
      testimonials: [
        {
          name: "Amina K.",
          text: "The hyperpigmentation products transformed my skin in just 8 weeks. I've never found such effective products in Nigeria before!",
          icon: User
        },
        {
          name: "Chinedu O.",
          text: "Finally an online store with authentic products! My acne has improved dramatically since using their recommendations.",
          icon: User2
        },
        {
          name: "Folake S.",
          text: "The personalized consultation helped me understand my dry skin better. The products they suggested worked wonders.",
          icon: UserCircle
        }
      ]
    }
  }
}
</script>

<style scoped>
/* Improved transitions and focus states */
a, button {
  transition: all 0.3s ease;
}

/* Better focus accessibility */
a:focus, button:focus {
  @apply outline-none ring-2 ring-[#0a5c3e] ring-opacity-50;
}

/* Smooth hover effects */
.hover-effect {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-effect:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(10, 92, 62, 0.1);
}
</style>