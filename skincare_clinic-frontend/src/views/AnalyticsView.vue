<template>
  <div class="min-h-screen bg-gray-50/50">
    <main class="mx-auto">
      <!-- Sub-header -->
      <div id="dashboard" class="section bg-white border-b border-gray-200/50 px-4 sm:px-8 py-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 class="text-2xl font-bold text-gray-800 tracking-tight">Dashboard Overview</h1>
        <div class="flex flex-col sm:flex-row gap-2">
          <div class="flex items-center gap-2">
            <label for="start-date" class="text-sm text-gray-600">From:</label>
            <input type="date" id="start-date" v-model="startDate" class="bg-white border border-gray-200 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 shadow-sm">
          </div>
          <div class="flex items-center gap-2">
            <label for="end-date" class="text-sm text-gray-600">To:</label>
            <input type="date" id="end-date" v-model="endDate" class="bg-white border border-gray-200 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 shadow-sm">
          </div>
          
          <button @click="fetchData" class="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-xl text-sm font-medium transition-colors shadow-sm">
            Apply
          </button>
        </div>
      </div>

      <!-- Export & Actions Bar -->
      <div class="bg-white border-b border-gray-200/50 px-4 sm:px-8 py-3 flex justify-between items-center">
        <div class="text-sm text-gray-500">
          <span v-if="lastUpdated">Last updated: {{ formatDateTime(lastUpdated) }}</span>
          <span v-else>Loading data...</span>
        </div>
        <div class="flex items-center gap-2">
          <button @click="refreshData" class="text-gray-500 hover:text-gray-700 p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <RefreshCw class="h-5 w-5" />
          </button>
          <button @click="printDashboard" class="flex items-center gap-1 text-gray-600 hover:text-gray-800 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors text-sm font-medium">
            <Printer class="h-5 w-5" />
            Print
          </button>
        </div>
      </div>

      <div class="p-4 sm:p-6 lg:p-8">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-6 sm:mb-8">
          <div v-for="stat in stats" :key="stat.label" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="p-4 sm:p-6">
              <div class="flex justify-between items-start">
                <div>
                  <p class="text-sm font-medium text-gray-500 tracking-wide">{{ stat.label }}</p>
                  <p class="text-xl sm:text-2xl font-bold text-gray-900 mt-1 tracking-tight">{{ stat.value }}</p>
                </div>
                <div class="p-2 rounded-lg" :class="stat.bgColor">
                  <component :is="stat.icon" class="h-5 sm:h-6 w-5 sm:w-6" :class="stat.iconColor" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Orders Section -->
        <div id="recent-orders" class="section bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mb-6 sm:mb-8">
          <div class="p-4 sm:p-6 border-b border-gray-100 flex justify-between items-center">
            <h3 class="text-lg font-bold text-gray-800 tracking-tight">Recent Orders</h3>
            <button class="text-xs font-medium text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
              View All <ChevronRight class="h-3 w-3" />
            </button>
          </div>

          <div v-if="orders.length > 0" class="overflow-x-auto">
            <table class="w-full divide-y divide-gray-100 table-fixed">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-16">ID</th>
                  <th scope="col" class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-1/4">Amount</th>
                  <th scope="col" class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-16">Refund</th>
                  <th scope="col" class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-1/3">Action</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-100">
                <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50/50 transition-colors">
                  <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900 tracking-tight">#{{ order.id }}</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900 tracking-tight text-right">{{ formatCurrency(order.order_amount) }}</td>
                  <td class="px-4 py-4 whitespace-nowrap">
                    <div v-if="order.has_refund" class="text-green-500 text-center">
                      <Check class="h-5 w-5 mx-auto" />
                    </div>
                    <div v-else class="text-gray-400 text-center">
                      <Minus class="h-5 w-5 mx-auto" />
                    </div>
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap text-center">
                    <button 
                      v-if="order.status === 0" 
                      @click="updateOrderStatus(order.id, 'set_processed')" 
                      class="px-3 py-1 text-xs font-medium text-white bg-emerald-500 hover:bg-emerald-600 rounded-full transition-colors">
                      Set Processed
                    </button>
                    <button 
                      v-else-if="order.status === 1" 
                      @click="updateOrderStatus(order.id, 'set_shipped')" 
                      class="px-3 py-1 text-xs font-medium text-white bg-blue-500 hover:bg-blue-600 rounded-full transition-colors">
                      Set Shipped
                    </button>
                    <span 
                      v-else-if="order.status === 2" 
                      class="px-3 py-1 text-xs font-medium text-white bg-gray-500 rounded-full">
                      Shipped
                    </span>
                    <span 
                      v-else-if="order.status === 3" 
                      class="px-3 py-1 text-xs font-medium text-white bg-orange-500 rounded-full">
                      Ordered
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="p-8 flex flex-col items-center justify-center text-center">
            <PackageOpen class="h-12 w-12 text-gray-400 mb-4" />
            <h4 class="text-lg font-medium text-gray-700 mb-1 tracking-tight">No recent orders</h4>
            <p class="text-sm text-gray-500 max-w-md">When you receive new orders, they'll appear here</p>
          </div>
        </div>

        <!-- Category Distribution -->
        <div id="analytics" class="section bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mb-6 sm:mb-8">
          <div class="p-4 sm:p-6">
            <h3 class="text-lg font-bold text-gray-800 mb-4 sm:mb-6 tracking-tight">Category Distribution</h3>
            <div class="h-64">
              <template v-if="pieData.length > 0">
                <Chart 
                  type="doughnut"
                  :data="doughnutChartData"
                  :options="chartOptions"
                />
              </template>
              <template v-else>
                <div class="h-full flex items-center justify-center text-gray-400">
                  No category data available
                </div>
              </template>
            </div>
            <div v-if="pieData.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mt-4 sm:mt-6">
              <div v-for="(item, index) in pieData" :key="item.name" class="flex items-center gap-2">
                <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: COLORS[index] }" />
                <span class="text-xs sm:text-sm text-gray-600 tracking-wide">{{ item.name }}</span>
                <span class="text-xs sm:text-sm font-medium text-gray-800 ml-auto tracking-tight">
                  {{ ((item.value / totalCategoryValue) * 100).toFixed(1) }}%
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Products -->
        <div id="products" class="section bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="p-4 sm:p-6 border-b border-gray-100">
            <h3 class="text-lg font-bold text-gray-800 tracking-tight">Top Performing Products</h3>
          </div>
          <div class="divide-y divide-gray-100">
            <div v-for="(product, index) in topProducts" :key="index" class="p-4 sm:p-6 flex items-center gap-2 sm:gap-4 hover:bg-gray-50/50 transition-colors">
              <div class="text-xs sm:text-sm font-medium text-gray-500 w-6 sm:w-8 tracking-tight">{{ index + 1 }}</div>
              <div class="w-10 h-10 sm:w-12 sm:h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                <ShoppingBag class="h-6 w-6 text-gray-400" />
              </div>
              <div class="flex-1 min-w-0">
                <h4 class="font-semibold text-sm sm:text-base text-gray-900 truncate tracking-tight">{{ product.product_name }}</h4>
                <p class="text-xs sm:text-sm text-gray-500 mt-1 tracking-wide">{{ product.category_name || 'Uncategorized' }}</p>
              </div>
              <div class="text-right">
                <p class="font-semibold text-sm sm:text-base text-gray-900 tracking-tight">
                  {{ formatCurrency(product.total_revenue) }}
                </p>
                <p class="text-xs text-gray-500 mt-1 tracking-wide">{{ product.total_quantity.toLocaleString() }} sales</p>
              </div>
              <div class="hidden sm:block w-24">
                <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div class="h-full bg-emerald-500" :style="{ width: `${(product.total_quantity / maxSales) * 100}%` }"></div>
                </div>
              </div>
            </div>
          </div>
          <div class="p-4 sm:p-6 flex justify-center">
            <button class="text-emerald-600 hover:text-emerald-700 text-sm font-medium flex items-center gap-1 tracking-wide">
              View All Products <ChevronRight class="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { 
  ShoppingBag, 
  DollarSign, 
  ChevronRight, 
  PackageOpen, 
  Users, 
  RefreshCw, 
  Printer, 
  Check, 
  Minus 
} from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast';
import axios from 'axios'
import Chart from '@/components/Chart.vue'

