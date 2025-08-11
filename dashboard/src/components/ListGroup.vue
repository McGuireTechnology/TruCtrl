<template>
  <div class="list-pane">
    <!-- Header with search and add button -->
    <div class="list-header p-3 border-bottom">
      <div class="d-flex align-items-center mb-3">
        <div class="search-container flex-grow-1 me-3">
          <div class="input-group">
            <span class="input-group-text bg-light border-end-0">
              <i class="bi bi-search text-muted"></i>
            </span>
            <input 
              type="text" 
              class="form-control border-start-0 bg-light" 
              placeholder="Search"
              v-model="searchQuery"
              @input="$emit('search', searchQuery)"
            >
          </div>
        </div>
        <button class="btn btn-outline-secondary" @click="$emit('add')">
          <i class="bi bi-plus-circle me-1"></i>
          Add
        </button>
      </div>
      
      <!-- Title and controls -->
      <div class="d-flex align-items-center justify-content-between">
        <h5 class="mb-0">{{ title }}</h5>
        <div class="d-flex align-items-center gap-2">
          <button 
            class="btn btn-sm"
            :class="isMultiSelect ? 'btn-primary' : 'btn-outline-secondary'"
            @click="$emit('toggle-multi-select')"
            :title="isMultiSelect ? 'Exit Multi-select' : 'Enable Multi-select'"
          >
            <i class="bi bi-check-square me-1"></i>
            {{ isMultiSelect ? 'Exit' : 'Select' }}
          </button>
          <button class="btn btn-sm btn-outline-secondary" @click="$emit('filter')">
            <i class="bi bi-funnel me-1"></i>
            Filter
          </button>
          <button class="btn btn-sm btn-outline-secondary" @click="$emit('sort')">
            Sort
            <i class="bi bi-arrow-down-up ms-1"></i>
          </button>
        </div>
      </div>
      
      <!-- Multi-select summary -->
      <div v-if="isMultiSelect" class="mt-2 d-flex align-items-center justify-content-between">
        <small class="text-muted">
          {{ selectedItems.length }} of {{ items.length }} selected
        </small>
        <div class="d-flex gap-2">
          <button 
            v-if="selectedItems.length > 0" 
            class="btn btn-sm btn-outline-danger"
            @click="handleBulkDelete"
          >
            <i class="bi bi-trash me-1"></i>
            Delete Selected
          </button>
        </div>
      </div>
    </div>

    <!-- List items -->
    <div class="list-group list-group-flush scrollarea">
      <!-- All items summary item -->
      <a href="#" 
         class="list-group-item list-group-item-action py-3 px-3 border-0 border-bottom bg-light"
         @click.prevent="$emit('select-all')"
         v-if="isMultiSelect || items.length > 0">
        <div class="d-flex align-items-center">
          <!-- Checkbox for select all -->
          <div v-if="isMultiSelect" class="me-3">
            <input 
              type="checkbox" 
              class="form-check-input"
              :checked="selectedItems.length === items.length && items.length > 0"
              :indeterminate="selectedItems.length > 0 && selectedItems.length < items.length"
              @change="$emit('select-all')"
            >
          </div>
          
          <!-- Avatar -->
          <div class="me-3">
            <div class="avatar-circle bg-primary text-white d-flex align-items-center justify-content-center">
              <i :class="avatarIcon"></i>
            </div>
          </div>
          
          <!-- Summary info -->
          <div class="flex-grow-1">
            <div class="d-flex align-items-center justify-content-between mb-1">
              <h6 class="mb-0 fw-bold">All {{ title }}</h6>
              <small class="text-muted">{{ items.length }} {{ items.length === 1 ? 'item' : 'items' }}</small>
            </div>
            <div class="text-muted small">
              {{ isMultiSelect ? 'Click to select/deselect all items' : `Manage all ${title.toLowerCase()}` }}
            </div>
          </div>
        </div>
      </a>
      
      <!-- Individual items -->
      <a v-for="item in filteredItems" :key="item.id" href="#"
         class="list-group-item list-group-item-action py-3 px-3 border-0 border-bottom"
         :class="{
           active: !isMultiSelect && item.id === selectedId,
           'bg-light': isMultiSelect && isItemSelected(item)
         }"
         @click.prevent="handleItemClick(item, $event)">
        <div class="d-flex align-items-center">
          <!-- Checkbox for multiselect -->
          <div v-if="isMultiSelect" class="me-3">
            <input 
              type="checkbox" 
              class="form-check-input"
              :checked="isItemSelected(item)"
              @change="$emit('multi-select', item)"
              @click.stop
            >
          </div>
          
          <!-- Avatar -->
          <div class="me-3">
            <div class="avatar-circle text-white d-flex align-items-center justify-content-center"
                 :style="{ backgroundColor: getItemColor(item) }">
              <i :class="avatarIcon"></i>
            </div>
          </div>
          
          <!-- Item info -->
          <div class="flex-grow-1">
            <div class="d-flex align-items-center justify-content-between mb-1">
              <h6 class="mb-0">{{ itemHeading(item) }}</h6>
              <small class="text-muted">{{ itemBadge(item) }}</small>
            </div>
            <div class="text-muted small">{{ itemSub(item) }}</div>
            <div class="text-muted small">{{ itemDesc(item) }}</div>
            <!-- Pills for related objects -->
            <div class="mt-2 d-flex flex-wrap gap-1" v-if="showPills(item)">
              <!-- Locked pill for configuration item types -->
              <span v-if="item.locked && itemType === 'configuration-item-types'" 
                    class="badge rounded-pill pill-sm bg-danger text-white">
                <i class="bi bi-lock-fill me-1"></i>
                Locked
              </span>
              <span v-if="item.function_short_name || item.function_name" 
                    class="badge rounded-pill text-white pill-sm"
                    :style="{ backgroundColor: item.function_color || '#0d6efd' }">
                <i class="bi bi-gear me-1"></i>
                {{ item.function_short_name || getShortName(item.function_name) }}
              </span>
              <span v-if="(item.framework_short_name || item.framework_name) && itemType !== 'safeguards'" 
                    class="badge rounded-pill text-white pill-sm"
                    :style="{ backgroundColor: item.framework_color || '#198754' }">
                <i class="bi bi-diagram-3 me-1"></i>
                {{ item.framework_short_name || getShortName(item.framework_name) }}
              </span>
              <span v-if="item.implementation_group_short_name || item.implementation_group_name" 
                    class="badge rounded-pill pill-sm"
                    :style="{ 
                      backgroundColor: item.implementation_group_color || '#ffc107',
                      color: isLightColor(item.implementation_group_color || '#ffc107') ? '#000' : '#fff'
                    }">
                <i class="bi bi-collection me-1"></i>
                {{ item.implementation_group_short_name || getShortName(item.implementation_group_name) }}
              </span>
              <span v-if="item.control_short_name || item.control_name" 
                    class="badge rounded-pill text-white pill-sm"
                    :style="{ backgroundColor: item.control_color || '#6c757d' }">
                <i class="bi bi-shield-check me-1"></i>
                {{ item.control_short_name || getShortName(item.control_name) }}
              </span>
              <span v-if="item.asset_class_short_name || item.asset_class_name" 
                    class="badge rounded-pill text-white pill-sm"
                    :style="{ backgroundColor: item.asset_class_color || '#17a2b8' }">
                <i class="bi bi-box me-1"></i>
                {{ item.asset_class_short_name || getShortName(item.asset_class_name) }}
              </span>
            </div>
          </div>
        </div>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  items: { type: Array, required: true },
  selectedId: { type: [String, Number], default: null },
  selectedItems: { type: Array, default: () => [] },
  isMultiSelect: { type: Boolean, default: false },
  title: { type: String, default: 'List' },
  itemType: { type: String, default: '' },
  itemHeading: { type: Function, default: item => item.name },
  itemSub: { type: Function, default: () => '' },
  itemDesc: { type: Function, default: () => '' },
  itemBadge: { type: Function, default: () => '' },
  avatarIcon: { type: String, default: 'bi bi-person' },
});

