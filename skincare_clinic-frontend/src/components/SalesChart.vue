<template>
  <div class="bg-white p-6 rounded-xl border border-gray-200">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">Sales Trend</h3>
    <div class="h-[400px]">
      <v-chart ref="chart" class="chart" :option="chartOption" :manual-update="true" autoresize />
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import { format, parse, subDays, eachDayOfInterval, startOfDay, endOfDay } from 'date-fns'

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
])

export default defineComponent({
  name: 'SalesChart',
  components: {
    VChart,
  },
  props: {
    salesData: {
      type: Array,
      required: true,
    },
    filter: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      processedData: [],
      chartOption: {},
    }
  },
  methods: {
    processChartData() {
      const interval = this.filter === '7_days' ? 7 : 30
      const end = new Date()
      const start = subDays(end, interval - 1)
      
      const dailyData = eachDayOfInterval({ start, end }).map(day => {
        const dayStart = startOfDay(day)
        const dayEnd = endOfDay(day)
        const dayData = this.salesData.filter(item => {
          const itemDate = parse(item.date, 'yyyy-MM-dd', new Date())
          return itemDate >= dayStart && itemDate <= dayEnd
        })
        const totalValue = dayData.reduce((sum, item) => sum + item.value, 0)
        return {
          date: format(day, 'yyyy-MM-dd'),
          value: totalValue,
          tooltip: `${format(day, 'MMM d, yyyy')}: $${totalValue.toLocaleString()}`
        }
      })

      if (interval > 7) {
        const groupSize = Math.ceil(interval / 7)
        this.processedData = dailyData.reduce((acc, item, index) => {
          const groupIndex = Math.floor(index / groupSize)
          if (!acc[groupIndex]) {
            acc[groupIndex] = { ...item, tooltip: '' }
          } else {
            acc[groupIndex].value += item.value
            acc[groupIndex].tooltip += '\n'
          }
          acc[groupIndex].tooltip += item.tooltip
          return acc
        }, [])
      } else {
        this.processedData = dailyData
      }
    },
    updateChartOption() {
      this.chartOption = {
        title: {
          text: this.filter === '7_days' ? 'Daily Sales for Last 7 Days' : 'Sales Trend for Last 30 Days',
          left: 'center',
        },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            const [param] = params
            return param.data.tooltip.split('\n').join('<br>')
          },
        },
        xAxis: {
          type: 'category',
          data: this.processedData.map(item => item.date),
          axisLabel: {
            formatter: (value) => format(parse(value, 'yyyy-MM-dd', new Date()), this.filter === '7_days' ? 'MMM d' : 'MMM d'),
            interval: this.filter === '7_days' ? 0 : 'auto',
            rotate: this.filter === '7_days' ? 0 : 45,
          },
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: (value) => `$${value.toLocaleString()}`,
          },
        },
        series: [
          {
            data: this.processedData.map(item => item.value),
            type: 'line',
            smooth: true,
            areaStyle: {
              color: '#ecfdf5',
            },
            lineStyle: {
              color: '#059669',
            },
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
              color: '#059669',
            },
          },
        ],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',
          containLabel: true,
        },
        dataZoom: [
          {
            type: 'inside',
            start: 0,
            end: 100,
          },
          {
            type: 'slider',
            start: 0,
            end: 100,
          },
        ],
      }
    },
    updateChart() {
      this.processChartData()
      this.updateChartOption()
      this.$nextTick(() => {
        if (this.$refs.chart) {
          this.$refs.chart.setOption(this.chartOption)
        }
      })
    },
    handleResize() {
      if (this.$refs.chart) {
        this.$refs.chart.resize()
      }
    },
  },
  watch: {
    salesData: {
      handler: 'updateChart',
      deep: true,
    },
    filter: {
      handler: 'updateChart',
    },
  },
  mounted() {
    this.updateChart()
    window.addEventListener('resize', this.handleResize)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
  },
})
</script>

<style scoped>
.chart {
  height: 100%;
  width: 100%;
}
</style>

