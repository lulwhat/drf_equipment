<template>
  <div class="register">
    <h1>Register</h1>
    <form @submit.prevent="register">
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>

      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>

      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
      </div>

      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>

      <div>
        <label for="confirmPassword">Confirm Password:</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required>
      </div>

      <button type="submit" :disabled="loading">
        <span v-if="loading">Registering...</span>
        <span v-else>Register</span>
      </button>
    </form>
    <p>Already have an account? <router-link to="/user/login">Login</router-link></p>
  <AppFooter />
  </div>
</template>

<script>
import AppFooter from '../src/components/AppFooter.vue'

export default {
  components: {
    AppFooter
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      loading: false,
      error: null,
      success: null
    }
  },
  methods: {
    async register() {
      this.loading = true
      this.error = null
      this.success = null
      
      // Basic validation
      if (this.password !== this.confirmPassword) {
        this.error = 'Passwords do not match'
        this.loading = false
        return
      }
      
      try {
        await this.$store.dispatch('register', {
          username: this.username,
          email: this.email,
          password: this.password
        })
        
        this.success = 'Registration successful! Redirecting to login...'
        
        // Redirect to login after a short delay
        setTimeout(() => {
          this.$router.push('/user/login')
        }, 2000)
        
      } catch (error) {
        this.error = error.response?.data?.error || 'Registration failed. Please try again.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.register h1 {
  text-align: center;
  margin-bottom: 20px;
}

.register div {
  margin-bottom: 15px;
}

.register label {
  display: block;
  margin-bottom: 5px;
}

.register input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.register button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}

.register button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.register .error {
  color: red;
  margin-bottom: 10px;
}

.register .success {
  color: green;
  margin-bottom: 10px;
}
</style>
