import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store';

import Login from '@/views/Login.vue';
import Logout from '@/views/Logout.vue';
import Network from '@/views/Network.vue';
import Visualize from '@/views/Visualize.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },
  {
    path: '/network',
    name: 'Network',
    component: Network,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/network/:id',
    name: 'Visualize',
    component: Visualize,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '*',
    redirect: '/network'
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  const userData = store.state.userData;
  if (to.matched.some(record => !record.meta.requiresAuth) || ((to.matched.some(record => !record.meta.requiresSuperuser) || userData.isSuperuser) && userData.isAuthed)) {
    if ((to.name === 'Login' && userData.isAuthed)) {
      next({ name: 'Network' });
    } else {
      next();
    }
  } else if (userData.isAuthed) {
    next({ name: 'Network' });
  } else {
    next({
      name: 'Login',
      query: { redirect: to.fullPath }
    });
  }
});

export default router;
