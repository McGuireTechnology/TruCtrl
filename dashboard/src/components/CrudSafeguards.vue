<template>
  <div>
    <h3 v-if="selected">Edit Safeguard</h3>
    <h3 v-else>Create Safeguard</h3>
    <form @submit.prevent="onSubmit">
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input v-model="form.name" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Description</label>
        <textarea v-model="form.description" class="form-control" />
      </div>
      <button class="btn btn-primary" type="submit">{{ selected ? 'Update' : 'Create' }}</button>
      <button v-if="selected" class="btn btn-danger ms-2" @click.prevent="onDelete">Delete</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { createSafeguard, updateSafeguard, deleteSafeguard } from '../api';
const props = defineProps({ selected: Object });
const emit = defineEmits(['refresh']);
const form = ref({ name: '', description: '' });
watch(() => props.selected, (val) => {
  if (val) form.value = { ...val };
  else form.value = { name: '', description: '' };
}, { immediate: true });
const onSubmit = async () => {
  if (props.selected) await updateSafeguard(props.selected.id, form.value);
  else await createSafeguard(form.value);
  emit('refresh');
};
const onDelete = async () => {
  await deleteSafeguard(props.selected.id);
  emit('refresh');
};
</script>
