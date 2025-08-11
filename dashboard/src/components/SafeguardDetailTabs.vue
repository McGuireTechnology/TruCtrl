<template>
  <div class="safeguard-detail-tabs">
    <!-- Tab Navigation -->
    <ul class="nav nav-tabs mb-3" role="tablist">
      <li class="nav-item" role="presentation">
        <button 
          class="nav-link" 
          :class="{ active: activeTab === 'overview' }"
          @click="activeTab = 'overview'"
          type="button"
        >
          <i class="fas fa-info-circle me-2"></i>
          Overview
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button 
          class="nav-link" 
          :class="{ active: activeTab === 'relationships' }"
          @click="activeTab = 'relationships'"
          type="button"
        >
          <i class="fas fa-sitemap me-2"></i>
          Relationships
          <span v-if="relationshipCount > 0" class="badge bg-primary ms-2">{{ relationshipCount }}</span>
        </button>
      </li>
    </ul>

    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Overview Tab -->
      <div v-if="activeTab === 'overview'" class="tab-pane fade show active">
        <div class="row">
          <div class="col-md-8">
            <div class="card">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="fas fa-lock me-2"></i>
                  Safeguard Details
                </h5>
              </div>
              <div class="card-body">
                <div class="row g-3">
                  <div class="col-sm-6">
                    <label class="form-label text-muted small">Name</label>
                    <div class="fw-medium">{{ safeguard.name }}</div>
                  </div>
                  <div class="col-sm-6" v-if="safeguard.short_name">
                    <label class="form-label text-muted small">Short Name</label>
                    <div class="fw-medium">{{ safeguard.short_name }}</div>
                  </div>
                  <div class="col-12" v-if="safeguard.description">
                    <label class="form-label text-muted small">Description</label>
                    <div>{{ safeguard.description }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="card">
              <div class="card-header">
                <h6 class="card-title mb-0">
                  <i class="fas fa-tags me-2"></i>
                  Related Objects
                </h6>
              </div>
              <div class="card-body">
                <div class="d-flex flex-column gap-2">
                  <div v-if="safeguard.framework_name" class="d-flex align-items-center">
                    <span class="badge me-2" :style="{ backgroundColor: safeguard.framework_color || '#198754' }">
                      Framework
                    </span>
                    <span class="small">{{ safeguard.framework_short_name || safeguard.framework_name }}</span>
                  </div>
                  <div v-if="safeguard.control_name" class="d-flex align-items-center">
                    <span class="badge me-2" :style="{ backgroundColor: safeguard.control_color || '#6c757d' }">
                      Control
                    </span>
                    <span class="small">{{ safeguard.control_short_name || safeguard.control_name }}</span>
                  </div>
                  <div v-if="safeguard.function_name" class="d-flex align-items-center">
                    <span class="badge me-2" :style="{ backgroundColor: safeguard.function_color || '#0d6efd' }">
                      Function
                    </span>
                    <span class="small">{{ safeguard.function_short_name || safeguard.function_name }}</span>
                  </div>
                  <div v-if="safeguard.asset_class_name" class="d-flex align-items-center">
                    <span class="badge me-2" :style="{ backgroundColor: safeguard.asset_class_color || '#17a2b8' }">
                      Asset Class
                    </span>
                    <span class="small">{{ safeguard.asset_class_short_name || safeguard.asset_class_name }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Relationships Tab -->
      <div v-if="activeTab === 'relationships'" class="tab-pane fade show active">
        <SafeguardRelationships 
          :safeguard="safeguard" 
          @relationships-updated="handleRelationshipsUpdated"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import SafeguardRelationships from './SafeguardRelationships.vue';

const props = defineProps({
  safeguard: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['relationships-updated']);

const activeTab = ref('overview');

const relationshipCount = computed(() => {
  if (!props.safeguard.outbound_relationships && !props.safeguard.inbound_relationships) {
    return 0;
  }
  return (props.safeguard.outbound_relationships?.length || 0) + (props.safeguard.inbound_relationships?.length || 0);
});

const handleRelationshipsUpdated = () => {
  emit('relationships-updated');
};

// Watch for safeguard changes and reset to overview tab
watch(() => props.safeguard?.id, () => {
  activeTab.value = 'overview';
});
</script>

<style scoped>
.safeguard-detail-tabs {
  min-height: 400px;
}

.nav-tabs .nav-link {
  color: #6c757d;
  border: none;
  border-bottom: 2px solid transparent;
  background: none;
  padding: 0.75rem 1rem;
}

.nav-tabs .nav-link:hover {
  color: #495057;
  border-bottom-color: #dee2e6;
}

.nav-tabs .nav-link.active {
  color: #0d6efd;
  border-bottom-color: #0d6efd;
  background: none;
}

.card {
  border: 1px solid #dee2e6;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.badge {
  font-size: 0.75rem;
  color: white;
}
</style>
