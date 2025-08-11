import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import { useAuth } from './stores/auth';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    redirect: '/users'
  },
  {
    path: '/dashboard',
    redirect: '/users'
  },
  // Activity Routes
  {
    path: '/activity',
    name: 'Activity',
    component: Home,
    meta: { requiresAuth: true, module: 'activity' }
  },
  {
    path: '/activity/:id',
    name: 'ActivityDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'activity' }
  },
  // User Management Routes
  {
    path: '/users',
    name: 'Users',
    component: Home,
    meta: { requiresAuth: true, module: 'users' }
  },
  {
    path: '/users/:id',
    name: 'UserDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'users' }
  },
  // Controls Module Routes
  {
    path: '/controls',
    name: 'Controls',
    component: Home,
    meta: { requiresAuth: true, module: 'controls' }
  },
  {
    path: '/controls/:id',
    name: 'ControlDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'controls' }
  },
  // Frameworks Routes
  {
    path: '/controls/frameworks',
    name: 'Frameworks',
    component: Home,
    meta: { requiresAuth: true, module: 'frameworks' }
  },
  {
    path: '/controls/frameworks/:id',
    name: 'FrameworkDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'frameworks' }
  },
  // Implementation Groups Routes
  {
    path: '/controls/implementation-groups',
    name: 'ImplementationGroups',
    component: Home,
    meta: { requiresAuth: true, module: 'implementationGroups' }
  },
  {
    path: '/controls/implementation-groups/:id',
    name: 'ImplementationGroupDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'implementationGroups' }
  },
  // Functions Routes
  {
    path: '/controls/functions',
    name: 'Functions',
    component: Home,
    meta: { requiresAuth: true, module: 'functions' }
  },
  {
    path: '/controls/functions/:id',
    name: 'FunctionDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'functions' }
  },
  // Safeguards Routes
  {
    path: '/controls/safeguards',
    name: 'Safeguards',
    component: Home,
    meta: { requiresAuth: true, module: 'safeguards' }
  },
  {
    path: '/controls/safeguards/:id',
    name: 'SafeguardDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'safeguards' }
  },
  // Configuration Item Types Routes (formerly Asset Classes)
  {
    path: '/cmdb/configuration-item-types',
    name: 'ConfigurationItemTypes',
    component: Home,
    meta: { requiresAuth: true, module: 'configuration-item-types' }
  },
  {
    path: '/cmdb/configuration-item-types/:id',
    name: 'ConfigurationItemTypeDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'configuration-item-types' }
  },
  // Devices Routes
  {
    path: '/devices',
    name: 'Devices',
    component: Home,
    meta: { requiresAuth: true, module: 'devices' }
  },
  {
    path: '/devices/:id',
    name: 'DeviceDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'devices' }
  },
  // Software Routes
  {
    path: '/software',
    name: 'Software',
    component: Home,
    meta: { requiresAuth: true, module: 'software' }
  },
  {
    path: '/software/:id',
    name: 'SoftwareDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'software' }
  },
  // Data Routes
  {
    path: '/data',
    name: 'Data',
    component: Home,
    meta: { requiresAuth: true, module: 'data' }
  },
  {
    path: '/data/:id',
    name: 'DataDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'data' }
  },
  // Network Routes
  {
    path: '/network',
    name: 'Network',
    component: Home,
    meta: { requiresAuth: true, module: 'network' }
  },
  {
    path: '/network/:id',
    name: 'NetworkDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'network' }
  },
  // Documentation Routes
  {
    path: '/documentation',
    name: 'Documentation',
    component: Home,
    meta: { requiresAuth: true, module: 'documentation' }
  },
  {
    path: '/documentation/:id',
    name: 'DocumentationDetail',
    component: Home,
    meta: { requiresAuth: true, module: 'documentation' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const { isAuthenticated, checkAuth } = useAuth();
  
  // Check if user is authenticated (including token validation)
  if (to.meta.requiresAuth) {
    if (!isAuthenticated.value) {
      next('/login');
      return;
    }
    
    // Verify token is still valid
    const isValid = await checkAuth();
    if (!isValid) {
      next('/login');
      return;
    }
  }
  
  // If route requires guest (like login page) and user is authenticated
  if (to.meta.requiresGuest && isAuthenticated.value) {
    next('/');
    return;
  }
  
  next();
});

export default router;
