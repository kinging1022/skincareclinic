<template>
    <main class="bg-[#f8faf8]">
      <!-- Hero Section -->
      <section class="relative py-20 bg-[#0a5c3e] text-white overflow-hidden">
        <div class="absolute inset-0 opacity-20">
          <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-[#e3efe7] to-transparent"></div>
        </div>
        <div class="container mx-auto px-6 relative z-10">
          <div class="max-w-3xl mx-auto text-center">
            <h1 class="text-4xl md:text-5xl font-light tracking-wide mb-4">Shipping Policy</h1>
            <p class="text-xl font-light text-[#e3efe7] max-w-2xl mx-auto">
              Our commitment to delivering your luxury skincare with care and precision
            </p>
          </div>
        </div>
      </section>
  
      <!-- Policy Content -->
      <section class="py-16 md:py-24">
        <div class="container mx-auto px-6 max-w-5xl">
          <div class="bg-white shadow-sm rounded-lg overflow-hidden border border-[#d7e5dc]">
            <!-- Policy Sections -->
            <div class="divide-y divide-[#e3efe7]">
              <!-- Domestic Shipping -->
              <div class="p-8 md:p-10">
                <div class="flex items-start">
                  <div class="flex-shrink-0 mr-6 text-[#0a5c3e]">
                    <CreditCardIcon class="w-7 h-7" />
                  </div>
                  <div>
                    <h2 class="text-2xl font-light text-[#1c3a2e] mb-4">Domestic Shipping</h2>
                    <div class="prose prose-lg text-[#4a6b5d]">
                      <ul class="space-y-3">
                        <li>All orders are processed within <strong>1-2 business days</strong> (excluding weekends and holidays)</li>
                        <li>Standard shipping: <strong>3-7 business days</strong> delivery</li>
                        <li>Express shipping with ibadan: <strong>1-2 business days</strong> delivery option available at checkout</li>
                        <li>You will receive a tracking number via email once your order ships</li>
                        <li>If an item sells out while your payment is processing, fulfillment may be delayed by 2-3 business days while we restock</li>

                      </ul>
                    </div>
                  </div>
                </div>
              </div>
  
              <!-- International Shipping -->
              <div class="p-8 md:p-10">
                <div class="flex items-start">
                  <div class="flex-shrink-0 mr-6 text-[#0a5c3e]">
                    <GlobeIcon class="w-7 h-7" />
                  </div>
                  <div>
                    <h2 class="text-2xl font-light text-[#1c3a2e] mb-4">International Shipping</h2>
                    <div class="prose prose-lg text-[#4a6b5d]">
                      <ul class="space-y-3">
                        <li>For International orders reach out to our <a href="https://linktr.ee/The_skincare_clinic"><strong>CUSTOMER CARE</strong></a> before placing the order</li>
                        <li>Currently shipping to <strong>usa, canada and european countries</strong> - please check at checkout</li>
                        <li>Orders typically arrive within <strong>5-14 business days</strong> after processing</li>
                        <li>Customs fees and import taxes may apply (customer's responsibility)</li>
                        <li>International orders may experience delays due to customs processing</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
  
              <!-- Order Processing -->
              <div class="p-8 md:p-10">
                <div class="flex items-start">
                  <div class="flex-shrink-0 mr-6 text-[#0a5c3e]">
                    <ZapIcon class="w-7 h-7" />
                  </div>
                  <div>
                    <h2 class="text-2xl font-light text-[#1c3a2e] mb-4">Order Processing</h2>
                    <div class="prose prose-lg text-[#4a6b5d]">
                      <ul class="space-y-3">
                        <li>Orders placed before <strong>12pm WAT</strong> are processed the same business day</li>
                        <li>Orders placed after 12pm or on weekends/holidays will be processed the next business day</li>
                        <li>During peak seasons, processing may take an additional 1-2 business days</li>
                        <li>If an item sells out while your payment is processing, fulfillment may be delayed by 2-3 business days while we restock</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
  
              <!-- Important Notes -->
              <div class="p-8 md:p-10 bg-[#f9fbf9]">
                <div class="flex items-start">
                  <div class="flex-shrink-0 mr-6 text-[#d32f2f]">
                    <AlertTriangleIcon class="w-7 h-7" />
                  </div>
                  <div>
                    <h2 class="text-2xl font-light text-[#1c3a2e] mb-4">Important Notes</h2>
                    <div class="prose prose-lg text-[#4a6b5d]">
                      <ul class="space-y-3">
                        <li>Delivery times are <strong>estimates</strong> and not guaranteed</li>
                        <li>We are not responsible for delays caused by carriers or customs</li>
                        <li>Please ensure your shipping address is correct - we cannot reroute packages once shipped</li>
                        <li>For fragile items, please inspect your package upon delivery before signing</li>
                        <li>Contact us within <strong>24 hours</strong> of delivery for any shipping-related issues</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Contact CTA -->
          <div class="mt-16 text-center">
            <h3 class="text-2xl font-light text-[#1c3a2e] mb-6">Have questions about shipping?</h3>
            <a
              href="https://linktr.ee/The_skincare_clinic" 
              class="inline-flex items-center justify-center rounded-none bg-[#0a5c3e] hover:bg-[#0b4a33] text-white px-8 py-3 text-lg transition-all duration-300 group shadow-lg"
            >
              <span class="font-light tracking-wider">CONTACT US</span>
              <ArrowRightIcon class="ml-2 w-5 h-5 transform transition-transform duration-300 group-hover:translate-x-1" />
            </a>
          </div>
        </div>
      </section>
    </main>
  </template>
  
  <script>
  import { 
    CreditCardIcon, 
    GlobeIcon, 
    ZapIcon, 
    AlertTriangleIcon, 
    ArrowRightIcon 
  } from 'lucide-vue-next';
  
  export default {
    name: 'ShippingPolicy',
    components: {
      CreditCardIcon,
      GlobeIcon,
      ZapIcon,
      AlertTriangleIcon,
      ArrowRightIcon
    },
    metaInfo() {
      return {
        title: 'Shipping Policy | The Skincarè Clinic',
        meta: [
          {
            name: 'description',
            content: 'Learn about our shipping policies, delivery times, and rates for your luxury skincare products.'
          }
        ]
      }
    }
  }
  </script>
  
  <style scoped>
  .prose ul {
    list-style-type: none;
    padding-left: 0;
  }
  
  .prose li {
    position: relative;
    padding-left: 1.75em;
  }
  
  .prose li:before {
    content: "•";
    color: #0a5c3e;
    font-size: 1.5em;
    position: absolute;
    left: 0;
    top: -0.15em;
  }
  
  table {
    font-variant-numeric: lining-nums tabular-nums;
  }
  
  thead {
    font-weight: 500;
  }
  </style>