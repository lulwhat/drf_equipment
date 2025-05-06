<template>
  <div class="home">
    <div class="container py-5">
      <h1 class="mb-4">Equipment Management Dashboard</h1>
      
      <!-- Summary Cards -->
      <div class="row mb-4">
        <div class="col-md-4 mb-3">
          <div class="card h-100 border-primary">
            <div class="card-body">
              <h5 class="card-title">Equipment</h5>
              <p class="card-text display-4">{{ equipmentCount }}</p>
              <p class="card-text text-muted">Total equipment items</p>
            </div>
            <div class="card-footer bg-transparent border-0">
              <router-link to="/equipment" class="btn btn-outline-primary btn-sm">View All</router-link>
            </div>
          </div>
        </div>
        
        <div class="col-md-4 mb-3">
          <div class="card h-100 border-success">
            <div class="card-body">
              <h5 class="card-title">Equipment Types</h5>
              <p class="card-text display-4">{{ equipmentTypeCount }}</p>
              <p class="card-text text-muted">Available equipment types</p>
            </div>
            <div class="card-footer bg-transparent border-0">
              <router-link to="/equipment-types" class="btn btn-outline-success btn-sm">View All</router-link>
            </div>
          </div>
        </div>
        
        <div class="col-md-4 mb-3">
          <div class="card h-100 border-info">
            <div class="card-body">
              <h5 class="card-title">Recent Activity</h5>
              <p class="card-text display-4">{{ recentActivityCount }}</p>
              <p class="card-text text-muted">Changes in the last 7 days</p>
            </div>
            <div class="card-footer bg-transparent border-0">
              <router-link to="/activity" class="btn btn-outline-info btn-sm">View All</router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Quick Actions -->
      <div class="card mb-4">
        <div class="card-header">
          <h5 class="mb-0">Quick Actions</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-3 col-sm-6 mb-3">
              <router-link to="/equipment/add" class="btn btn-primary w-100 py-3">
                <i class="bi bi-plus-circle me-2"></i> Add Equipment
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6 mb-3">
              <router-link to="/equipment" class="btn btn-outline-secondary w-100 py-3">
                <i class="bi bi-search me-2"></i> Search Equipment
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6 mb-3">
              <router-link to="/reports" class="btn btn-outline-secondary w-100 py-3">
                <i class="bi bi-file-earmark-bar-graph me-2"></i> Generate Report
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6 mb-3">
              <router-link to="/settings" class="btn btn-outline-secondary w-100 py-3">
                <i class="bi bi-gear me-2"></i> Settings
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Recent Equipment -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0">Recently Added Equipment</h5>
          <router-link to="/equipment" class="btn btn-sm btn-link">View All</router-link>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          
          <div v-else-if="recentEquipment.length === 0" class="alert alert-info">
            No equipment found.
          </div>
          
          <div v-else class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Equipment Type</th>
                  <th>Serial Number</th>
                  <th>Added Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in recentEquipment" :key="item.id">
                  <td>{{ item.id }}</td>
                  <td>{{ item.equipment_type_name }}</td>
                  <td>{{ item.serial_number }}</td>
                  <td>{{ formatDate(item.created_at) }}</td>
                  <td>
                    <button
                      class="btn btn-sm btn-outline-primary me-1"
                      @click="$router.push(`/equipment/${item.id}`)"
                    >
                      <i class="bi bi-eye me-1"></i> View
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
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
  name: 'HomeView',
  components: {
    AppFooter
  },
  data() {
    return {
      equipmentCount: 0,
      equipmentTypeCount: 0,
      recentActivityCount: 0,
      recentEquipment: [],
      loading: true
    }
  },
  watch: {
    '$route': {
      immediate: true,
      handler() {
        if (this.isAuthenticated) {
          this.fetchDashboardData()
        }
      }
    }
  },
  methods: {
    async fetchDashboardData() {
      try {
        // Fetch equipment count
        const equipmentResponse = await api.get('equipment?page_size=1')
        this.equipmentCount = equipmentResponse.data.count || 0
        
        // Fetch equipment types count
        const typesResponse = await api.get('equipment-type?page_size=1')
        this.equipmentTypeCount = typesResponse.data.count || 0
        
        // Fetch recent equipment (last 5 items)
        const recentResponse = await api.get('equipment?page_size=5')
        this.recentEquipment = recentResponse.data.results || []
        
        // For demo purposes, set a random number for recent activity
        this.recentActivityCount = Math.floor(Math.random() * 20) + 1
        
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      } finally {
        this.loading = false
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
  },
  mounted() {
    this.fetchDashboardData()
  }
}
</script>

<style scoped>
.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.display-4 {
  font-size: 2.5rem;
  font-weight: 300;
}
</style>
