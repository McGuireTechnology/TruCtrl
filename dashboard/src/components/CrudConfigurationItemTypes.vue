<template>
  <div>
    <h3 v-if="selected">Edit Configuration Item Type</h3>
    <h3 v-else>Create Configuration Item Type</h3>
    <form @submit.prevent="onSubmit">
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input v-model="form.name" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Short Name</label>
        <input v-model="form.short_name" class="form-control" placeholder="e.g., PHYS, TECH" />
      </div>
      <div class="mb-3">
        <label class="form-label">Description</label>
        <textarea v-model="form.description" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Color</label>
        <div class="d-flex align-items-center gap-2">
          <input 
            v-model="form.color" 
            type="color" 
            class="form-control form-control-color" 
            style="width: 3rem; height: 38px;"
            title="Choose color"
          />
          <input 
            v-model="form.color" 
            type="text" 
            class="form-control" 
            placeholder="#17a2b8"
            pattern="^#[0-9A-Fa-f]{6}$"
            title="Enter hex color code (e.g., #17a2b8)"
          />
        </div>
        <div class="form-text">Choose a color to identify this configuration item type in the interface</div>
      </div>

      <!-- Relationship Management - only show when editing -->
      <div v-if="selected" class="mb-4">
        <hr>
        <h5 class="mb-3">Configuration Item Type Relationships</h5>
        
        <!-- Parent Configuration Item Types -->
        <div class="mb-3">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <label class="form-label mb-0">Parent Configuration Item Types</label>
            <button type="button" class="btn btn-sm btn-outline-primary" @click="showAddParentModal = true">
              <i class="bi bi-plus"></i> Add Parent
            </button>
          </div>
          <div v-if="parents.length === 0" class="text-muted fst-italic">No parent configuration item types</div>
          <div v-else class="d-flex flex-wrap gap-2">
            <span v-for="parent in parents" :key="parent.id" class="badge d-flex align-items-center gap-1" :style="`background-color: ${parent.color}`">
              {{ parent.name }}
              <button type="button" class="btn-close btn-close-white" style="font-size: 0.6em;" @click="removeParent(parent.id)"></button>
            </span>
          </div>
        </div>

        <!-- Child Configuration Item Types -->
        <div class="mb-3">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <label class="form-label mb-0">Child Configuration Item Types</label>
            <button type="button" class="btn btn-sm btn-outline-primary" @click="showAddChildModal = true">
              <i class="bi bi-plus"></i> Add Child
            </button>
          </div>
          <div v-if="children.length === 0" class="text-muted fst-italic">No child configuration item types</div>
          <div v-else class="d-flex flex-wrap gap-2">
            <span v-for="child in children" :key="child.id" class="badge d-flex align-items-center gap-1" :style="`background-color: ${child.color}`">
              {{ child.name }}
              <button type="button" class="btn-close btn-close-white" style="font-size: 0.6em;" @click="removeChild(child.id)"></button>
            </span>
          </div>
        </div>
      </div>

      <button class="btn btn-primary" type="submit">{{ selected ? 'Update' : 'Create' }}</button>
      <button v-if="selected" class="btn btn-danger ms-2" @click.prevent="onDelete">Delete</button>
    </form>

    <!-- Add Parent Modal -->
    <div v-if="showAddParentModal" class="modal show d-block" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Parent Configuration Item Type</h5>
            <button type="button" class="btn-close" @click="showAddParentModal = false"></button>
          </div>
          <div class="modal-body">
            <label class="form-label">Select Parent Configuration Item Type</label>
            <select v-model="selectedParentId" class="form-select">
              <option value="">Choose a parent configuration item type...</option>
              <option v-for="configItemType in availableParents" :key="configItemType.id" :value="configItemType.id">
                {{ configItemType.name }}
              </option>
            </select>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showAddParentModal = false">Cancel</button>
            <button type="button" class="btn btn-primary" @click="addParent" :disabled="!selectedParentId">Add Parent</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Child Modal -->
    <div v-if="showAddChildModal" class="modal show d-block" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Child Configuration Item Type</h5>
            <button type="button" class="btn-close" @click="showAddChildModal = false"></button>
          </div>
          <div class="modal-body">
            <label class="form-label">Select Child Configuration Item Type</label>
            <select v-model="selectedChildId" class="form-select">
              <option value="">Choose a child configuration item type...</option>
              <option v-for="configItemType in availableChildren" :key="configItemType.id" :value="configItemType.id">
                {{ configItemType.name }}
              </option>
            </select>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showAddChildModal = false">Cancel</button>
            <button type="button" class="btn btn-primary" @click="addChild" :disabled="!selectedChildId">Add Child</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { 
  createConfigurationItemType, 
  updateConfigurationItemType, 
  deleteConfigurationItemType,
  getConfigurationItemTypes,
  getConfigurationItemTypeParents,
  getConfigurationItemTypeChildren,
  addConfigurationItemTypeParent,
  removeConfigurationItemTypeParent
} from '../api';

const props = defineProps({ selected: Object });
const emit = defineEmits(['refresh']);

const form = ref({ name: '', short_name: '', description: '', color: '#17a2b8' });

