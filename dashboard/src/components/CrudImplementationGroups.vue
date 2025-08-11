<template>
  <div>
    <h3 v-if="selected">Edit Implementation Group</h3>
    <h3 v-else>Create Implementation Group</h3>
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
            placeholder="#ffc107"
            pattern="^#[0-9A-Fa-f]{6}$"
            title="Enter hex color code (e.g., #ffc107)"
          />
        </div>
        <div class="form-text">Choose a color to identify this implementation group in the interface</div>
      </div>
      <button class="btn btn-primary" type="submit">{{ selected ? 'Update' : 'Create' }}</button>
      <button v-if="selected" class="btn btn-danger ms-2" @click.prevent="onDelete">Delete</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { createImplementationGroup, updateImplementationGroup, deleteImplementationGroup } from '../api';
const props = defineProps({ selected: Object });
const emit = defineEmits(['refresh']);
const form = ref({ name: '', description: '', color: '#ffc107' });
watch(() => props.selected, (val) => {
  if (val) form.value = { ...val };
  else form.value = { name: '', description: '', color: '#ffc107' };
}, { immediate: true });
const onSubmit = async () => {
  if (props.selected) await updateImplementationGroup(props.selected.id, form.value);
  else await createImplementationGroup(form.value);
  emit('refresh');
};
const onDelete = async () => {
  await deleteImplementationGroup(props.selected.id);
  emit('refresh');
};
</script>
