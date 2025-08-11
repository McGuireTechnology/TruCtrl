// src/api.js
// Simple API service for FastAPI backend
import { useAuth } from './stores/auth.js';

const API_BASE = 'http://localhost:8000';

async function request(path, options = {}) {
  const token = localStorage.getItem('auth-token');
  const headers = { 
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };
  
  // Add Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const res = await fetch(`${API_BASE}${path}`, {
    headers,
    credentials: 'include',
    ...options,
  });
  
  // Handle 401 Unauthorized - try to refresh token first
  if (res.status === 401) {
    const auth = useAuth();
    const refreshToken = localStorage.getItem('refresh-token');
    
    // If we have a refresh token, try to refresh the access token
    if (refreshToken && !options._isRetry) {
      try {
        const refreshed = await auth.refreshAccessToken();
        if (refreshed) {
          // Retry the original request with new token
          const newToken = localStorage.getItem('auth-token');
          const retryHeaders = {
            ...headers,
            'Authorization': `Bearer ${newToken}`
          };
          
          return request(path, {
            ...options,
            headers: retryHeaders,
            _isRetry: true // Prevent infinite retry loop
          });
        }
      } catch (error) {
        console.error('Token refresh failed:', error);
      }
    }
    
    // If refresh failed or no refresh token, clear auth and redirect
    localStorage.removeItem('auth-token');
    localStorage.removeItem('refresh-token');
    localStorage.removeItem('token-expires-at');
    localStorage.removeItem('refresh-expires-at');
    
    // Redirect to login page
    window.location.href = '/login';
    throw new Error('Unauthorized - redirecting to login');
  }
  
  if (!res.ok) throw new Error(await res.text());
  
  // Handle 204 No Content responses
  if (res.status === 204) {
    return null;
  }
  
  return res.json();
}

// --- User Endpoints ---
export function getUsers() {
  return request('/users/');
}
export function getUser(id) {
  return request(`/users/${id}`);
}
export function createUser(data) {
  return request('/users/', { method: 'POST', body: JSON.stringify(data) });
}
export function updateUser(id, data) {
  return request(`/users/${id}`, { method: 'PATCH', body: JSON.stringify(data) });
}
export function deleteUser(id) {
  return request(`/users/${id}`, { method: 'DELETE' });
}

// --- Controls Endpoints ---
export function getControls() {
  return request('/controls/');
}
export function getControl(id) {
  return request(`/controls/${id}`);
}
export function createControl(data) {
  return request('/controls/', { method: 'POST', body: JSON.stringify(data) });
}
export function updateControl(id, data) {
  return request(`/controls/${id}`, { method: 'PATCH', body: JSON.stringify(data) });
}
export function deleteControl(id) {
  return request(`/controls/${id}`, { method: 'DELETE' });
}

// --- Frameworks Endpoints ---
export function getFrameworks() {
  return request('/controls/frameworks/');
}
export function getFramework(id) {
  return request(`/controls/frameworks/${id}`);
}
export function createFramework(data) {
  return request('/controls/frameworks/', { method: 'POST', body: JSON.stringify(data) });
}
export function updateFramework(id, data) {
  return request(`/controls/frameworks/${id}`, { method: 'PATCH', body: JSON.stringify(data) });
}
export function deleteFramework(id) {
  return request(`/controls/frameworks/${id}`, { method: 'DELETE' });
}

// --- Implementation Groups Endpoints ---
export function getImplementationGroups() {
  return request('/controls/implementation-groups/');
}
export function getImplementationGroup(id) {
  return request(`/controls/implementation-groups/${id}`);
}
export function createImplementationGroup(data) {
  return request('/controls/implementation-groups/', { method: 'POST', body: JSON.stringify(data) });
}
export function updateImplementationGroup(id, data) {
  return request(`/controls/implementation-groups/${id}`, { method: 'PATCH', body: JSON.stringify(data) });
}
export function deleteImplementationGroup(id) {
  return request(`/controls/implementation-groups/${id}`, { method: 'DELETE' });
}

