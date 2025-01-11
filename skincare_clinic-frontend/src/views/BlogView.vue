<template>
      <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          <article
            v-for="post in blogPosts"
            :key="post.id"
            class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
          >
            <img
              :src="post.image"
              :alt="post.title"
              class="h-48 w-full object-cover"
            />
            <div class="p-6">
              <div class="flex items-center space-x-2 mb-2">
                <span class="px-2 py-1 bg-emerald-50 text-emerald-600 text-xs font-medium rounded">
                  {{ post.category }}
                </span>
                <span class="text-sm text-gray-500">{{ post.readTime }}</span>
              </div>
              <h2 class="text-xl font-semibold text-gray-800 mb-2">
                {{ post.title }}
              </h2>
              <p class="text-gray-600 mb-4">{{ post.excerpt }}</p>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-500">{{ post.date }}</span>
                <button class="text-emerald-600 hover:text-emerald-500 font-medium">
                  Read More →
                </button>
              </div>
            </div>
          </article>
        </div>
      </main>
  </template>
  
  <script>
  import { Search, Menu } from 'lucide-vue-next'
  
  export default {
    name: 'App',
    components: {
      Search,
      Menu
    },
    data() {
      return {
        blogPosts: [
          {
            id: 1,
            title: "The Ultimate Guide to Double Cleansing",
            excerpt:
              "Discover why double cleansing is the key to achieving clear, glowing skin...",
            image:
              "https://images.unsplash.com/photo-1556228720-195a672e8a03?ixlib=rb-4.0.1&auto=format&fit=crop&w=800&q=80",
            category: "Skincare Routine",
            readTime: "5 min read",
            date: "Oct 15, 2023",
          },
          {
            id: 2,
            title: "Understanding Your Skin Barrier",
            excerpt:
              "Learn how to protect and strengthen your skin's natural barrier function...",
            image:
              "https://images.unsplash.com/photo-1570554886111-e80fcca6a029?ixlib=rb-4.0.1&auto=format&fit=crop&w=800&q=80",
            category: "Skin Health",
            readTime: "7 min read",
            date: "Oct 12, 2023",
          },
          {
            id: 3,
            title: "The Power of Natural Ingredients",
            excerpt:
              "Explore the benefits of incorporating natural ingredients in your skincare routine...",
            image:
              "https://images.unsplash.com/photo-1576426863848-c21f53c60b19?ixlib=rb-4.0.1&auto=format&fit=crop&w=800&q=80",
            category: "Natural Beauty",
            readTime: "6 min read",
            date: "Oct 10, 2023",
          },
          {
            id: 4,
            title: "Nighttime Skincare Rituals",
            excerpt:
              "Create the perfect evening routine for rejuvenated, glowing skin...",
            image:
              "https://images.unsplash.com/photo-1567721913486-6585f069b332?ixlib=rb-4.0.1&auto=format&fit=crop&w=800&q=80",
            category: "Skincare Routine",
            readTime: "8 min read",
            date: "Oct 8, 2023",
          },
        ],
      }
    }
  }
  </script>
  
  <style scoped>
  /* Add any component-specific styles here */
  </style>