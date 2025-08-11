<template>
  <div class="dashboard-container">
    <!-- Left Navigation Sidebar -->
    <nav class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <h1 class="app-title">TruCtrl</h1>
          <p class="app-subtitle">Security Control Management</p>
        </div>
      </div>

      <div class="sidebar-content">
        <!-- Activity Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('activity')"
            :class="['nav-item', { active: view === 'activity' }]"
          >
            <i class="fas fa-heartbeat me-2"></i>
            Activity
          </button>
        </div>

        <!-- Spacer -->
        <div class="nav-spacer"></div>

        <!-- Devices Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('devices')"
            :class="['nav-item', { active: view === 'devices' }]"
          >
            <i class="fas fa-laptop me-2"></i>
            Devices
          </button>
        </div>

        <!-- Software Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('software')"
            :class="['nav-item', { active: view === 'software' }]"
          >
            <i class="fas fa-code me-2"></i>
            Software
          </button>
        </div>

        <!-- Data Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('data')"
            :class="['nav-item', { active: view === 'data' }]"
          >
            <i class="fas fa-database me-2"></i>
            Data
          </button>
        </div>

        <!-- User Management Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('users')"
            :class="['nav-item', { active: view === 'users' }]"
          >
            <i class="fas fa-users me-2"></i>
            Users
          </button>
        </div>

        <!-- Network Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('network')"
            :class="['nav-item', { active: view === 'network' }]"
          >
            <i class="fas fa-network-wired me-2"></i>
            Network
          </button>
        </div>

        <!-- Documentation Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('documentation')"
            :class="['nav-item', { active: view === 'documentation' }]"
          >
            <i class="fas fa-file-alt me-2"></i>
            Documentation
          </button>
        </div>

        <!-- Spacer -->
        <div class="nav-spacer"></div>

        <!-- Safeguards Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('safeguards')"
            :class="['nav-item', { active: view === 'safeguards' }]"
          >
            <i class="fas fa-lock me-2"></i>
            Safeguards
          </button>
        </div>

        <!-- Controls Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('controls')"
            :class="['nav-item', { active: view === 'controls' }]"
          >
            <i class="fas fa-shield me-2"></i>
            Controls
          </button>
        </div>

        <!-- Implementation Groups Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('implementationGroups')"
            :class="['nav-item', { active: view === 'implementationGroups' }]"
          >
            <i class="fas fa-layer-group me-2"></i>
            Implementation Groups
          </button>
        </div>

        <!-- Security Functions Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('functions')"
            :class="['nav-item', { active: view === 'functions' }]"
          >
            <i class="fas fa-cogs me-2"></i>
            Security Functions
          </button>
        </div>

        <!-- Configuration Item Types Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('configuration-item-types')"
            :class="['nav-item', { active: view === 'configuration-item-types' }]"
          >
            <i class="bi bi-box me-2"></i>
            Configuration Item Types
          </button>
        </div>

        <!-- Frameworks Section -->
        <div class="nav-section">
          <button
            @click="navigateToModule('frameworks')"
            :class="['nav-item', { active: view === 'frameworks' }]"
          >
            <i class="fas fa-sitemap me-2"></i>
            Frameworks
          </button>
        </div>
      </div>

      <div class="sidebar-footer">
        <div class="user-profile">
          <div class="user-info" @click="toggleUserMenu" style="cursor: pointer;">
            <div class="user-avatar">
              {{ (user?.name || 'U').charAt(0).toUpperCase() }}
            </div>
            <div class="user-details">
              <div class="user-name">{{ user?.name || 'User' }}</div>
              <div class="user-email">{{ user?.email || 'user@example.com' }}</div>
              <div v-if="refreshTokenCountdown" class="token-countdown">
                <i class="fas fa-clock me-1"></i>
                <span class="countdown-text" :style="{ color: countdownColor }">{{ refreshTokenCountdown }}</span>
              </div>
            </div>
            <div class="dropdown-arrow">
              <i class="fas fa-chevron-up" :class="{ rotated: showUserMenu }"></i>
            </div>
          </div>
          
          <!-- User Dropdown Menu -->
          <div class="user-menu" :class="{ show: showUserMenu }">
            <div class="user-menu-header">
              <div class="user-avatar-large">
                {{ (user?.name || 'U').charAt(0).toUpperCase() }}
              </div>
              <div class="user-details-full">
                <div class="user-name-large">{{ user?.name || 'User' }}</div>
                <div class="user-email-small">{{ user?.email || 'user@example.com' }}</div>
              </div>
            </div>
            
            <div class="user-menu-divider"></div>
            
            <div class="user-menu-items">
              <button class="user-menu-item" @click="handleProfile">
                <i class="fas fa-user me-2"></i>
                Profile Settings
              </button>
              <button class="user-menu-item" @click="handleChangePassword">
                <i class="fas fa-lock me-2"></i>
                Change Password
              </button>
              <div class="user-menu-divider"></div>
              <button class="user-menu-item logout" @click="handleLogout">
                <i class="fas fa-sign-out-alt me-2"></i>
                Sign Out
              </button>
            </div>
            
            <!-- Token Expiry Info -->
            <div v-if="refreshTokenCountdown" class="token-info">
              <div class="token-info-header">
                <i class="fas fa-shield-alt me-2"></i>
                Session Status
              </div>
              <div class="token-expiry">
                <span class="expiry-label">Expires in:</span>
                <span class="expiry-time" :style="{ color: countdownColor }">{{ refreshTokenCountdown }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <div class="main-content">
      <!-- Content Panels -->
      <div class="content-panels">
        <!-- Master Panel (List) -->
        <div class="master-panel">
        <div class="panel-content">
          <ListGroup
            :items="items"
            :selected-id="selected && selected.id"
            :selected-items="selectedItems"
            :is-multi-select="isMultiSelectMode"
            :title="listConfig.title"
            :item-type="view"
            :item-heading="listConfig.itemHeading"
            :item-sub="listConfig.itemSub"
            :item-desc="listConfig.itemDesc"
            :item-badge="listConfig.itemBadge"
            :avatar-icon="getAvatarIcon(view)"
            @select="handleSelect"
            @multi-select="handleMultiSelect"
            @range-select="handleRangeSelect"
            @toggle-multi-select="toggleMultiSelect"
            @select-all="handleSelectAll"
            @bulk-delete="handleBulkDelete"
            @search="handleSearch"
            @add="handleAdd"
            @filter="handleFilter"
            @sort="handleSort"
          />
        </div>
      </div>

      <!-- Detail Panel -->
      <div class="detail-panel">
        <div class="panel-content h-100">
          <!-- Form View (Edit/Create) -->
          <FormView
            v-if="showForm"
            ref="formViewRef"
            :key="formKey"
            :item="formItem"
            :item-type="view"
            :item-type-name="getSingularTitle(listConfig.title)"
            :avatar-icon="getAvatarIcon(view)"
            :fields="editFields"
            :is-create="isCreateMode"
            :create-function="getCreateFunction(view)"
            :update-function="getUpdateFunction(view)"
            @created="handleItemCreated"
            @updated="handleItemUpdated"
            @cancel="handleFormCancel"
            @delete="handleFormDelete"
            @error="handleFormError"
            @field-change="handleFieldChange"
          />
          
          <!-- Module Home (when no item selected) -->
          <div v-else-if="!selected" class="module-home h-100 d-flex flex-column">
            <div class="module-header p-4 border-bottom bg-light">
              <div class="d-flex align-items-center">
                <div class="me-3">
                  <div class="module-avatar bg-primary text-white d-flex align-items-center justify-content-center">
                    <i :class="getAvatarIcon(view)"></i>
                  </div>
                </div>
                <div>
                  <h2 class="mb-1">{{ getModuleDisplayName(view) }}</h2>
                  <p class="text-muted mb-0">{{ getModuleDescription(view) }}</p>
                </div>
              </div>
              <div class="mt-3">
                <button class="btn btn-primary" @click="handleAdd">
                  <i class="fas fa-plus me-2"></i>
                  Add {{ getSingularTitle(listConfig.title) }}
                </button>
              </div>
            </div>
            
            <div class="module-content flex-1 p-4">
              <div class="row">
                <div class="col-md-8">
                  <div class="module-stats mb-4">
                    <h5 class="mb-3">Overview</h5>
                    <div class="row g-3">
                      <div class="col-sm-6">
                        <div class="stat-card p-3 border rounded">
                          <div class="d-flex align-items-center">
                            <div class="stat-icon me-3">
                              <i :class="getAvatarIcon(view)" class="text-primary"></i>
                            </div>
                            <div>
                              <div class="stat-value h4 mb-0">{{ items.length }}</div>
                              <div class="stat-label text-muted small">Total {{ listConfig.title }}</div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="col-sm-6">
                        <div class="stat-card p-3 border rounded">
                          <div class="d-flex align-items-center">
                            <div class="stat-icon me-3">
                              <i class="fas fa-clock text-success"></i>
                            </div>
                            <div>
                              <div class="stat-value h4 mb-0">{{ getActiveCount() }}</div>
                              <div class="stat-label text-muted small">Active</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="module-actions">
                    <h5 class="mb-3">Quick Actions</h5>
                    <div class="row g-3">
                      <div class="col-sm-6">
                        <button class="btn btn-outline-primary w-100 p-3" @click="handleAdd">
                          <i class="fas fa-plus mb-2 d-block"></i>
                          <div class="fw-medium">Add New {{ getSingularTitle(listConfig.title) }}</div>
                          <small class="text-muted">Create a new {{ getSingularTitle(listConfig.title).toLowerCase() }}</small>
                        </button>
                      </div>
                      <div class="col-sm-6">
                        <button class="btn btn-outline-secondary w-100 p-3" @click="handleBulkImport">
                          <i class="fas fa-upload mb-2 d-block"></i>
                          <div class="fw-medium">Import {{ listConfig.title }}</div>
                          <small class="text-muted">Bulk import from file</small>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="col-md-4">
                  <div class="help-section">
                    <h5 class="mb-3">Getting Started</h5>
                    <div class="help-item mb-3 p-3 bg-light rounded">
                      <h6 class="mb-2">
                        <i class="fas fa-info-circle text-info me-2"></i>
                        {{ getModuleHelpTitle(view) }}
                      </h6>
                      <p class="mb-0 small text-muted">{{ getModuleHelpText(view) }}</p>
                    </div>
                    
                    <div class="recent-activity">
                      <h6 class="mb-3">
                        <i class="fas fa-history me-2"></i>
                        Recent Activity
                      </h6>
                      <div v-if="items.length === 0" class="text-muted small">
                        No {{ listConfig.title.toLowerCase() }} created yet.
                      </div>
                      <div v-else class="activity-list">
                        <div v-for="item in items.slice(0, 3)" :key="item.id" 
                             class="activity-item d-flex align-items-center mb-2 p-2 border rounded cursor-pointer"
                             @click="handleSelect(item)">
                          <div class="activity-icon me-2">
                            <i :class="getAvatarIcon(view)" class="text-muted small"></i>
                          </div>
                          <div class="flex-1">
                            <div class="activity-title small fw-medium">{{ getItemName(item) }}</div>
                            <div class="activity-time text-muted" style="font-size: 0.75rem;">
                              {{ item.updated_at ? formatDate(item.updated_at) : formatDate(item.created_at) }}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Detail View (Read-only) -->
          <DetailView
            v-else
            :item="selected"
            :item-name="getItemName(selected)"
            :item-subtitle="getItemSubtitle(selected)"
            :item-status="getItemStatus(selected)"
            :item-type="view"
            :avatar-icon="getAvatarIcon(view)"
            :linked-objects="getLinkedObjects(selected)"
            :activity-log="getActivityLog(selected)"
            :quick-info-fields="getQuickInfoFields(view)"
            :can-edit="!isItemLocked(selected)"
            :can-delete="!isItemLocked(selected)"
            :can-duplicate="true"
            @edit="handleEdit"
            @duplicate="handleDuplicate"
            @delete="handleDelete"
            @refresh="handleDetailRefresh"
            @export="handleExport"
            @view-linked="handleViewLinked"
            @view-related="handleViewRelated"
          />
        </div>
      </div>
      </div>
    </div>
  </div>

  <!-- Unsaved Changes Confirmation Modal -->
  <div class="modal fade" id="unsavedChangesModal" tabindex="-1" aria-labelledby="unsavedChangesModalLabel" aria-hidden="true" ref="confirmModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="unsavedChangesModalLabel">Unsaved Changes</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>You have unsaved changes that will be lost if you continue. What would you like to do?</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="handleStayOnForm">
            Stay and Continue Editing
          </button>
          <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="handleDiscardChanges">
            Discard Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuth } from '../stores/auth';
