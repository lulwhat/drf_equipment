<template>
  <div class="about">
    <div class="container py-5">
      <div class="row">
        <div class="col-lg-8 mx-auto">
          <div class="card shadow">
            <div class="card-body p-5">
              <h1 class="display-5 fw-bold text-center mb-4">About Equipment Management System</h1>
              
              <div class="mb-5">
                <h2 class="h4 mb-3">Overview</h2>
                <p>
                  The Equipment Management System is a comprehensive solution designed to help organizations track, 
                  manage, and maintain their equipment inventory efficiently. Our system provides a centralized 
                  platform for recording equipment details, tracking serial numbers, and managing equipment types.
                </p>
              </div>
              
              <div class="mb-5">
                <h2 class="h4 mb-3">Key Features</h2>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <div class="d-flex">
                      <div class="flex-shrink-0">
                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                      </div>
                      <div>
                        <h3 class="h6 mb-1">Equipment Tracking</h3>
                        <p class="text-muted small">Track all your equipment with detailed information</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <div class="d-flex">
                      <div class="flex-shrink-0">
                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                      </div>
                      <div>
                        <h3 class="h6 mb-1">Serial Number Validation</h3>
                        <p class="text-muted small">Validate serial numbers against custom masks</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <div class="d-flex">
                      <div class="flex-shrink-0">
                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                      </div>
                      <div>
                        <h3 class="h6 mb-1">Bulk Operations</h3>
                        <p class="text-muted small">Add or update multiple equipment items at once</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <div class="d-flex">
                      <div class="flex-shrink-0">
                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                      </div>
                      <div>
                        <h3 class="h6 mb-1">Search & Filter</h3>
                        <p class="text-muted small">Quickly find equipment with powerful search capabilities</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <div class="d-flex">
                      <div class="flex-shrink-0">
                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                      </div>
                      <div>
                        <h3 class="h6 mb-1">Equipment Types</h3>
                        <p class="text-muted small">Manage different types of equipment with custom attributes</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <div class="d-flex">
                      <div class="flex-shrink-0">
                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                      </div>
                      <div>
                        <h3 class="h6 mb-1">Secure Access</h3>
                        <p class="text-muted small">Role-based access control for different user types</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="mb-5">
                <h2 class="h4 mb-3">Technical Details</h2>
                <p>
                  This application is built using modern web technologies to ensure reliability, 
                  security, and performance:
                </p>
                <ul class="list-group list-group-flush mb-3">
                  <li class="list-group-item d-flex align-items-center">
                    <span class="badge bg-primary me-2">Frontend</span>
                    Vue.js with Vuex for state management
                  </li>
                  <li class="list-group-item d-flex align-items-center">
                    <span class="badge bg-success me-2">Backend</span>
                    Django REST Framework
                  </li>
                  <li class="list-group-item d-flex align-items-center">
                    <span class="badge bg-info me-2">Database</span>
                    MySQL for reliable data storage
                  </li>
                  <li class="list-group-item d-flex align-items-center">
                    <span class="badge bg-warning text-dark me-2">Authentication</span>
                    Token-based authentication for security
                  </li>
                </ul>
              </div>
              
              <div class="mb-5">
                <h2 class="h4 mb-3">Version Information</h2>
                <div class="table-responsive">
                  <table class="table table-sm">
                    <tbody>
                      <tr>
                        <th scope="row" style="width: 150px;">Version</th>
                        <td>1.0.0</td>
                      </tr>
                      <tr>
                        <th scope="row">Release Date</th>
                        <td>{{ new Date().toLocaleDateString() }}</td>
                      </tr>
                      <tr>
                        <th scope="row">Last Updated</th>
                        <td>{{ new Date().toLocaleDateString() }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              
              <div class="text-center">
                <h2 class="h4 mb-3">Contact Information</h2>
                <p>
                  For support or inquiries, please contact:
                  <a href="mailto:support@example.com" class="text-decoration-none">support@example.com</a>
                </p>
                <p class="text-muted small mt-4">
                  &copy; {{ new Date().getFullYear() }} Equipment Management System. All rights reserved.
                </p>
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
  name: 'AboutView'
}
</script>

<style scoped>
.about {
  background-color: #f8f9fa;
  min-height: calc(100vh - 56px);
  padding-bottom: 56px;
}

.card {
  border-radius: 10px;
  border: none;
}

.badge {
  font-weight: normal;
  font-size: 0.75rem;
  padding: 0.35em 0.65em;
}
</style>
