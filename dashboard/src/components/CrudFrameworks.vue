<template>
  <div>
    <h3 v-if="selected">Edit Framework</h3>
    <h3 v-else>Create Framework</h3>
    <form @submit.prevent="onSubmit">
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input v-model="form.name" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Short Name</label>
        <input v-model="form.short_name" class="form-control" placeholder="e.g., NIST, CIS" />
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
            placeholder="#198754"
            pattern="^#[0-9A-Fa-f]{6}$"
            title="Enter hex color code (e.g., #198754)"
          />
        </div>
        <div class="form-text">Choose a color to identify this framework in the interface</div>
      </div>
      <button class="btn btn-primary" type="submit">{{ selected ? 'Update' : 'Create' }}</button>
      <button v-if="selected" class="btn btn-danger ms-2" @click.prevent="onDelete">Delete</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { createFramework, updateFramework, deleteFramework } from '../api';
const props = defineProps({ selected: Object });
const emit = defineEmits(['refresh']);
const form = ref({ name: '', short_name: '', description: '', color: '#198754' });
watch(() => props.selected, (val) => {
  if (val) form.value = { ...val };
  else form.value = { name: '', short_name: '', description: '', color: '#198754' };
}, { immediate: true });
const onSubmit = async () => {
  if (props.selected) await updateFramework(props.selected.id, form.value);
  else await createFramework(form.value);
  emit('refresh');
};
const onDelete = async () => {
  await deleteFramework(props.selected.id);
  emit('refresh');
};
</script>