import ListGroup from '../components/ListGroup.vue';
import DetailView from '../components/DetailView.vue';
import FormView from '../components/FormView.vue';
import { getUsers, getControls, getFrameworks, getImplementationGroups, getFunctions, getSafeguards, getConfigurationItemTypes, getConfigurationItemType,
         createUser, createControl, createFramework, createImplementationGroup, createFunction, createSafeguard, createAssetClass,
         updateUser, updateControl, updateFramework, updateImplementationGroup, updateFunction, updateSafeguard, updateAssetClass,
         deleteUser, deleteControl, deleteFramework, deleteImplementationGroup, deleteFunction, deleteSafeguard, deleteAssetClass } from '../api';
import CrudUsers from '../components/CrudUsers.vue';
import CrudControls from '../components/CrudControls.vue';
import CrudFrameworks from '../components/CrudFrameworks.vue';
import CrudImplementationGroups from '../components/CrudImplementationGroups.vue';
import CrudSafeguards from '../components/CrudSafeguards.vue';
import CrudConfigurationItemTypes from '../components/CrudConfigurationItemTypes.vue';

const router = useRouter();
const route = useRoute();
const { user, logout, timeUntilRefreshExpiry, timeUntilRefreshExpiryDetailed } = useAuth();

const view = ref('users');
const items = ref([]);
const showUserMenu = ref(false);

// Dropdown data for forms
const frameworks = ref([]);
const implementationGroups = ref([]);
const functions = ref([]);
const configurationItemTypes = ref([]);
const controls = ref([]);
const selectedFrameworkId = ref(null);
const formKey = ref(0); // Force form re-render when needed

// Initialize view from route
const initializeFromRoute = () => {
  const module = route.meta?.module || 'users';
  view.value = module;
  
  // If there's an ID in the route, we'll select that item after fetching
  const recordId = route.params?.id;
  if (recordId) {
    // Store the ID to select after items are loaded
    pendingSelectionId.value = recordId;
  }
  
  // Ensure we fetch items on initialization
  fetchItems();
};

// Track pending selection from URL
const pendingSelectionId = ref(null);

// Real-time refresh token countdown
const refreshTokenCountdown = computed(() => {
  const detail = timeUntilRefreshExpiryDetailed.value;
  if (!detail) return null;
  
  // Show seconds when less than 5 minutes remaining
  if (detail.totalMinutes < 5) {
    return `${detail.minutes}m ${detail.seconds}s`;
  } else {
    return `${detail.totalMinutes}m`;
  }
});

// Color coding for countdown
const countdownColor = computed(() => {
  const detail = timeUntilRefreshExpiryDetailed.value;
  if (!detail) return '#f39c12';
  
  if (detail.totalMinutes < 5) return '#e74c3c'; // Red for under 5 minutes
  if (detail.totalMinutes < 15) return '#f39c12'; // Orange for under 15 minutes
  return '#27ae60'; // Green for 15+ minutes
});
const selected = ref(null);
const selectedItems = ref([]); // For multiselect
const isMultiSelectMode = ref(false);
const lastSelectedItem = ref(null); // For range selection

// Form state
const showForm = ref(false);
const isCreateMode = ref(false);
const formItem = ref(null);
const formViewRef = ref(null);

// Confirmation modal state
const confirmModal = ref(null);
const pendingSelection = ref(null);

// Navigation state
// Navigation state and functions are handled by the main view logic

const currentSectionTitle = computed(() => {
  if (view.value === 'users') return 'User Management';
  if (isControlsViewActive.value) return 'Controls Management';
  return 'Management';
});