// Constants
const COLORS = ["#10B981", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6"]
const CACHE_TTL = 5 * 60 * 1000 // 5 minutes cache TTL
//store
const toastStore = useToastStore();


// State
const startDate = ref(getDefaultStartDate())
const endDate = ref(getDefaultEndDate())
const comparisonPeriod = ref('none')
const pieData = ref([])
const salesData = ref({})
const comparisonData = ref({})
const topProducts = ref([])
const maxSales = ref(0)
const orders = ref([])
const lastUpdated = ref(null)
const isLoading = ref(false)

const cache = reactive({
  data: {},
  timestamp: null
})

// Chart options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const label = context.label || ''
          const value = context.raw || 0
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const percentage = Math.round((value / total) * 100)
          return `${label}: ${percentage}% (${value})`
        }
      }
    }
  },
  cutout: '70%',
  animation: {
    animateScale: true,
    animateRotate: true
  },
  elements: {
    arc: {
      borderWidth: 0
    }
  }
}

// Computed properties
const totalCategoryValue = computed(() => {
  return pieData.value.reduce((sum, item) => sum + item.value, 0)
})

const cacheKey = computed(() => {
  return `${startDate.value}_${endDate.value}_${comparisonPeriod.value}`
})

const doughnutChartData = computed(() => {
  // Ensure we have valid data
  if (!pieData.value || pieData.value.length === 0) {
    return {
      labels: ['No Data'],
      datasets: [{
        data: [1],
        backgroundColor: ['#e5e7eb'],
        borderWidth: 0
      }]
    }
  }

  return {
    labels: pieData.value.map(d => d.name || 'Unnamed'),
    datasets: [{
      data: pieData.value.map(d => Number(d.value) || 0),
      backgroundColor: COLORS,
      borderWidth: 0
    }]
  }
})

