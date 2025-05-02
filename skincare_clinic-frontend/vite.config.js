import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { visualizer } from 'rollup-plugin-visualizer'
import viteCompression from 'vite-plugin-compression'
import { ViteImageOptimizer } from 'vite-plugin-image-optimizer'
import legacy from '@vitejs/plugin-legacy'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: {
        transformAssetUrls: {
          includeAbsolute: false,
        },
        compilerOptions: {
          whitespace: 'condense'
        }
      },
    }),
    ViteImageOptimizer({
      avif: { quality: 60 },  // Most efficient format first
      webp: { quality: 75 },
      png: { quality: 80 },
      jpeg: { quality: 80 },
      jpg: { quality: 80 },
    }),
    viteCompression({
      algorithm: 'brotliCompress',
      threshold: 10240,
      ext: '.br',
      filter: /\.(js|css|html|svg|json|webmanifest)$/i
    }),
    legacy({
      targets: ['defaults', 'not IE 11'],
      modernPolyfills: true
    }),
    visualizer({
      open: true,
      gzipSize: true,
      brotliSize: true,
      filename: 'stats.html'
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      'vue': 'vue/dist/vue.esm-bundler.js'
    }
  },
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString())
  },
  build: {
    target: 'esnext',
    cssTarget: 'esnext',
    chunkSizeWarningLimit: 1600,
    cssCodeSplit: true,
    reportCompressedSize: false, // More accurate size reporting
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('vue')) return 'vendor-vue';
            if (id.includes('lucide-vue-next')) return 'vendor-icons';
            if (id.includes('chart.js') || id.includes('vue-chart-3')) return 'vendor-charts';
            if (id.includes('date-fns')) return 'vendor-dates';
            if (id.includes('axios') || id.includes('lodash')) return 'vendor-essentials';
            if (id.includes('pinia') || id.includes('vue-router')) return 'vendor-state';
            return 'vendor';
          }
          if (id.includes('Scrollable') && (id.includes('Category') || id.includes('Product'))) {
            return 'scrollable-components';
          }
        },
        entryFileNames: 'assets/[name].[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash][extname]',
        minifyInternalExports: true
      },
      treeshake: {
        preset: 'recommended',
        moduleSideEffects: false,
        tryCatchDeoptimization: false
      }
    },
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
        pure_funcs: ['console.log']
      },
      format: {
        comments: false
      }
    }
  },
  server: {
    host: true,
    headers: {
      "X-Content-Type-Options": "nosniff",
      "X-Frame-Options": "DENY"
    },
    hmr: {
      overlay: false
    },
    watch: {
      usePolling: process.env.WSL_INTEROP ? true : false
    }
  },
  css: {
    devSourcemap: true,
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/assets/styles/variables.scss";`
      }
    }
  },
  optimizeDeps: {
    include: [
      'vue',
      'pinia',
      'vue-router',
      'lucide-vue-next'
    ],
    exclude: ['vue-demi'],
    esbuildOptions: {
      target: 'esnext',
      define: {
        global: 'globalThis'
      }
    }
  },
  esbuild: {
    legalComments: 'none',
    pure: process.env.NODE_ENV === 'production' ? ['console.log'] : []
  }
})