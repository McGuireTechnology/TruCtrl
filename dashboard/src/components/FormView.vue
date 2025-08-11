<template>
  <div class="form-view h-100">
    <!-- Action Buttons Bar -->
    <div class="action-bar p-3 border-bottom bg-light">
      <div class="d-flex align-items-center justify-content-between">
        <div class="d-flex align-items-center gap-2">
          <button class="btn btn-outline-secondary btn-sm" @click="$emit('cancel')">
            <i class="bi bi-arrow-left me-1"></i>
            {{ isCreate ? 'Back to List' : 'Cancel' }}
          </button>
        </div>
        <div class="d-flex align-items-center gap-2">
          <button class="btn btn-primary btn-sm" @click="handleSubmit" :disabled="loading || !isFormValid">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            {{ loading ? 'Saving...' : (isCreate ? 'Create' : 'Save Changes') }}
          </button>
          <button v-if="!isCreate" class="btn btn-outline-danger btn-sm" @click="$emit('delete')" :disabled="loading">
            <i class="bi bi-trash me-1"></i>
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Header with Avatar and Title -->
    <div class="item-header p-4 border-bottom">
      <div class="d-flex align-items-center">
        <!-- Avatar/Icon -->
        <div class="me-3">
          <div class="item-avatar bg-primary text-white d-flex align-items-center justify-content-center">
            <i :class="avatarIcon || 'bi bi-box'"></i>
          </div>
        </div>
        
        <!-- Item Name and Info -->
        <div class="flex-grow-1">
          <h3 class="mb-1">{{ headerTitle }}</h3>
          <div class="text-muted">{{ headerSubtitle }}</div>
          <div v-if="!isCreate && item" class="d-flex align-items-center gap-3 mt-2">
            <span v-if="item.created_at" class="badge bg-light text-dark">
              <i class="bi bi-calendar me-1"></i>
              Created {{ formatDate(item.created_at) }}
            </span>
            <span v-if="item.updated_at" class="badge bg-light text-dark">
              <i class="bi bi-clock me-1"></i>
              Updated {{ formatDate(item.updated_at) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Form Content -->
    <div class="form-content flex-grow-1 overflow-auto p-4">
      <form @submit.prevent="handleSubmit">
        <div class="row">
          <div v-for="field in fields" :key="field.key" :class="field.colClass || 'col-12'">
            <div class="mb-3">
              <label :for="field.key" class="form-label fw-bold">
                {{ field.label }}
                <span v-if="field.required" class="text-danger">*</span>
              </label>
              
              <!-- Text Input -->
              <input 
                v-if="field.type === 'text' || !field.type"
                :id="field.key"
                v-model="formData[field.key]"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': fieldErrors[field.key] }"
                :placeholder="field.placeholder"
                :required="field.required"
                :readonly="field.readonly"
              />
              
              <!-- Email Input -->
              <input 
                v-else-if="field.type === 'email'"
                :id="field.key"
                v-model="formData[field.key]"
                type="email"
                class="form-control"
                :class="{ 'is-invalid': fieldErrors[field.key] }"
                :placeholder="field.placeholder"
                :required="field.required"
                :readonly="field.readonly"
              />
              
              <!-- Textarea -->
              <textarea 
                v-else-if="field.type === 'textarea'"
                :id="field.key"
                v-model="formData[field.key]"
                class="form-control"
                :class="{ 'is-invalid': fieldErrors[field.key] }"
                :rows="field.rows || 3"
                :placeholder="field.placeholder"
                :required="field.required"
                :readonly="field.readonly"
              ></textarea>
              
              <!-- Select -->
              <select 
                v-else-if="field.type === 'select'"
                :id="field.key"
                v-model="formData[field.key]"
                class="form-select"
                :class="{ 'is-invalid': fieldErrors[field.key] }"
                :required="field.required"
                :disabled="field.readonly"
                @change="$emit('field-change', field.key, formData[field.key])"
              >
                <option value="">{{ field.placeholder || 'Select...' }}</option>
                <option v-for="option in field.options" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
              
              <!-- Checkbox -->
              <div v-else-if="field.type === 'checkbox'" class="form-check">
                <input 
                  :id="field.key"
                  v-model="formData[field.key]"
                  type="checkbox"
                  class="form-check-input"
                  :class="{ 'is-invalid': fieldErrors[field.key] }"
                  :disabled="field.readonly"
                />
                <label :for="field.key" class="form-check-label">
                  {{ field.checkboxLabel || field.label }}
                </label>
              </div>
              
              <!-- Number Input -->
              <input 
                v-else-if="field.type === 'number'"
                :id="field.key"
                v-model.number="formData[field.key]"
                type="number"
                class="form-control"
                :class="{ 'is-invalid': fieldErrors[field.key] }"
                :placeholder="field.placeholder"
                :required="field.required"
                :readonly="field.readonly"
                :min="field.min"
                :max="field.max"
                :step="field.step"
              />
              
              <!-- Color Input -->
              <div v-else-if="field.type === 'color'" class="d-flex align-items-center gap-2">
                <input 
                  :id="field.key + '_picker'"
                  v-model="formData[field.key]"
                  type="color"
                  class="form-control form-control-color"
                  style="width: 3rem; height: 38px;"
                  :disabled="field.readonly"
                  :title="'Choose color'"
                />
                <input 
                  :id="field.key"
                  v-model="formData[field.key]"
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': fieldErrors[field.key] }"
                  :placeholder="field.placeholder"
                  :required="field.required"
                  :readonly="field.readonly"
                  pattern="^#[0-9A-Fa-f]{6}$"
                  :title="'Enter hex color code (e.g., ' + field.placeholder + ')'"
                />
              </div>
              
              <!-- Date Input -->
              <input 
                v-else-if="field.type === 'date'"
                :id="field.key"
                v-model="formData[field.key]"
                type="date"
                class="form-control"
                :class="{ 'is-invalid': fieldErrors[field.key] }"
                :required="field.required"
                :readonly="field.readonly"
              />
              
              <!-- Help text -->
              <div v-if="field.help" class="form-text">{{ field.help }}</div>
              
              <!-- Error message -->
              <div v-if="fieldErrors[field.key]" class="invalid-feedback">
                {{ fieldErrors[field.key] }}
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  item: { type: Object, default: null },
  itemType: { type: String, required: true },
  itemTypeName: { type: String, required: true },
  avatarIcon: { type: String, default: 'bi bi-box' },
  fields: { type: Array, required: true },
  isCreate: { type: Boolean, default: false },
  createFunction: { type: Function, default: null },
  updateFunction: { type: Function, default: null }
});

