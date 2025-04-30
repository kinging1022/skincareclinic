<template>
  <section class="py-16">
    <div class="container px-4 md:px-6">
      <div class="mb-8 flex items-center justify-between">
        <h2 class="text-2xl font-light tracking-wider text-[#1c3a2e] md:text-3xl">Curated Collections</h2>
        <div class="flex gap-2">
          <button
            class="rounded-full border border-[#d7e5dc] hover:bg-[#e3efe7] hover:border-[#0a5c3e] p-2 transition-colors duration-200"
            @click="scroll('left')"
            aria-label="Scroll left"
          >
            <ChevronLeftIcon class="h-4 w-4 text-[#1c3a2e]" />
          </button>
          <button
            class="rounded-full border border-[#d7e5dc] hover:bg-[#e3efe7] hover:border-[#0a5c3e] p-2 transition-colors duration-200"
            @click="scroll('right')"
            aria-label="Scroll right"
          >
            <ChevronRightIcon class="h-4 w-4 text-[#1c3a2e]" />
          </button>
        </div>
      </div>

      <div
        ref="scrollContainer"
        class="flex gap-4 overflow-x-auto pb-4 scrollbar-hide snap-x"
        style="scrollbar-width: none; -ms-overflow-style: none"
      >
        <RouterLink
          v-for="category in categories"
          :key="category.id"
          :to="{ name: 'collections', params: {slug: category.slug } }"
          class="relative flex-shrink-0 w-[200px] sm:w-[240px] md:w-[280px] snap-start"
        >
          <!-- Aspect ratio container with placeholder -->
          <div class="aspect-[3/4] w-full bg-[#e3efe7] overflow-hidden">
            <img
              :src="category.get_thumbnail"
              :alt="category.name"
              loading="lazy"
              width="280"
              height="373"
              class="h-full w-full object-cover transition-opacity duration-300"
              :class="{ 'opacity-0': !imageLoaded[category.id] }"
              @load="imageLoaded[category.id] = true"
            />
            <div 
              v-if="!imageLoaded[category.id]"
              class="absolute inset-0 bg-[#e3efe7] animate-pulse"
            ></div>
          </div>
          
          <div class="absolute inset-0 flex flex-col items-center justify-end bg-gradient-to-t from-[#0a5c3e]/60 to-transparent p-6 text-white">
            <h3 class="mb-2 text-lg font-light tracking-wide line-clamp-2 text-center">{{ category.name }}</h3>
            <span class="flex items-center text-sm font-light">
              Explore <ChevronRightIcon class="ml-1 h-3 w-3" />
            </span>
          </div>
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ChevronRight as ChevronRightIcon, ChevronLeft as ChevronLeftIcon } from 'lucide-vue-next'
import { ref } from 'vue'

const props = defineProps({
  categories: {
    type: Array,
    required: true,
    validator: (value) => {
      return value.every(item => item.id && item.name && item.slug && item.get_thumbnail)
    }
  }
})

const scrollContainer = ref(null)
const imageLoaded = ref({})

const scroll = (direction) => {
  if (!scrollContainer.value) return
  
  const scrollAmount = direction === 'left' ? -300 : 300
  scrollContainer.value.scrollBy({ 
    left: scrollAmount, 
    behavior: 'smooth' 
  })
}

// Initialize image loaded state
props.categories.forEach(category => {
  imageLoaded.value[category.id] = false
})
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
}

.animate-pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>