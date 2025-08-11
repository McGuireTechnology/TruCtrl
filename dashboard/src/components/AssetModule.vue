<template>
  <div class="asset-module">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="h4 mb-0">{{ moduleTitle }}</h2>
        <p class="text-muted small mb-0">{{ moduleDescription }}</p>
      </div>
      <button class="btn btn-primary" @click="handleAdd">
        <i class="fas fa-plus me-1"></i>
        Add {{ moduleTitle.slice(0, -1) }}
      </button>
    </div>

    <div class="card">
      <div class="card-body">
        <div class="text-center text-muted py-5">
          <i :class="moduleIcon" class="fa-3x mb-3 text-secondary"></i>
          <h5>{{ moduleTitle }} Management</h5>
          <p class="mb-0">This module is under development. Coming soon!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  moduleType: {
    type: String,
    required: true
  }
});

const moduleConfig = {
  devices: {
    title: 'Devices',
    description: 'Manage hardware devices and endpoints',
    icon: 'fas fa-laptop'
  },
  software: {
    title: 'Software',
    description: 'Manage software applications and systems',
    icon: 'fas fa-code'
  },
  data: {
    title: 'Data',
    description: 'Manage data assets and classifications',
    icon: 'fas fa-database'
  },
  network: {
    title: 'Network',
    description: 'Manage network infrastructure and connections',
    icon: 'fas fa-network-wired'
  },
  documentation: {
    title: 'Documentation',
    description: 'Access guides, policies, and procedures',
    icon: 'fas fa-file-alt'
  },
  activity: {
    title: 'Activity',
    description: 'View system activity and audit logs',
    icon: 'fas fa-history'
  }
};

const moduleTitle = computed(() => moduleConfig[props.moduleType]?.title || 'Module');
const moduleDescription = computed(() => moduleConfig[props.moduleType]?.description || 'Module description');
const moduleIcon = computed(() => moduleConfig[props.moduleType]?.icon || 'fas fa-cube');

const handleAdd = () => {
  console.log(`Add ${props.moduleType} functionality will be implemented here`);
  // TODO: Implement add functionality for each module type
};
</script>

<style scoped>
/* Module-specific styles will be added here as needed */
</style>
