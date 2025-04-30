<template>
    <section class="py-12">
      <div class="flex flex-col items-center justify-between gap-6 sm:flex-row">
        <div class="text-sm font-light text-[#4a6b5d]">
          Showing {{ paginationStart }} - {{ paginationEnd }} of {{ totalItems }} items
        </div>
        
        <div class="flex items-center gap-3">
          <button
            @click="changePage(1)"
            :disabled="currentPage === 1"
            class="rounded-none border border-[#d7e5dc] p-2 text-[#1c3a2e] hover:bg-[#e3efe7] hover:border-[#0a5c3e] disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="First page"
          >
            <chevrons-left-icon class="h-4 w-4" />
          </button>
          
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="rounded-none border border-[#d7e5dc] p-2 text-[#1c3a2e] hover:bg-[#e3efe7] hover:border-[#0a5c3e] disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Previous page"
          >
            <chevron-left-icon class="h-4 w-4" />
          </button>
          
          <div class="flex items-center gap-2">
            <div v-for="page in visiblePageNumbers" :key="page" class="flex items-center">
              <button
                v-if="page !== '...'"
                @click="changePage(page)"
                :class="[
                  'h-8 w-8 flex items-center justify-center text-sm font-light',
                  currentPage === page 
                    ? 'bg-[#0a5c3e] text-white' 
                    : 'border border-[#d7e5dc] text-[#1c3a2e] hover:bg-[#e3efe7] hover:border-[#0a5c3e]'
                ]"
              >
                {{ page }}
              </button>
              <span v-else class="px-1 text-[#4a6b5d]">{{ page }}</span>
            </div>
          </div>
          
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="rounded-none border border-[#d7e5dc] p-2 text-[#1c3a2e] hover:bg-[#e3efe7] hover:border-[#0a5c3e] disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Next page"
          >
            <chevron-right-icon class="h-4 w-4" />
          </button>
          
          <button
            @click="changePage(totalPages)"
            :disabled="currentPage === totalPages"
            class="rounded-none border border-[#d7e5dc] p-2 text-[#1c3a2e] hover:bg-[#e3efe7] hover:border-[#0a5c3e] disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Last page"
          >
            <chevrons-right-icon class="h-4 w-4" />
          </button>
        </div>
        
        <div class="flex items-center gap-3">
          <span class="text-sm font-light text-[#4a6b5d]">View</span>
          <select
            v-model="itemsPerPage"
            @change="$emit('items-per-page-change', itemsPerPage)"
            class="rounded-none border border-[#d7e5dc] bg-white px-3 py-2 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none text-sm"
          >
            <option :value="12">12</option>
            <option :value="24">24</option>
            <option :value="36">36</option>
            <option :value="48">48</option>
          </select>
          <span class="text-sm font-light text-[#4a6b5d]">per page</span>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { 
    ChevronRight as ChevronRightIcon, 
    ChevronLeft as ChevronLeftIcon, 
    ChevronsLeft as ChevronsLeftIcon, 
    ChevronsRight as ChevronsRightIcon 
  } from 'lucide-vue-next'
  import { computed, ref, watch } from 'vue'
  
  const props = defineProps({
    currentPage: {
      type: Number,
      required: true
    },
    itemsPerPage: {
      type: Number,
      required: true
    },
    totalItems: {
      type: Number,
      required: true
    }
  })
  
  const emit = defineEmits(['page-change', 'items-per-page-change'])
  
  const itemsPerPage = ref(props.itemsPerPage)
  
  const totalPages = computed(() => Math.ceil(props.totalItems / itemsPerPage.value))
  const paginationStart = computed(() => (props.currentPage - 1) * itemsPerPage.value + 1)
  const paginationEnd = computed(() => Math.min(props.currentPage * itemsPerPage.value, props.totalItems))
  
  const visiblePageNumbers = computed(() => {
    const pages = []
    const totalDisplayPages = 5
    
    if (totalPages.value <= totalDisplayPages) {
      for (let i = 1; i <= totalPages.value; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1)
      
      let startPage = Math.max(2, props.currentPage - 1)
      let endPage = Math.min(totalPages.value - 1, props.currentPage + 1)
      
      if (props.currentPage <= 2) {
        endPage = 4
      } else if (props.currentPage >= totalPages.value - 1) {
        startPage = totalPages.value - 3
      }
      
      if (startPage > 2) {
        pages.push('...')
      }
      
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i)
      }
      
      if (endPage < totalPages.value - 1) {
        pages.push('...')
      }
      
      pages.push(totalPages.value)
    }
    
    return pages
  })
  
  const changePage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
      emit('page-change', page)
    }
  }
  
  watch(() => props.itemsPerPage, (newVal) => {
    itemsPerPage.value = newVal
  })
  </script>