const listConfig = computed(() => {
  switch (view.value) {
    case 'users':
      return { 
        title: 'Users', 
        fetch: getUsers,
        itemHeading: (item) => item.name || 'Unnamed User',
        itemSub: (item) => item.email || '',
        itemDesc: (item) => '',
        itemBadge: (item) => item.is_active ? '' : 'New'
      };
    case 'controls':
      return { 
        title: 'Controls', 
        fetch: getControls,
        itemHeading: (item) => item.name || item.title || 'Unnamed Control',
        itemSub: (item) => item.short_name || '',
        itemDesc: (item) => '',
        itemBadge: (item) => item.status || ''
      };
    case 'frameworks':
      return { 
        title: 'Frameworks', 
        fetch: getFrameworks,
        itemHeading: (item) => item.name || 'Unnamed Framework',
        itemSub: (item) => item.short_name || '',
        itemDesc: (item) => '',
        itemBadge: (item) => ''
      };
    case 'implementationGroups':
      return { 
        title: 'Implementation Groups', 
        fetch: getImplementationGroups,
        itemHeading: (item) => item.name || 'Unnamed Group',
        itemSub: (item) => item.short_name || '',
        itemDesc: (item) => '',
        itemBadge: (item) => item.status || ''
      };
    case 'functions':
      return { 
        title: 'Functions', 
        fetch: getFunctions,
        itemHeading: (item) => item.name || 'Unnamed Function',
        itemSub: (item) => item.short_name || '',
        itemDesc: (item) => '',
        itemBadge: (item) => item.status || ''
      };
    case 'safeguards':
      return { 
        title: 'Safeguards', 
        fetch: getSafeguards,
        itemHeading: (item) => item.name || 'Unnamed Safeguard',
        itemSub: (item) => item.short_name || '',
        itemDesc: (item) => '',
        itemBadge: (item) => item.status || ''
      };
    case 'configuration-item-types':
      return { 
        title: 'Configuration Item Types', 
        fetch: getConfigurationItemTypes,
        get: getConfigurationItemType,
        itemHeading: (item) => item.name || 'Unnamed Configuration Item Type',
        itemSub: (item) => item.short_name || '',
        itemDesc: (item) => item.description || '',
        itemBadge: (item) => ''
      };
    default:
      return { 
        title: 'List', 
        fetch: () => Promise.resolve([]),
        itemHeading: (item) => item.name || 'Unnamed Item',
        itemSub: (item) => '',
        itemDesc: (item) => '',
        itemBadge: (item) => ''
      };
  }
});

// Check if form has unsaved changes
const hasUnsavedChanges = computed(() => {
  if (!showForm.value || !formViewRef.value) return false;
  
  try {
    const formData = formViewRef.value.formData;
    if (!formData) return false;
    
    // For create mode, check if any field has been filled
    if (isCreateMode.value) {
      return Object.values(formData).some(value => 
        value !== null && value !== undefined && value !== ''
      );
    }
    
    // For edit mode, check if any field has changed from original
    if (formItem.value) {
      return Object.keys(formData).some(key => 
        formData[key] !== formItem.value[key]
      );
    }
  } catch (error) {
    // If there's an error accessing formData, assume no changes
    return false;
  }
  
  return false;
});

// Fetch and manage dropdown options
const fetchDropdownData = async () => {
  try {
    // Fetch frameworks
    const frameworksResponse = await getFrameworks();
    frameworks.value = Array.isArray(frameworksResponse) ? frameworksResponse : frameworksResponse.data || [];
    
    // Fetch implementation groups
    const implementationGroupsResponse = await getImplementationGroups();
    implementationGroups.value = Array.isArray(implementationGroupsResponse) ? implementationGroupsResponse : implementationGroupsResponse.data || [];
    
    // Fetch functions
    const functionsResponse = await getFunctions();
    functions.value = Array.isArray(functionsResponse) ? functionsResponse : functionsResponse.data || [];
    
    // Fetch configuration item types
    const configurationItemTypesResponse = await getConfigurationItemTypes();
    configurationItemTypes.value = Array.isArray(configurationItemTypesResponse) ? configurationItemTypesResponse : configurationItemTypesResponse.data || [];
    
    // Fetch controls
    const controlsResponse = await getControls();
    controls.value = Array.isArray(controlsResponse) ? controlsResponse : controlsResponse.data || [];
  } catch (error) {
    console.error('Error fetching dropdown data:', error);
    frameworks.value = [];
    implementationGroups.value = [];
    functions.value = [];
    configurationItemTypes.value = [];
    controls.value = [];
  }
};

// Get framework options for dropdown
const getFrameworkOptions = () => {
  return frameworks.value.map(framework => ({
    value: framework.id,
    label: framework.short_name ? `${framework.short_name} — ${framework.name}` : framework.name
  }));
};

// Get implementation group options for dropdown (filtered by framework if selected)
const getImplementationGroupOptions = (frameworkId = null) => {
  const targetFrameworkId = frameworkId || selectedFrameworkId.value;
  
  let filteredGroups = implementationGroups.value;
  
  // Filter by framework if one is selected
  if (targetFrameworkId) {
    filteredGroups = implementationGroups.value.filter(group => 
      group.framework_id === targetFrameworkId
    );
  }
  
  return filteredGroups.map(group => ({
    value: group.id,
    label: group.short_name ? `${group.short_name} — ${group.name}` : group.name
  }));
};

// Get control options for dropdown (filtered by framework if selected)
const getControlOptions = (frameworkId = null) => {
  const targetFrameworkId = frameworkId || selectedFrameworkId.value;
  
  let filteredControls = controls.value;
  
  // Filter by framework if one is selected
  if (targetFrameworkId) {
    filteredControls = controls.value.filter(control => 
      control.framework_id === targetFrameworkId
    );
  }
  
  return filteredControls.map(ctrl => ({
    value: ctrl.id,
    label: ctrl.short_name ? `${ctrl.short_name} — ${ctrl.name}` : ctrl.name
  }));
};

// Computed property for edit fields that updates when dropdown data changes
const editFields = computed(() => {
  return getEditFields(view.value);
});

// Computed options for dropdowns that update reactively
const computedControlOptions = computed(() => {
  return getControlOptions();
});

const computedImplementationGroupOptions = computed(() => {
  return getImplementationGroupOptions();
});

const fetchItems = async () => {
  const { fetch } = listConfig.value;
  try {
    // Fetch main items
    const response = await fetch();
    items.value = Array.isArray(response) ? response : response.data || [];
    
    // Fetch dropdown data for forms (only when needed)
    if (view.value === 'controls' || view.value === 'implementationGroups' || view.value === 'safeguards' || showForm.value) {
      await fetchDropdownData();
    }
    
    // Handle selection based on URL
    if (pendingSelectionId.value) {
      // Find item by ID from URL
      const itemToSelect = items.value.find(item => item.id === pendingSelectionId.value);
      if (itemToSelect) {
        // For configuration item types, fetch the full item data with relationships
        if (view.value === 'configuration-item-types') {
          try {
            console.log('Fetching full configuration item type data for pending selection:', itemToSelect.name);
            const fullItem = await getConfigurationItemType(itemToSelect.id);
            console.log('Received full item data:', fullItem);
            selected.value = fullItem;
          } catch (error) {
            console.error('Error fetching full asset class data:', error);
            selected.value = itemToSelect;
          }
        } else {
          selected.value = itemToSelect;
        }
      } else {
        selected.value = null;
      }
      pendingSelectionId.value = null; // Clear pending selection
      
      // If item not found and URL has an ID, redirect to module root
      if (!itemToSelect && route.params?.id) {
        router.push(getModuleRootPath(view.value));
      }
    } else if (route.params?.id) {
      // URL has an ID but we haven't processed it yet - find and select the item
      const itemToSelect = items.value.find(item => item.id === route.params.id);
      if (itemToSelect) {
        // For configuration item types, fetch the full item data with relationships
        if (view.value === 'configuration-item-types') {
          try {
            console.log('Fetching full configuration item type data for route selection:', itemToSelect.name);
            const fullItem = await getConfigurationItemType(itemToSelect.id);
            console.log('Received full item data:', fullItem);
            selected.value = fullItem;
          } catch (error) {
            console.error('Error fetching full asset class data:', error);
            selected.value = itemToSelect;
          }
        } else {
          selected.value = itemToSelect;
        }
      } else {
        selected.value = null;
        // If item not found, redirect to module root
        router.push(getModuleRootPath(view.value));
      }
    } else {
      // No ID in URL - show module home without selection
      selected.value = null;
    }
  } catch (error) {
    console.error('Error fetching items:', error);
    items.value = [];
    selected.value = null;
  }
};

