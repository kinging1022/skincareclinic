<template>
  <main class="flex-1">
    <!-- Hero Section -->
    <section class="relative">
      <div
        class="flex h-[70vh] w-full flex-col items-center justify-center bg-cover bg-center px-4 text-center text-white"
        :style="{
          backgroundImage:
            'linear-gradient(rgba(10, 60, 40, 0.65), rgba(10, 60, 40, 0.65)), url(' + aboutHeroImage + ')'
        }"
      >
        <h1 class="mb-4 max-w-3xl text-4xl font-light tracking-wide md:text-5xl lg:text-6xl drop-shadow-sm">
          BEST SKIN CARE SHOP IN NIGERIA
        </h1>
        <p class="mb-8 max-w-md text-base font-light md:text-lg drop-shadow-sm">
          Clinically effective products formulated and  tailored for healthy and glowing skin
        </p>
      </div>
    </section>

    <!-- Our Story Section -->
    <section class="py-16 bg-white">
      <div class="container px-4 md:px-6">
        <div class="mx-auto max-w-4xl text-center">
          <h2 class="mb-4 text-2xl font-medium tracking-wider text-[#1c3a2e]">REDEFINING SKIN CARE HEALTH</h2>
          <div class="mb-12 h-px w-24 bg-[#d7e5dc] mx-auto"></div>
          <p class="mb-8 text-lg text-[#4a6b5d] font-light leading-relaxed">
            Welcome to Skin Care Clinic, your go to destination for glowing, healthy skin online. At Skin Care Clinic, 
            we blend expert skincare knowledge with premium products to help you feel confident in your skin every day.
            Whether you shop with us online or in our designated pick up location,we are committed to providing you with the best
            skincare experience possible. Our range of products is here to help you find the perfect products for your unique skin type and concerns.
          </p>
          <p class="text-lg text-[#4a6b5d] font-light leading-relaxed">
            we sell range of top-rated cleansers, moisturizers, serums, and treatments tailored to all skin 
            types from sensitive to acne-prone. Our friendly skincare experts are here to guide you with personalized advice and recommendations. 
            Discover trusted brands, effective routines, and unbeatable value at Skin Care Clinic where beautiful skin begins.Authentic 
            products from top brands like
            <span class="font-medium text-[#1c3a2e]">Cerave</span>, <span class="font-medium text-[#1c3a2e]">Dr Rashel</span>,
            <span class="font-medium text-[#1c3a2e]">Simple</span>,<span class="font-medium text-[#1c3a2e]">FaceFact</span>, 
            <span class="font-medium text-[#1c3a2e]">Beauty Formula</span>,<span class="font-medium text-[#1c3a2e]">Olay</span>,
            <span class="font-medium text-[#1c3a2e]">Amalactin</span>,<span class="font-medium text-[#1c3a2e]">Black Girl</span>,
            and <span class="font-medium text-[#1c3a2e]"></span> many more .
          </p>
        </div>
      </div>
    </section>


    <!-- Expertise Section -->
    <section class="py-16 bg-[#f0f5f1]">
      <div class="container px-4 md:px-6">
        <h2 class="mb-12 text-center text-2xl font-medium tracking-wider text-[#1c3a2e]">SPECIALIZED IN TREATING</h2>
        <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div v-for="(condition, index) in skinConditions" :key="index" class="bg-white p-8 text-center rounded-none border border-[#d7e5dc]">
            <h3 class="mb-4 text-xl font-medium text-[#1c3a2e]">{{ condition.name }}</h3>
            <p class="mb-4 text-[#4a6b5d] font-light">
              {{ condition.description }}
            </p>
            <RouterLink 
            :to="{ name: 'collections', params: { collections_name:condition.name, slug: condition.slug} }"
            class="inline-block text-sm text-[#0a5c3e] hover:underline"
            >
              View Recommended Products →
            </RouterLink>
          </div>
        </div>
      </div>
    </section>


    <!-- Why Choose Us -->
    <section class="py-16 bg-[#f0f5f1]">
      <div class="container px-4 md:px-6">
        <div class="mx-auto max-w-4xl">
          <h2 class="mb-12 text-center text-2xl font-medium tracking-wider text-[#1c3a2e]">WHY SKINCARE CLINIC STANDS OUT</h2>
          <div class="space-y-8">
            <div v-for="(reason, index) in reasons" :key="index" class="flex items-start">
              <div class="mr-6 mt-1 flex h-8 w-8 items-center justify-center rounded-full bg-[#0a5c3e] text-white">
                <span class="text-lg font-medium">{{ index + 1 }}</span>
              </div>
              <div>
                <h3 class="mb-2 text-lg font-medium text-[#1c3a2e]">{{ reason.title }}</h3>
                <p class="text-[#4a6b5d] font-light">
                  {{ reason.description }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- CTA Section -->
    <section class="bg-[#e3efe7] py-16">
      <div class="container px-4 md:px-6">
        <div class="mx-auto max-w-3xl text-center">
          <h2 class="mb-4 text-2xl font-light tracking-wider text-[#1c3a2e]">YOUR JOURNEY TO RADIANT AND HEALTHY SKIN BEGINS HERE</h2>
          <p class="mb-8 text-base text-[#4a6b5d] font-light">
            Visit us today to shop our clinically-proven collections online.
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <RouterLink 
              to="/shop" 
              class="inline-block rounded-none bg-[#0a5c3e] hover:bg-[#0b4a33] text-base text-white px-8 py-3"
            >
              Shop Now
            </RouterLink>
            <RouterLink 
              to="/consultation" 
              class="inline-block rounded-none border border-[#0a5c3e] text-[#0a5c3e] hover:bg-[#0a5c3e]/10 text-base px-8 py-3"
            >
              Book Consultation
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router'

export default {
  name: 'AboutView',
  components: {
    RouterLink
  },
  data() {
    return {
      aboutHeroImage: 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80',
      skinConditions: [
        {
          name: "Hyperpigmentation",
          description: "At Skin Care Clinic, we stock a variety of dermatologist-recommended products designed to reduce dark spots, brighten dull skin, and even out your skin tone. Explore top treatments with vitamin C, niacinamide, and more—available both in-store and online.",
          slug: "hyperpigmentation"
        },
        {
          name: "Acne & Breakouts",
          description: "From gentle cleansers to targeted treatments, Skin Care Clinic offers a curated selection of acne solutions that fight breakouts and soothe irritation without drying out your skin. Let us help you build a routine that works.",
          slug: "acne"
        },
        {
          name: "Dry/Dehydrated Skin",
          description: "Struggling with dryness or tight, flaky skin? Our collection of hydrating products includes rich moisturizers, serums, and oils that nourish and restore moisture—perfect for all skin types and available at Skin Care Clinic.",
          slug: "dry-skin"
        }
      ],
      reasons: [
        {
          title: "Expert-Recommended Skincare for Every Skin Type",
          description: "At Skin Care Clinic, we carefully select dermatologist-approved and science-backed skincare products that work for all skin types—including oily, dry, sensitive, and acne-prone skin. Our expert team ensures you’re choosing products that truly deliver results."
        },
        {
          title: "Trusted Brands & Authentic Products",
          description: "We partner directly with top skincare brands to bring you 100% authentic products. From gentle cleansers to powerful serums, everything we stock is tried, tested, and trusted by professionals and skincare lovers alike."
        },
        {
          title: "Personalized Skincare Advice—Online & In-Store",
          description: "you get access to real skincare guidance tailored to your unique skin needs. Our commitment to customer care and skin health is what makes Skin Care Clinic your trusted skincare destination."
        }
      ],
     
    }
  }
}
</script>

<style scoped>
/* Custom styling to maintain luxury aesthetic */
section {
  scroll-margin-top: 80px;
}

.router-link-active {
  @apply text-[#0a5c3e] border-b-2 border-[#0a5c3e];
}

/* Smooth image hover effect */
img {
  transition: transform 0.5s cubic-bezier(0.25, 0.45, 0.45, 0.95);
}
</style>