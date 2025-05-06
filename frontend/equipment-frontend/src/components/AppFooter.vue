<template>
  <footer class="footer mt-auto py-3 bg-light">
    <div class="container text-center">
      <span class="text-muted">
        &copy; {{ new Date().getFullYear() }} Equipment Management System |
        <router-link to="/about" class="text-decoration-none">About</router-link>
      </span>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
}
</script>

<style scoped>
.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
}
</style>