const stats = computed(() => {
  const totalRevenue = getTotalRevenue()
  const totalOrders = getTotalOrders()
  const avgOrderValue = getAverageOrderValue()
  
  let revenueComparison = null
  let ordersComparison = null
  let avgOrderComparison = null
  
  if (comparisonPeriod.value !== 'none' && comparisonData.value?.sales_data) {
    const prevRevenue = comparisonData.value.sales_data.total_revenue || 0
    const prevOrders = comparisonData.value.sales_data.total_order || 0
    const prevAvgOrder = prevOrders > 0 ? Math.round(prevRevenue / prevOrders) : 0
    
    revenueComparison = {
      value: prevRevenue,
      percentage: prevRevenue > 0 ? ((totalRevenue - prevRevenue) / prevRevenue) * 100 : 0
    }
    
    ordersComparison = {
      value: prevOrders,
      percentage: prevOrders > 0 ? ((totalOrders - prevOrders) / prevOrders) * 100 : 0
    }
    
    avgOrderComparison = {
      value: prevAvgOrder,
      percentage: prevAvgOrder > 0 ? ((avgOrderValue - prevAvgOrder) / prevAvgOrder) * 100 : 0
    }
  }
  
  return [
    { 
      icon: DollarSign, 
      label: "Total Revenue", 
      value: formatCurrency(totalRevenue),
      comparison: revenueComparison,
      bgColor: 'bg-emerald-500/10',
      iconColor: 'text-emerald-500'
    },
    { 
      icon: ShoppingBag, 
      label: "Total Orders", 
      value: totalOrders.toLocaleString(),
      comparison: ordersComparison,
      bgColor: 'bg-blue-500/10',
      iconColor: 'text-blue-500'
    },
    { 
      icon: ShoppingBag, 
      label: "Avg. Order Value", 
      value: formatCurrency(avgOrderValue),
      comparison: avgOrderComparison,
      bgColor: 'bg-violet-500/10',
      iconColor: 'text-violet-500'
    },
  ]
})

// Helper functions
function getDefaultStartDate() {
  const date = new Date()
  date.setDate(date.getDate() - 30)
  return date.toISOString().split('T')[0]
}

function getDefaultEndDate() {
  return new Date().toISOString().split('T')[0]
}

