<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h1 class="register-title">Create Account</h1>
        <p class="register-subtitle">Join TruCtrl Security Control Management</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="name" class="form-label">Full Name</label>
          <input 
            id="name"
            v-model="name" 
            type="text" 
            class="form-control"
            :class="{ 'is-invalid': nameError }"
            placeholder="Enter your full name"
            required 
          />
          <div v-if="nameError" class="invalid-feedback">{{ nameError }}</div>
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Email Address</label>
          <input 
            id="email"
            v-model="email" 
            type="email" 
            class="form-control"
            :class="{ 'is-invalid': emailError }"
            placeholder="Enter your email"
            required 
          />
          <div v-if="emailError" class="invalid-feedback">{{ emailError }}</div>
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            class="form-control"
            :class="{ 'is-invalid': passwordError }"
            placeholder="Enter your password"
            required 
          />
          <div v-if="passwordError" class="invalid-feedback">{{ passwordError }}</div>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword" class="form-label">Confirm Password</label>
          <input 
            id="confirmPassword"
            v-model="confirmPassword" 
            type="password" 
            class="form-control"
            :class="{ 'is-invalid': confirmPasswordError }"
            placeholder="Confirm your password"
            required 
          />
          <div v-if="confirmPasswordError" class="invalid-feedback">{{ confirmPasswordError }}</div>
        </div>
        
        <button 
          type="submit" 
          class="btn btn-primary btn-register"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
          {{ isLoading ? 'Creating Account...' : 'Create Account' }}
        </button>
        
        <div v-if="error" class="alert alert-danger mt-3" role="alert">
          {{ error }}
        </div>

        <div v-if="success" class="alert alert-success mt-3" role="alert">
          Account created successfully! Please contact an administrator to activate your account.
        </div>
      </form>
      
      <div class="register-footer">
        <p class="mb-0">
          Already have an account? 
          <router-link to="/login" class="text-decoration-none">Sign in here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuth } from '../stores/auth';

const { register } = useAuth();

const name = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const error = ref('');
const success = ref(false);
const nameError = ref('');
const emailError = ref('');
const passwordError = ref('');
const confirmPasswordError = ref('');
const isLoading = ref(false);

const validateForm = () => {
  nameError.value = '';
  emailError.value = '';
  passwordError.value = '';
  confirmPasswordError.value = '';
  
  let isValid = true;
  
  if (!name.value.trim()) {
    nameError.value = 'Name is required';
    isValid = false;
  }
  
  if (!email.value) {
    emailError.value = 'Email is required';
    isValid = false;
  } else if (!email.value.includes('@')) {
    emailError.value = 'Please enter a valid email';
    isValid = false;
  }
  
  if (!password.value) {
    passwordError.value = 'Password is required';
    isValid = false;
  } else if (password.value.length < 8) {
    passwordError.value = 'Password must be at least 8 characters';
    isValid = false;
  }
  
  if (!confirmPassword.value) {
    confirmPasswordError.value = 'Please confirm your password';
    isValid = false;
  } else if (password.value !== confirmPassword.value) {
    confirmPasswordError.value = 'Passwords do not match';
    isValid = false;
  }
  
  return isValid;
};

const handleRegister = async () => {
  if (!validateForm()) return;
  
  isLoading.value = true;
  error.value = '';
  success.value = false;
  
  try {
    const result = await register({
      name: name.value.trim(),
      email: email.value,
      password: password.value,
      is_active: false // Require admin activation
    });
    
    if (result.success) {
      success.value = true;
      // Reset form
      name.value = '';
      email.value = '';
      password.value = '';
      confirmPassword.value = '';
    } else {
      error.value = result.error || 'Registration failed';
    }
  } catch (e) {
    error.value = 'An unexpected error occurred';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 450px;
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.register-subtitle {
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 0;
}

.register-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.form-control {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.btn-register {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: transform 0.2s ease-in-out;
}

.btn-register:hover {
  transform: translateY(-2px);
}

.btn-register:disabled {
  transform: none;
  opacity: 0.7;
}

.register-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.alert {
  border-radius: 8px;
  border: none;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>
