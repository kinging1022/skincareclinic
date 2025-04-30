<template>
  <div class="not-found">
    <!-- Decorative elements -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
      <div class="absolute top-1/4 -left-20 w-64 h-64 rounded-full bg-[#0a5c3e]/10 blur-xl"></div>
      <div class="absolute bottom-1/3 -right-20 w-80 h-80 rounded-full bg-[#0a5c3e]/10 blur-xl"></div>
      <div class="absolute top-1/2 left-1/4 w-40 h-40 rounded-full bg-[#e3efe7]/20 blur-lg"></div>
    </div>

    <!-- Main content -->
    <div class="relative z-10 text-center px-6">
      <div class="mb-8 text-[#0a5c3e]">
        <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mx-auto">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
          <line x1="12" y1="9" x2="12" y2="13"></line>
          <line x1="12" y1="17" x2="12.01" y2="17"></line>
        </svg>
      </div>

      <h1 class="text-5xl md:text-6xl font-light tracking-tight text-[#1c3a2e] mb-4">
        404
      </h1>
      <h2 class="text-2xl md:text-3xl font-light text-[#4a6b5d] mb-6">
        Page Not Found
      </h2>
      <p class="max-w-md mx-auto text-lg text-[#4a6b5d]/90 mb-8 leading-relaxed">
        The page you're looking for doesn't exist or has been moved. 
        Let's get you back to where you belong.
      </p>

      <router-link 
        to="/" 
        class="inline-flex items-center justify-center rounded-none bg-[#0a5c3e] hover:bg-[#0b4a33] text-white px-8 py-3 text-lg transition-all duration-300 group shadow-lg"
      >
        <span class="font-light tracking-wider">RETURN HOME</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="ml-2 transform transition-transform duration-300 group-hover:translate-x-1">
          <path d="M5 12h14M12 5l7 7-7 7"></path>
        </svg>
      </router-link>

      <div class="mt-12 text-sm text-[#4a6b5d]/70">
        <p>Error code: 404</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100%;
  background-color: #f0f5f1;
  position: relative;
  overflow: hidden;
}

/* Animation for decorative blobs */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.absolute:nth-child(1) {
  animation: float 8s ease-in-out infinite;
}
.absolute:nth-child(2) {
  animation: float 10s ease-in-out infinite 2s;
}
.absolute:nth-child(3) {
  animation: float 12s ease-in-out infinite 1s;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  h1 {
    font-size: 3.5rem;
  }
  h2 {
    font-size: 1.75rem;
  }
  p {
    font-size: 1rem;
  }
}
</style>