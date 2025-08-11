<template>
  <div>
    <h3 v-if="selected">Edit Control</h3>
    <h3 v-else>Create Control</h3>
    <form @submit.prevent="onSubmit">
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input v-model="form.name" class="form-control" required />
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
            placeholder="#6c757d"
            pattern="^#[0-9A-Fa-f]{6}$"
            title="Enter hex color code (e.g., #6c757d)"
          />
        </div>
        <div class="form-text">Choose a color to identify this control in the interface</div>
      </div>
      <button class="btn btn-primary" type="submit">{{ selected ? 'Update' : 'Create' }}</button>
      <button v-if="selected" class="btn btn-danger ms-2" @click.prevent="onDelete">Delete</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { createControl, updateControl, deleteControl } from '../api';
const props = defineProps({ selected: Object });
const emit = defineEmits(['refresh']);
const form = ref({ name: '', description: '', color: '#6c757d' });
watch(() => props.selected, (val) => {
  if (val) form.value = { ...val };
  else form.value = { name: '', description: '', color: '#6c757d' };
}, { immediate: true });
const onSubmit = async () => {
  if (props.selected) await updateControl(props.selected.id, form.value);
  else await createControl(form.value);
  emit('refresh');
};
const onDelete = async () => {
  await deleteControl(props.selected.id);
  emit('refresh');
};
</script>