const emit = defineEmits(['created', 'updated', 'cancel', 'delete', 'error', 'field-change']);

const formData = ref({});
const fieldErrors = ref({});
const loading = ref(false);

const headerTitle = computed(() => {
  if (props.isCreate) {
    return `New ${props.itemTypeName}`;
  }
  return `Edit ${props.itemTypeName}`;
});

const headerSubtitle = computed(() => {
  if (props.isCreate) {
    return `Create a new ${props.itemTypeName.toLowerCase()}`;
  }
  return `Modify ${props.itemTypeName.toLowerCase()} details`;
});

const isFormValid = computed(() => {
  // Check required fields
  const requiredFields = props.fields.filter(field => field.required && !field.readonly);
  return requiredFields.every(field => {
    const value = formData.value[field.key];
    return value !== undefined && value !== null && value !== '';
  });
});

// Initialize form data when item changes
watch(() => props.item, (newItem) => {
  if (newItem) {
    // Edit mode - populate with existing data
    formData.value = { ...newItem };
  } else {
    // Create mode - initialize empty form
    const emptyForm = {};
    props.fields.forEach(field => {
      if (field.type === 'checkbox') {
        emptyForm[field.key] = field.defaultValue || false;
      } else {
        emptyForm[field.key] = field.defaultValue || '';
      }
    });
    formData.value = emptyForm;
  }
  // Clear errors when item changes
  fieldErrors.value = {};
}, { immediate: true });

// Watch for field changes to update form data for new fields without losing existing data
watch(() => props.fields, (newFields) => {
  // Add any new fields that don't exist in formData yet
  newFields.forEach(field => {
    if (!(field.key in formData.value)) {
      if (field.type === 'checkbox') {
        formData.value[field.key] = field.defaultValue || false;
      } else {
        formData.value[field.key] = field.defaultValue || '';
      }
    }
  });
}, { immediate: true });

const validateForm = () => {
  fieldErrors.value = {};
  let isValid = true;

  props.fields.forEach(field => {
    if (field.required && !field.readonly) {
      const value = formData.value[field.key];
      if (value === undefined || value === null || value === '') {
        fieldErrors.value[field.key] = `${field.label} is required`;
        isValid = false;
      }
    }

    // Email validation
    if (field.type === 'email' && formData.value[field.key]) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formData.value[field.key])) {
        fieldErrors.value[field.key] = 'Please enter a valid email address';
        isValid = false;
      }
    }
  });

  return isValid;
};

const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }

  loading.value = true;

  try {
    if (props.isCreate) {
      // Create new item
      if (!props.createFunction) {
        throw new Error('Create function not provided');
      }
      
      const newItem = await props.createFunction(formData.value);
      emit('created', newItem);
    } else {
      // Update existing item
      if (!props.updateFunction || !props.item) {
        throw new Error('Update function or item not provided');
      }
      
      // Create update object with only changed fields
      const updates = {};
      props.fields.forEach(field => {
        if (formData.value[field.key] !== props.item[field.key]) {
          updates[field.key] = formData.value[field.key];
        }
      });
      
      if (Object.keys(updates).length === 0) {
        emit('cancel');
        return;
      }
      
      const updatedItem = await props.updateFunction(props.item.id, updates);
      emit('updated', updatedItem);
    }
  } catch (error) {
    console.error('Form submission error:', error);
    emit('error', error.message || 'Failed to save changes');
  } finally {
    loading.value = false;
  }
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

// Expose formData to parent component
defineExpose({
  formData
});
</script>

<style scoped>
.form-view {
  display: flex;
  flex-direction: column;
  background: #fff;
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

.form-content {
  background-color: #fff;
}

.form-label {
  color: #495057;
  margin-bottom: 0.5rem;
}

.form-control:focus,
.form-select:focus,
.form-check-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  display: block;
  font-size: 0.875rem;
  color: #dc3545;
  margin-top: 0.25rem;
}

.badge {
  font-size: 0.75rem;
}
</style>
