<template>
  <!-- Main Content -->
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
          <div class="flex items-center gap-2">
            <label for="comparison" class="text-sm text-gray-600 hidden sm:inline">Compare:</label>
            <select id="comparison" v-model="comparisonPeriod" class="bg-white border border-gray-200 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 shadow-sm">
              <option value="none">No Comparison</option>
              <option value="previous_period">Previous Period</option>
              <option value="previous_year">Previous Year</option>
            </select>
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
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
          <button @click="exportCSV" class="flex items-center gap-1 text-gray-600 hover:text-gray-800 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors text-sm font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export CSV
          </button>
          <button @click="printDashboard" class="flex items-center gap-1 text-gray-600 hover:text-gray-800 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors text-sm font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
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
                  
                  <!-- Comparison indicator -->
                  <div v-if="stat.comparison && comparisonPeriod !== 'none'" class="flex items-center mt-2">
                    <span 
                      class="text-xs font-medium flex items-center gap-1" 
                      :class="stat.comparison.percentage >= 0 ? 'text-emerald-600' : 'text-red-600'"
                    >
                      <svg v-if="stat.comparison.percentage >= 0" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                      </svg>
                      {{ Math.abs(stat.comparison.percentage).toFixed(1) }}%
                    </span>
                    <span class="text-xs text-gray-500 ml-1">vs {{ comparisonPeriod === 'previous_year' ? 'last year' : 'previous period' }}</span>
                  </div>
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
              View All <chevron-right class="h-3 w-3" />
            </button>
          </div>

          <div v-if="orders.length > 0" class="overflow-x-auto">
            <table class="w-full divide-y divide-gray-100">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order ID</th>
                  <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                  <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th scope="col" class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-100">
                <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50/50 transition-colors">
                  <td class="px-4 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900 tracking-tight">#{{ order.id }}</div>
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900 tracking-tight">{{ order.full_name }}</div>
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-500">{{ formatDate(order.created_at) }}</div>
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap text-right">
                    <div class="text-sm font-medium text-gray-900 tracking-tight">{{ formatCurrency(order.order_amount) }}</div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="p-8 flex flex-col items-center justify-center text-center">
            <package-open class="h-12 w-12 text-gray-400 mb-4" />
            <h4 class="text-lg font-medium text-gray-700 mb-1 tracking-tight">No recent orders</h4>
            <p class="text-sm text-gray-500 max-w-md">When you receive new orders, they'll appear here</p>
          </div>
        </div>

        <!-- Category Distribution -->
        <div id="analytics" class="section bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mb-6 sm:mb-8">
          <div class="p-4 sm:p-6">
            <h3 class="text-lg font-bold text-gray-800 mb-4 sm:mb-6 tracking-tight">Category Distribution</h3>
            <div class="h-56 sm:h-64">
              <apexchart 
                type="donut" 
                height="100%" 
                :options="categoryChartOptions" 
                :series="categorySeries" 
              />
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mt-4 sm:mt-6">
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
                <shopping-bag class="h-6 w-6 text-gray-400" />
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
              View All Products <chevron-right class="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'
import {
  ShoppingBag, DollarSign, ChevronRight, PackageOpen, Users
} from 'lucide-vue-next'
import axios from 'axios'

