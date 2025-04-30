<template>
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
  import { Chart, registerables } from 'chart.js'
  
  export default {
    name: 'ChartComponent',
    props: {
      type: {
        type: String,
        default: 'bar'
      },
      data: {
        type: Object,
        required: true
      },
      options: {
        type: Object,
        default: () => ({})
      }
    },
    setup(props) {
      const chartCanvas = ref(null)
      let chartInstance = null
  
      // Register all chart types
      Chart.register(...registerables)
  
      const renderChart = () => {
        if (!chartCanvas.value) return
        
        // Destroy previous instance if exists
        if (chartInstance) {
          chartInstance.destroy()
        }
  
        // Create new chart instance
        chartInstance = new Chart(chartCanvas.value, {
          type: props.type,
          data: JSON.parse(JSON.stringify(props.data)), // Deep clone to prevent mutations
          options: JSON.parse(JSON.stringify(props.options)) // Deep clone options
        })
      }
  
      const updateChart = () => {
        if (!chartInstance) return
        
        // Update chart data without full re-render
        chartInstance.data = JSON.parse(JSON.stringify(props.data))
        chartInstance.options = JSON.parse(JSON.stringify(props.options))
        chartInstance.update()
      }
  
      onMounted(() => {
        renderChart()
      })
  
      onBeforeUnmount(() => {
        if (chartInstance) {
          chartInstance.destroy()
        }
      })
  
      watch(
        () => props.type,
        () => {
          renderChart() // Full re-render on type change
        }
      )
  
      watch(
        () => [props.data, props.options],
        (newVal, oldVal) => {
          // Only update if data actually changed
          if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
            if (chartInstance) {
              updateChart()
            } else {
              renderChart()
            }
          }
        },
        { deep: true }
      )
  
      return { chartCanvas }
    }
  }
  </script>
  
  <style scoped>
  .chart-container {
    position: relative;
    width: 100%;
    height: 100%;
  }
  </style>