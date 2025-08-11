<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">TruCtrl</h1>
        <p class="login-subtitle">A Security Control Management Platform</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
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
        
        <button 
          type="submit" 
          class="btn btn-primary btn-login"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
          {{ isLoading ? 'Signing in...' : 'Sign In' }}
        </button>
        
        <div v-if="error" class="alert alert-danger mt-3" role="alert">
          {{ error }}
        </div>
      </form>
      
      <div class="login-footer">
        <p class="mb-2">
          <a href="#" class="text-decoration-none">Forgot your password?</a>
        </p>
        <p class="mb-0">
          Don't have an account? 
          <router-link to="/register" class="text-decoration-none">Sign up here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../stores/auth';

const router = useRouter();
const { login } = useAuth();

const email = ref('');
const password = ref('');
const error = ref('');
const emailError = ref('');
const passwordError = ref('');
const isLoading = ref(false);

const validateForm = () => {
  emailError.value = '';
  passwordError.value = '';
  
  if (!email.value) {
    emailError.value = 'Email is required';
    return false;
  }
  
  if (!email.value.includes('@')) {
    emailError.value = 'Please enter a valid email';
    return false;
  }
  
  if (!password.value) {
    passwordError.value = 'Password is required';
    return false;
  }
  
  if (password.value.length < 6) {
    passwordError.value = 'Password must be at least 6 characters';
    return false;
  }
  
  return true;
};

const handleLogin = async () => {
  if (!validateForm()) return;
  
  isLoading.value = true;
  error.value = '';
  
  try {
    const result = await login(email.value, password.value);
    
    if (result.success) {
      // Redirect to dashboard
      router.push('/');
    } else {
      error.value = result.error || 'Login failed';
    }
  } catch (e) {
    error.value = 'An unexpected error occurred';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 0;
}

.login-form {
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

.btn-login {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: transform 0.2s ease-in-out;
}

.btn-login:hover {
  transform: translateY(-2px);
}

.btn-login:disabled {
  transform: none;
  opacity: 0.7;
}

.login-footer {
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
