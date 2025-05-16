<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Equipment Details</h1>
      <router-link to="/equipment" class="btn btn-outline-secondary">
        <i class="bi bi-arrow-left me-1"></i> Back to List
      </router-link>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else class="card">
      <div class="card-header">
        <h5 class="mb-0">{{ equipment.equipment_type_name }}</h5>
      </div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3">
              <label class="form-label fw-bold">ID:</label>
              <p>{{ equipment.id }}</p>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Serial Number:</label>
              <p class="serial-number">{{ equipment.serial_number }}</p>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Equipment Type:</label>
              <p>{{ equipment.equipment_type_name }}</p>
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3">
              <label class="form-label fw-bold">Created At:</label>
              <p>{{ formatDate(equipment.created_at) }}</p>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Last Updated:</label>
              <p>{{ formatDate(equipment.updated_at) }}</p>
            </div>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label fw-bold">Notes:</label>
          <p class="notes" v-if="equipment.notes">{{ equipment.notes }}</p>
          <p class="text-muted" v-else>No notes available</p>
        </div>

        <div class="d-flex gap-2">
          <button
            @click="showEditModal"
            class="btn btn-outline-primary"
          >
            <i class="bi bi-pencil me-1"></i> Edit
          </button>
          <button
            @click="confirmDelete"
            class="btn btn-outline-danger"
          >
            <i class="bi bi-trash me-1"></i> Delete
          </button>
          <button
            @click="$router.push('/equipment')"
            class="btn btn-outline-secondary"
          >
            <i class="bi bi-arrow-left me-1"></i> Back to List
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Modal  -->
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
                  :class="{ 'is-invalid': hasSerialNumberErrors }"
                >
                <div v-if="hasSerialNumberErrors" class="invalid-feedback">
                  <div v-for="(errorGroup, index) in editErrors.serial_numbers_errors" :key="index">
                    <strong>{{ errorGroup.serial_number }}:</strong>
                    <ul class="mb-0">
                      <li v-for="(error, i) in errorGroup.error" :key="i">{{ error }}</li>
                    </ul>
                  </div>
                </div>
                <div v-else-if="editErrors.serial_number" class="invalid-feedback">
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
            <p><strong>Type:</strong> {{ equipment.equipment_type_name }}</p>
            <p><strong>Serial Number:</strong> {{ equipment.serial_number }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button
              type="button"
              class="btn btn-danger"
              @click="deleteEquipment"
              :disabled="deleting"
            >
              <span v-if="deleting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
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
  name: 'EquipmentDetail',
  props: ['id'],
  data() {
    return {
      equipment: {},
      equipmentTypes: [],
      loading: true,
      error: null,
      deleting: false,
      deleteModal: null,
      editModal: null,
      editForm: {
        id: null,
        equipment_type: null,
        serial_number: '',
        notes: ''
      },
      editErrors: {},
      updating: false
    }
  },
  computed: {
    hasSerialNumberErrors() {
      return this.editErrors.serial_numbers_errors || this.editErrors.serial_number
    }
  },
  methods: {
    async fetchEquipment() {
      try {
        const response = await api.get(`equipment/${this.id}/`)
        this.equipment = response.data
        this.editForm = {
          id: this.equipment.id,
          equipment_type: this.equipment.equipment_type,
          serial_number: this.equipment.serial_number,
          notes: this.equipment.notes || ''
        }
      } catch (error) {
        this.error = 'Equipment is not found or has been deleted'
      } finally {
        this.loading = false
      }
    },
    async loadEquipmentTypes() {
      try {
        const response = await api.get('/equipment-type/')
        this.equipmentTypes = response.data.results
      } catch (error) {
        console.error('Failed to load equipment types:', error)
      }
    },
    showEditModal() {
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
        await this.fetchEquipment()
      } catch (error) {
        if (error.response?.data) {
          if (error.response.data.serial_numbers_errors) {
            this.editErrors = {
              serial_numbers_errors: error.response.data.serial_numbers_errors
            }
          } else {
            this.editErrors = error.response.data
          }
        } else {
          console.error('Error updating equipment:', error)
        }
      } finally {
        this.updating = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    confirmDelete() {
      this.deleteModal.show()
    },
    async deleteEquipment() {
      this.deleting = true
      try {
        await api.delete(`equipment/${this.id}/`)
        this.$router.push('/equipment')
      } catch (error) {
        console.error('Error deleting equipment:', error)
      } finally {
        this.deleting = false
        this.deleteModal.hide()
      }
    }
  },
  mounted() {
    this.editModal = new Modal(this.$refs.editModal)
    this.deleteModal = new Modal(this.$refs.deleteModal)
    this.fetchEquipment()
    this.loadEquipmentTypes()
  }
}
</script>

<style scoped>
.serial-number {
  font-family: monospace;
  font-size: 1.1rem;
  font-weight: bold;
}

.notes {
  white-space: pre-line;
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.25rem;
}
</style>