// Relationship data
const parents = ref([]);
const children = ref([]);
const allConfigurationItemTypes = ref([]);

// Modal states
const showAddParentModal = ref(false);
const showAddChildModal = ref(false);
const selectedParentId = ref('');
const selectedChildId = ref('');

// Computed available options (exclude current item and existing relationships)
const availableParents = computed(() => {
  if (!props.selected) return [];
  return allConfigurationItemTypes.value.filter(cit => 
    cit.id !== props.selected.id && 
    !parents.value.some(p => p.id === cit.id)
  );
});

const availableChildren = computed(() => {
  if (!props.selected) return [];
  return allConfigurationItemTypes.value.filter(cit => 
    cit.id !== props.selected.id && 
    !children.value.some(c => c.id === cit.id)
  );
});

// Load all configuration item types for the dropdowns
async function loadAllConfigurationItemTypes() {
  try {
    const response = await getConfigurationItemTypes();
    allConfigurationItemTypes.value = response.data || [];
  } catch (error) {
    console.error('Error loading configuration item types:', error);
  }
}

// Load relationships for the selected configuration item type
async function loadRelationships() {
  if (!props.selected?.id) {
    parents.value = [];
    children.value = [];
    return;
  }

  try {
    const [parentsResponse, childrenResponse] = await Promise.all([
      getConfigurationItemTypeParents(props.selected.id),
      getConfigurationItemTypeChildren(props.selected.id)
    ]);
    
    parents.value = parentsResponse.data || [];
    children.value = childrenResponse.data || [];
  } catch (error) {
    console.error('Error loading relationships:', error);
    parents.value = [];
    children.value = [];
  }
}

watch(() => props.selected, async (newSelected) => {
  if (newSelected) {
    form.value = { ...newSelected };
    await loadRelationships();
  } else {
    form.value = { name: '', short_name: '', description: '', color: '#17a2b8' };
    parents.value = [];
    children.value = [];
  }
}, { immediate: true });

// Load all configuration item types when component mounts
loadAllConfigurationItemTypes();

async function onSubmit() {
  try {
    if (props.selected) {
      await updateConfigurationItemType(props.selected.id, form.value);
    } else {
      await createConfigurationItemType(form.value);
    }
    emit('refresh');
  } catch (error) {
    console.error('Error saving configuration item type:', error);
    alert('Error saving configuration item type: ' + error.message);
  }
}

async function onDelete() {
  if (confirm('Are you sure you want to delete this configuration item type?')) {
    try {
      await deleteConfigurationItemType(props.selected.id);
      emit('refresh');
    } catch (error) {
      console.error('Error deleting configuration item type:', error);
      alert('Error deleting configuration item type: ' + error.message);
    }
  }
}

// Relationship management functions
async function addParent() {
  if (!selectedParentId.value || !props.selected?.id) return;
  
  try {
    await addConfigurationItemTypeParent(props.selected.id, selectedParentId.value);
    await loadRelationships();
    showAddParentModal.value = false;
    selectedParentId.value = '';
  } catch (error) {
    console.error('Error adding parent:', error);
    let errorMessage = 'Unknown error';
    if (error.message) {
      try {
        const errorData = JSON.parse(error.message);
        errorMessage = errorData.detail || error.message;
      } catch {
        errorMessage = error.message;
      }
    }
    alert('Error adding parent: ' + errorMessage);
  }
}

async function addChild() {
  if (!selectedChildId.value || !props.selected?.id) return;
  
  try {
    await addConfigurationItemTypeParent(selectedChildId.value, props.selected.id);
    await loadRelationships();
    showAddChildModal.value = false;
    selectedChildId.value = '';
  } catch (error) {
    console.error('Error adding child:', error);
    let errorMessage = 'Unknown error';
    if (error.message) {
      try {
        const errorData = JSON.parse(error.message);
        errorMessage = errorData.detail || error.message;
      } catch {
        errorMessage = error.message;
      }
    }
    alert('Error adding child: ' + errorMessage);
  }
}

async function removeParent(parentId) {
  if (!props.selected?.id) return;
  
  if (confirm('Are you sure you want to remove this parent relationship?')) {
    try {
      await removeConfigurationItemTypeParent(props.selected.id, parentId);
      await loadRelationships();
    } catch (error) {
      console.error('Error removing parent:', error);
      let errorMessage = 'Unknown error';
      if (error.message) {
        try {
          const errorData = JSON.parse(error.message);
          errorMessage = errorData.detail || error.message;
        } catch {
          errorMessage = error.message;
        }
      }
      alert('Error removing parent: ' + errorMessage);
    }
  }
}

async function removeChild(childId) {
  if (!props.selected?.id) return;
  
  if (confirm('Are you sure you want to remove this child relationship?')) {
    try {
      await removeConfigurationItemTypeParent(childId, props.selected.id);
      await loadRelationships();
    } catch (error) {
      console.error('Error removing child:', error);
      let errorMessage = 'Unknown error';
      if (error.message) {
        try {
          const errorData = JSON.parse(error.message);
          errorMessage = errorData.detail || error.message;
        } catch {
          errorMessage = error.message;
        }
      }
      alert('Error removing child: ' + errorMessage);
    }
  }
}
</script>