const handleSelect = async item => {
  // If we're in multiselect mode, handle differently
  if (isMultiSelectMode.value) {
    handleMultiSelect(item);
    return;
  }
  
  // If we're in form mode and have unsaved changes, show confirmation
  if (showForm.value && hasUnsavedChanges.value) {
    pendingSelection.value = item;
    showConfirmationModal();
    return;
  }
  
  // If the same item is already selected, don't reload it (prevents overwriting full data with basic data)
  if (selected.value && selected.value.id === item.id) {
    console.log('HandleSelect: Item already selected, skipping reload:', item.name);
    return;
  }
  
  // For configuration item types, fetch the full item data with relationships
  if (view.value === 'configuration-item-types' && item.id) {
    try {
      console.log('HandleSelect: Fetching full configuration item type data for:', item.name);
      const fullItem = await getConfigurationItemType(item.id);
      console.log('HandleSelect: Received full item data:', fullItem);
      console.log('HandleSelect: About to set selected.value to fullItem');
      selected.value = fullItem;
      console.log('HandleSelect: selected.value has been set to:', selected.value.name, 'with relationships:', {
        parents: selected.value.parents?.length || 0,
        children: selected.value.children?.length || 0
      });
    } catch (error) {
      console.error('Error fetching full asset class data:', error);
      // Fallback to the list item if fetch fails
      selected.value = item;
    }
  } else {
    // For other item types, use the list item directly
    selected.value = item;
  }
  
  lastSelectedItem.value = item; // Track for range selection
  
  // Update URL to reflect selection
  if (item && item.id) {
    navigateToRecord(view.value, item.id);
  }
  
  // If in edit mode, switch to the new item's edit form
  if (showForm.value && !isCreateMode.value) {
    formItem.value = selected.value;
  }
};

const handleMultiSelect = (item) => {
  const index = selectedItems.value.findIndex(selectedItem => selectedItem.id === item.id);
  if (index > -1) {
    // Item is already selected, remove it
    selectedItems.value.splice(index, 1);
  } else {
    // Item is not selected, add it
    selectedItems.value.push(item);
  }
  
  // Track last selected item for range selection
  lastSelectedItem.value = item;
  
  // Clear single selection when in multiselect mode
  selected.value = null;
};

const handleRangeSelect = (item) => {
  if (!lastSelectedItem.value) {
    // No previous selection, just select this item
    handleMultiSelect(item);
    return;
  }
  
  // Find the indices of the last selected item and current item
  const lastIndex = items.value.findIndex(i => i.id === lastSelectedItem.value.id);
  const currentIndex = items.value.findIndex(i => i.id === item.id);
  
  if (lastIndex === -1 || currentIndex === -1) {
    // Can't find one of the items, just select the current item
    handleMultiSelect(item);
    return;
  }
  
  // Determine the range
  const startIndex = Math.min(lastIndex, currentIndex);
  const endIndex = Math.max(lastIndex, currentIndex);
  
  // Select all items in the range
  const rangeItems = items.value.slice(startIndex, endIndex + 1);
  
  // Add all items in range to selection (avoiding duplicates)
  rangeItems.forEach(rangeItem => {
    const isAlreadySelected = selectedItems.value.some(selectedItem => selectedItem.id === rangeItem.id);
    if (!isAlreadySelected) {
      selectedItems.value.push(rangeItem);
    }
  });
  
  // Clear single selection when in multiselect mode
  selected.value = null;
};

const toggleMultiSelect = () => {
  isMultiSelectMode.value = !isMultiSelectMode.value;
  
  // Clear selections when toggling modes
  if (!isMultiSelectMode.value) {
    selectedItems.value = [];
    lastSelectedItem.value = null;
  } else {
    selected.value = null;
  }
};

const handleSelectAll = () => {
  if (selectedItems.value.length === items.value.length) {
    // All items are selected, deselect all
    selectedItems.value = [];
  } else {
    // Not all items are selected, select all
    selectedItems.value = [...items.value];
  }
};

const handleBulkDelete = async (itemsToDelete) => {
  try {
    const deleteFunction = getDeleteFunction(view.value);
    if (deleteFunction) {
      // Delete all selected items
      await Promise.all(itemsToDelete.map(item => deleteFunction(item.id)));
      
      // Remove deleted items from the list
      const deletedIds = itemsToDelete.map(item => item.id);
      items.value = items.value.filter(item => !deletedIds.includes(item.id));
      
      // Clear selections
      selectedItems.value = [];
      selected.value = null;
      
      // Exit multiselect mode
      isMultiSelectMode.value = false;
      
      console.log(`${itemsToDelete.length} items deleted successfully`);
    }
  } catch (error) {
    console.error('Bulk delete error:', error);
    // TODO: Show error notification to user
  }
};

const showConfirmationModal = () => {
  if (confirmModal.value) {
    const bootstrapModal = new window.bootstrap.Modal(confirmModal.value);
    bootstrapModal.show();
  }
};

const handleStayOnForm = () => {
  // User chose to stay, clear pending selection
  pendingSelection.value = null;
};

const handleDiscardChanges = () => {
  // User chose to discard changes, proceed with selection
  if (pendingSelection.value) {
    selected.value = pendingSelection.value;
    
    // Update URL to reflect selection
    if (pendingSelection.value && pendingSelection.value.id) {
      navigateToRecord(view.value, pendingSelection.value.id);
    }
    
    // If in edit mode, switch to the new item's edit form
    if (showForm.value && !isCreateMode.value) {
      formItem.value = pendingSelection.value;
    }
    
    pendingSelection.value = null;
  }
};

const handleLogout = () => {
  logout();
  router.push('/login');
};

const handleProfile = () => {
  showUserMenu.value = false;
  // TODO: Implement profile management
  console.log('Profile clicked');
};

const handleChangePassword = () => {
  showUserMenu.value = false;
  // TODO: Implement change password
  console.log('Change password clicked');
};

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
};

const formatTimeRemaining = (minutes) => {
  if (minutes < 60) {
    return `${minutes}m`;
  } else if (minutes < 1440) { // Less than 24 hours
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return `${hours}h ${remainingMinutes}m`;
  } else {
    const days = Math.floor(minutes / 1440);
    const remainingHours = Math.floor((minutes % 1440) / 60);
    return `${days}d ${remainingHours}h`;
  }
};

// Close user menu when clicking outside
const handleOutsideClick = (event) => {
  if (showUserMenu.value && !event.target.closest('.user-profile')) {
    showUserMenu.value = false;
  }
};

// Add event listener for clicking outside
document.addEventListener('click', handleOutsideClick);

// Navigation functions
const navigateToModule = (module) => {
  console.log('navigateToModule called with:', module);
  const routeMap = {
    activity: '/activity',
    users: '/users',
    controls: '/controls',
    frameworks: '/controls/frameworks',
    implementationGroups: '/controls/implementation-groups',
    functions: '/controls/functions',
    safeguards: '/controls/safeguards',
    'configuration-item-types': '/cmdb/configuration-item-types',
    devices: '/devices',
    software: '/software',
    data: '/data',
    network: '/network',
    documentation: '/documentation'
  };
  
  const path = routeMap[module] || '/users';
  console.log('Navigating to path:', path);
  router.push(path);
};

const getModuleRootPath = (module) => {
  const routeMap = {
    activity: '/activity',
    users: '/users',
    controls: '/controls',
    frameworks: '/controls/frameworks',
    implementationGroups: '/controls/implementation-groups',
    functions: '/controls/functions',
    safeguards: '/controls/safeguards',
    'configuration-item-types': '/cmdb/configuration-item-types',
    devices: '/devices',
    software: '/software',
    data: '/data',
    network: '/network',
    documentation: '/documentation'
  };
  
  return routeMap[module] || '/users';
};

const navigateToRecord = (module, recordId) => {
  const routeMap = {
    activity: `/activity/${recordId}`,
    users: `/users/${recordId}`,
    controls: `/controls/${recordId}`,
    frameworks: `/controls/frameworks/${recordId}`,
    implementationGroups: `/controls/implementation-groups/${recordId}`,
    functions: `/controls/functions/${recordId}`,
    safeguards: `/controls/safeguards/${recordId}`,
    'configuration-item-types': `/cmdb/configuration-item-types/${recordId}`,
    devices: `/devices/${recordId}`,
    software: `/software/${recordId}`,
    data: `/data/${recordId}`,
    network: `/network/${recordId}`,
    documentation: `/documentation/${recordId}`
  };
  
  const path = routeMap[module] || `/users/${recordId}`;
  router.push(path);
};

const handleAdd = async () => {
  showForm.value = true;
  isCreateMode.value = true;
  formItem.value = null;
  selected.value = null;
  
  // Fetch dropdown data for controls and implementation groups
  if (view.value === 'controls' || view.value === 'implementationGroups' || view.value === 'safeguards') {
    await fetchDropdownData();
  }
  
  // Navigate to module root (without ID) when creating new items
  navigateToModule(view.value);
};

