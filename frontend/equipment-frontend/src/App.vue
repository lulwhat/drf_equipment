<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4" v-if="isAuthenticated">
      <div class="container">
        <a class="navbar-brand" href="/">Equipment Management</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/equipment">Equipment List</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/equipment/add">Add Equipment</router-link>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <button class="btn btn-outline-light" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    
    <router-view />
  </div>
</template>

<script>
import api from 'axios'

export default {
  name: 'App',
  created() {
    this.validateTokenOnStartup();
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated
    }
  },
  methods: {
    async validateTokenOnStartup() {
      const access_token = localStorage.getItem('access_token');
      if (access_token) {
        try {
          await api.get('/token/verify/');
          this.$store.commit('SET_AUTHENTICATED', true);
        } catch (error) {
          this.clearAuthData();
        }
      }
    },
    clearAuthData() {
      localStorage.removeItem('access_token');
      delete api.defaults.headers.common['Authorization'];
      this.$store.commit('SET_AUTHENTICATED', false);
    },
    logout() {
        this.$store.dispatch('logout').then(() => {
          this.$router.push('/user/login')
        })
    }
  }
}
</script>