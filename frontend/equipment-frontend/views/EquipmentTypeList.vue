<template>
  <div class="container">
    <h1 class="mb-4">Equipment Types</h1>

    <!-- Search -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-center">
          <div class="col-md-8">
            <input
              type="text"
              class="form-control"
              placeholder="Search by name or mask"
              v-model="searchQuery"
              @input="debounceSearch"
            >
          </div>
          <div class="col-md-4 text-end">
            <button class="btn btn-outline-secondary" @click="resetFilters">
              <i class="bi bi-arrow-counterclockwise me-1"></i> Reset
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Equipment Types Table -->
    <div class="card">
      <div class="card-body">
        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else-if="equipmentTypes.length === 0" class="alert alert-info">
          No equipment types found.
        </div>

        <div v-else class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Serial Mask</th>
                <th>Linked Equipment</th>
                <th>Mask Pattern</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="type in equipmentTypes" :key="type.id">
                <td>{{ type.id }}</td>
                <td>{{ type.name }}</td>
                <td><code>{{ type.serial_number_mask }}</code></td>
                <td>
                  <span class="badge" :class="type.equipment_count > 0 ? 'bg-primary' : 'bg-secondary'">
                    {{ type.equipment_count || 0 }} items
                  </span>
                </td>
                <td>
                  <div class="mask-preview">
                    <span
                      v-for="(char, index) in type.serial_number_mask"
                      :key="index"
                      class="mask-char"
                      :class="getMaskCharClass(char)"
                      :title="getMaskDescription(char)"
                    >
                      {{ char }}
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <nav v-if="totalPages > 1">
            <ul class="pagination justify-content-center">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">
                  <i class="bi bi-chevron-left"></i>
                </a>
              </li>
              <li
                v-for="page in paginationRange"
                :key="page"
                class="page-item"
                :class="{ active: currentPage === page }"
              >
                <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">
                  <i class="bi bi-chevron-right"></i>
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../src/axios'

export default {
  name: 'EquipmentTypeList',
  data() {
    return {
      equipmentTypes: [],
      loading: true,
      searchQuery: '',
      currentPage: 1,
      totalPages: 1,
      pageSize: 10,

      // Debounce search
      searchTimeout: null
    }
  },
  computed: {
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
    getMaskDescription(char) {
      const descriptions = {
        'N': 'Digit (0-9)',
        'A': 'Uppercase letter (A-Z)',
        'a': 'Lowercase letter (a-z)',
        'X': 'Uppercase letter or digit',
        'Z': 'Special character (-, _, @)'
      }
      return descriptions[char] || 'Unknown character'
    },

    getMaskCharClass(char) {
      return {
        'digit-char': char === 'N',
        'upper-char': char === 'A',
        'lower-char': char === 'a',
        'mixed-char': char === 'X',
        'special-char': char === 'Z'
      }
    },

    async loadEquipmentTypes() {
      this.loading = true

      try {
        let url = `equipment-type/?page=${this.currentPage}&page_size=${this.pageSize}`

        if (this.searchQuery) {
          url += `&search=${encodeURIComponent(this.searchQuery)}`
        }

        const response = await api.get(url)
        this.equipmentTypes = response.data.results || []
        this.totalPages = Math.ceil(this.equipmentTypes.length / this.pageSize) || 1
      } catch (error) {
        console.error('Failed to load equipment types:', error)
        this.equipmentTypes = []
        this.totalPages = 1
      } finally {
        this.loading = false
      }
    },

    changePage(page) {
      if (page < 1 || page > this.totalPages) return
      this.currentPage = page
      this.loadEquipmentTypes()
    },

    resetFilters() {
      this.searchQuery = ''
      this.currentPage = 1
      this.loadEquipmentTypes()
    },

    debounceSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.currentPage = 1
        this.loadEquipmentTypes()
      }, 500)
    }
  },
  mounted() {
    this.loadEquipmentTypes()
  }
}
</script>

<style scoped>
.mask-preview {
  display: flex;
  gap: 2px;
  flex-wrap: wrap;
}

.mask-char {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  border-radius: 3px;
  font-family: monospace;
  font-weight: bold;
  font-size: 0.85rem;
}

.digit-char {
  background-color: #e3f2fd;
  color: #0d47a1;
}

.upper-char {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.lower-char {
  background-color: #fff8e1;
  color: #ff8f00;
}

.mixed-char {
  background-color: #f3e5f5;
  color: #6a1b9a;
}

.special-char {
  background-color: #ffebee;
  color: #c62828;
}

.badge {
  font-size: 0.85rem;
  padding: 0.35em 0.65em;
}
</style>