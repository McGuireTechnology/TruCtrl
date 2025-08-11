import { ref, computed } from 'vue';

// Simple reactive store for authentication
const user = ref(null);
const token = ref(localStorage.getItem('auth-token') || null);
const refreshToken = ref(localStorage.getItem('refresh-token') || null);
const tokenExpiresAt = ref(localStorage.getItem('token-expires-at') || null);
const refreshExpiresAt = ref(localStorage.getItem('refresh-expires-at') || null);
const refreshTimer = ref(null);
const warningTimer = ref(null);
const currentTime = ref(Date.now());

// Update current time every second for real-time countdown
setInterval(() => {
  currentTime.value = Date.now();
}, 1000);

// Helper function to decode JWT and get expiration
const decodeTokenExpiry = (token) => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.exp * 1000; // Convert to milliseconds
  } catch (error) {
    return null;
  }
};

// Helper function to set up refresh timer
const setupRefreshTimer = () => {
  clearTimeout(refreshTimer.value);
  clearTimeout(warningTimer.value);
  
  if (!tokenExpiresAt.value) return;
  
  const now = currentTime.value;
  const accessExpiryTime = parseInt(tokenExpiresAt.value);
  const timeUntilAccessExpiry = accessExpiryTime - now;
  
  // Refresh access token 2 minutes before expiry (more aggressive due to shorter refresh token life)
  const refreshTime = timeUntilAccessExpiry - (2 * 60 * 1000);
  
  // Show warning if refresh token expires soon (15 minutes before refresh token expiry)
  if (refreshExpiresAt.value) {
    const refreshExpiryTime = parseInt(refreshExpiresAt.value);
    const timeUntilRefreshExpiry = refreshExpiryTime - now;
    const refreshWarningTime = timeUntilRefreshExpiry - (15 * 60 * 1000);
    
    if (refreshWarningTime > 0 && refreshWarningTime < timeUntilRefreshExpiry) {
      warningTimer.value = setTimeout(() => {
        console.warn('Refresh token will expire in 15 minutes. Session will end soon.');
        // You can emit an event or show a notification here
      }, refreshWarningTime);
    }
  }
  
  if (refreshTime > 0) {
    refreshTimer.value = setTimeout(() => {
      refreshAccessToken();
    }, refreshTime);
  }
};

