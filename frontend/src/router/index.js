import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store';

import Visualize from '@/views/Visualize.vue';

Vue.use(VueRouter);

const routes = [
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
    redirect: '/'
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
