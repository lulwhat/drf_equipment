<template>
  <div class="container">
    <h1 class="mb-4">Add Equipment</h1>
    
    <div class="card">
      <div class="card-body">
        <form @submit.prevent="submitForm">
          <div class="mb-3">
            <label for="equipmentType" class="form-label">Equipment Type</label>
            <select 
              id="equipmentType" 
              class="form-select" 
              v-model="form.equipment_type" 
              required
            >
              <option value="" disabled>Select Equipment Type</option>
              <option v-for="type in equipmentTypes" :key="type.id" :value="type.id">
                {{ type.name }} (Mask: {{ type.serial_number_mask }})
              </option>
            </select>
          </div>
          
          <div class="mb-3">
            <label for="serialNumbers" class="form-label">Serial Numbers</label>
            <textarea 
              id="serialNumbers" 
              class="form-control" 
              v-model="form.serial_numbers_text" 
              rows="5"
              placeholder="Enter one serial number per line"
              required
            ></textarea>
            <div class="form-text">
              Enter one serial number per line. Each serial number will be validated against the selected equipment type's mask.
            </div>
            
            <div v-if="errors.serial_numbers_errors" class="mt-2">
              <div class="alert alert-danger">
                <p><strong>The following serial numbers have errors:</strong></p>
                <ul>
                  <li v-for="(error, index) in errors.serial_numbers_errors" :key="index">
                    <p><strong>{{ error.serial_number }}:</strong></p>
                    <ul>
                      <li v-for="(message, idx) in error.error" :key="idx">
                        {{ message }}
                      </li>
                    </ul>
                  </li>
                </ul>
              </div>
            </div>

          </div>
          
          <div class="mb-3">
            <label for="notes" class="form-label">Notes</label>
            <textarea 
              id="notes" 
              class="form-control" 
              v-model="form.notes" 
              rows="3"
              placeholder="Optional notes about this equipment"
            ></textarea>
          </div>
          
          <div class="d-flex justify-content-end">
            <button type="button" class="btn btn-secondary me-2" @click="resetForm">
              Reset
            </button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? 'Adding...' : 'Add Equipment' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Success Alert -->
    <div 
      v-if="showSuccess" 
      class="alert alert-success mt-4 alert-dismissible fade show" 
      role="alert"
    >
      Successfully added {{ successCount }} equipment items!
      <button 
        type="button" 
        class="btn-close" 
        @click="showSuccess = false" 
        aria-label="Close"
      ></button>
    </div>
  </div>
</template>

<script>
import api from '../src/axios'

export default {
  name: 'AddEquipment',
  data() {
    return {
      equipmentTypes: [],
      form: {
        equipment_type: '',
        serial_numbers_text: '',
        notes: ''
      },
      errors: {},
      submitting: false,
      showSuccess: false,
      successCount: 0
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
    
    async submitForm() {
      this.submitting = true
      this.errors = {}
      
      try {
        // Parse serial numbers from textarea (one per line)
        const serial_numbers = this.form.serial_numbers_text
          .split('\n')
          .map(sn => sn.trim())
          .filter(sn => sn !== '')
        
        const response = await api.post('/equipment/', {
          equipment_type: this.form.equipment_type,
          serial_numbers: serial_numbers,
          notes: this.form.notes
        })
        
        // Show success message
        this.showSuccess = true
        this.successCount = response.data.length
        
        // Reset form
        this.resetForm()
      } catch (error) {
        if (error.response?.data) {
          this.errors = error.response.data
        }
      } finally {
        this.submitting = false
      }
    },
    
    resetForm() {
      this.form = {
        equipment_type: '',
        serial_numbers_text: '',
        notes: ''
      }
      this.errors = {}
    }
  },
  mounted() {
    this.loadEquipmentTypes()
  }
}
</script>