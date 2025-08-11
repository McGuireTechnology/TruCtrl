<template>
  <!-- Edit Modal -->
  <div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true" ref="modal">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="editModalLabel">
            Edit {{ itemTypeName }}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="row">
              <div v-for="field in editableFields" :key="field.key" :class="field.colClass || 'col-12'">
                <div class="mb-3">
                  <label :for="field.key" class="form-label">{{ field.label }}</label>
                  
                  <!-- Text Input -->
                  <input 
                    v-if="field.type === 'text' || !field.type"
                    :id="field.key"
                    v-model="formData[field.key]"
                    type="text"
                    class="form-control"
                    :placeholder="field.placeholder"
                    :required="field.required"
                  />
                  
                  <!-- Email Input -->
                  <input 
                    v-else-if="field.type === 'email'"
                    :id="field.key"
                    v-model="formData[field.key]"
                    type="email"
                    class="form-control"
                    :placeholder="field.placeholder"
                    :required="field.required"
                  />
                  
                  <!-- Textarea -->
                  <textarea 
                    v-else-if="field.type === 'textarea'"
                    :id="field.key"
                    v-model="formData[field.key]"
                    class="form-control"
                    :rows="field.rows || 3"
                    :placeholder="field.placeholder"
                    :required="field.required"
                  ></textarea>
                  
                  <!-- Select -->
                  <select 
                    v-else-if="field.type === 'select'"
                    :id="field.key"
                    v-model="formData[field.key]"
                    class="form-select"
                    :required="field.required"
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
                    :placeholder="field.placeholder"
                    :required="field.required"
                    :min="field.min"
                    :max="field.max"
                    :step="field.step"
                  />
                  
                  <!-- Date Input -->
                  <input 
                    v-else-if="field.type === 'date'"
                    :id="field.key"
                    v-model="formData[field.key]"
                    type="date"
                    class="form-control"
                    :required="field.required"
                  />
                  
                  <div v-if="field.help" class="form-text">{{ field.help }}</div>
                </div>
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary" @click="handleSubmit" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            {{ loading ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';

const props = defineProps({
  item: { type: Object, default: null },
  itemType: { type: String, required: true },
  itemTypeName: { type: String, required: true },
  fields: { type: Array, required: true },
  updateFunction: { type: Function, required: true }
});

const emit = defineEmits(['updated', 'error']);

const modal = ref(null);
const formData = ref({});
const loading = ref(false);

const editableFields = props.fields.filter(field => !field.readonly);

// Initialize form data when item changes
watch(() => props.item, (newItem) => {
  if (newItem) {
    formData.value = { ...newItem };
  }
}, { immediate: true });

const show = () => {
  if (modal.value) {
    const bootstrapModal = new window.bootstrap.Modal(modal.value);
    bootstrapModal.show();
  }
};

const hide = () => {
  if (modal.value) {
    const bootstrapModal = window.bootstrap.Modal.getInstance(modal.value);
    if (bootstrapModal) {
      bootstrapModal.hide();
    }
  }
};

const handleSubmit = async () => {
  if (!props.item || !props.updateFunction) return;
  
  loading.value = true;
  
  try {
    // Create update object with only changed fields
    const updates = {};
    editableFields.forEach(field => {
      if (formData.value[field.key] !== props.item[field.key]) {
        updates[field.key] = formData.value[field.key];
      }
    });
    
    if (Object.keys(updates).length === 0) {
      hide();
      return;
    }
    
    await props.updateFunction(props.item.id, updates);
    emit('updated', { ...props.item, ...updates });
    hide();
  } catch (error) {
    console.error('Error updating item:', error);
    emit('error', error.message || 'Failed to update item');
  } finally {
    loading.value = false;
  }
};

// Expose methods to parent
defineExpose({
  show,
  hide
});
</script>

<style scoped>
.modal-header {
  background-color: #f8f9fa;
}

.form-label {
  font-weight: 600;
  color: #495057;
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
</style>