const handleSearch = (query) => {
  // Search is handled by the ListGroup component internally
  console.log('Search query:', query);
};

const handleFilter = () => {
  // TODO: Implement filter functionality
  console.log('Filter clicked');
};

const handleSort = () => {
  // TODO: Implement sort functionality
  console.log('Sort clicked');
};

// DetailView helper methods
const getItemName = (item) => {
  if (!item) return '';
  return listConfig.value.itemHeading(item);
};

const getItemSubtitle = (item) => {
  if (!item) return '';
  return listConfig.value.itemSub(item);
};

const getItemStatus = (item) => {
  if (!item) return '';
  if (item.locked) return 'Locked';
  return listConfig.value.itemBadge(item) || item.status;
};

const getSingularTitle = (title) => {
  const singularMap = {
    'Configuration Item Types': 'Configuration Item Type',
    'Controls': 'Control',
    'Frameworks': 'Framework',
    'Implementation Groups': 'Implementation Group',
    'Functions': 'Function',
    'Safeguards': 'Safeguard'
  };
  return singularMap[title] || title.slice(0, -1);
};

const isItemLocked = (item) => {
  if (!item) return false;
  return item.locked === true;
};

const getAvatarIcon = (viewType) => {
  const icons = {
    users: 'bi bi-person',
    controls: 'bi bi-shield-check',
    frameworks: 'bi bi-diagram-3',
    implementationGroups: 'bi bi-layers',
    functions: 'bi bi-gear',
    safeguards: 'bi bi-lock',
    'configuration-item-types': 'bi bi-diagram-3',
    devices: 'fas fa-laptop',
    software: 'fas fa-code',
    data: 'fas fa-database',
    network: 'fas fa-network-wired',
    documentation: 'fas fa-file-alt',
    activity: 'fas fa-heartbeat'
  };
  return icons[viewType] || 'bi bi-box';
};

// Module home helper methods
const getModuleDisplayName = (viewType) => {
  const names = {
    users: 'User Management',
    controls: 'Security Controls',
    frameworks: 'Control Frameworks',
    implementationGroups: 'Implementation Groups',
    functions: 'Security Functions',
    safeguards: 'Control Safeguards',
    'configuration-item-types': 'Configuration Item Types',
    devices: 'Device Management',
    software: 'Software Management',
    data: 'Data Management',
    network: 'Network Management',
    documentation: 'Documentation',
    activity: 'Activity Monitor'
  };
  return names[viewType] || 'Management';
};

const getModuleDescription = (viewType) => {
  const descriptions = {
    users: 'Manage user accounts, roles, and permissions within the system.',
    controls: 'Define and manage security controls and their implementation requirements.',
    frameworks: 'Organize controls into frameworks for compliance and governance.',
    implementationGroups: 'Group controls by implementation priority and organizational maturity.',
    functions: 'Organize controls by security function areas like Asset Management, Access Control, etc.',
    safeguards: 'Specific safeguards and technical measures for control implementation.',
    'configuration-item-types': 'Define configuration item types and their hierarchical relationships for CMDB organization.',
    devices: 'Track and manage hardware devices, endpoints, and physical assets.',
    software: 'Catalog and manage software applications, systems, and digital assets.',
    data: 'Organize and classify data assets, databases, and information repositories.',
    network: 'Monitor and manage network infrastructure, connections, and communication paths.',
    documentation: 'Access policies, procedures, guides, and regulatory documentation.',
    activity: 'View system activity, audit logs, and security monitoring information.'
  };
  return descriptions[viewType] || 'Manage system resources and settings.';
};

const getModuleHelpTitle = (viewType) => {
  const titles = {
    users: 'Managing Users',
    controls: 'About Security Controls',
    frameworks: 'Understanding Frameworks',
    implementationGroups: 'Implementation Strategy',
    functions: 'Security Function Areas',
    safeguards: 'Technical Safeguards',
    'asset-classes': 'Asset Classification',
    devices: 'Device Inventory',
    software: 'Software Catalog',
    data: 'Data Classification',
    network: 'Network Topology',
    documentation: 'Documentation Library',
    activity: 'Activity Monitoring'
  };
  return titles[viewType] || 'Getting Started';
};

const getModuleHelpText = (viewType) => {
  const texts = {
    users: 'Create user accounts, assign roles, and manage access permissions. Users can be administrators, standard users, or viewers.',
    controls: 'Security controls define the policies, procedures, and technical measures required to protect your organization.',
    frameworks: 'Frameworks provide structured approaches to security compliance like NIST, ISO 27001, or CIS Controls.',
    implementationGroups: 'Prioritize control implementation based on your organization\'s security maturity and risk profile.',
    functions: 'Group controls by functional areas such as Asset Management, Access Control, Incident Response, etc.',
    safeguards: 'Technical safeguards are specific measures and configurations that implement security controls.',
    'asset-classes': 'Define asset categories to organize controls by the types of resources they protect, such as Physical devices, Technical systems, or Administrative processes.',
    devices: 'Track physical and virtual devices, including servers, workstations, mobile devices, and IoT equipment. Monitor device status, compliance, and security posture.',
    software: 'Maintain an inventory of software applications, operating systems, and digital services. Track versions, licenses, and security updates.',
    data: 'Classify and manage data assets based on sensitivity, regulatory requirements, and business value. Track data flows and access patterns.',
    network: 'Document network architecture, monitor connections, and manage network security policies. Track network devices and communication paths.',
    documentation: 'Access organizational policies, security procedures, compliance documentation, and user guides. Maintain document versioning and approval workflows.',
    activity: 'Monitor system events, user activities, and security incidents. Review audit logs and generate compliance reports for regulatory requirements.'
  };
  return texts[viewType] || 'Learn how to use this module effectively.';
};

const getActiveCount = () => {
  if (!items.value) return 0;
  return items.value.filter(item => 
    item.is_active !== false && 
    item.status !== 'disabled' && 
    item.status !== 'inactive'
  ).length;
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};

const handleBulkImport = () => {
  // TODO: Implement bulk import functionality
  console.log('Bulk import clicked for:', view.value);
};

const getQuickInfoFields = (viewType) => {
  const fields = {
    users: ['role', 'organization', 'is_active'],
    controls: ['short_name', 'framework_id', 'function_id'],
    frameworks: ['short_name', 'description'],
    implementationGroups: ['short_name', 'type', 'category', 'status'],
    functions: ['short_name', 'description'],
    safeguards: ['short_name', 'implementation_group_id', 'function_id', 'control_id']
  };
  return fields[viewType] || ['type', 'status', 'category'];
};

const getLinkedObjects = (item) => {
  // TODO: Implement based on item type and relationships
  if (!item) return [];
  
  // Example linked objects structure
  return [
    // { id: '1', name: 'Related Control', type: 'Control', relationship: 'Parent', icon: 'bi bi-shield-check' }
  ];
};

const getActivityLog = (item) => {
  // TODO: Implement activity log retrieval
  if (!item) return [];
  
  // Example activity log structure
  return [
    // { id: '1', action: 'Created', user: 'Admin', timestamp: item.created_at, icon: 'bi bi-plus-circle' },
    // { id: '2', action: 'Updated', user: 'Admin', timestamp: item.updated_at, icon: 'bi bi-pencil' }
  ];
};

// DetailView action handlers
const handleEdit = async () => {
  if (selected.value) {
    showForm.value = true;
    isCreateMode.value = false;
    formItem.value = selected.value;
    
    // Fetch dropdown data for controls and implementation groups
    if (view.value === 'controls' || view.value === 'implementationGroups' || view.value === 'safeguards') {
      await fetchDropdownData();
      // Set the selected framework ID for filtering implementation groups (controls only)
      if (view.value === 'controls') {
        selectedFrameworkId.value = selected.value.framework_id || null;
      }
    }
  }
};

const handleDuplicate = () => {
  // TODO: Implement duplicate functionality
  console.log('Duplicate clicked for:', selected.value);
};