function formatCurrency(value, isKobo = false) {
  try {
    if (value === null || value === undefined || value === '') {
      return '₦0.00'
    }

    if (typeof value === 'string' && value.includes(',')) {
      value = value.replace(/,/g, '')
    }

    let numericValue = typeof value === 'string' 
      ? parseFloat(value) 
      : Number(value)

    if (isNaN(numericValue)) {
      console.warn('Invalid currency value:', value)
      return '₦0.00'
    }

    if (isKobo) {
      numericValue = numericValue / 100
    }

    return new Intl.NumberFormat('en-NG', {
      style: 'currency',
      currency: 'NGN',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(numericValue)
  } catch (error) {
    console.error('Error formatting currency:', error)
    return '₦0.00'
  }
}


function formatDateTime(dateString) {
  try {
    if (!dateString) return ''
    
    const date = typeof dateString === 'string' 
      ? new Date(dateString) 
      : dateString
    
    return date.toLocaleString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    console.error('Error formatting date time:', error)
    return dateString || ''
  }
}

function getTotalRevenue() {
  if (salesData.value && salesData.value.total_revenue !== undefined) {
    return salesData.value.total_revenue
  }
  return totalCategoryValue.value
}

function getTotalOrders() {
  if (salesData.value && salesData.value.total_order !== undefined) {
    return salesData.value.total_order
  }
  if (!topProducts.value || !Array.isArray(topProducts.value)) return 0
  return topProducts.value.reduce((total, product) => total + product.total_quantity, 0)
}

function getAverageOrderValue() {
  const totalRevenue = getTotalRevenue()
  const totalOrders = getTotalOrders()
  return totalOrders > 0 ? Math.round(totalRevenue / totalOrders) : 0
}

// API calls
async function fetchUnprocessedOrders() {
  try {
    // Use AbortController for cancelable requests
    const controller = new AbortController()
    const signal = controller.signal
    
    const response = await axios.get('/api/unprocessed_orders', { signal })
    orders.value = response.data || []
  } catch (error) {
    if (!axios.isCancel(error)) {
      console.error('Error fetching unprocessed orders:', error)
      orders.value = []
    }
  }
}

async function updateOrderStatus(id,action){
  try {
    const response = await axios.post('/api/update_order_status/', {
      id: id,
      action: action
    })
    if (response.status === 200) {
      fetchUnprocessedOrders()
      toastStore.showToast(3000, response.data.message, 'bg-[#0a5c3e] text-white')
    } else {
      console.error('Error updating order status:', response.data.message)
    }
  } catch (error) {
    console.error('Error updating order status:', error)
  }
  if (error.response) {
    console.error('Error response:', error.response.data)
  } else {
    console.error('Error message:', error.message)
  }

}

function refreshData() {
  Object.keys(cache.data).forEach(key => {
    delete cache.data[key]
  })
  fetchData()
}

async function fetchData() {
  if (isLoading.value) return
  
  isLoading.value = true
  
  try {
    // Check cache first
    if (cache.data[cacheKey.value] && 
        cache.timestamp && 
        (Date.now() - cache.timestamp) < CACHE_TTL) {
      const cachedData = cache.data[cacheKey.value]
      pieData.value = cachedData.category || []
      topProducts.value = cachedData.products || []
      salesData.value = cachedData.sales_data || {}
      comparisonData.value = cachedData.comparison_data || {}
      
      if (topProducts.value.length) {
        maxSales.value = Math.max(...topProducts.value.map(p => p.total_quantity))
      }
      
      lastUpdated.value = new Date(cache.timestamp)
      isLoading.value = false
      return
    }
    
    const params = {
      start_date: startDate.value,
      end_date: endDate.value,
      comparison: comparisonPeriod.value
    }
    
    // Use AbortController for cancelable requests
    const controller = new AbortController()
    const signal = controller.signal
    
    const response = await axios.get('/api/get_analytics', { params, signal })
    
    // Ensure category data exists and is in correct format
    if (response.data?.category) {
      pieData.value = response.data.category.map(item => ({
        name: item.name || 'Unnamed Category',
        value: Number(item.value) || 0
      }))
    } else {
      console.warn('No category data in response')
      pieData.value = []
    }
    
    topProducts.value = response.data.products || []
    salesData.value = response.data.sales_data || {}
    comparisonData.value = response.data.comparison_data || {}
    
    if (topProducts.value.length) {
      maxSales.value = Math.max(...topProducts.value.map(p => p.total_quantity))
    }
    
    cache.data[cacheKey.value] = response.data
    cache.timestamp = Date.now()
    lastUpdated.value = new Date()
  } catch (error) {
    if (!axios.isCancel(error)) {
      console.error('Error fetching analytics data:', error)
      pieData.value = []
      topProducts.value = []
      salesData.value = {}
      comparisonData.value = {}
    }
  } finally {
    isLoading.value = false
  }
}



function printDashboard() {
  window.print();
}

// Lifecycle hooks and watchers
onMounted(() => {
  fetchData()
  fetchUnprocessedOrders()
})

// Create a debounced fetch function for better performance
let fetchDataTimeout = null
const debouncedFetchData = () => {
  clearTimeout(fetchDataTimeout)
  fetchDataTimeout = setTimeout(() => {
    fetchData()
  }, 300)
}

// Watch for date changes
watch([startDate, endDate, comparisonPeriod], () => {
  debouncedFetchData()
}, { deep: true })
</script>

<style scoped>
table {
  font-feature-settings: 'tnum' on, 'lnum' on;
}

th {
  letter-spacing: 0.025em;
}

td {
  letter-spacing: -0.01em;
}

@media (max-width: 640px) {
  table {
    min-width: 600px;
  }
}

tr {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.overflow-x-auto::-webkit-scrollbar {
  height: 4px;
}
.overflow-x-auto::-webkit-scrollbar-track {
  background: #f8f8f8;
  border-radius: 2px;
}
.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #e5e5e5;
  border-radius: 2px;
}
.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #d4d4d4;
}

@media print {
  .section {
    break-inside: avoid;
    page-break-inside: avoid;
  }
  
  button {
    display: none;
  }
  
  .min-h-screen {
    min-height: auto;
  }
  
  body {
    background: white;
  }
}
</style>