<template>
    <section class="py-16">
      <div class="container px-4 md:px-6">
        <div class="mb-8 flex items-center justify-between">
          <h2 class="text-2xl font-light tracking-wider text-[#1c3a2e] md:text-3xl">Curated Collections</h2>
          <div class="flex gap-2">
            <button
              class="rounded-full border border-[#d7e5dc] hover:bg-[#e3efe7] hover:border-[#0a5c3e] p-2"
              @click="scroll('left')"
            >
              <chevron-left-icon class="h-4 w-4 text-[#1c3a2e]" />
            </button>
            <button
              class="rounded-full border border-[#d7e5dc] hover:bg-[#e3efe7] hover:border-[#0a5c3e] p-2"
              @click="scroll('right')"
            >
              <chevron-right-icon class="h-4 w-4 text-[#1c3a2e]" />
            </button>
          </div>
        </div>
  
        <div
          ref="scrollContainer"
          class="flex gap-4 overflow-x-auto pb-4 scrollbar-hide snap-x"
          style="scrollbar-width: none; -ms-overflow-style: none"
          @scroll="handleScroll"
        >
          <RouterLink
            :to="{ name: 'collections', params: { collections_name:category.name, slug: category.slug} }"
            v-for="(category, index) in categories"
            :key="category.name"
            class="group relative flex-shrink-0 overflow-hidden snap-start"
            style="width: calc(100% / 1.5); min-width: 200px; max-width: 280px"
            ref="categoryItems"
          >
            <div class="aspect-[3/4] w-full overflow-hidden bg-[#e3efe7]">
              <img
                v-if="shouldLoadImage(index)"
                :src="category.get_thumbnail"
                :alt="category.name"
                loading="lazy"
                class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                @load="imageLoaded(index)"
                @error="imageError(index)"
              />
              <div v-else class="h-full w-full flex items-center justify-center">
                <div class="w-8 h-8 rounded-full border-2 border-t-transparent border-[#0a5c3e] animate-spin"></div>
              </div>
            </div>
            <div class="absolute inset-0 flex flex-col items-center justify-end bg-gradient-to-t from-[#0a5c3e]/60 to-transparent p-6 text-white">
              <h3 class="mb-2 text-lg font-light tracking-wide line-clamp-2 text-center">{{ category.name }}</h3>
              <span class="flex items-center text-sm font-light">
                Explore <chevron-right-icon class="ml-1 h-3 w-3" />
              </span>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  import { ChevronRight as ChevronRightIcon, ChevronLeft as ChevronLeftIcon } from 'lucide-vue-next'
  import { RouterLink } from 'vue-router'
  
  export default {
    name: 'ScrollableCategories',
    components: {
      ChevronRightIcon,
      ChevronLeftIcon,
      RouterLink
    },
    props: {
      categories: {
        type: Array,
        required: true
      }
    },
    data() {
      return {
        visibleItems: new Set([0, 1, 2]), // Initially load first 3 items
        loadedImages: new Set(),
        observer: null,
        isScrolling: false,
        scrollTimer: null
      }
    },
    mounted() {
      this.setupIntersectionObserver()
      
      // Add resize event listener
      window.addEventListener('resize', this.updateVisibleItems)
      // Initial calculation
      this.updateVisibleItems()
    },
    beforeUnmount() {
      // Clean up
      if (this.observer) {
        this.observer.disconnect()
      }
      window.removeEventListener('resize', this.updateVisibleItems)
    },
    methods: {
      scroll(direction) {
        const scrollAmount = direction === 'left' ? -300 : 300
        this.$refs.scrollContainer.scrollBy({ left: scrollAmount, behavior: 'smooth' })
      },
      setupIntersectionObserver() {
        if ('IntersectionObserver' in window) {
          this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
              if (entry.isIntersecting) {
                const index = Array.from(this.$refs.categoryItems).indexOf(entry.target)
                if (index !== -1) {
                  this.visibleItems.add(index)
                  
                  // Preload adjacent images
                  if (index > 0) this.visibleItems.add(index - 1)
                  if (index < this.categories.length - 1) this.visibleItems.add(index + 1)
                }
              }
            })
          }, {
            root: this.$refs.scrollContainer,
            rootMargin: '100px',
            threshold: 0.1
          })
          
          // Wait for nextTick to ensure refs are available
          this.$nextTick(() => {
            if (this.$refs.categoryItems) {
              const items = Array.isArray(this.$refs.categoryItems) 
                ? this.$refs.categoryItems 
                : [this.$refs.categoryItems]
              
              items.forEach(item => {
                if (item) this.observer.observe(item)
              })
            }
          })
        }
      },
      shouldLoadImage(index) {
        return this.visibleItems.has(index)
      },
      imageLoaded(index) {
        this.loadedImages.add(index)
      },
      imageError(index) {
        console.error(`Failed to load image at index ${index}`)
        // Add fallback handling if needed
      },
      handleScroll() {
        // Debounce scroll events
        if (!this.isScrolling) {
          this.isScrolling = true
          
          if (this.scrollTimer) clearTimeout(this.scrollTimer)
          
          this.scrollTimer = setTimeout(() => {
            this.updateVisibleItems()
            this.isScrolling = false
          }, 100)
        }
      },
      updateVisibleItems() {
        if (!this.$refs.scrollContainer || !this.$refs.categoryItems) return
        
        const container = this.$refs.scrollContainer
        const containerWidth = container.clientWidth
        const scrollLeft = container.scrollLeft
        
        // Calculate visible range with buffer
        const startVisible = scrollLeft - 300
        const endVisible = scrollLeft + containerWidth + 300
        
        const items = Array.isArray(this.$refs.categoryItems) 
          ? this.$refs.categoryItems 
          : [this.$refs.categoryItems]
          
        items.forEach((item, index) => {
          if (!item) return
          
          const itemLeft = item.offsetLeft
          const itemRight = itemLeft + item.offsetWidth
          
          // Check if the item is visible
          if (itemRight >= startVisible && itemLeft <= endVisible) {
            this.visibleItems.add(index)
          }
        })
      }
    }
  }
  </script>
  
  <style scoped>
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
  
  @keyframes placeholder-pulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 0.8; }
  }
  
  img[loading] {
    background-color: #e3efe7;
  }
  </style>