const handleDetailRefresh = async () => {
  // Refresh the items list to get updated data
  await fetchItems();
  
  // If we have a selected item, refresh its data to include updated relationships
  if (selected.value && selected.value.id) {
    // For asset classes, use the same logic as handleSelect to get full data with relationships
    if (view.value === 'asset-classes') {
      try {
        const fullItem = await getAssetClass(selected.value.id);
        selected.value = fullItem;
      } catch (error) {
        console.error('Error refreshing full asset class data:', error);
        // Fallback to basic API
        const { get } = listConfig.value;
        if (get) {
          try {
            const refreshedItem = await get(selected.value.id);
            selected.value = refreshedItem;
          } catch (fallbackError) {
            console.error('Error with fallback refresh:', fallbackError);
          }
        }
      }
    } else {
      // For other item types, use the basic get function
      const { get } = listConfig.value;
      if (get) {
        try {
          const refreshedItem = await get(selected.value.id);
          selected.value = refreshedItem;
        } catch (error) {
          console.error('Error refreshing selected item:', error);
          // If refresh fails, just keep the current item
        }
      }
    }
  }
};

const handleDelete = async () => {
  if (!selected.value) return;
  
  // Confirm deletion
  if (!confirm(`Are you sure you want to delete this ${getSingularTitle(listConfig.value.title).toLowerCase()}?`)) {
    return;
  }
  
  try {
    const deleteFunction = getDeleteFunction(view.value);
    if (deleteFunction) {
      await deleteFunction(selected.value.id);
      
      // Remove item from list directly instead of refetching
      const deletedItemId = selected.value.id;
      items.value = items.value.filter(item => item.id !== deletedItemId);
      
      // Select the next item or clear selection
      if (items.value.length > 0) {
        const currentIndex = items.value.findIndex(item => item.id === deletedItemId);
        const nextIndex = Math.min(currentIndex, items.value.length - 1);
        selected.value = items.value[nextIndex] || items.value[0];
      } else {
        selected.value = null;
      }
      
      console.log('Item deleted successfully');
    }
  } catch (error) {
    console.error('Delete error:', error);
    // TODO: Show error notification to user
  }
};

const handleExport = () => {
  // TODO: Implement export functionality
  console.log('Export clicked for:', selected.value);
};

const handleViewLinked = (linkedItem) => {
  // TODO: Implement view linked object functionality
  console.log('View linked clicked for:', linkedItem);
};

const handleViewRelated = async (relatedItem) => {
  console.log('HandleViewRelated called with:', relatedItem);
  console.log('HandleViewRelated stack trace:', new Error().stack);
  
  // Navigate to the related asset class
  if (relatedItem.type === 'asset-class') {
    // For asset classes, use the same logic as handleSelect to get full data with relationships
    if (view.value === 'asset-classes') {
      try {
        console.log('HandleViewRelated: Fetching full asset class data for:', relatedItem.id);
        const fullItem = await getAssetClass(relatedItem.id);
        console.log('HandleViewRelated: Setting selected.value to full item with relationships');
        selected.value = fullItem;
      } catch (error) {
        console.error('HandleViewRelated: Error fetching full asset class data:', error);
        // Fallback to finding in list
        const assetClass = items.value.find(item => item.id === relatedItem.id);
        if (assetClass) {
          console.log('HandleViewRelated: Fallback - Setting selected.value to basic list item');
          selected.value = assetClass;
        }
      }
    } else {
      // For other views, find the asset class in the list
      const assetClass = items.value.find(item => item.id === relatedItem.id);
      if (assetClass) {
        console.log('HandleViewRelated: Setting selected.value to basic list item (not asset-classes view)');
        selected.value = assetClass;
      }
    }
    showForm.value = false; // Make sure we're in detail view mode
  }
};

// Edit Modal helpers
const getEditFields = (viewType) => {
  const fieldConfigs = {
    users: [
      { key: 'name', label: 'Full Name', type: 'text', required: true, colClass: 'col-md-6', placeholder: 'Enter full name' },
      { key: 'email', label: 'Email Address', type: 'email', required: true, colClass: 'col-md-6', placeholder: 'user@example.com' },
      { key: 'role', label: 'Role', type: 'select', options: [
        { value: 'admin', label: 'Administrator' },
        { value: 'user', label: 'User' },
        { value: 'viewer', label: 'Viewer' }
      ], colClass: 'col-md-6', placeholder: 'Select a role', defaultValue: 'user' },
      { key: 'organization', label: 'Organization', type: 'text', colClass: 'col-md-6', placeholder: 'Organization name', defaultValue: 'MCGUIRE TECHNOLOGY, LLC' },
      { key: 'is_active', label: 'Account Status', type: 'checkbox', checkboxLabel: 'Account is active', defaultValue: true }
    ],
    controls: [
      { key: 'name', label: 'Control Name', type: 'text', required: true, colClass: 'col-md-6', placeholder: 'Enter control name' },
      { key: 'short_name', label: 'Short Name', type: 'text', colClass: 'col-md-6', placeholder: 'e.g., AC-1' },
      { key: 'description', label: 'Description', type: 'textarea', rows: 4, placeholder: 'Describe the control objective and implementation details' },
      { 
        key: 'framework_id', 
        label: 'Framework', 
        type: 'select', 
        options: frameworks.value.map(framework => ({
          value: framework.id,
          label: framework.short_name ? `${framework.short_name} — ${framework.name}` : framework.name
        })), 
        colClass: 'col-md-6', 
        placeholder: 'Select framework (required)',
        required: true
      },
      { 
        key: 'asset_class_id', 
        label: 'Asset Class', 
        type: 'select', 
        options: assetClasses.value.map(assetClass => ({
          value: assetClass.id,
          label: assetClass.short_name ? `${assetClass.short_name} — ${assetClass.name}` : assetClass.name
        })), 
        colClass: 'col-md-6', 
        placeholder: 'Select asset class (optional)'
      },
      { 
        key: 'color', 
        label: 'Color', 
        type: 'color', 
        colClass: 'col-md-6', 
        placeholder: '#6c757d',
        defaultValue: '#6c757d',
        help: 'Choose a color to identify this control in the interface'
      }
    ],
    frameworks: [
      { key: 'name', label: 'Framework Name', type: 'text', required: true, colClass: 'col-md-8', placeholder: 'Enter framework name' },
      { key: 'short_name', label: 'Short Name', type: 'text', colClass: 'col-md-4', placeholder: 'e.g., NIST, CIS' },
      { key: 'description', label: 'Description', type: 'textarea', rows: 4, placeholder: 'Describe the framework scope and purpose' },
      { 
        key: 'color', 
        label: 'Color', 
        type: 'color', 
        colClass: 'col-md-12', 
        placeholder: '#198754',
        defaultValue: '#198754',
        help: 'Choose a color to identify this framework in the interface'
      }
    ],
    implementationGroups: [
      { key: 'name', label: 'Group Name', type: 'text', required: true, colClass: 'col-md-6', placeholder: 'Enter implementation group name' },
      { key: 'short_name', label: 'Short Name', type: 'text', colClass: 'col-md-6', placeholder: 'e.g., IG1' },
      { key: 'description', label: 'Description', type: 'textarea', rows: 4, placeholder: 'Describe the implementation group purpose and scope' },
      { 
        key: 'framework_id', 
        label: 'Framework', 
        type: 'select', 
        options: frameworks.value.map(framework => ({
          value: framework.id,
          label: framework.short_name ? `${framework.short_name} — ${framework.name}` : framework.name
        })), 
        colClass: 'col-md-6', 
        placeholder: 'Select framework (optional)'
      },
      { 
        key: 'color', 
        label: 'Color', 
        type: 'color', 
        colClass: 'col-md-6', 
        placeholder: '#ffc107',
        defaultValue: '#ffc107',
        help: 'Choose a color to identify this implementation group in the interface'
      }
    ],
    functions: [
      { key: 'name', label: 'Function Name', type: 'text', required: true, colClass: 'col-md-6', placeholder: 'Enter security function name' },
      { key: 'short_name', label: 'Short Name', type: 'text', colClass: 'col-md-6', placeholder: 'e.g., AM, AC' },
      { key: 'description', label: 'Description', type: 'textarea', rows: 4, placeholder: 'Describe the security function scope and purpose' },
      { 
        key: 'framework_id', 
        label: 'Framework', 
        type: 'select', 
        options: getFrameworkOptions(), 
        colClass: 'col-md-6', 
        placeholder: 'Select framework (optional)'
      },
      { 
        key: 'color', 
        label: 'Color', 
        type: 'color', 
        colClass: 'col-md-6', 
        placeholder: '#0d6efd',
        defaultValue: '#0d6efd',
        help: 'Choose a color to identify this function in the interface'
      }
    ],
    safeguards: [
      { key: 'name', label: 'Safeguard Name', type: 'text', required: true, colClass: 'col-md-6', placeholder: 'Enter safeguard name' },
      { key: 'short_name', label: 'Short Name', type: 'text', colClass: 'col-md-6', placeholder: 'e.g., 1.1' },
      { key: 'description', label: 'Description', type: 'textarea', rows: 4, placeholder: 'Describe the safeguard implementation and purpose' },
      { 
        key: 'implementation_group_id', 
        label: 'Implementation Group', 
        type: 'select', 
        options: computedImplementationGroupOptions.value, 
        colClass: 'col-md-6', 
        placeholder: 'Select implementation group (optional)'
      },
      { 
        key: 'function_id', 
        label: 'Security Function', 
        type: 'select', 
        options: functions.value.map(func => ({
          value: func.id,
          label: func.name
        })), 
        colClass: 'col-md-6', 
        placeholder: 'Select security function (optional)'
      },
      { 
        key: 'control_id', 
        label: 'Control', 
        type: 'select', 
        options: controls.value.map(ctrl => ({
          value: ctrl.id,
          label: ctrl.short_name ? `${ctrl.short_name} — ${ctrl.name}` : ctrl.name
        })), 
        colClass: 'col-md-6', 
        placeholder: 'Select control (optional)'
      },
      { 
        key: 'asset_class_id', 
        label: 'Asset Class', 
        type: 'select', 
        options: assetClasses.value.map(assetClass => ({
          value: assetClass.id,
          label: assetClass.short_name ? `${assetClass.short_name} — ${assetClass.name}` : assetClass.name
        })), 
        colClass: 'col-md-6', 
        placeholder: 'Select asset class (optional)'
      }
    ],
    'asset-classes': [
      { key: 'name', label: 'Asset Class Name', type: 'text', required: true, colClass: 'col-md-6', placeholder: 'Enter asset class name' },
      { key: 'short_name', label: 'Short Name', type: 'text', colClass: 'col-md-6', placeholder: 'e.g., PHYS, TECH' },
      { key: 'description', label: 'Description', type: 'textarea', rows: 4, placeholder: 'Describe the asset class scope and purpose' },
      { 
        key: 'framework_id', 
        label: 'Framework', 
        type: 'select', 
        options: getFrameworkOptions(), 
        colClass: 'col-md-6', 
        placeholder: 'Select framework (optional)'
      },
      { 
        key: 'color', 
        label: 'Color', 
        type: 'color', 
        colClass: 'col-md-6', 
        placeholder: '#17a2b8',
        defaultValue: '#17a2b8',
        help: 'Choose a color to identify this asset class in the interface'
      },
      { 
        key: 'locked', 
        label: 'Protection Status', 
        type: 'checkbox', 
        checkboxLabel: 'Lock this asset class (prevents modification and deletion)',
        colClass: 'col-md-12',
        defaultValue: false,
        help: 'Locked asset classes cannot be modified or deleted via the API'
      }
    ]
  };
  return fieldConfigs[viewType] || [];
};

