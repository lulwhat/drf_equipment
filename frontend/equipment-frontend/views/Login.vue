<template>
  <div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
      <div class="card mt-5">
        <div class="card-header">
          <h4 class="mb-0">Login</h4>
        </div>
        <div class="card-body">
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          
          <form @submit.prevent="login">
            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input 
                type="text" 
                class="form-control" 
                id="username" 
                v-model="username" 
                required
              >
            </div>
            
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input 
                type="password" 
                class="form-control" 
                id="password" 
                v-model="password" 
                required
              >
            </div>
            
            <button type="submit" class="btn btn-primary w-100" :disabled="loading">
              {{ loading ? 'Logging in...' : 'Login' }}
            </button>
          </form>
          <p>Don't have an account? <router-link to="/user/register">Register</router-link></p>
        </div>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script>
import api from '../src/axios'
import AppFooter from '../src/components/AppFooter.vue'

export default {
  name: 'Login',
  components: {
    AppFooter
  },
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: null
    }
  },
  methods: {
    async login(event) {
      event.preventDefault();
      event.stopPropagation();
      this.loading = true
      this.error = null

      try {
        await this.$store.dispatch('login', {
          username: this.username,
          password: this.password
        })
        this.$router.push('/')
      } catch (error) {
        this.error = this.$store.getters.errorMessage || 'Login failed. Please check your credentials.'
      } finally {
        this.loading = false
      }
    }
  },
  created() {
    if (this.$route.query.error) {
      this.error = this.$route.query.error;
    }
    // Redirect if already logged in
    if (localStorage.getItem('access_token')) {
      this.$router.push('/')
    }
  }
}
</script>