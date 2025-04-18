<template>
  <main class="flex-1">
    <!-- Hero Section -->
    <section class="relative">
      <div
        class="flex h-[70vh] w-full flex-col items-center justify-center bg-cover bg-center px-4 text-center text-white"
        :style="{
          backgroundImage:
            'linear-gradient(rgba(10, 60, 40, 0.65), rgba(10, 60, 40, 0.65)), url(' + blogHeroImage + ')'
        }"
      >
        <h1 class="mb-4 max-w-3xl text-4xl font-light tracking-wide md:text-5xl lg:text-6xl drop-shadow-sm">
          The Science of Beautiful Skin
        </h1>
        <p class="mb-8 max-w-md text-base font-light md:text-lg drop-shadow-sm">
          Expert insights, skincare breakthroughs, and beauty rituals for radiant health
        </p>
      </div>
    </section>

    <!-- Coming Soon Section -->
    <section class="py-32 bg-white">
      <div class="container px-4 md:px-6">
        <div class="mx-auto max-w-2xl text-center">
          <!-- Animated Coming Soon Text -->
          <div class="relative mb-12 inline-block">
            <span class="relative z-10 text-5xl md:text-7xl font-light tracking-wider text-[#1c3a2e]">
              COMING SOON
            </span>
            <div class="absolute -bottom-2 left-0 h-1 w-full bg-[#0a5c3e] animate-pulse"></div>
          </div>

          <div class="mb-12 h-px w-24 bg-[#d7e5dc] mx-auto"></div>
          
          <p class="mb-8 text-xl text-[#4a6b5d] font-light leading-relaxed">
            We're crafting something extraordinary—a sanctuary of skincare wisdom where science meets beauty.
          </p>
          
          <!-- Countdown Animation -->
          <div class="mb-12 flex justify-center space-x-4">
            <div v-for="(item, index) in countdown" :key="index" class="flex flex-col items-center">
              <div class="flex h-16 w-16 items-center justify-center rounded-full border-2 border-[#0a5c3e] text-2xl font-medium text-[#1c3a2e]">
                {{ item.value }}
              </div>
              <span class="mt-2 text-xs uppercase text-[#4a6b5d]">{{ item.label }}</span>
            </div>
          </div>

          <p class="mb-8 text-lg text-[#4a6b5d] font-light leading-relaxed">
            Subscribe to be the first to access our expert articles on:
          </p>
          
          <!-- Topics Grid -->
          <div class="mb-12 grid grid-cols-2 gap-4 md:grid-cols-4">
            <div v-for="(topic, index) in topics" :key="index" class="rounded-none border border-[#d7e5dc] p-4 text-center">
              <p class="text-sm font-medium text-[#1c3a2e]">{{ topic }}</p>
            </div>
          </div>

          <!-- Newsletter Signup -->
          <div class="mx-auto max-w-md">
            <h3 class="mb-4 text-xl font-light text-[#1c3a2e]">Join Our Beauty Community</h3>
            <div class="flex">
              <input
                type="email"
                placeholder="Your email address"
                class="flex-1 rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-sm text-[#1c3a2e] focus:border-[#0a5c3e] focus:outline-none focus:ring-1 focus:ring-[#0a5c3e]"
              />
              <button class="rounded-none bg-[#0a5c3e] px-6 py-3 text-sm font-medium text-white hover:bg-[#0b4a33]">
                Notify Me
              </button>
            </div>
            <p class="mt-2 text-xs text-[#4a6b5d]">
              We respect your privacy. Unsubscribe at any time.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Preview Section -->
    <section class="bg-[#f0f5f1] py-16">
      <div class="container px-4 md:px-6">
        <h2 class="mb-12 text-center text-2xl font-medium tracking-wider text-[#1c3a2e]">WHAT TO EXPECT</h2>
        <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div v-for="(preview, index) in previews" :key="index" class="bg-white p-8">
            <div class="mb-6 flex h-12 w-12 items-center justify-center rounded-full bg-[#0a5c3e] text-white">
              <component :is="preview.icon" class="h-6 w-6" />
            </div>
            <h3 class="mb-3 text-xl font-medium text-[#1c3a2e]">{{ preview.title }}</h3>
            <p class="text-[#4a6b5d] font-light">
              {{ preview.description }}
            </p>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { PenLine, FlaskConical, Gem } from 'lucide-vue-next'

export default {
  name: 'BlogView',
  components: {
    PenLine,
    FlaskConical,
    Gem
  },
  data() {
    return {
      blogHeroImage: 'https://images.unsplash.com/photo-1498843053639-170ff2715e72?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80',
      countdown: [
        { value: '2', label: 'Weeks' },
        { value: '3', label: 'Days' },
        { value: '12', label: 'Hours' },
        { value: '45', label: 'Minutes' }
      ],
      topics: [
        'Acne Solutions',
        'Anti-Aging',
        'Hyperpigmentation',
        'Sensitive Skin',
        'Product Reviews',
        'Ingredients 101',
        'Skin Barrier',
        'Seasonal Care'
      ],
      previews: [
        {
          title: "Expert Insights",
          description: "Articles written by dermatologists and skincare scientists breaking down complex concepts into practical advice.",
          icon: PenLine
        },
        {
          title: "Science-Backed Guides",
          description: "Evidence-based routines and product recommendations tailored for different skin types and concerns.",
          icon: FlaskConical
        },
        {
          title: "Luxury Skincare Secrets",
          description: "Behind-the-scenes looks at premium formulations and how to get the most from your skincare investment.",
          icon: Gem
        }
      ]
    }
  },
  mounted() {
    // Simulate countdown animation
    setInterval(() => {
      this.countdown[3].value = parseInt(this.countdown[3].value) - 1;
      if (this.countdown[3].value < 0) {
        this.countdown[3].value = '59';
        this.countdown[2].value = parseInt(this.countdown[2].value) - 1;
      }
    }, 60000);
  }
}
</script>

<style scoped>
/* Custom animations */
@keyframes pulse-glow {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}

.animate-pulse {
  animation: pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Hover effects */
.bg-white {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.bg-white:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px -5px rgba(10, 92, 62, 0.1);
}
</style>