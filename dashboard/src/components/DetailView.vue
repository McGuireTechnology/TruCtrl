<template>
  <div class="detail-view h-100" v-if="item">
    <!-- Action Buttons Bar -->
    <div class="action-bar p-3 border-bottom bg-light">
      <div class="d-flex align-items-center gap-2">
        <button class="btn btn-outline-primary btn-sm" @click="$emit('edit')" :disabled="!canEdit">
          <i class="bi bi-pencil me-1"></i>
          Edit
        </button>
        <button class="btn btn-outline-secondary btn-sm" @click="$emit('duplicate')" :disabled="!canDuplicate">
          <i class="bi bi-files me-1"></i>
          Duplicate
        </button>
        <button class="btn btn-outline-danger btn-sm" @click="$emit('delete')" :disabled="!canDelete">
          <i class="bi bi-trash me-1"></i>
          Delete
        </button>
        <div class="vr mx-2"></div>
        <button class="btn btn-outline-secondary btn-sm" @click="$emit('refresh')">
          <i class="bi bi-arrow-clockwise me-1"></i>
          Refresh
        </button>
        <button class="btn btn-outline-secondary btn-sm" @click="$emit('export')">
          <i class="bi bi-download me-1"></i>
          Export
        </button>
      </div>
    </div>

    <!-- Header with Avatar and Title -->
    <div class="item-header p-4 border-bottom">
      <div class="d-flex align-items-center">
        <!-- Avatar/Icon -->
        <div class="me-3">
          <div class="item-avatar text-white d-flex align-items-center justify-content-center"
               :style="{ backgroundColor: getAvatarColor() }">
            <i :class="avatarIcon || 'bi bi-box'"></i>
          </div>
        </div>
        
        <!-- Item Name and Info -->
        <div class="flex-grow-1">
          <h3 class="mb-1">{{ itemName }}</h3>
          <div class="text-muted">{{ itemSubtitle }}</div>
          
          <!-- Related object pills -->
          <div class="d-flex flex-wrap gap-2 mt-2" v-if="hasRelatedObjects">
            <span v-if="item.function_short_name || item.function_name" 
                  class="badge rounded-pill text-white"
                  :style="{ backgroundColor: item.function_color || '#0d6efd' }">
              <i class="bi bi-gear me-1"></i>
              {{ item.function_short_name || getShortDisplayName(item.function_name) }}
            </span>
            <span v-if="showFrameworkPill" 
                  class="badge rounded-pill text-white"
                  :style="{ backgroundColor: item.framework_color || '#198754' }">
              <i class="bi bi-diagram-3 me-1"></i>
              {{ item.framework_short_name || getShortDisplayName(item.framework_name) }}
            </span>
            <span v-if="item.implementation_group_short_name || item.implementation_group_name" 
                  class="badge rounded-pill"
                  :style="{ 
                    backgroundColor: item.implementation_group_color || '#ffc107',
                    color: isLightColor(item.implementation_group_color || '#ffc107') ? '#000' : '#fff'
                  }">
              <i class="bi bi-collection me-1"></i>
              {{ item.implementation_group_short_name || getShortDisplayName(item.implementation_group_name) }}
            </span>
            <span v-if="item.control_short_name || item.control_name" 
                  class="badge rounded-pill text-white"
                  :style="{ backgroundColor: item.control_color || '#6c757d' }">
              <i class="bi bi-shield-check me-1"></i>
              {{ item.control_short_name || getShortDisplayName(item.control_name) }}
            </span>
          </div>
          
          <div class="d-flex align-items-center gap-3 mt-2">
            <span v-if="item.created_at" class="badge bg-light text-dark">
              <i class="bi bi-calendar me-1"></i>
              Created {{ formatDate(item.created_at) }}
            </span>
            <span v-if="item.updated_at" class="badge bg-light text-dark">
              <i class="bi bi-clock me-1"></i>
              Updated {{ formatDate(item.updated_at) }}
            </span>
            <span v-if="itemStatus" class="badge" :class="statusClass">
              {{ itemStatus }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tabs-container">
      <ul class="nav nav-tabs nav-fill border-bottom-0" role="tablist">
        <li class="nav-item" role="presentation">
          <button 
            class="nav-link" 
            :class="{ active: activeTab === 'overview' }"
            @click="activeTab = 'overview'"
            type="button"
          >
            <i class="bi bi-info-circle me-1"></i>
            Overview
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button 
            class="nav-link" 
            :class="{ active: activeTab === 'details' }"
            @click="activeTab = 'details'"
            type="button"
          >
            <i class="bi bi-list-ul me-1"></i>
            Details
          </button>
        </li>
        <li class="nav-item" role="presentation" v-if="hasLinkedObjects">
          <button 
            class="nav-link" 
            :class="{ active: activeTab === 'linked' }"
            @click="activeTab = 'linked'"
            type="button"
          >
            <i class="bi bi-link-45deg me-1"></i>
            Linked Objects
          </button>
        </li>
        <li class="nav-item" role="presentation" v-if="showRelationshipsTab">
          <button 
            class="nav-link" 
            :class="{ active: activeTab === 'relationships' }"
            @click="activeTab = 'relationships'"
            type="button"
          >
            <i class="bi bi-diagram-3 me-1"></i>
            Relationships
          </button>
        </li>
        <li class="nav-item" role="presentation" v-if="hasActivity">
          <button 
            class="nav-link" 
            :class="{ active: activeTab === 'activity' }"
            @click="activeTab = 'activity'"
            type="button"
          >
            <i class="bi bi-clock-history me-1"></i>
            Activity
          </button>
        </li>
      </ul>
    </div>

    <!-- Tab Content -->
        <div class="tab-content flex-grow-1 overflow-auto">
      <!-- Safeguard-specific content with custom tabs -->
      <div v-if="itemType === 'safeguards'" class="p-4">
        <SafeguardDetailTabs 
          :safeguard="item" 
          @relationships-updated="$emit('refresh')"
        />
      </div>

      <!-- Standard content for all other item types -->
      <template v-else>
        <!-- Overview Tab -->
        <div v-if="activeTab === 'overview'" class="tab-pane active p-4">
          <div class="row">
            <div class="col-md-8">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-0">Description</h5>
                </div>
                <div class="card-body">
                  <p class="mb-0">{{ item.description || 'No description available.' }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-0">Quick Info</h5>
                </div>
                <div class="card-body">
                  <div class="mb-3" v-for="(value, key) in quickInfo" :key="key">
                    <strong>{{ formatLabel(key) }}:</strong>
                    <div class="mt-1">
                      <span v-if="value">
                        <span v-if="isPillField(key)" class="badge rounded-pill" :class="getPillClass(key)">
                          <i v-if="getPillIcon(key)" :class="getPillIcon(key)" class="me-1"></i>
                          {{ formatValue(value, key) }}
                        </span>
                        <span v-else class="text-muted">{{ formatValue(value, key) }}</span>
                      </span>
                      <span v-else class="text-muted">Not set</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Details Tab -->
        <div v-if="activeTab === 'details'" class="tab-pane active p-4">
          <div class="row">
            <div class="col-12">
              <div class="card">
                <div class="card-header">
                  <h5 class="card-title mb-0">All Properties</h5>
                </div>
                <div class="card-body">
                  <div class="table-responsive">
                    <table class="table table-borderless">
                      <tbody>
                        <tr v-for="(value, key) in filteredDetails" :key="key">
                          <td class="fw-bold text-end" style="width: 200px;">{{ formatLabel(key) }}</td>
                          <td>
                            <span v-if="value">
                              <span v-if="isPillField(key)" class="badge rounded-pill" :class="getPillClass(key)">
                                <i v-if="getPillIcon(key)" :class="getPillIcon(key)" class="me-1"></i>
                                {{ formatValue(value, key) }}
                              </span>
                              <span v-else class="text-break">{{ formatValue(value, key) }}</span>
                            </span>
                            <span v-else class="text-muted">Not set</span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Linked Objects Tab -->
        <div v-if="activeTab === 'linked' && hasLinkedObjects" class="tab-pane active p-4">
          <div class="row">
            <div class="col-12">
              <div class="card">
                <div class="card-header">
                  <h5 class="card-title mb-0">Related Items</h5>
                </div>
                <div class="card-body">
                  <div v-if="linkedObjects.length === 0" class="text-muted text-center py-4">
                    No linked objects found.
                  </div>
                  <div v-else>
                    <div v-for="link in linkedObjects" :key="link.id" class="border rounded p-3 mb-3">
                      <div class="d-flex align-items-center">
                        <div class="me-3">
                          <i :class="link.icon || 'bi bi-link'" class="text-primary"></i>
                        </div>
                        <div class="flex-grow-1">
                          <h6 class="mb-1">{{ link.name }}</h6>
                          <div class="text-muted small">{{ link.type }} • {{ link.relationship }}</div>
                        </div>
                        <button class="btn btn-outline-primary btn-sm" @click="$emit('view-linked', link)">
                          View
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Asset Class Relationships Tab -->
        <div v-if="activeTab === 'relationships' && showRelationshipsTab" class="tab-pane active p-4">
          <div class="row">
            <div class="col-md-6">
              <div class="card h-100">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h5 class="card-title mb-0">
                    <i class="bi bi-arrow-up-circle me-2"></i>
                    Parent Asset Classes
                  </h5>
                  <button class="btn btn-sm btn-outline-primary" @click="showAddParentModal = true">
                    <i class="bi bi-plus"></i>
                  </button>
                </div>
                <div class="card-body">
                  <div v-if="!item.parents || item.parents.length === 0" class="text-muted text-center py-4">
                    <i class="bi bi-arrow-up-circle display-6 text-muted"></i>
                    <p class="mt-2">No parent asset classes</p>
                  </div>
                  <div v-else>
                    <div v-for="parent in item.parents" :key="parent.id" class="border rounded p-3 mb-3">
                      <div class="d-flex align-items-center">
                        <div class="me-3">
                          <div class="rounded-circle d-flex align-items-center justify-content-center" 
                               :style="`width: 40px; height: 40px; background-color: ${parent.color}`">
                            <i class="bi bi-box text-white"></i>
                          </div>
                        </div>
                        <div class="flex-grow-1">
                          <h6 class="mb-1">{{ parent.name }}</h6>
                          <div class="text-muted small" v-if="parent.short_name">{{ parent.short_name }}</div>
                        </div>
                        <div class="d-flex gap-2">
                          <button class="btn btn-outline-primary btn-sm" @click="$emit('view-related', { type: 'asset-class', id: parent.id })">
                            <i class="bi bi-eye"></i>
                          </button>
                          <button class="btn btn-outline-danger btn-sm" @click="removeParentRelationship(parent.id)" title="Remove parent relationship">
                            <i class="bi bi-x"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card h-100">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h5 class="card-title mb-0">
                    <i class="bi bi-arrow-down-circle me-2"></i>
                    Child Asset Classes
                  </h5>
                  <button class="btn btn-sm btn-outline-primary" @click="showAddChildModal = true">
                    <i class="bi bi-plus"></i>
                  </button>
                </div>
                <div class="card-body">
                  <div v-if="!item.children || item.children.length === 0" class="text-muted text-center py-4">
                    <i class="bi bi-arrow-down-circle display-6 text-muted"></i>
                    <p class="mt-2">No child asset classes</p>
                  </div>
                  <div v-else>
                    <div v-for="child in item.children" :key="child.id" class="border rounded p-3 mb-3">
                      <div class="d-flex align-items-center">
                        <div class="me-3">
                          <div class="rounded-circle d-flex align-items-center justify-content-center" 
                               :style="`width: 40px; height: 40px; background-color: ${child.color}`">
                            <i class="bi bi-box text-white"></i>
                          </div>
                        </div>
                        <div class="flex-grow-1">
                          <h6 class="mb-1">{{ child.name }}</h6>
                          <div class="text-muted small" v-if="child.short_name">{{ child.short_name }}</div>
                        </div>
                        <div class="d-flex gap-2">
                          <button class="btn btn-outline-primary btn-sm" @click="$emit('view-related', { type: 'asset-class', id: child.id })">
                            <i class="bi bi-eye"></i>
                          </button>
                          <button class="btn btn-outline-danger btn-sm" @click="removeChildRelationship(child.id)" title="Remove child relationship">
                            <i class="bi bi-x"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Add Parent Modal -->
          <div v-if="showAddParentModal" class="modal show d-block" style="background-color: rgba(0,0,0,0.5);">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">Add Parent Asset Class</h5>
                  <button type="button" class="btn-close" @click="closeParentModal"></button>
                </div>
                <div class="modal-body">
                  <label class="form-label">Select Parent Asset Class</label>
                  <select v-model="selectedParentId" class="form-select">
                    <option value="">Choose a parent asset class...</option>
                    <option v-for="assetClass in availableParents" :key="assetClass.id" :value="assetClass.id">
                      {{ assetClass.name }}
                    </option>
                  </select>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeParentModal">Cancel</button>
                  <button type="button" class="btn btn-primary" @click="addParentRelationship" :disabled="!selectedParentId || addingParent">
                    <span v-if="addingParent">
                      <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                      Adding...
                    </span>
                    <span v-else>Add Parent</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Add Child Modal -->
          <div v-if="showAddChildModal" class="modal show d-block" style="background-color: rgba(0,0,0,0.5);">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">Add Child Asset Class</h5>
                  <button type="button" class="btn-close" @click="closeChildModal"></button>
                </div>
                <div class="modal-body">
                  <label class="form-label">Select Child Asset Class</label>
                  <select v-model="selectedChildId" class="form-select">
                    <option value="">Choose a child asset class...</option>
                    <option v-for="assetClass in availableChildren" :key="assetClass.id" :value="assetClass.id">
                      {{ assetClass.name }}
                    </option>
                  </select>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeChildModal">Cancel</button>
                  <button type="button" class="btn btn-primary" @click="addChildRelationship" :disabled="!selectedChildId || addingChild">
                    <span v-if="addingChild">
                      <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                      Adding...
                    </span>
                    <span v-else>Add Child</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Activity Tab -->
        <div v-if="activeTab === 'activity' && hasActivity" class="tab-pane active p-4">
          <div class="row">
            <div class="col-12">
              <div class="card">
                <div class="card-header">
                  <h5 class="card-title mb-0">Activity Log</h5>
                </div>
                <div class="card-body">
                  <div v-if="activityLog.length === 0" class="text-muted text-center py-4">
                    No activity recorded.
                  </div>
                  <div v-else class="timeline">
                    <div v-for="activity in activityLog" :key="activity.id" class="timeline-item mb-3">
                      <div class="d-flex">
                        <div class="timeline-marker me-3">
                          <i :class="activity.icon || 'bi bi-circle-fill'" class="text-primary"></i>
                        </div>
                        <div class="flex-grow-1">
                          <div class="fw-medium">{{ activity.action }}</div>
                          <div class="text-muted small">{{ activity.user }} • {{ formatDate(activity.timestamp) }}</div>
                          <div v-if="activity.details" class="text-muted small mt-1">{{ activity.details }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>

  <!-- Empty State -->
  <div v-else class="detail-view h-100 d-flex align-items-center justify-content-center">
    <div class="text-center text-muted">
      <i class="bi bi-arrow-left display-1"></i>
      <h4 class="mt-3">Select an item</h4>
      <p>Choose an item from the list to view its details</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { 
  getAssetClasses,
  addAssetClassParent,
  removeAssetClassParent
} from '../api';
import SafeguardDetailTabs from './SafeguardDetailTabs.vue';

const props = defineProps({
  item: { type: Object, default: null },
  itemName: { type: String, default: '' },
  itemSubtitle: { type: String, default: '' },
  itemStatus: { type: String, default: '' },
  itemType: { type: String, default: '' },
  avatarIcon: { type: String, default: 'bi bi-box' },
  linkedObjects: { type: Array, default: () => [] },
  activityLog: { type: Array, default: () => [] },
  canEdit: { type: Boolean, default: true },
  canDuplicate: { type: Boolean, default: true },
  canDelete: { type: Boolean, default: true },
  excludeFields: { type: Array, default: () => [
    'id', 'created_at', 'updated_at',
    'control_id', 'function_id', 'framework_id', 'implementation_group_id',
    'control_name', 'function_name', 'framework_name', 'implementation_group_name'
  ] },
  quickInfoFields: { type: Array, default: () => [
    'type', 'status', 'category', 'owner',
    'security_function', 'framework', 'implementation_group', 'control'
  ] }
});

const emit = defineEmits([
  'edit', 'duplicate', 'delete', 'refresh', 'export', 'view-linked', 'view-related'
]);

const activeTab = ref('overview');

// Relationship management state
const showAddParentModal = ref(false);
const showAddChildModal = ref(false);
const selectedParentId = ref('');
const selectedChildId = ref('');
const addingParent = ref(false);
const addingChild = ref(false);
const allAssetClasses = ref([]);

// Load all asset classes for the dropdowns
const loadAllAssetClasses = async () => {
  if (props.itemType !== 'asset-classes') return;
  
  try {
    const response = await getAssetClasses();
    allAssetClasses.value = response.data || [];
  } catch (error) {
    console.error('Error loading asset classes:', error);
  }
};

// Watch for item type changes to load asset classes when needed
watch(() => props.itemType, (newType) => {
  if (newType === 'asset-classes') {
    loadAllAssetClasses();
  }
}, { immediate: true });

// Watch for item changes to debug relationships
watch(() => props.item, (newItem, oldItem) => {
  if (newItem && props.itemType === 'asset-classes') {
    console.log('DetailView - Asset class data received:', {
      name: newItem.name,
      parents: newItem.parents?.length || 0,
      children: newItem.children?.length || 0,
      hasParentsArray: Array.isArray(newItem.parents),
      hasChildrenArray: Array.isArray(newItem.children),
      parentsData: newItem.parents,
      childrenData: newItem.children,
      timestamp: new Date().toISOString()
    });
  }
}, { immediate: true, deep: true });

// Computed available options (exclude current item and existing relationships)
const availableParents = computed(() => {
  if (!props.item || props.itemType !== 'asset-classes') return [];
  const currentParents = props.item.parents || [];
  return allAssetClasses.value.filter(ac => 
    ac.id !== props.item.id && 
    !currentParents.some(p => p.id === ac.id)
  );
});

const availableChildren = computed(() => {
  if (!props.item || props.itemType !== 'asset-classes') return [];
  const currentChildren = props.item.children || [];
  return allAssetClasses.value.filter(ac => 
    ac.id !== props.item.id && 
    !currentChildren.some(c => c.id === ac.id)
  );
});

// Relationship management methods
const addParentRelationship = async () => {
  if (!selectedParentId.value || !props.item?.id || addingParent.value) return;
  
  addingParent.value = true;
  try {
    await addAssetClassParent(props.item.id, selectedParentId.value);
    closeParentModal();
    emit('refresh'); // Refresh the detail view to show updated relationships
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
  } finally {
    addingParent.value = false;
  }
};

const addChildRelationship = async () => {
  if (!selectedChildId.value || !props.item?.id || addingChild.value) return;
  
  addingChild.value = true;
  try {
    await addAssetClassParent(selectedChildId.value, props.item.id);
    closeChildModal();
    emit('refresh'); // Refresh the detail view to show updated relationships
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
  } finally {
    addingChild.value = false;
  }
};

const removeParentRelationship = async (parentId) => {
  if (!props.item?.id) return;
  
  if (confirm('Are you sure you want to remove this parent relationship?')) {
    try {
      await removeAssetClassParent(props.item.id, parentId);
      emit('refresh'); // Refresh the detail view to show updated relationships
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
};

const removeChildRelationship = async (childId) => {
  if (!props.item?.id) return;
  
  if (confirm('Are you sure you want to remove this child relationship?')) {
    try {
      await removeAssetClassParent(childId, props.item.id);
      emit('refresh'); // Refresh the detail view to show updated relationships
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
};

const closeParentModal = () => {
  showAddParentModal.value = false;
  selectedParentId.value = '';
};

const closeChildModal = () => {
  showAddChildModal.value = false;
  selectedChildId.value = '';
};

const hasLinkedObjects = computed(() => props.linkedObjects.length > 0);
const hasActivity = computed(() => props.activityLog.length > 0);

const showRelationshipsTab = computed(() => {
  // Show tab for asset classes, regardless of whether relationships exist
  return props.itemType === 'asset-classes' && props.item;
});

const statusClass = computed(() => {
  const status = props.itemStatus?.toLowerCase();
  if (status === 'active' || status === 'enabled') return 'bg-success';
  if (status === 'inactive' || status === 'disabled') return 'bg-secondary';
  if (status === 'pending' || status === 'draft') return 'bg-warning';
  if (status === 'error' || status === 'failed') return 'bg-danger';
  return 'bg-info';
});

const hasRelatedObjects = computed(() => {
  if (!props.item) return false;
  return props.item.function_name || props.item.function_short_name || 
         props.item.framework_name || props.item.framework_short_name || 
         props.item.implementation_group_name || props.item.implementation_group_short_name || 
         props.item.control_name || props.item.control_short_name;
});

const showFrameworkPill = computed(() => {
  if (!props.item) return false;
  const hasFramework = props.item.framework_short_name || props.item.framework_name;
  const isNotSafeguards = props.itemType !== 'safeguards';
  console.log('Framework pill check:', { hasFramework, isNotSafeguards, itemType: props.itemType });
  return hasFramework && isNotSafeguards;
});

const getShortDisplayName = (name) => {
  if (!name) return '';
  
  // If name contains a dash, pipe, or similar separator, take the first part
  const separators = [' — ', ' - ', ' | ', ' / '];
  for (const sep of separators) {
    if (name.includes(sep)) {
      return name.split(sep)[0].trim();
    }
  }
  
  // Otherwise, take first 2-3 words or abbreviate if too long
  const words = name.split(' ');
  if (words.length <= 2) {
    return name.length > 20 ? name.substring(0, 17) + '...' : name;
  }
  
  // Take first 2 words if reasonable length
  const firstTwo = words.slice(0, 2).join(' ');
  return firstTwo.length > 20 ? words[0] : firstTwo;
};

const isLightColor = (color) => {
  if (!color) return false;
  // Remove the # if present
  const hex = color.replace('#', '');
  
  // Convert to RGB
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  
  // Calculate luminance
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  
  // Return true if color is light (luminance > 0.5)
  return luminance > 0.5;
};

const getAvatarColor = () => {
  if (!props.item) return '#6c757d'; // Default gray
  
  // Return the color based on item type, with fallbacks to defaults
  if (props.item.color) return props.item.color;
  if (props.item.function_color) return props.item.function_color;
  if (props.item.framework_color) return props.item.framework_color;
  if (props.item.implementation_group_color) return props.item.implementation_group_color;
  if (props.item.control_color) return props.item.control_color;
  
  // Fallback to defaults based on what fields exist
  if (props.item.function_name || props.item.function_short_name) return '#0d6efd';
  if (props.item.framework_name || props.item.framework_short_name) return '#198754';
  if (props.item.implementation_group_name || props.item.implementation_group_short_name) return '#ffc107';
  if (props.item.control_name || props.item.control_short_name) return '#6c757d';
  
  return '#6c757d'; // Default gray
};

const quickInfo = computed(() => {
  if (!props.item) return {};
  
  const info = {};
  props.quickInfoFields.forEach(field => {
    if (props.item[field] !== undefined) {
      info[field] = props.item[field];
    }
  });
  return info;
});

const filteredDetails = computed(() => {
  if (!props.item) return {};
  
  const details = {};
  Object.keys(props.item).forEach(key => {
    if (!props.excludeFields.includes(key)) {
      details[key] = props.item[key];
    }
  });
  
  // Add derived fields for pill display
  if (props.item.control_name) {
    details['control'] = props.item.control_name;
  }
  if (props.item.function_name) {
    details['security_function'] = props.item.function_name;
  }
  if (props.item.framework_name) {
    details['framework'] = props.item.framework_name;
  }
  if (props.item.implementation_group_name) {
    details['implementation_group'] = props.item.implementation_group_name;
  }
  
  return details;
});

const formatLabel = (key) => {
  return key
    .replace(/_/g, ' ')
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
    .trim();
};

const formatValue = (value, key) => {
  if (typeof value === 'boolean') {
    return value ? 'Yes' : 'No';
  }
  if (typeof value === 'object' && value !== null) {
    return JSON.stringify(value, null, 2);
  }
  
  // For pill fields, try to get the display name from the item
  if (isPillField(key) && props.item) {
    const keyLower = key.toLowerCase();
    
    if (keyLower.includes('control') && props.item.control_name) {
      return props.item.control_name;
    }
    if (keyLower.includes('function') && props.item.function_name) {
      return props.item.function_name;
    }
    if (keyLower.includes('framework') && props.item.framework_name) {
      return props.item.framework_name;
    }
    if ((keyLower.includes('implementation') || keyLower.includes('group')) && props.item.implementation_group_name) {
      return props.item.implementation_group_name;
    }
  }
  
  return value?.toString() || '';
};

const isPillField = (key) => {
  // Define which fields should be displayed as pills
  const pillFields = [
    'asset_type', 'assetType', 'type',
    'security_function', 'securityFunction', 'function_id', 'functionId', 'function',
    'framework', 'framework_id', 'frameworkId',
    'implementation_group', 'implementationGroup', 'implementation_group_id', 'implementationGroupId', 'group',
    'control_id', 'controlId', 'control',
    'category', 'status', 'level', 'priority'
  ];
  return pillFields.includes(key);
};

const getPillClass = (key) => {
  // Define color classes for different types of pills
  const keyLower = key.toLowerCase();
  
  if (keyLower.includes('asset') || keyLower.includes('type')) {
    return 'bg-info text-white';
  }
  if (keyLower.includes('function')) {
    return 'bg-primary text-white';
  }
  if (keyLower.includes('framework')) {
    return 'bg-success text-white';
  }
  if (keyLower.includes('implementation') || keyLower.includes('group')) {
    return 'bg-warning text-dark';
  }
  if (keyLower.includes('control')) {
    return 'bg-secondary text-white';
  }
  if (keyLower.includes('category')) {
    return 'bg-dark text-white';
  }
  if (keyLower.includes('status')) {
    return 'bg-success text-white';
  }
  if (keyLower.includes('level') || keyLower.includes('priority')) {
    return 'bg-danger text-white';
  }
  
  return 'bg-light text-dark';
};

const getPillIcon = (key) => {
  // Define icons for different types of pills
  const keyLower = key.toLowerCase();
  
  if (keyLower.includes('asset') || keyLower.includes('type')) {
    return 'bi bi-hdd-stack';
  }
  if (keyLower.includes('function')) {
    return 'bi bi-gear';
  }
  if (keyLower.includes('framework')) {
    return 'bi bi-diagram-3';
  }
  if (keyLower.includes('implementation') || keyLower.includes('group')) {
    return 'bi bi-collection';
  }
  if (keyLower.includes('control')) {
    return 'bi bi-shield-check';
  }
  if (keyLower.includes('category')) {
    return 'bi bi-tags';
  }
  if (keyLower.includes('status')) {
    return 'bi bi-check-circle';
  }
  if (keyLower.includes('level') || keyLower.includes('priority')) {
    return 'bi bi-bar-chart';
  }
  
  return null;
};

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown';
  try {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch {
    return dateString;
  }
};
</script>

<style scoped>
.detail-view {
  display: flex;
  flex-direction: column;
}

.item-avatar {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  font-size: 24px;
}

.action-bar {
  flex-shrink: 0;
}

.item-header {
  flex-shrink: 0;
}

.tabs-container {
  flex-shrink: 0;
  background-color: #f8f9fa;
}

.nav-tabs {
  border-bottom: 1px solid #dee2e6;
}

.nav-tabs .nav-link {
  border: none;
  background: none;
  color: #6c757d;
  font-weight: 500;
}

.nav-tabs .nav-link:hover {
  color: #495057;
  background-color: #e9ecef;
}

.nav-tabs .nav-link.active {
  color: #0d6efd;
  background-color: #fff;
  border-bottom: 2px solid #0d6efd;
}

.tab-content {
  background-color: #fff;
}

.timeline-marker {
  width: 20px;
  text-align: center;
  padding-top: 2px;
}

.table td {
  vertical-align: top;
  padding: 0.75rem;
}

.vr {
  opacity: 0.25;
}

/* Pill styles */
.badge.rounded-pill {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.35em 0.75em;
  border: 1px solid transparent;
}

.badge.rounded-pill i {
  font-size: 0.7rem;
}

/* Pill color schemes */
.badge.bg-info {
  background-color: #0dcaf0 !important;
  border-color: #0dcaf0;
}

.badge.bg-primary {
  background-color: #0d6efd !important;
  border-color: #0d6efd;
}

.badge.bg-success {
  background-color: #198754 !important;
  border-color: #198754;
}

.badge.bg-warning {
  background-color: #ffc107 !important;
  border-color: #ffc107;
  color: #000 !important;
}

.badge.bg-secondary {
  background-color: #6c757d !important;
  border-color: #6c757d;
}
</style>
