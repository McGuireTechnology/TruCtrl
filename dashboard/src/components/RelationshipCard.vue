<template>
  <div class="relationship-card card h-100">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <div class="relationship-type">
          <span 
            class="badge" 
            :class="relationshipTypeBadgeClass"
          >
            <i :class="relationshipTypeIcon" class="me-1"></i>
            {{ relationshipTypeLabel }}
          </span>
        </div>
        <div class="relationship-actions">
          <button 
            class="btn btn-sm btn-outline-primary me-1" 
            @click="$emit('edit', relationship)"
            title="Edit Relationship"
          >
            <i class="fas fa-edit"></i>
          </button>
          <button 
            class="btn btn-sm btn-outline-danger" 
            @click="$emit('delete', relationship)"
            title="Delete Relationship"
          >
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>

      <div class="target-safeguard mb-3">
        <h6 class="mb-1">
          {{ relationship.target_safeguard_name }}
        </h6>
        <div class="text-muted small">
          {{ relationship.target_safeguard_short_name }}
        </div>
        <div v-if="relationship.target_framework_name" class="mt-1">
          <span 
            class="badge badge-framework" 
            :style="{ backgroundColor: relationship.target_framework_color || '#198754' }"
          >
            {{ relationship.target_framework_short_name || relationship.target_framework_name }}
          </span>
        </div>
      </div>

      <div class="relationship-details">
        <div class="row g-2 mb-2">
          <div class="col-6">
            <label class="form-label text-muted small mb-1">Confidence</label>
            <div class="confidence-bar">
              <div class="progress" style="height: 6px;">
                <div 
                  class="progress-bar" 
                  :class="confidenceBarClass"
                  :style="{ width: `${relationship.confidence * 100}%` }"
                ></div>
              </div>
              <span class="small text-muted">{{ Math.round(relationship.confidence * 100) }}%</span>
            </div>
          </div>
          <div class="col-6" v-if="direction">
            <label class="form-label text-muted small mb-1">Direction</label>
            <div class="direction-indicator">
              <i 
                :class="direction === 'outbound' ? 'fas fa-arrow-right text-primary' : 'fas fa-arrow-left text-info'"
              ></i>
              <span class="small ms-1">{{ direction === 'outbound' ? 'Outbound' : 'Inbound' }}</span>
            </div>
          </div>
        </div>

        <div v-if="relationship.notes" class="notes">
          <label class="form-label text-muted small mb-1">Notes</label>
          <div class="small text-muted">{{ relationship.notes }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  relationship: {
    type: Object,
    required: true
  },
  direction: {
    type: String,
    required: false,
    validator: value => ['inbound', 'outbound'].includes(value)
  }
});

defineEmits(['edit', 'delete']);

const relationshipTypeLabel = computed(() => {
  switch (props.relationship.relationship_type) {
    case 'superset':
      return 'Superset';
    case 'subset':
      return 'Subset';
    case 'equivalent':
      return 'Equivalent';
    default:
      return 'Unknown';
  }
});

const relationshipTypeBadgeClass = computed(() => {
  switch (props.relationship.relationship_type) {
    case 'superset':
      return 'bg-success';
    case 'subset':
      return 'bg-warning';
    case 'equivalent':
      return 'bg-info';
    default:
      return 'bg-secondary';
  }
});

const relationshipTypeIcon = computed(() => {
  switch (props.relationship.relationship_type) {
    case 'superset':
      return 'fas fa-expand-arrows-alt';
    case 'subset':
      return 'fas fa-compress-arrows-alt';
    case 'equivalent':
      return 'fas fa-equals';
    default:
      return 'fas fa-question';
  }
});

const confidenceBarClass = computed(() => {
  const confidence = props.relationship.confidence;
  if (confidence >= 0.8) return 'bg-success';
  if (confidence >= 0.6) return 'bg-warning';
  return 'bg-danger';
});
</script>

<style scoped>
.relationship-card {
  border: 1px solid #dee2e6;
  transition: all 0.2s ease;
}

.relationship-card:hover {
  border-color: #0d6efd;
  box-shadow: 0 0.125rem 0.25rem rgba(13, 110, 253, 0.25);
}

.relationship-actions {
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.relationship-card:hover .relationship-actions {
  opacity: 1;
}

.badge-framework {
  color: white;
  font-size: 0.75rem;
}

.confidence-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progress {
  flex: 1;
  background-color: #e9ecef;
}

.direction-indicator {
  display: flex;
  align-items: center;
}

.notes {
  background-color: #f8f9fa;
  padding: 0.5rem;
  border-radius: 0.25rem;
  border-left: 3px solid #dee2e6;
}

.btn-sm {
  font-size: 0.75rem;
  padding: 0.25rem 0.4rem;
}
</style>
