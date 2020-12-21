import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store';

import Login from '@/views/Login.vue';
import Logout from '@/views/Logout.vue';
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
    path: '/visualize',
    name: 'Visualize',
    component: Visualize,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '*',
    redirect: '/login'
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
      next({ name: 'Visualize' });
    } else {
      next();
    }
  } else if (userData.isAuthed) {
    next({ name: 'Visualize' });
  } else {
    next({
      name: 'Login',
      query: { redirect: to.fullPath }
    });
  }
});

export default router;
