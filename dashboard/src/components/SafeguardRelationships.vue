<template>
  <div class="safeguard-relationships">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5 class="mb-0">
        <i class="fas fa-sitemap me-2"></i>
        Safeguard Relationships
      </h5>
      <button 
        class="btn btn-primary btn-sm" 
        @click="showAddRelationshipModal = true"
        :disabled="loading"
      >
        <i class="fas fa-plus me-2"></i>
        Add Relationship
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <div class="mt-2 text-muted">Loading relationships...</div>
    </div>

    <!-- Relationships Tabs -->
    <div v-else>
      <!-- Tab Navigation -->
      <ul class="nav nav-tabs" role="tablist">
        <li class="nav-item" role="presentation">
          <button 
            class="nav-link" 
            :class="{ active: activeRelationshipTab === 'outbound' }"
            @click="activeRelationshipTab = 'outbound'"
            type="button"
          >
            <i class="fas fa-arrow-right me-2"></i>
            Outbound
            <span class="badge bg-secondary ms-2">{{ outboundRelationships.length }}</span>
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button 
            class="nav-link" 
            :class="{ active: activeRelationshipTab === 'inbound' }"
            @click="activeRelationshipTab = 'inbound'"
            type="button"
          >
            <i class="fas fa-arrow-left me-2"></i>
            Inbound
            <span class="badge bg-secondary ms-2">{{ inboundRelationships.length }}</span>
          </button>
        </li>
      </ul>

      <!-- Tab Content -->
      <div class="tab-content mt-3">
        <!-- Outbound Relationships Tab -->
        <div v-if="activeRelationshipTab === 'outbound'" class="tab-pane active">
          <div v-if="outboundRelationships.length === 0" class="alert alert-light">
            <i class="fas fa-info-circle me-2"></i>
            No outbound relationships defined. This safeguard doesn't reference other safeguards.
            <div class="mt-2">
              <small class="text-muted">
                Outbound relationships show what other safeguards this one relates to.
              </small>
            </div>
          </div>
          <div v-else class="row g-3">
            <div 
              v-for="relationship in outboundRelationships" 
              :key="relationship.id"
              class="col-md-6"
            >
              <RelationshipCard 
                :relationship="relationship" 
                :direction="'outbound'"
                @edit="editRelationship"
                @delete="deleteRelationship"
              />
            </div>
          </div>
        </div>

        <!-- Inbound Relationships Tab -->
        <div v-if="activeRelationshipTab === 'inbound'" class="tab-pane active">
          <div v-if="inboundRelationships.length === 0" class="alert alert-light">
            <i class="fas fa-info-circle me-2"></i>
            No inbound relationships found. Other safeguards don't reference this one.
            <div class="mt-2">
              <small class="text-muted">
                Inbound relationships show what other safeguards relate to this one.
              </small>
            </div>
          </div>
          <div v-else class="row g-3">
            <div 
              v-for="relationship in inboundRelationships" 
              :key="relationship.id"
              class="col-md-6"
            >
              <RelationshipCard 
                :relationship="relationship" 
                :direction="'inbound'"
                @edit="editRelationship"
                @delete="deleteRelationship"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Relationship Modal -->
    <div class="modal fade" :class="{ show: showAddRelationshipModal }" :style="{ display: showAddRelationshipModal ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Safeguard Relationship</h5>
            <button type="button" class="btn-close" @click="closeAddModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createRelationship">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Target Safeguard</label>
                  <select 
                    v-model="newRelationship.target_safeguard_id" 
                    class="form-select" 
                    required
                  >
                    <option value="">Select a safeguard...</option>
                    <option 
                      v-for="safeguard in availableSafeguards" 
                      :key="safeguard.id" 
                      :value="safeguard.id"
                    >
                      {{ safeguard.short_name ? `${safeguard.short_name} — ${safeguard.name}` : safeguard.name }}
                      <span v-if="safeguard.framework_short_name" class="text-muted">
                        ({{ safeguard.framework_short_name }})
                      </span>
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Relationship Type</label>
                  <select v-model="newRelationship.relationship_type" class="form-select" required>
                    <option value="">Select relationship...</option>
                    <option value="superset">Superset (covers more than target)</option>
                    <option value="equivalent">Equivalent (same as target)</option>
                    <option value="subset">Subset (covers less than target)</option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Confidence Level</label>
                  <div class="d-flex align-items-center gap-2">
                    <input 
                      v-model.number="newRelationship.confidence" 
                      type="range" 
                      class="form-range flex-1" 
                      min="0" 
                      max="1" 
                      step="0.1"
                    >
                    <span class="badge bg-secondary">{{ Math.round(newRelationship.confidence * 100) }}%</span>
                  </div>
                </div>
                <div class="col-12">
                  <label class="form-label">Notes (Optional)</label>
                  <textarea 
                    v-model="newRelationship.notes" 
                    class="form-control" 
                    rows="3" 
                    placeholder="Additional notes about this relationship..."
                  ></textarea>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeAddModal">Cancel</button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="createRelationship"
              :disabled="!newRelationship.target_safeguard_id || !newRelationship.relationship_type || submitting"
            >
              <i v-if="submitting" class="fas fa-spinner fa-spin me-2"></i>
              Create Relationship
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Backdrop -->
    <div v-if="showAddRelationshipModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import RelationshipCard from './RelationshipCard.vue';
