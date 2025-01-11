<template>
    <div class="flex h-screen bg-gray-50">
      <!-- Sidebar -->
      <aside class="hidden md:flex flex-col w-64 bg-white border-r border-gray-200 p-4">
        <div class="flex items-center gap-2 px-2 mb-6">
          <shopping-basket class="h-6 w-6 text-emerald-600" />
          <span class="font-semibold text-gray-800">Beauty Analytics</span>
        </div>
        <nav class="space-y-1">
          <a v-for="item in navItems" :key="item.label" href="#" class="flex items-center gap-2 px-2 py-2 text-gray-600 hover:bg-emerald-50 hover:text-emerald-600 rounded-lg">
            <component :is="item.icon" class="h-5 w-5" />
            {{ item.label }}
          </a>
        </nav>
      </aside>
  
      <!-- Main Content -->
      <main class="flex-1 overflow-auto">
        <div class="p-8">
          <!-- Header -->
          <div class="flex justify-between items-center mb-8">
            <h1 class="text-2xl font-semibold text-gray-800">Dashboard Overview</h1>
            <select v-model="filter" class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm">
              <option value="7_days">Last 7 Days</option>
              <option value="30_days">Last 30 Days</option>
              <option value="90_days">Last 90 Days</option>
              <option value="all">All Time</option>
            </select>
          </div>
  
          <!-- Stats Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div v-for="stat in stats" :key="stat.label" class="bg-white p-6 rounded-xl border border-gray-200">
              <div class="flex items-center justify-between mb-4">
                <div class="p-2 bg-emerald-50 rounded-lg">
                  <component :is="stat.icon" class="h-6 w-6 text-emerald-600" />
                </div>
              </div>
              <h3 class="text-sm font-medium text-gray-500">{{ stat.label }}</h3>
              <p class="text-2xl font-semibold text-gray-900 mt-1">{{ stat.value }}</p>
            </div>
          </div>
  
          <!-- Charts Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <!-- Sales Trend Chart -->
            <div class="lg:col-span-2 bg-white p-6 rounded-xl border border-gray-200">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">Sales Trend</h3>
                <div class="h-[300px] w-full">
                <v-chart class="chart" :option="salesChartOption" autoresize />
                </div>
            </div>
  
            <!-- Category Distribution Chart -->
            <div class="bg-white p-6 rounded-xl border border-gray-200 flex flex-col">
              <h3 class="text-lg font-semibold text-gray-800 mb-4">Category Distribution</h3>
              <div class="flex-grow flex items-center justify-center">
                <div class="w-full h-[300px] max-w-[300px]">
                  <v-chart class="chart" :option="pieChartOption" />
                </div>
              </div>
              <div class="grid grid-cols-2 gap-2 mt-4">
                <div v-for="(item, index) in pieData" :key="item.name" class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: COLORS[index] }" />
                  <span class="text-sm text-gray-600">{{ item.name }}</span>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Popular Products -->
          <div class="bg-white rounded-xl border border-gray-200">
            <div class="p-6 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-800">Popular Products</h3>
            </div>
            <div class="divide-y divide-gray-200">
              <div v-for="product in popularProducts" :key="product.name" class="p-6 flex items-center gap-4">
                <img :src="product.image" :alt="product.name" class="w-16 h-16 object-cover rounded-lg" />
                <div class="flex-1">
                  <h4 class="font-medium text-gray-900">{{ product.name }}</h4>
                  <p class="text-sm text-gray-500 mt-1">{{ product.sales.toLocaleString() }} sales</p>
                </div>
                <div class="text-right">
                  <p class="font-medium text-gray-900">${{ product.revenue.toLocaleString() }}</p>
                  <p class="text-sm text-gray-500 mt-1">Revenue</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  import { defineComponent } from 'vue'
  import { use } from 'echarts/core'
  import { CanvasRenderer } from 'echarts/renderers'
  import { LineChart, PieChart } from 'echarts/charts'
  import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent
  } from 'echarts/components'
  import VChart from 'vue-echarts'
  import { format } from 'date-fns'
  import {
    BarChart3, Users, ShoppingBag, DollarSign, ChevronDown,
    Layout, ShoppingBasket, PieChart as PieChartIcon, UserCircle
  } from 'lucide-vue-next'
  import axios from 'axios'
  
  use([
    CanvasRenderer,
    LineChart,
    PieChart,
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent
  ])
  
  export default defineComponent({
    components: {
      VChart,
      BarChart3,
      Users,
      ShoppingBag,
      DollarSign,
      ChevronDown,
      Layout,
      ShoppingBasket,
      PieChart: PieChartIcon,
      UserCircle,
      testSaleData:[]
    },
    data() {
    return {
      filter: '7_days',
      testSaleData: [],
      navItems: [
        { icon: Layout, label: "Dashboard" },
        { icon: BarChart3, label: "Analytics" },
        { icon: ShoppingBag, label: "Products" },
        { icon: Users, label: "Customers" },
      ],
      salesData: [],
      pieData: [],
      COLORS: ["#059669", "#10b981", "#34d399", "#6ee7b7"],
      popularProducts: [],
    };
  },
  computed: {
    stats() {
      return [
        { icon: DollarSign, label: "Total Revenue", value: this.getTotalRevenue(), delta: "+12.3%" },
        { icon: ShoppingBag, label: "Total Orders", value: this.getTotalOrders(), delta: "+8.1%" },
        { icon: Users, label: "Total Customers", value: "1,789", delta: "+5.4%" },
        { icon: BarChart3, label: "Avg. Order Value", value: `${this.averageOrderValue}`, delta: "+2.5%" },
      ];
    },
    averageOrderValue() {
    const totalRevenue = parseFloat(this.getTotalRevenue().replace(/,/g, ''));
    const totalOrders = this.getTotalOrders();
    
    // Ensure totalRevenue is a valid number and totalOrders > 0
    if (totalOrders > 0 && !isNaN(totalRevenue)) {
      const avgOrderValue = totalRevenue / totalOrders;
      return avgOrderValue.toLocaleString('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
    
    return '$0.00';
  },
    salesChartOption() {
      return {
        xAxis: {
          type: 'category',
          data: this.salesData.map(item => format(new Date(item.date), 'MMM d')),
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            data: this.salesData.map(item => item.value),
            type: 'line',
            smooth: true,
            areaStyle: {
              color: '#ecfdf5',
            },
            lineStyle: {
              color: '#059669',
            },
          },
        ],
        tooltip: {
          trigger: 'axis',
        },
      };
    },
    pieChartOption() {
      return {
        series: [
          {
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '50%'],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: 'center',
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '20',
                fontWeight: 'bold',
              },
            },
            labelLine: {
              show: false,
            },
            data: this.pieData.map((item, index) => ({
              value: item.value,
              name: item.name,
              itemStyle: {
                color: this.COLORS[index % this.COLORS.length],
              },
            })),
          },
        ],
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)',
        },
      };
    },
  },
  mounted() {
    this.getSalesData();
  },
  methods: {
    async getSalesData() {
      try {
        const response = await axios.get('api/get_sale_data', { params: { filter: this.filter } });
        this.pieData = response.data.category
        this.popularProducts = response.data.products || []

        this.salesData = response.data.sales || [];
      } catch (error) {
        console.error('Error fetching sales data:', error);
      }
    },
    getTotalRevenue() {
      if (!this.salesData || !Array.isArray(this.salesData)) {
        return 0;
      }
      return this.salesData
        .filter(item => item.paid)
        .reduce((total, item) => total + item.value, 0)
        .toLocaleString();
    },
    getTotalOrders(){
        if(!this.salesData || !Array.isArray(this.salesData)){
            return 0;
        }
        return this.salesData.filter(item => item.paid).length;

    },
  },
  watch: {
    filter: {
      handler: 'getSalesData',
    },
  },
  })
  </script>
  
  <style scoped>
  .chart {
    height: 100%;
    width: 100%;
  }
  </style>
  
  