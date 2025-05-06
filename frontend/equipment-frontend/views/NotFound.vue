<template>
  <div class="not-found">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card border-danger">
            <div class="card-body text-center py-5">
              <div class="error-icon mb-4">
                <i class="bi bi-exclamation-octagon-fill text-danger" style="font-size: 4rem;"></i>
              </div>
              <h2 class="error-title mb-3">404 - Page Not Found</h2>
              <p class="error-message lead mb-4">
                The page you're looking for doesn't exist or has been moved.
              </p>
              <div class="d-flex justify-content-center gap-3">
                <router-link to="/" class="btn btn-primary">
                  <i class="bi bi-house-door me-2"></i> Go to Homepage
                </router-link>
                <button @click="$router.go(-1)" class="btn btn-outline-secondary">
                  <i class="bi bi-arrow-left me-2"></i> Go Back
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  metaInfo: {
    title: '404 Not Found',
    meta: [
      { name: 'robots', content: 'noindex' }
    ]
  },
  created() {
    if (this.$route.name !== 'NotFound') {
      this.$router.replace({ name: 'NotFound' })
    }
  }
}
</script>

<style scoped>
.not-found {
  min-height: 100vh;
}

.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.error-title {
  font-size: 2rem;
  color: #dc3545;
}

.error-message {
  color: #6c757d;
}

@media (max-width: 768px) {
  .error-icon i {
    font-size: 3rem !important;
  }

  .error-title {
    font-size: 1.5rem;
  }

  .d-flex {
    flex-direction: column;
    gap: 1rem !important;
  }

  .btn {
    width: 100% !important;
  }
}
</style>