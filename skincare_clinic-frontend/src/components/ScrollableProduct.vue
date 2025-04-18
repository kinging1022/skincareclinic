<template>
    <section class="bg-white py-16">
      <div class="container px-4 md:px-6">
        <div class="mb-8 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
          <h2 class="text-2xl font-light tracking-wider text-[#1c3a2e] md:text-3xl">{{ title }}</h2>
          <div class="flex w-full flex-col gap-4 sm:w-auto sm:flex-row sm:items-center">
            <div class="flex gap-2 self-end sm:self-auto">
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
        </div>
  
        <div
          ref="scrollContainer"
          class="flex gap-4 overflow-x-auto pb-4 scrollbar-hide snap-x"
          style="scrollbar-width: none; -ms-overflow-style: none"
        >
          <div
            v-for="product in products"
            :key="product.name"
            class="group flex-shrink-0 snap-start"
            style="width: calc(100% / 2.5); min-width: 160px; max-width: 240px"
          >
            <div class="mb-4 aspect-square overflow-hidden bg-[#e3efe7]">
              <img
                :src="product.get_thumbnail"
                :alt="product.name"
                class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
              />
            </div>
            <RouterLink :to="{name:'product-detail', params:{slug:product.slug}}">
              <h3 class="mb-1 text-base font-medium text-[#1c3a2e] line-clamp-1">{{ product.brand.name }}</h3>
              <p class="mb-2 text-sm text-[#0a5c3e]">{{ product.name }}</p>
              <p class="text-base font-medium text-[#1c3a2e]">₦ {{ product.price }}</p>
            </RouterLink>
            <div class="mt-4">
                <button 
                  @click="addToCart(product)" 
                  v-if="product.stock > 0"
                  class="w-full py-2.5 border border-[#0a5c3e] text-[#0a5c3e] hover:bg-[#0a5c3e] hover:text-white transition-colors duration-300 text-sm font-medium tracking-wider flex items-center justify-center"
                >
                  <shopping-cart-icon class="h-4 w-4 mr-2" />
                  ADD TO CART
                </button>
                <button 
                  v-else
                  disabled
                  class="w-full py-2.5 border border-[#d7e5dc] text-[#4a6b5d] cursor-not-allowed text-sm font-medium tracking-wider flex items-center justify-center"
                >
                  OUT OF STOCK
                </button>
            </div>
          </div>
        </div>
  
        <div class="mt-8 flex justify-center" v-if="showViewAll">
          <RouterLink to='/shop' class="rounded-none border border-[#0a5c3e] bg-transparent px-8 text-[#0a5c3e] hover:bg-[#e3efe7] text-base py-6">
            View All Products
          </RouterLink>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  import { ChevronRight as ChevronRightIcon, ChevronLeft as ChevronLeftIcon, ShoppingCart as ShoppingCartIcon } from 'lucide-vue-next'
  import { RouterLink } from 'vue-router'
  
  export default {
    name: 'ScrollableProducts',
    components: {
      ChevronRightIcon,
      ChevronLeftIcon,
      ShoppingCartIcon,
      RouterLink
    },
    props: {
      products: {
        type: Array,
        required: true
      },
      title: {
        type: String,
        default: 'Bestsellers'
      },
      showViewAll: {
        type: Boolean,
        default: true
      }
    },
    methods: {
      scroll(direction) {
        const scrollAmount = direction === 'left' ? -300 : 300
        this.$refs.scrollContainer.scrollBy({ left: scrollAmount, behavior: 'smooth' })
      },
      addToCart(product) {
        this.$emit('add-to-cart', product)
      }
    }
  }
  </script>
  
  <style scoped>
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
  </style>