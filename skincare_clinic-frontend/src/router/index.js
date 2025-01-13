import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ShopView from '@/views/ShopView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import CartView from '@/views/CartView.vue'
import TrackingView from '@/views/TrackingView.vue'
import CheckoutView from '@/views/CheckoutView.vue'
import PaymentSuccess from '@/views/PaymentSuccess.vue'
import PaymentFailed from '@/views/PaymentFailed.vue'
import BlogView from '@/views/BlogView.vue'
import AnalyticsView from '@/views/AnalyticsView.vue'
import SearchView from '@/views/SearchView.vue'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/shop',
      name: 'shop',
      component: ShopView,
    },
    {
      path: '/shop/:slug',
      name: 'product-detail',
      component: ProductDetailView,
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView,
    },
    {
      path: '/track-order',
      name: 'track-order',
      component: TrackingView,
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: CheckoutView,
    },
    {
      path: '/payment-success/:id',
      name: 'payment-success',
      component: PaymentSuccess,
    },
    {
      path: '/payment-failed',
      name: 'payment-failed',
      component: PaymentFailed,
    },
    {
      path: '/blog',
      name: 'blog',
      component: BlogView,
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: AnalyticsView,
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/admin/login',
      name: 'login',
      component: LoginView,
    },
  ],
})

export default router
