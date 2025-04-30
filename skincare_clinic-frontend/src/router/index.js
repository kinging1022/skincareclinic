import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'


// Track preloaded components to avoid duplicate loading
const preloadedComponents = new Set()

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import(/* webpackChunkName: "home" */ '../views/HomeView.vue'),
      meta: { 
        preload: true,
        scrollBehavior: { top: 0, behavior: 'instant' }
      }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
      meta: { scrollBehavior: { top: 0, behavior: 'smooth' } }
    },
    {
      path: '/shop',
      name: 'shop',
      component: () => import(/* webpackChunkName: "shop" */ '@/views/ShopView.vue'),
      meta: { 
        preload: true,
        scrollBehavior: { top: 0, behavior: 'smooth' }
      }
    },
    {
      path: '/collections/:slug',
      name: 'collections',
      component: () => import(/* webpackChunkName: "collections" */ '@/views/Collections.vue'),
      meta: { scrollBehavior: { top: 0, behavior: 'smooth' } }
    },
    {
      path: '/shop/product/:slug',
      name: 'product-detail',
      component: () => import(/* webpackChunkName: "product" */ '@/views/ProductDetailView.vue'),
      meta: { 
        preload: true,
        scrollBehavior: { top: 0, behavior: 'smooth' }
      }
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import(/* webpackChunkName: "cart" */ '@/views/CartView.vue'),
      meta: { 
        noScroll: true,
        transition: 'slide-up' 
      }
    },
    {
      path: '/track-order',
      name: 'track-order',
      component: () => import(/* webpackChunkName: "tracking" */ '@/views/TrackingView.vue'),
      meta: { scrollBehavior: { top: 0, behavior: 'smooth' } }
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: () => import(/* webpackChunkName: "checkout" */ '@/views/CheckoutView.vue'),
      meta: { 
        preload: true,
        scrollBehavior: { top: 0, behavior: 'instant' },
      }
    },
    {
      path: '/payment-success/:id',
      name: 'payment-success',
      component: () => import(/* webpackChunkName: "payment" */ '@/views/PaymentSuccess.vue'),
      meta: { 
        noScroll: true,
        transition: 'fade' 
      }
    },
    {
      path: '/payment-failed',
      name: 'payment-failed',
      component: () => import(/* webpackChunkName: "payment" */ '@/views/PaymentFailed.vue'),
      meta: { 
        noScroll: true,
        transition: 'fade' 
      }
    },
    {
      path: '/blog',
      name: 'blog',
      component: () => import(/* webpackChunkName: "blog" */ '@/views/BlogView.vue'),
      meta: { scrollBehavior: { top: 0, behavior: 'smooth' } }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import(/* webpackChunkName: "analytics" */ '@/views/AnalyticsView.vue'),
      meta: { 
        scrollBehavior: { top: 0, behavior: 'instant' }
      }
    },
    {
      path: '/search',
      name: 'search',
      component: () => import(/* webpackChunkName: "search" */ '@/views/SearchView.vue'),
      meta: { scrollBehavior: { top: 0, behavior: 'instant' },
      hideNavigation: true // Add this custom meta field

    }
    },
    {
      path: '/admin/login',
      name: 'login',
      component: () => import(/* webpackChunkName: "auth" */ '@/views/LoginView.vue'),
      meta: { 
        requiresAuth: false,
        hideForAuth: true
      }
    },
    {
      path: '/admin/add-product',
      name: 'add-product',

      component: () => import(/* webpackChunkName: "addproduct" */ '@/views/AddProduct.vue'),
      meta: { 
        requiresAuth: false,
      }
    },
    {
      path: '/shipping-policy',
      name: 'shipping-policy',
      component: () => import(/* webpackChunkName: "policy" */ '@/views/ShippingPolicy.vue'),
      meta: { scrollBehavior: { top: 0, behavior: 'smooth' } }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import(/* webpackChunkName: "error" */ '@/views/NotFound.vue'),
      meta: { 
        scrollBehavior: { top: 0, behavior: 'instant' },
        layout: 'error'
      }
    }
  ],
  
  scrollBehavior(to, from, savedPosition) {
    return new Promise((resolve) => {
      // Route-specific override
      if (to.meta?.scrollBehavior) {
        return resolve(to.meta.scrollBehavior)
      }

      // No-scroll routes
      if (to.meta?.noScroll) {
        return resolve(false)
      }

      // Anchor links
      if (to.hash) {
        setTimeout(() => {
          const el = document.querySelector(to.hash)
          if (el) {
            const headerHeight = document.querySelector('header')?.offsetHeight || 0
            const y = el.getBoundingClientRect().top + window.scrollY - headerHeight
            resolve({ top: y, behavior: 'smooth' })
          }
          resolve({ top: 0, behavior: 'smooth' })
        }, 600)
        return
      }

      // Back/forward navigation
      if (savedPosition) {
        setTimeout(() => resolve(savedPosition), 50)
        return
      }

      // Default behavior
      setTimeout(() => {
        resolve({ 
          top: 0, 
          behavior: to.meta?.scrollBehavior?.behavior || 'smooth' 
        })
      }, 150)
    })
  }
})

// Unified route guard
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // Initialize the store if not already done
  if (!userStore.initialized) {
    await userStore.initStore()
  }

  // Preload marked routes
  if (to.meta?.preload) {
    to.matched.forEach(record => {
      const component = record.components?.default
      if (typeof component === 'function' && !preloadedComponents.has(component)) {
        preloadedComponents.add(component)
        component()
      }
    })
  }

  // Check authentication status
  const isAuthenticated = userStore.isAuthenticated

  // Redirect to login if auth required but not authenticated
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({
      name: 'login',
      query: { redirect: to.fullPath }
    })
  }

  // Redirect away from login if already authenticated
  if (to.meta.hideForAuth && isAuthenticated) {
    return next(to.query.redirect || '/analytics')
  }


  // Handle 404
  if (!to.matched.length) {
    return next({ name: 'not-found' })
  }

  next()
})


export default router