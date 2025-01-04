<template>
    <section class="py-12 md:py-16 bg-white product-slider">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-2xl md:text-3xl font-bold text-emerald-800 mb-8">
          {{ title }}
        </h2>
        <div ref="sliderContainer" class="slider-container scroll-smooth cursor-grab overflow-x-auto hide-scrollbar">
          <div class="flex gap-5 min-w-max">
            <div
              v-for="product in products"
              :key="product.id"
              class="w-[280px] flex-none group cursor-pointer"
            >
              <div class="relative aspect-square overflow-hidden rounded-lg mb-4">
                <img
                  :src="product.get_thumbnail"
                  :alt="product.name"
                  class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-300"
                />
              </div>
              <RouterLink :to="{name:'product-detail', params:{slug:product.slug}}"><h3 v-if="product.brand" class="text-lg font-medium text-gray-800 mb-2">
                {{ product.brand.name }}
              </h3>
              <p class="text-lg font-small text-gray-600 mb-2">
                {{ product.name }}
              </p>
              <p class="text-emerald-700 font-medium">{{ product.price }}</p></RouterLink>
            </div>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: "ProductSlider",
    props: {
      title: {
        type: String,
        required: true,
      },
      products: {
        type: Array,
        required: true,
      },
    },
    mounted() {
      this.initializeSlider();
    },
    beforeUnmount() {
      this.cleanUpListeners();
    },
    methods: {
      initializeSlider() {
        const container = this.$refs.sliderContainer;
        this.isDown = false;
        this.startX = 0;
        this.scrollLeft = 0;
  
        // Event listeners
        this.onMouseDown = (e) => {
          this.isDown = true;
          container.style.cursor = "grabbing";
          this.startX = e.pageX - container.offsetLeft;
          this.scrollLeft = container.scrollLeft;
        };
  
        this.onMouseLeave = () => {
          this.isDown = false;
          container.style.cursor = "grab";
        };
  
        this.onMouseUp = () => {
          this.isDown = false;
          container.style.cursor = "grab";
        };
  
        this.onMouseMove = (e) => {
          if (!this.isDown) return;
          e.preventDefault();
          const x = e.pageX - container.offsetLeft;
          const walk = (x - this.startX) * 2; // Adjust scroll speed
          container.scrollLeft = this.scrollLeft - walk;
        };
  
        this.onTouchStart = (e) => {
          this.isDown = true;
          this.startX = e.touches[0].pageX - container.offsetLeft;
          this.scrollLeft = container.scrollLeft;
        };
  
        this.onTouchEnd = () => {
          this.isDown = false;
        };
  
        this.onTouchMove = (e) => {
          if (!this.isDown) return;
          e.preventDefault();
          const x = e.touches[0].pageX - container.offsetLeft;
          const walk = (x - this.startX) * 2; // Adjust scroll speed
          container.scrollLeft = this.scrollLeft - walk;
        };
  
        // Attach event listeners
        container.addEventListener("mousedown", this.onMouseDown);
        container.addEventListener("mouseleave", this.onMouseLeave);
        container.addEventListener("mouseup", this.onMouseUp);
        container.addEventListener("mousemove", this.onMouseMove);
        container.addEventListener("touchstart", this.onTouchStart);
        container.addEventListener("touchend", this.onTouchEnd);
        container.addEventListener("touchmove", this.onTouchMove);
      },
      cleanUpListeners() {
        const container = this.$refs.sliderContainer;
  
        // Remove event listeners
        container.removeEventListener("mousedown", this.onMouseDown);
        container.removeEventListener("mouseleave", this.onMouseLeave);
        container.removeEventListener("mouseup", this.onMouseUp);
        container.removeEventListener("mousemove", this.onMouseMove);
        container.removeEventListener("touchstart", this.onTouchStart);
        container.removeEventListener("touchend", this.onTouchEnd);
        container.removeEventListener("touchmove", this.onTouchMove);
      },
    },
  };
  </script>
  
  <style scoped>
  .hide-scrollbar::-webkit-scrollbar {
    display: none;
  }
  .hide-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  .scroll-smooth {
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
  }
  .slider-container {
    position: relative;
    user-select: none;
    touch-action: pan-y pinch-zoom;
  }
  </style>
  