
<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
// App.vue now serves as the main router container
</script>

<style>
#app {
  min-height: 100vh;
}

.nav-link.active {
  background: #0d6efd !important;
  color: #fff !important;
}
.bg-body-tertiary {
  background-color: #f8f9fa !important;
}
.border-end {
  border-right: 1px solid #dee2e6 !important;
}
</style>