const emit = defineEmits(['select', 'multi-select', 'range-select', 'toggle-multi-select', 'select-all', 'bulk-delete', 'search', 'add', 'filter', 'sort']);

const searchQuery = ref('');

const filteredItems = computed(() => {
  if (!searchQuery.value) return props.items;
  
  return props.items.filter(item => {
    const heading = props.itemHeading(item).toLowerCase();
    const sub = props.itemSub(item).toLowerCase();
    const desc = props.itemDesc(item).toLowerCase();
    const query = searchQuery.value.toLowerCase();
    
    return heading.includes(query) || sub.includes(query) || desc.includes(query);
  });
});

const isItemSelected = (item) => {
  return props.selectedItems.some(selectedItem => selectedItem.id === item.id);
};

const handleItemClick = (item, event) => {
  // Check for keyboard modifiers
  const isCtrlOrCmd = event.ctrlKey || event.metaKey; // Ctrl on Windows/Linux, Cmd on Mac
  const isShift = event.shiftKey;
  
  if (isCtrlOrCmd || isShift) {
    // Force multiselect mode when using keyboard modifiers
    if (!props.isMultiSelect) {
      emit('toggle-multi-select');
    }
    
    if (isShift) {
      // Handle range selection
      emit('range-select', item);
    } else if (isCtrlOrCmd) {
      // Handle individual multi-selection
      emit('multi-select', item);
    }
  } else {
    // Normal click behavior
    if (props.isMultiSelect) {
      emit('multi-select', item);
    } else {
      emit('select', item);
    }
  }
};

