<template>
    <div class="bg-white p-4 rounded-lg shadow-md">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">Filters</h2>
      
      <div class="mb-4">
        <h3 class="font-medium text-gray-700 mb-2">Price Range</h3>
        <div class="flex items-center">
          <input type="number" v-model="minPrice" placeholder="Min" class="w-20 px-2 py-1 border rounded-md mr-2" />
          <span>-</span>
          <input type="number" v-model="maxPrice" placeholder="Max" class="w-20 px-2 py-1 border rounded-md ml-2" />
        </div>
      </div>
      
      <div class="mb-4">
        <h3 class="font-medium text-gray-700 mb-2">Product Type</h3>
        <div v-for="type in productTypes" :key="type" class="flex items-center mb-2">
          <input type="checkbox" :id="type" :value="type" v-model="selectedTypes" class="mr-2" />
          <label :for="type" class="text-gray-600">{{ type }}</label>
        </div>
      </div>
      
      <div class="mb-4">
        <h3 class="font-medium text-gray-700 mb-2">Skin Concern</h3>
        <div v-for="concern in skinConcerns" :key="concern" class="flex items-center mb-2">
          <input type="checkbox" :id="concern" :value="concern" v-model="selectedConcerns" class="mr-2" />
          <label :for="concern" class="text-gray-600">{{ concern }}</label>
        </div>
      </div>
      
      <button @click="applyFilters" class="w-full bg-emerald-500 text-white py-2 rounded-md hover:bg-emerald-600 transition-colors">
        Apply Filters
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'FilterSection',
    data() {
      return {
        minPrice: '',
        maxPrice: '',
        productTypes: ['Serum', 'Cream', 'Toner', 'Cleanser', 'Mask'],
        selectedTypes: [],
        skinConcerns: ['Dryness', 'Acne', 'Aging', 'Dullness', 'Uneven Texture'],
        selectedConcerns: []
      }
    },
    methods: {
      applyFilters() {
        // Implement filter logic here
        console.log('Applying filters:', {
          priceRange: { min: this.minPrice, max: this.maxPrice },
          types: this.selectedTypes,
          concerns: this.selectedConcerns
        })
        // Emit an event with the filter data to be handled by the parent component
        this.$emit('filter', {
          priceRange: { min: this.minPrice, max: this.maxPrice },
          types: this.selectedTypes,
          concerns: this.selectedConcerns
        })
      }
    }
  }
  </script>