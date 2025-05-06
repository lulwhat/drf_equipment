<template>
  <div class="logout-container">
    <div class="card">
      <div class="card-body text-center">
        <div class="spinner-border mb-3" role="status" v-if="loggingOut">
          <span class="visually-hidden">Loading...</span>
        </div>
        <h2 class="mb-4">Logging Out</h2>
        <p class="mb-4">{{ message }}</p>
        <router-link to="/user/login" class="btn btn-primary">Return to Login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Logout',
  data() {
    return {
      loggingOut: true,
      message: 'Please wait while we log you out...'
    }
  },
  created() {
    // Perform logout actions
    this.logout()
  },
  methods: {
    logout() {
      // Simulate a brief delay for better UX
      setTimeout(() => {
        // Clear the authentication token
        localStorage.removeItem('access_token')
        
        // Update the UI
        this.loggingOut = false
        this.message = 'You have been successfully logged out.'
        
        // Redirect to login page after a short delay
        setTimeout(() => {
          this.$router.push('/user/login')
        }, 1500)
      }, 1000)
    }
  }
}
</script>

<style scoped>
.logout-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.card {
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
