<template>
  <div>
    <h3 v-if="selected">Edit User</h3>
    <h3 v-else>Create User</h3>
    <form @submit.prevent="onSubmit">
      <div class="mb-3">
        <label class="form-label">Username</label>
        <input v-model="form.username" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input v-model="form.email" class="form-control" type="email" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Role</label>
        <input v-model="form.role" class="form-control" />
      </div>
      <button class="btn btn-primary" type="submit">{{ selected ? 'Update' : 'Create' }}</button>
      <button v-if="selected" class="btn btn-danger ms-2" @click.prevent="onDelete">Delete</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { createUser, updateUser, deleteUser } from '../api';
const props = defineProps({ selected: Object });
const emit = defineEmits(['refresh']);
const form = ref({ username: '', email: '', role: '' });
watch(() => props.selected, (val) => {
  if (val) form.value = { ...val };
  else form.value = { username: '', email: '', role: '' };
}, { immediate: true });
const onSubmit = async () => {
  if (props.selected) await updateUser(props.selected.id, form.value);
  else await createUser(form.value);
  emit('refresh');
};
const onDelete = async () => {
  await deleteUser(props.selected.id);
  emit('refresh');
};
</script>