export const useAuth = () => {
  const isAuthenticated = computed(() => {
    if (!token.value) return false;
    
    // Check if token is expired using reactive currentTime
    if (tokenExpiresAt.value) {
      const now = currentTime.value;
      const expiryTime = parseInt(tokenExpiresAt.value);
      return now < expiryTime;
    }
    
    return true;
  });

  const timeUntilRefreshExpiry = computed(() => {
    if (!refreshExpiresAt.value) return null;
    
    // Use reactive currentTime to trigger updates
    const now = currentTime.value;
    const expiryTime = parseInt(refreshExpiresAt.value);
    const timeLeft = expiryTime - now;
    
    if (timeLeft <= 0) return null;
    
    // Return time in minutes
    return Math.floor(timeLeft / (1000 * 60));
  });

  const timeUntilRefreshExpiryDetailed = computed(() => {
    if (!refreshExpiresAt.value) return null;
    
    // Use reactive currentTime to trigger updates
    const now = currentTime.value;
    const expiryTime = parseInt(refreshExpiresAt.value);
    const timeLeft = expiryTime - now;
    
    if (timeLeft <= 0) return null;
    
    const minutes = Math.floor(timeLeft / (1000 * 60));
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
    
    return { minutes, seconds, totalMinutes: minutes };
  });

  const login = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8000/auth/login/json', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Invalid credentials');
      }

      const data = await response.json();
      token.value = data.access_token;
      refreshToken.value = data.refresh_token;
      
      // Calculate and store token expiry times
      const accessTokenExpiry = decodeTokenExpiry(data.access_token);
      const refreshTokenExpiry = decodeTokenExpiry(data.refresh_token);
      
      if (accessTokenExpiry) {
        tokenExpiresAt.value = accessTokenExpiry.toString();
        localStorage.setItem('token-expires-at', tokenExpiresAt.value);
      }
      
      if (refreshTokenExpiry) {
        refreshExpiresAt.value = refreshTokenExpiry.toString();
        localStorage.setItem('refresh-expires-at', refreshExpiresAt.value);
      }
      
      // Store tokens in localStorage
      localStorage.setItem('auth-token', data.access_token);
      localStorage.setItem('refresh-token', data.refresh_token);
      
      // Setup automatic refresh timer
      setupRefreshTimer();
      
      // Get user info
      await getCurrentUser();
      
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const refreshAccessToken = async () => {
    try {
      if (!refreshToken.value) {
        throw new Error('No refresh token available');
      }

      const response = await fetch('http://localhost:8000/auth/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken.value })
      });

      if (!response.ok) {
        throw new Error('Token refresh failed');
      }

      const data = await response.json();
      token.value = data.access_token;
      refreshToken.value = data.refresh_token;
      
      // Calculate and store new token expiry times
      const accessTokenExpiry = decodeTokenExpiry(data.access_token);
      const refreshTokenExpiry = decodeTokenExpiry(data.refresh_token);
      
      if (accessTokenExpiry) {
        tokenExpiresAt.value = accessTokenExpiry.toString();
        localStorage.setItem('token-expires-at', tokenExpiresAt.value);
      }
      
      if (refreshTokenExpiry) {
        refreshExpiresAt.value = refreshTokenExpiry.toString();
        localStorage.setItem('refresh-expires-at', refreshExpiresAt.value);
      }
      
      // Update stored tokens
      localStorage.setItem('auth-token', data.access_token);
      localStorage.setItem('refresh-token', data.refresh_token);
      
      // Reset the refresh timer with new tokens
      setupRefreshTimer();
      
      return true;
    } catch (error) {
      // If refresh fails, logout user and redirect to login
      logout();
      window.location.href = '/login';
      return false;
    }
  };

  const getCurrentUser = async () => {
    try {
      const response = await fetch('http://localhost:8000/auth/me', {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to get user info');
      }

      const userData = await response.json();
      user.value = userData;
      return userData;
    } catch (error) {
      console.error('Error getting user info:', error);
      return null;
    }
  };

  const logout = () => {
    token.value = null;
    refreshToken.value = null;
    user.value = null;
    tokenExpiresAt.value = null;
    refreshExpiresAt.value = null;
    
    // Clear timers
    if (refreshTimer.value) {
      clearTimeout(refreshTimer.value);
      refreshTimer.value = null;
    }
    if (warningTimer.value) {
      clearTimeout(warningTimer.value);
      warningTimer.value = null;
    }
    
    localStorage.removeItem('auth-token');
    localStorage.removeItem('refresh-token');
    localStorage.removeItem('token-expires-at');
    localStorage.removeItem('refresh-expires-at');
  };

  const register = async (userData) => {
    try {
      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      const data = await response.json();
      return { success: true, user: data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const makeAuthenticatedRequest = async (url, options = {}) => {
    const requestOptions = {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${token.value}`
      }
    };

    let response = await fetch(url, requestOptions);
    
    // If unauthorized, try to refresh token
    if (response.status === 401) {
      const refreshed = await refreshAccessToken();
      if (refreshed) {
        // Retry the request with new token
        requestOptions.headers['Authorization'] = `Bearer ${token.value}`;
        response = await fetch(url, requestOptions);
      } else {
        // If refresh failed, redirect to login
        window.location.href = '/login';
        throw new Error('Unauthorized - redirecting to login');
      }
    }

    return response;
  };

  const checkAuth = async () => {
    // Check if token exists and is valid
    if (token.value) {
      try {
        await getCurrentUser();
        return true;
      } catch (error) {
        // Try to refresh token
        const refreshed = await refreshAccessToken();
        if (refreshed) {
          await getCurrentUser();
          return true;
        }
      }
    }
    return false;
  };

  // Initialize refresh timer if user is already authenticated
  if (token.value && refreshToken.value) {
    setupRefreshTimer();
  }

  return {
    user: computed(() => user.value),
    token: computed(() => token.value),
    isAuthenticated,
    timeUntilRefreshExpiry,
    timeUntilRefreshExpiryDetailed,
    login,
    logout,
    register,
    checkAuth,
    getCurrentUser,
    refreshAccessToken,
    makeAuthenticatedRequest
  };
};
