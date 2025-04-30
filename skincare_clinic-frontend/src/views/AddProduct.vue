<template>
    <div class="min-h-screen bg-white">
      <!-- Form Header -->
      <div class="relative overflow-hidden">
        <div class="py-12 relative z-10 text-white" 
             :style="{ backgroundImage: 'linear-gradient(rgba(10, 60, 40, 0.65), rgba(10, 60, 40, 0.65))' }">
          <div class="container mx-auto px-4 text-center">
            <h2 class="text-3xl md:text-4xl font-light tracking-wide mb-3">Add New Product</h2>
            <p class="max-w-2xl mx-auto text-base font-light md:text-lg">Fill out the form to add a new product to your store</p>
          </div>
        </div>
      </div>
  
      <!-- Main Form Section -->
      <section class="py-8 md:py-12 bg-white">
        <div class="container mx-auto px-4 md:px-6">
          <div v-if="loading" class="text-center py-20">
            <div class="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-[#0a5c3e] border-r-4 border-[#0a5c3e] border-b-4 border-[#0a5c3e] border-l-4 border-[#d7e5dc]"></div>
            <p class="mt-6 text-lg text-[#4a6b5d] font-light">Loading form data...</p>
          </div>
  
          <form v-else @submit.prevent="submitForm" class="max-w-4xl mx-auto">
            <!-- Basic Information -->
            <div class="mb-8 p-6 border border-[#d7e5dc] bg-[#f0f5f1]">
              <h3 class="text-xl font-medium text-[#1c3a2e] mb-4">Product Information</h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Name -->
                <div class="flex flex-col">
                  <label class="text-sm font-medium text-[#4a6b5d] mb-1">Product Name *</label>
                  <input 
                    v-model="product.name"
                    type="text" 
                    required
                    class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none"
                  >
                </div>
  
                <!-- Price -->
                <div class="flex flex-col">
                  <label class="text-sm font-medium text-[#4a6b5d] mb-1">Price *</label>
                  <input 
                    v-model.number="product.price"
                    type="number" 
                    min="0"
                    step="0.01"
                    required
                    class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none"
                  >
                </div>
  
                <!-- Category -->
                <div class="flex flex-col">
                  <label class="text-sm font-medium text-[#4a6b5d] mb-1">Category *</label>
                  <select
                    v-model="product.category"
                    required
                    class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none"
                  >
                    <option value="" disabled>Select a category</option>
                    <option v-for="category in categories" :key="category.id" :value="category.id">
                      {{ category.name }}
                    </option>
                  </select>
                </div>
  
                <!-- Brand -->
                <div class="flex flex-col">
                  <label class="text-sm font-medium text-[#4a6b5d] mb-1">Brand *</label>
                  <select
                    v-model="product.brand"
                    required
                    class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none"
                  >
                    <option value="" disabled>Select a brand</option>
                    <option v-for="brand in brands" :key="brand.id" :value="brand.id">
                      {{ brand.name }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
  
            <!-- Collections Section -->
            <div class="mb-8 p-6 border border-[#d7e5dc] bg-[#f0f5f1]">
              <h3 class="text-xl font-medium text-[#1c3a2e] mb-4">Collections</h3>
              <p class="text-sm text-[#4a6b5d] mb-4">Select which collections this product belongs to</p>
              
              <!-- Collections Grid -->
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                <div v-for="collection in collections" :key="collection.id" class="flex items-center">
                  <input
                    type="checkbox"
                    :id="'collection-' + collection.id"
                    :value="collection.id"
                    v-model="product.collections"
                    class="h-4 w-4 text-[#0a5c3e] focus:ring-[#0a5c3e] border-[#d7e5dc] rounded-none"
                  >
                  <label :for="'collection-' + collection.id" class="ml-2 text-sm text-[#1c3a2e]">
                    {{ collection.name }}
                  </label>
                </div>
              </div>
            </div>
  
            <!-- Image Upload -->
            <div class="mb-8 p-6 border border-[#d7e5dc] bg-[#f0f5f1]">
              <h3 class="text-xl font-medium text-[#1c3a2e] mb-4">Product Image</h3>
              
              <div class="flex flex-col items-center">
                <div v-if="previewImage" class="mb-4">
                  <img :src="previewImage" alt="Preview" class="max-w-full h-48 object-contain border border-[#d7e5dc]">
                </div>
                
                <label class="cursor-pointer">
                  <span class="rounded-none bg-[#0a5c3e] px-6 py-3 text-white hover:bg-[#0b4a33] text-sm font-medium tracking-wider inline-block mb-2">
                    {{ product.image ? 'Change Image' : 'Upload Image' }}
                  </span>
                  <input 
                    type="file" 
                    @change="handleImageUpload"
                    accept="image/*"
                    class="hidden"
                  >
                </label>
                <p class="text-xs text-[#4a6b5d] mt-1">Recommended size: 800x800px, WEBP format preferred</p>
              </div>
            </div>
  
            <!-- Additional Details -->
            <div class="mb-8 p-6 border border-[#d7e5dc] bg-[#f0f5f1]">
              <h3 class="text-xl font-medium text-[#1c3a2e] mb-4">Additional Details</h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Description -->
                <div class="flex flex-col md:col-span-2">
                  <label class="text-sm font-medium text-[#4a6b5d] mb-1">Description</label>
                  <textarea
                    v-model="product.description"
                    rows="4"
                    class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none"
                  ></textarea>
                </div>
  
                <!-- Stock -->
                <div class="flex flex-col">
                  <label class="text-sm font-medium text-[#4a6b5d] mb-1">Stock Quantity</label>
                  <input 
                    v-model.number="product.stock"
                    type="number" 
                    min="0"
                    class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none"
                  >
                </div>
  
                <!-- Weight -->
                <div class="flex flex-col">
                  <label class="text-sm font-medium text-[#4a6b5d] mb-1">Weight (grams)</label>
                  <input 
                    v-model.number="product.weight"
                    type="number" 
                    min="0"
                    step="0.01"
                    class="rounded-none border border-[#d7e5dc] bg-white px-4 py-3 text-[#1c3a2e] focus:ring-[#0a5c3e] focus:border-[#0a5c3e] outline-none"
                  >
                </div>
  
                <!-- Toggles -->
                <div class="flex flex-col md:col-span-2">
                  <div class="flex items-center space-x-4">
                    <div class="flex items-center">
                      <input
                        type="checkbox"
                        id="available"
                        v-model="product.available"
                        class="h-4 w-4 text-[#0a5c3e] focus:ring-[#0a5c3e] border-[#d7e5dc] rounded-none"
                      >
                      <label for="available" class="ml-2 text-sm text-[#1c3a2e]">
                        Available for purchase
                      </label>
                    </div>
  
                    <div class="flex items-center">
                      <input
                        type="checkbox"
                        id="featured"
                        v-model="product.featured"
                        class="h-4 w-4 text-[#0a5c3e] focus:ring-[#0a5c3e] border-[#d7e5dc] rounded-none"
                      >
                      <label for="featured" class="ml-2 text-sm text-[#1c3a2e]">
                        Featured product
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Form Actions -->
            <div class="flex flex-col sm:flex-row justify-end gap-4">
              <button
                type="button"
                @click="$router.back()"
                class="rounded-none border border-[#0a5c3e] px-6 py-3 text-[#0a5c3e] hover:bg-[#e3efe7] text-sm font-medium tracking-wider"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="rounded-none bg-[#0a5c3e] px-6 py-3 text-white hover:bg-[#0b4a33] text-sm font-medium tracking-wider disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="submitting">Saving...</span>
                <span v-else>Save Product</span>
              </button>
            </div>
          </form>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useToastStore } from '@/stores/toast'
  import axios from 'axios'
  
  const toastStore = useToastStore()
  
  // Form state
  const product = ref({
    name: '',
    category: '',
    brand: '',
    collections: [],
    description: '',
    price: 0,
    image: null,
    stock: 0,
    weight: 0,
    available: true,
    featured: false
  })
  
  const previewImage = ref(null)
  const submitting = ref(false)
  const loading = ref(true)
  
  // Data lists
  const categories = ref([])
  const brands = ref([])
  const collections = ref([])
  
  // Fetch initial data
  onMounted(async () => {
    try {
      const [categoriesRes, brandsRes, collectionsRes] = await Promise.all([
        axios.get('/api/shop/categories/'),
        axios.get('/api/shop/brands/'),
        axios.get('/api/shop/collections/')
      ])
      
      categories.value = categoriesRes.data
      brands.value = brandsRes.data
      collections.value = collectionsRes.data
      loading.value = false
    } catch (error) {
      console.error('Error loading form data:', error)
      toastStore.showError('Failed to load form data')
    }
  })
  
  // Handle image upload
  const handleImageUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      product.value.image = file
      
      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        previewImage.value = e.target.result
      }
      reader.readAsDataURL(file)
    }
  }
  
  // Reset form to initial state
  const resetForm = () => {
    product.value = {
      name: '',
      category: '',
      brand: '',
      collections: [],
      description: '',
      price: 0,
      image: null,
      stock: 0,
      weight: 0,
      available: true,
      featured: false
    }
    previewImage.value = null
  }
  
  // Submit form
  const submitForm = async () => {
    submitting.value = true
    
    try {
      const formData = new FormData()
      
      // Append all product data to formData
      Object.keys(product.value).forEach(key => {
        if (key === 'collections') {
          product.value.collections.forEach(collectionId => {
            formData.append('collections', collectionId)
          })
        } else if (key === 'image' && product.value.image) {
          formData.append('image', product.value.image)
        } else if (product.value[key] !== null && product.value[key] !== undefined) {
          formData.append(key, product.value[key])
        }
      })
      
      const response = await axios.post('/api/products/create/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      // Show success message
      const message = `Product ${response.data.name} created successfully!`
      toastStore.showToast(5000,message, "bg-[#0a5c3e] text-white")
      
      // Clear the form
      resetForm()
      
    } catch (error) {
      console.error('Error saving product:', error)
      toastStore.showToast(5000,error.response?.data?.message || 'Failed to create product',"bg-red text-white")
    } finally {
      submitting.value = false
    }
  }
  </script>
  
  <style scoped>
  input[type="text"],
  input[type="number"],
  textarea,
  select {
    transition: all 0.3s ease;
  }
  
  input[type="text"]:focus,
  input[type="number"]:focus,
  textarea:focus,
  select:focus {
    box-shadow: 0 0 0 2px rgba(10, 92, 62, 0.1);
  }
  
  input[type="checkbox"] {
    border-radius: 0;
  }
  
  @media (max-width: 640px) {
    .grid-cols-2 {
      grid-template-columns: 1fr;
    }
  }
  </style>