const handleBulkDelete = () => {
  if (props.selectedItems.length > 0) {
    const itemType = props.title.slice(0, -1).toLowerCase();
    if (confirm(`Are you sure you want to delete ${props.selectedItems.length} ${itemType}${props.selectedItems.length === 1 ? '' : 's'}?`)) {
      emit('bulk-delete', props.selectedItems);
    }
  }
};

const showPills = (item) => {
  // Show pills for items that have related object data or are locked asset classes
  return item.function_name || item.function_short_name || 
         item.framework_name || item.framework_short_name || 
         item.implementation_group_name || item.implementation_group_short_name || 
         item.control_name || item.control_short_name ||
         item.asset_class_name || item.asset_class_short_name ||
         (item.locked && props.itemType === 'configuration-item-types');
};

const getShortName = (name) => {
  // Extract short name from full name, or return first few words
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
    return name.length > 15 ? name.substring(0, 12) + '...' : name;
  }
  
  // Take first 2 words if reasonable length
  const firstTwo = words.slice(0, 2).join(' ');
  return firstTwo.length > 15 ? words[0] : firstTwo;
};

const getItemColor = (item) => {
  // Return the item's color if it has one, otherwise use a default
  return item.color || '#6c757d';
};

const isLightColor = (hexColor) => {
  // Convert hex to RGB and calculate brightness
  const hex = hexColor.replace('#', '');
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  
  // Calculate brightness using standard formula
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 155; // Threshold for light colors
};
</script>

<style scoped>
.list-pane {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.scrollarea {
  flex: 1;
  overflow-y: auto;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 0.9rem;
}

kbd {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 3px;
  padding: 2px 4px;
  font-size: 0.75rem;
  color: #495057;
  font-family: monospace;
}

/* Pill styles */
.pill-sm {
  font-size: 0.65rem;
  font-weight: 500;
  padding: 0.2em 0.5em;
  border: 1px solid transparent;
}

.pill-sm i {
  font-size: 0.6rem;
}

/* Pill color schemes */
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