<template>
  <div class="container">
    <h1 class="mb-4">Equipment List</h1>
    
    <!-- Search Form -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <input 
              type="text" 
              class="form-control" 
              placeholder="Search by serial number or notes" 
              v-model="searchQuery"
              @input="debounceSearch"
            >
          </div>
          <div class="col-md-4">
            <select class="form-select" v-model="selectedType" @change="loadEquipment">
              <option value="">All Equipment Types</option>
              <option v-for="type in equipmentTypes" :key="type.id" :value="type.id">
                {{ type.name }}
              </option>
            </select>
          </div>
          <div class="col-md-4">
            <button class="btn btn-primary" @click="loadEquipment">
              Search
            </button>
            <button class="btn btn-outline-secondary ms-2" @click="resetFilters">
              Reset
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Equipment Table -->
    <div class="card">
      <div class="card-body">
        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        
        <div v-else-if="equipment.length === 0" class="alert alert-info">
          No equipment found.
        </div>
        
        <div v-else class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Equipment Type</th>
                <th>Serial Number</th>
                <th>Notes</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in equipment" :key="item.id">
                <td>{{ item.id }}</td>
                <td>{{ item.equipment_type_name }}</td>
                <td>{{ item.serial_number }}</td>
                <td>{{ item.notes }}</td>
                <td>
                  <button
                    class="btn btn-sm btn-outline-primary me-1"
                    @click="$router.push(`/equipment/${item.id}`)"
                  >
                  <i class="bi bi-eye me-1"></i> View
                  </button>
                  <button 
                    class="btn btn-sm btn-outline-primary me-1" 
                    @click="editEquipment(item)"
                  >
                    <i class="bi bi-pencil me-1"></i> Edit
                  </button>
                  <button 
                    class="btn btn-sm btn-outline-danger" 
                    @click="confirmDelete(item)"
                  >
                    <i class="bi bi-trash me-1"></i> Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          
          <!-- Pagination -->
          <nav v-if="totalPages > 1">
              <ul class="pagination justify-content-center">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">Previous</a>
                </li>

                <!-- Always show first page -->
                <li class="page-item" :class="{ active: currentPage === 1 }">
                  <a class="page-link" href="#" @click.prevent="changePage(1)">1</a>
                </li>

                <!-- Show ellipsis if current range doesn't include page 2 -->
                <li class="page-item disabled" v-if="currentPage > 3">
                  <span class="page-link">...</span>
                </li>

                <!-- Show pages around current page -->
                <template v-for="page in middlePages" :key="page">
                  <li class="page-item" :class="{ active: currentPage === page }">
                    <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
                  </li>
                </template>

                <!-- Show ellipsis if current range doesn't include last page - 1 -->
                <li class="page-item disabled" v-if="currentPage < totalPages - 2">
                  <span class="page-link">...</span>
                </li>

                <!-- Always show last page if it's not 1 -->
                <li class="page-item" :class="{ active: currentPage === totalPages }" v-if="totalPages > 1">
                  <a class="page-link" href="#" @click.prevent="changePage(totalPages)">{{ totalPages }}</a>
                </li>

                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">Next</a>
                </li>
              </ul>
          </nav>
        </div>
      </div>
    </div>
    
    <!-- Edit Modal -->
    <div class="modal fade" id="editModal" tabindex="-1" ref="editModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Equipment</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateEquipment">
              <div class="mb-3">
                <label class="form-label">Equipment Type</label>
                <select class="form-select" v-model="editForm.equipment_type" required>
                  <option v-for="type in equipmentTypes" :key="type.id" :value="type.id">
                    {{ type.name }}
                  </option>
                </select>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Serial Number</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="editForm.serial_number" 
                  required
                >
                <div v-if="editErrors.serial_number" class="text-danger mt-1">
                  {{ editErrors.serial_number }}
                </div>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Notes</label>
                <textarea 
                  class="form-control" 
                  v-model="editForm.notes" 
                  rows="3"
                ></textarea>
              </div>
              
              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary" :disabled="updating">
                  {{ updating ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1" ref="deleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this equipment?</p>
            <p><strong>Type:</strong> {{ deleteItem?.equipment_type_name }}</p>
            <p><strong>Serial Number:</strong> {{ deleteItem?.serial_number }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button 
              type="button" 
              class="btn btn-danger" 
              @click="deleteEquipment" 
              :disabled="deleting"
            >
              {{ deleting ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../src/axios'
import { Modal } from 'bootstrap'

export default {
  name: 'EquipmentList',
  data() {
    return {
      equipment: [],
      equipmentTypes: [],
      loading: true,
      searchQuery: '',
      selectedType: '',
      currentPage: 1,
      totalPages: 1,
      pageSize: 10,
      
      // Edit form
      editModal: null,
      editForm: {
        id: null,
        equipment_type: null,
        serial_number: '',
        notes: ''
      },
      editErrors: {},
      updating: false,
      
      // Delete
      deleteModal: null,
      deleteItem: null,
      deleting: false,
      
      // Debounce search
      searchTimeout: null
    }
  },
  computed: {
    middlePages() {
      const pages = [];
      const rangeSize = 3; // Number of pages to show around current page

      let start = Math.max(2, this.currentPage - Math.floor(rangeSize / 2));
      let end = Math.min(this.totalPages - 1, start + rangeSize - 1);

      // Adjust if we're at the end
      if (end === this.totalPages - 1) {
        start = Math.max(2, end - rangeSize + 1);
      }

      // Don't show middle pages if they would overlap with first/last
      if (this.totalPages <= 5) {
        for (let i = 2; i <= this.totalPages - 1; i++) {
          pages.push(i);
        }
      } else {
        for (let i = start; i <= end; i++) {
          pages.push(i);
        }
      }

      return pages;
    },
    paginationRange() {
      const range = []
      const maxVisiblePages = 5
      
      let start = Math.max(1, this.currentPage - Math.floor(maxVisiblePages / 2))
      let end = Math.min(this.totalPages, start + maxVisiblePages - 1)
      
      if (end - start + 1 < maxVisiblePages) {
        start = Math.max(1, end - maxVisiblePages + 1)
      }
      
      for (let i = start; i <= end; i++) {
        range.push(i)
      }
      
      return range
    }
  },
  methods: {
    async loadEquipmentTypes() {
      try {
        const response = await api.get('/equipment-type/')
        this.equipmentTypes = response.data.results
      } catch (error) {
        console.error('Failed to load equipment types:', error)
      }
    },
    
    async loadEquipment() {
      this.loading = true
      
      try {
        let url = `equipment?page=${this.currentPage}&page_size=${this.pageSize}`
        
        if (this.searchQuery) {
          url += `&search=${encodeURIComponent(this.searchQuery)}`
        }
        
        if (this.selectedType) {
          url += `&equipment_type=${this.selectedType}`
        }
        
        const response = await api.get(url)
        this.equipment = response.data.results
        this.totalPages = Math.ceil(response.data.count / this.pageSize)
      } catch (error) {
        console.error('Failed to load equipment:', error)
      } finally {
        this.loading = false
      }
    },
    
    changePage(page) {
      if (page < 1 || page > this.totalPages) return
      this.currentPage = page
      this.loadEquipment()
    },
    
    resetFilters() {
      this.searchQuery = ''
      this.selectedType = ''
      this.currentPage = 1
      this.loadEquipment()
    },
    
    debounceSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.currentPage = 1
        this.loadEquipment()
      }, 500)
    },
    
    editEquipment(item) {
      this.editForm = {
        id: item.id,
        equipment_type: item.equipment_type,
        serial_number: item.serial_number,
        notes: item.notes || ''
      }
      this.editErrors = {}
      this.editModal.show()
    },
    
    async updateEquipment() {
      this.updating = true
      this.editErrors = {}
      
      try {
        await api.put(`equipment/${this.editForm.id}/`, {
          equipment_type: this.editForm.equipment_type,
          serial_number: this.editForm.serial_number,
          notes: this.editForm.notes
        })
        
        this.editModal.hide()
        await this.loadEquipment()
        
      } catch (error) {
        if (error.response?.data) {
          this.editErrors = error.response.data
        }
      } finally {
        this.updating = false
      }
    },
    
    confirmDelete(item) {
      this.deleteItem = item
      this.deleteModal.show()
    },
    
    async deleteEquipment() {
      this.deleting = true
      
      try {
        await api.delete(`equipment/${this.deleteItem.id}/`)
        this.deleteModal.hide()
        await this.loadEquipment()
      } catch (error) {
        console.error('Failed to delete equipment:', error)
      } finally {
        this.deleting = false
      }
    }
  },
  mounted() {
    this.editModal = new Modal(this.$refs.editModal)
    this.deleteModal = new Modal(this.$refs.deleteModal)
    
    this.loadEquipmentTypes()
    this.loadEquipment()
  }
}
</script>