import { 
  getSafeguards, 
  getSafeguardRelationships, 
  createSafeguardRelationship, 
  deleteSafeguardRelationship 
} from '../api';

const props = defineProps({
  safeguard: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['relationships-updated']);

const loading = ref(false);
const submitting = ref(false);
const showAddRelationshipModal = ref(false);
const activeRelationshipTab = ref('outbound');
const allSafeguards = ref([]);
const relationships = ref({
  outbound_relationships: [],
  inbound_relationships: []
});

const newRelationship = ref({
  target_safeguard_id: '',
  relationship_type: '',
  confidence: 1.0,
  notes: ''
});

const outboundRelationships = computed(() => {
  return relationships.value.outbound_relationships || [];
});

const inboundRelationships = computed(() => {
  return relationships.value.inbound_relationships || [];
});

const availableSafeguards = computed(() => {
  return allSafeguards.value.filter(sg => 
    sg.id !== props.safeguard.id && 
    !outboundRelationships.value.some(rel => rel.target_safeguard_id === sg.id)
  );
});

const loadRelationships = async () => {
  if (!props.safeguard?.id) {
    console.warn('loadRelationships called but no safeguard ID available');
    return;
  }
  
  console.log('Loading relationships for safeguard:', props.safeguard.id, props.safeguard.name);
  loading.value = true;
  try {
    const data = await getSafeguardRelationships(props.safeguard.id);
    relationships.value = {
      outbound_relationships: data.outbound_relationships || [],
      inbound_relationships: data.inbound_relationships || []
    };
    console.log('Successfully loaded relationships:', relationships.value);
  } catch (error) {
    console.error('Error loading relationships for safeguard', props.safeguard.id, ':', error);
    // Don't fail silently - show the user what happened
    if (error.message && error.message.includes('Load failed')) {
      console.error('This is likely an authentication or CORS issue');
    }
  } finally {
    loading.value = false;
  }
};

const loadSafeguards = async () => {
  try {
    const response = await getSafeguards();
    allSafeguards.value = Array.isArray(response) ? response : response.data || [];
  } catch (error) {
    console.error('Error loading safeguards:', error);
    allSafeguards.value = [];
  }
};

const createRelationship = async () => {
  if (!newRelationship.value.target_safeguard_id || !newRelationship.value.relationship_type) {
    return;
  }

  console.log('Creating relationship from', props.safeguard.id, 'to', newRelationship.value.target_safeguard_id);
  submitting.value = true;
  try {
    await createSafeguardRelationship(props.safeguard.id, newRelationship.value);
    console.log('Relationship created successfully, now reloading...');
    await loadRelationships();
    closeAddModal();
    emit('relationships-updated');
  } catch (error) {
    console.error('Error creating relationship:', error);
    alert('Error creating relationship: ' + (error.message || 'Unknown error'));
  } finally {
    submitting.value = false;
  }
};

const editRelationship = (relationship) => {
  // TODO: Implement edit functionality
  console.log('Edit relationship:', relationship);
};

const deleteRelationship = async (relationship) => {
  if (!confirm('Are you sure you want to delete this relationship? This will also remove the reverse relationship.')) {
    return;
  }

  try {
    await deleteSafeguardRelationship(relationship.id);
    await loadRelationships();
    emit('relationships-updated');
  } catch (error) {
    console.error('Error deleting relationship:', error);
    alert('Error deleting relationship: ' + (error.message || 'Unknown error'));
  }
};

const closeAddModal = () => {
  showAddRelationshipModal.value = false;
  newRelationship.value = {
    target_safeguard_id: '',
    relationship_type: '',
    confidence: 1.0,
    notes: ''
  };
};

// Watch for safeguard changes
watch(() => props.safeguard?.id, () => {
  loadRelationships();
}, { immediate: true });

onMounted(() => {
  loadSafeguards();
});
</script>

<style scoped>
.modal.show {
  display: block !important;
}

.modal-backdrop {
  z-index: 1040;
}

.modal {
  z-index: 1050;
}

.form-range {
  flex: 1;
}

.alert-light {
  background-color: #f8f9fa;
  border-color: #dee2e6;
  color: #6c757d;
}
</style>