const getUpdateFunction = (viewType) => {
  const updateFunctions = {
    users: updateUser,
    controls: updateControl,
    frameworks: updateFramework,
    implementationGroups: updateImplementationGroup,
    functions: updateFunction,
    safeguards: updateSafeguard,
    'asset-classes': updateAssetClass
  };
  return updateFunctions[viewType];
};

const getCreateFunction = (viewType) => {
  const createFunctions = {
    users: createUser,
    controls: createControl,
    frameworks: createFramework,
    implementationGroups: createImplementationGroup,
    functions: createFunction,
    safeguards: createSafeguard,
    'asset-classes': createAssetClass
  };
  return createFunctions[viewType];
};

const getDeleteFunction = (viewType) => {
  const deleteFunctions = {
    users: deleteUser,
    controls: deleteControl,
    frameworks: deleteFramework,
    implementationGroups: deleteImplementationGroup,
    functions: deleteFunction,
    safeguards: deleteSafeguard,
    'asset-classes': deleteAssetClass
  };
  return deleteFunctions[viewType];
};

const handleItemUpdated = (updatedItem) => {
  // Close form and return to detail view
  showForm.value = false;
  isCreateMode.value = false;
  formItem.value = null;
  
  // Update the selected item
  selected.value = updatedItem;
  
  // Update the item in the items array
  const index = items.value.findIndex(item => item.id === updatedItem.id);
  if (index !== -1) {
    items.value[index] = updatedItem;
  }
  
  console.log('Item updated successfully');
};

const handleEditError = (error) => {
  console.error('Edit error:', error);
  // TODO: Show error notification to user
};

// Form event handlers
const handleFormCancel = () => {
  showForm.value = false;
  const wasCreateMode = isCreateMode.value;
  isCreateMode.value = false;
  formItem.value = null;
  
  // Navigate based on context
  if (wasCreateMode) {
    // If canceling create, go back to first item or module root
    if (items.value.length > 0) {
      selected.value = items.value[0];
      navigateToRecord(view.value, items.value[0].id);
    } else {
      selected.value = null;
      navigateToModule(view.value);
    }
  } else if (selected.value) {
    // If canceling edit, stay on the current item
    navigateToRecord(view.value, selected.value.id);
  }
};

const handleItemCreated = (newItem) => {
  showForm.value = false;
  isCreateMode.value = false;
  formItem.value = null;
  
  // Add the new item to the list directly
  items.value.push(newItem);
  selected.value = newItem;
  
  // Navigate to the new item
  if (newItem && newItem.id) {
    navigateToRecord(view.value, newItem.id);
  }
  
  console.log('Item created successfully:', newItem);
};

const handleFormDelete = async () => {
  if (!selected.value) return;
  
  // Confirm deletion
  if (!confirm(`Are you sure you want to delete this ${getSingularTitle(listConfig.value.title).toLowerCase()}?`)) {
    return;
  }
  
  try {
    const deleteFunction = getDeleteFunction(view.value);
    if (deleteFunction) {
      await deleteFunction(selected.value.id);
      
      // Remove item from list directly instead of refetching
      const deletedItemId = selected.value.id;
      items.value = items.value.filter(item => item.id !== deletedItemId);
      
      // Close form and clear selection
      showForm.value = false;
      isCreateMode.value = false;
      formItem.value = null;
      
      // Select the next item or clear selection
      if (items.value.length > 0) {
        selected.value = items.value[0];
      } else {
        selected.value = null;
      }
      
      console.log('Item deleted successfully');
    }
  } catch (error) {
    console.error('Delete error:', error);
    // TODO: Show error notification to user
  }
};

const handleFormError = (error) => {
  console.error('Form error:', error);
  // TODO: Show error notification to user
};

// Handle field changes from the form
const handleFieldChange = (fieldKey, newValue) => {
  if (view.value === 'controls' && fieldKey === 'framework_id') {
    selectedFrameworkId.value = newValue;
    // The computed editFields will automatically update when selectedFrameworkId changes
  } else if (view.value === 'implementationGroups' && fieldKey === 'framework_id') {
    selectedFrameworkId.value = newValue;
    // Implementation groups can be filtered by framework
  }
};

// Watch for route changes
watch(route, (newRoute, oldRoute) => {
  const module = newRoute.meta?.module;
  const oldModule = oldRoute?.meta?.module;
  
  console.log('Route changed - new module:', module, 'old module:', oldModule, 'current view:', view.value);
  
  if (module && module !== view.value) {
    console.log('Setting view to:', module);
    view.value = module;
  }
  
  // Handle record selection from URL
  const recordId = newRoute.params?.id;
  if (recordId) {
    pendingSelectionId.value = recordId;
  }
  
  // If we're staying in the same module but the route changed, we need to handle selection
  if (module === oldModule && module === view.value) {
    if (recordId && items.value.length > 0) {
      const itemToSelect = items.value.find(item => item.id === recordId);
      if (itemToSelect) {
        // For asset classes, fetch the full item data with relationships (same logic as handleSelect)
        if (view.value === 'asset-classes') {
          getAssetClass(itemToSelect.id).then(fullItem => {
            console.log('Route watcher: Setting selected.value to full asset class data');
            selected.value = fullItem;
          }).catch(error => {
            console.error('Route watcher: Error fetching full asset class data:', error);
            console.log('Route watcher: Fallback - Setting selected.value to basic list item');
            selected.value = itemToSelect;
          });
        } else {
          console.log('Route watcher: Setting selected.value to basic list item (not asset-classes)');
          selected.value = itemToSelect;
        }
      }
    }
  }
}, { immediate: true });