// --- Functions Endpoints ---
export function getFunctions() {
  return request('/controls/functions/');
}
export function getFunction(id) {
  return request(`/controls/functions/${id}`);
}
export function createFunction(data) {
  return request('/controls/functions/', { method: 'POST', body: JSON.stringify(data) });
}
export function updateFunction(id, data) {
  return request(`/controls/functions/${id}`, { method: 'PATCH', body: JSON.stringify(data) });
}
export function deleteFunction(id) {
  return request(`/controls/functions/${id}`, { method: 'DELETE' });
}

// --- Safeguards Endpoints ---
export function getSafeguards() {
  return request('/controls/safeguards/');
}
export function getSafeguard(id) {
  return request(`/controls/safeguards/${id}`);
}
export function createSafeguard(data) {
  return request('/controls/safeguards/', { method: 'POST', body: JSON.stringify(data) });
}
export function updateSafeguard(id, data) {
  return request(`/controls/safeguards/${id}`, { method: 'PATCH', body: JSON.stringify(data) });
}
export function deleteSafeguard(id) {
  return request(`/controls/safeguards/${id}`, { method: 'DELETE' });
}

// --- Safeguard Relationships Endpoints ---
export function getSafeguardRelationships(safeguardId) {
  return request(`/controls/safeguards/${safeguardId}/relationships`);
}
export function createSafeguardRelationship(safeguardId, data) {
  return request(`/controls/safeguards/${safeguardId}/relationships`, { 
    method: 'POST', 
    body: JSON.stringify(data) 
  });
}
export function updateSafeguardRelationship(relationshipId, data) {
  return request(`/controls/safeguards/relationships/${relationshipId}`, { 
    method: 'PATCH', 
    body: JSON.stringify(data) 
  });
}
export function deleteSafeguardRelationship(relationshipId) {
  return request(`/controls/safeguards/relationships/${relationshipId}`, { 
    method: 'DELETE' 
  });
}

// --- Configuration Item Types Endpoints (formerly Asset Classes) ---
export function getConfigurationItemTypes() {
  return request('/cmdb/configuration-item-types/');
}
export function getConfigurationItemType(id) {
  return request(`/cmdb/configuration-item-types/${id}`);
}
export function createConfigurationItemType(data) {
  return request('/cmdb/configuration-item-types/', { method: 'POST', body: JSON.stringify(data) });
}
export function updateConfigurationItemType(id, data) {
  return request(`/cmdb/configuration-item-types/${id}`, { method: 'PATCH', body: JSON.stringify(data) });
}
export function deleteConfigurationItemType(id) {
  return request(`/cmdb/configuration-item-types/${id}`, { method: 'DELETE' });
}

// Configuration Item Type Relationship endpoints
export function getConfigurationItemTypeParents(id) {
  return request(`/cmdb/configuration-item-types/${id}/parents`);
}
export function getConfigurationItemTypeChildren(id) {
  return request(`/cmdb/configuration-item-types/${id}/children`);
}
export function addConfigurationItemTypeParent(childId, parentId) {
  return request(`/cmdb/configuration-item-types/${childId}/parents/${parentId}`, { method: 'POST' });
}
export function removeConfigurationItemTypeParent(childId, parentId) {
  return request(`/cmdb/configuration-item-types/${childId}/parents/${parentId}`, { method: 'DELETE' });
}

// Legacy aliases for backward compatibility
export const getAssetClasses = getConfigurationItemTypes;
export const getAssetClass = getConfigurationItemType;
export const createAssetClass = createConfigurationItemType;
export const updateAssetClass = updateConfigurationItemType;
export const deleteAssetClass = deleteConfigurationItemType;
export const getAssetClassParents = getConfigurationItemTypeParents;
export const getAssetClassChildren = getConfigurationItemTypeChildren;
export const addAssetClassParent = addConfigurationItemTypeParent;
export const removeAssetClassParent = removeConfigurationItemTypeParent;