export default {
  components: {
    apexchart: VueApexCharts,
    ShoppingBag,
    DollarSign,
    ChevronRight,
    PackageOpen,
    Users
  },
  data() {
    return {
      startDate: this.getDefaultStartDate(),
      endDate: this.getDefaultEndDate(),
      comparisonPeriod: 'none', // 'none', 'previous_period', 'previous_year'
      pieData: [],
      salesData: {},
      comparisonData: {},
      COLORS: ["#10B981", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6"],
      topProducts: [],
      maxSales: 0,
      orders: [],
      lastUpdated: null,
      isLoading: false,
      cache: {
        data: {},
        timestamp: null,
        ttl: 5 * 60 * 1000 // 5 minutes cache TTL
      }
    }
  },
  computed: {
    totalCategoryValue() {
      return this.pieData.reduce((sum, item) => sum + item.value, 0)
    },
    stats() {
      const totalRevenue = this.getTotalRevenue()
      const totalOrders = this.getTotalOrders()
      const avgOrderValue = this.getAverageOrderValue()
      
      // Calculate comparisons if we have comparison data
      let revenueComparison = null
      let ordersComparison = null
      let avgOrderComparison = null
      
      if (this.comparisonPeriod !== 'none' && this.comparisonData && this.comparisonData.sales_data) {
        const prevRevenue = this.comparisonData.sales_data.total_revenue || 0
        const prevOrders = this.comparisonData.sales_data.total_order || 0
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
          value: this.formatCurrency(totalRevenue),
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
          value: this.formatCurrency(avgOrderValue),
          comparison: avgOrderComparison,
          bgColor: 'bg-violet-500/10',
          iconColor: 'text-violet-500'
        },
      ]
    },
    categorySeries() {
      return this.pieData.map(item => item.value)
    },
    categoryChartOptions() {
      return {
        chart: {
          type: 'donut',
          height: '100%'
        },
        colors: this.COLORS,
        labels: this.pieData.map(item => item.name),
        dataLabels: {
          enabled: false
        },
        legend: {
          show: false
        },
        plotOptions: {
          pie: {
            donut: {
              size: '70%',
              labels: {
                show: true,
                total: {
                  show: true,
                  label: 'Total Sales',
                  formatter: () => {
                    // Fixed: Don't divide by 100 here
                    return this.formatCurrency(this.totalCategoryValue)
                  },
                  color: '#6B7280',
                  fontSize: '14px',
                  fontWeight: 600
                },
                value: {
                  formatter: (value) => {
                    // Fixed: Don't divide by 100 here
                    return this.formatCurrency(value)
                  },
                  color: '#111827',
                  fontSize: '20px',
                  fontWeight: 700
                }
              }
            }
          }
        },
        tooltip: {
          y: {
            formatter: (value) => {
              // Fixed: Don't divide by 100 here
              return this.formatCurrency(value)
            }
          }
        }
      }
    },
    cacheKey() {
      return `${this.startDate}_${this.endDate}_${this.comparisonPeriod}`
    }
  },
  mounted() {
    this.fetchData()
    this.fetchUnprocessedOrders()
  },
  methods: {
    getDefaultStartDate() {
      const date = new Date()
      date.setDate(date.getDate() - 30)
      return date.toISOString().split('T')[0]
    },
    getDefaultEndDate() {
      return new Date().toISOString().split('T')[0]
    },
    formatCurrency(value, isKobo = false) {
      try {
        if (value === null || value === undefined || value === '') {
          return '₦0.00'
        }

        // Handle string values with commas (like "12,200.00")
        if (typeof value === 'string' && value.includes(',')) {
          value = value.replace(/,/g, '')
        }

        // Convert to number
        let numericValue = typeof value === 'string' 
          ? parseFloat(value) 
          : Number(value)

        if (isNaN(numericValue)) {
          console.warn('Invalid currency value:', value)
          return '₦0.00'
        }

        // Convert kobo to naira if needed - FIXED: Only convert if isKobo is true
        // Most values are already in Naira, so we don't need to divide by 100
        if (isKobo) {
          numericValue = numericValue / 100
        }

        // Use Intl.NumberFormat for consistent formatting
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
    },
    formatDate(dateString) {
      try {
        if (!dateString) return ''
        
        // Handle both Date objects and strings
        const date = typeof dateString === 'string' 
          ? new Date(dateString) 
          : dateString
        
        return date.toLocaleDateString('en-US', { 
          month: 'short', 
          day: 'numeric',
          year: 'numeric'
        })
      } catch (error) {
        console.error('Error formatting date:', error)
        return dateString || ''
      }
    },
    formatDateTime(dateString) {
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
    },
    async fetchUnprocessedOrders() {
      try {
        const response = await axios.get('/api/unprocessed_orders')
        this.orders = response.data || []
      } catch (error) {
        console.error('Error fetching unprocessed orders:', error)
        this.orders = []
      }
    },
    refreshData() {
      // Force refresh by clearing cache
      this.cache.data = {}
      this.fetchData()
    },
    async fetchData() {
      if (this.isLoading) return
      
      this.isLoading = true
      
      try {
        // Check cache first
        if (this.cache.data[this.cacheKey] && 
            this.cache.timestamp && 
            (Date.now() - this.cache.timestamp) < this.cache.ttl) {
          console.log('Using cached data')
          const cachedData = this.cache.data[this.cacheKey]
          this.pieData = cachedData.category || []
          this.topProducts = cachedData.products || []
          this.salesData = cachedData.sales_data || {}
          this.comparisonData = cachedData.comparison_data || {}
          
          if (this.topProducts.length) {
            this.maxSales = Math.max(...this.topProducts.map(p => p.total_quantity))
          }
          
          this.isLoading = false
          return
        }
        
        const params = {
          start_date: this.startDate,
          end_date: this.endDate,
          comparison: this.comparisonPeriod
        }
        
        const response = await axios.get('/api/get_analytics', { params })
        console.log('Analytics data:', response.data)
        
        // Update data with API response
        this.pieData = response.data.category || []
        this.topProducts = response.data.products || []
        this.salesData = response.data.sales_data || {}
        this.comparisonData = response.data.comparison_data || {}
        
        if (this.topProducts.length) {
          this.maxSales = Math.max(...this.topProducts.map(p => p.total_quantity))
        }
        
        // Update cache
        this.cache.data[this.cacheKey] = response.data
        this.cache.timestamp = Date.now()
        
        // Update last updated timestamp
        this.lastUpdated = new Date()
      } catch (error) {
        console.error('Error fetching analytics data:', error)
        this.pieData = []
        this.topProducts = []
        this.salesData = {}
        this.comparisonData = {}
      } finally {
        this.isLoading = false
      }
    },
    getTotalRevenue() {
      // Use sales_data if available (already in naira)
      if (this.salesData && this.salesData.total_revenue !== undefined) {
        return this.salesData.total_revenue
      }
      
      // Fallback to sum of category values (already in naira)
      // FIXED: Don't divide by 100 here
      return this.totalCategoryValue
    },
    getTotalOrders() {
      // Use sales_data if available
      if (this.salesData && this.salesData.total_order !== undefined) {
        return this.salesData.total_order
      }
      
      // Fallback to product quantity
      if (!this.topProducts || !Array.isArray(this.topProducts)) return 0
      return this.topProducts.reduce((total, product) => total + product.total_quantity, 0)
    },
    getAverageOrderValue() {
      const totalRevenue = this.getTotalRevenue()
      const totalOrders = this.getTotalOrders()
      return totalOrders > 0 ? Math.round(totalRevenue / totalOrders) : 0
    },
    exportCSV() {
      // Create CSV content
      let csvContent = "data:text/csv;charset=utf-8,";
      
      // Add header
      csvContent += "Category,Revenue (₦)\n";
      
      // Add category data
      this.pieData.forEach(item => {
        // FIXED: Don't divide by 100 here
        const revenue = item.value.toFixed(2);
        csvContent += `${item.name},${revenue}\n`;
      });
      
      // Add separator
      csvContent += "\n";
      
      // Add products header
      csvContent += "Product,Brand,Category,Quantity,Revenue (₦)\n";
      
      // Add products data
      this.topProducts.forEach(product => {
        // FIXED: Don't divide by 100 here
        const revenue = product.total_revenue.toFixed(2);
        csvContent += `${product.product_name},${product.brand_name || 'N/A'},${product.category_name || 'Uncategorized'},${product.total_quantity},${revenue}\n`;
      });
      
      // Create download link
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", `dashboard_export_${this.formatDate(new Date()).replace(/,/g, '')}.csv`);
      document.body.appendChild(link);
      
      // Trigger download
      link.click();
      
      // Clean up
      document.body.removeChild(link);
    },
    printDashboard() {
      window.print();
    }
  }
}
</script>

<style scoped>
/* Inherits font from your main layout */
table {
  font-feature-settings: 'tnum' on, 'lnum' on;
}

th {
  letter-spacing: 0.025em;
}

td {
  letter-spacing: -0.01em;
}

/* Responsive table */
@media (max-width: 640px) {
  table {
    min-width: 600px;
  }
}

/* Hover effects */
tr {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Custom scrollbar */
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

/* Print styles */
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