watch(view, () => {
  console.log('View changed to:', view.value);
  
  // Reset form state when switching views
  showForm.value = false;
  isCreateMode.value = false;
  formItem.value = null;
  selected.value = null;
  pendingSelectionId.value = null;
  
  // Reset multiselect state when switching views
  isMultiSelectMode.value = false;
  selectedItems.value = [];
  lastSelectedItem.value = null;
  
  fetchItems();
});

// Watch for framework selection changes to update implementation group options
watch(selectedFrameworkId, (newFrameworkId) => {
  // The computed editFields will automatically update when selectedFrameworkId changes
});

// Debug watcher to track all changes to selected value
watch(selected, (newSelected, oldSelected) => {
  if (view.value === 'asset-classes' && newSelected && newSelected.id) {
    console.log('WATCH: selected.value changed to:', {
      name: newSelected.name,
      parents: newSelected.parents?.length || 0,
      children: newSelected.children?.length || 0,
      hasParentsArray: Array.isArray(newSelected.parents),
      hasChildrenArray: Array.isArray(newSelected.children),
      timestamp: new Date().toISOString(),
      stackTrace: new Error().stack
    });
  }
}, { deep: true });

// Initialize dropdown data on component mount
const initializeApp = async () => {
  initializeFromRoute();
  await fetchDropdownData();
};

// Initialize from route on component mount
initializeApp();
</script>

<style scoped>
.dashboard-container {
  display: flex;
  height: 100vh;
  background: #f8f9fa;
}

/* Left Sidebar Navigation */
.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
  position: relative;
  z-index: 1000;
}

.sidebar-header {
  padding: 2rem 1.5rem 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo {
  text-align: center;
}

.app-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  color: white;
}

.app-subtitle {
  font-size: 0.85rem;
  margin: 0.25rem 0 0;
  opacity: 0.8;
  color: white;
}

.sidebar-content {
  flex: 1;
  padding: 1.5rem 0;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 0.5rem;
}

.nav-spacer {
  height: 1rem;
  margin: 0.5rem 0;
}

.nav-section-title {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: rgba(255,255,255,0.7);
  margin: 0 0 1rem 1.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.5rem 1.5rem;
  border: none;
  background: none;
  color: rgba(255,255,255,0.9);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.nav-item:hover {
  background: rgba(255,255,255,0.1);
  color: white;
}

.nav-item.active {
  background: rgba(255,255,255,0.2);
  color: white;
  font-weight: 600;
  border-right: 3px solid white;
}

.nav-item i {
  width: 20px;
  margin-right: 0.75rem;
  text-align: center;
}

/* Hierarchical Navigation Styles */
.nav-section-header {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.5rem 1.5rem;
  border: none;
  background: none;
  color: rgba(255,255,255,0.9);
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.nav-section-header:hover {
  background: rgba(255,255,255,0.1);
  color: white;
}

.nav-section-header.expanded {
  background: rgba(255,255,255,0.1);
  color: white;
}

.nav-section-header.has-active-child {
  background: rgba(255,255,255,0.15);
  color: white;
  border-right: 3px solid rgba(255,255,255,0.6);
}

.section-title {
  flex: 1;
}

.section-chevron {
  font-size: 0.75rem;
  transition: transform 0.2s ease;
}

.section-chevron.rotated {
  transform: rotate(180deg);
}

.nav-subsection {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.nav-subsection.expanded {
  max-height: 300px; /* Adjust based on content */
}

.nav-subitem {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.4rem 1.5rem 0.4rem 2.5rem; /* Extra left padding for hierarchy */
  border: none;
  background: none;
  color: rgba(255,255,255,0.8);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  border-left: 2px solid transparent;
}

.nav-subitem:hover {
  background: rgba(255,255,255,0.1);
  color: white;
  border-left-color: rgba(255,255,255,0.3);
}

.nav-subitem.active {
  background: rgba(255,255,255,0.15);
  color: white;
  font-weight: 600;
  border-left-color: white;
}

.nav-subitem i {
  width: 16px;
  margin-right: 0.75rem;
  text-align: center;
  font-size: 0.8rem;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255,255,255,0.1);
}

.user-profile {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.user-info:hover {
  background: rgba(255,255,255,0.05);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  font-size: 0.9rem;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 0.75rem;
  opacity: 0.7;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.token-countdown {
  font-size: 0.7rem;
  opacity: 0.6;
  margin-top: 2px;
  display: flex;
  align-items: center;
}

.countdown-text {
  margin-left: 2px;
}

/* Add visual warning when time is low */
.token-countdown:has(.countdown-text:matches([content*="m "])) {
  opacity: 0.8;
}

.token-info .expiry-time {
  animation: none;
}

/* Pulse animation for low time */
@keyframes pulse-warning {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.token-expiry .expiry-time:matches([content*="m "]) {
  animation: pulse-warning 2s infinite;
  color: #e74c3c !important;
}

.dropdown-arrow {
  color: rgba(255,255,255,0.6);
  transition: transform 0.2s ease;
}

.dropdown-arrow .rotated {
  transform: rotate(180deg);
}

/* User Menu Dropdown */
.user-menu {
  position: absolute;
  bottom: 100%;
  left: 0;
  right: 0;
  background: #2c3e50;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  opacity: 0;
  transform: translateY(10px);
  visibility: hidden;
  transition: all 0.2s ease;
  z-index: 1000;
  margin-bottom: 8px;
}

.user-menu.show {
  opacity: 1;
  transform: translateY(0);
  visibility: visible;
}

.user-menu-header {
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar-large {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.3rem;
  flex-shrink: 0;
}

.user-details-full {
  flex: 1;
  min-width: 0;
}

.user-name-large {
  font-weight: 600;
  font-size: 1rem;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email-small {
  font-size: 0.8rem;
  opacity: 0.7;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-menu-divider {
  height: 1px;
  background: rgba(255,255,255,0.1);
  margin: 0 0.5rem;
}

.user-menu-items {
  padding: 0.5rem 0;
}

.user-menu-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  background: none;
  color: rgba(255,255,255,0.9);
  font-size: 0.85rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  text-align: left;
}

.user-menu-item:hover {
  background: rgba(255,255,255,0.1);
  color: white;
}

.user-menu-item.logout {
  color: #e74c3c;
}

.user-menu-item.logout:hover {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

.token-info {
  padding: 0.75rem 1rem;
  background: rgba(0,0,0,0.1);
  border-top: 1px solid rgba(255,255,255,0.1);
}

.token-info-header {
  font-size: 0.75rem;
  font-weight: 600;
  opacity: 0.8;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
}

.token-expiry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
}

.expiry-label {
  opacity: 0.7;
}

.expiry-time {
  font-weight: 600;
  color: #f39c12;
}

.btn-icon:hover {
  background: rgba(255,255,255,0.2);
}

/* Main Content Area */
.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* Content Panels */
.content-panels {
  flex: 1;
  display: flex;
  overflow: hidden;
  gap: 0;
}

.master-panel {
  width: 420px;
  background: white;
  border-right: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.detail-panel {
  flex: 1;
  background: white;
  display: flex;
  flex-direction: column;
  border-left: none;
  height: 100vh;
}

.panel-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8f9fa;
}

.panel-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #2c3e50;
}

.panel-actions {
  display: flex;
  gap: 0.5rem;
}

.panel-content {
  flex: 1;
  height: 0; /* Force flex child to respect parent height */
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6c757d;
  text-align: center;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  font-size: 1.1rem;
  margin: 0;
}

.detail-content {
  padding: 1.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5a67d8;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.8rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .sidebar {
    width: 260px;
  }
  
  .master-panel {
    width: 350px;
  }
  
  .panel-header {
    padding: 1rem;
  }
  
  .detail-content {
    padding: 1rem;
  }
}

@media (max-width: 576px) {
  .main-content {
    flex-direction: column;
  }
  
  .master-panel {
    width: 100%;
    height: 40%;
  }
  
  .detail-panel {
    height: 60%;
  }
}

/* Module Home Styles */
.module-home {
  background: white;
}

.module-header {
  background: #f8f9fa !important;
}

.module-avatar {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  font-size: 1.5rem;
}

.module-content {
  overflow-y: auto;
}

.stat-card {
  transition: all 0.2s ease;
}

.stat-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transform: translateY(-1px);
}

.stat-icon {
  font-size: 1.5rem;
}

.activity-item {
  transition: all 0.2s ease;
}

.activity-item:hover {
  background: #f8f9fa !important;
  transform: translateX(4px);
}

.cursor-pointer {
  cursor: pointer;
}

.help-item {
  border-left: 4px solid #667eea;
}
</style>
