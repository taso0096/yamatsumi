import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store';

import Login from '@/views/Login.vue';
import Logout from '@/views/Logout.vue';
import CyberspaceList from '@/views/CyberspaceList.vue';
import Cyberspace from '@/views/Cyberspace.vue';

Vue.use(VueRouter);

const appName = 'YAMATSUMI';
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: `Login - ${appName}`
    }
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout,
    meta: {
      title: `Logout - ${appName}`
    }
  },
  {
    path: '/cyberspace',
    name: 'CyberspaceList',
    component: CyberspaceList,
    meta: {
      title: appName,
      requiresAuth: true
    }
  },
  {
    path: '/cyberspace/:id',
    name: 'Cyberspace',
    component: Cyberspace,
    meta: {
      title: `Cyberspace - ${appName}`,
      requiresAuth: true
    }
  },
  {
    path: '*',
    redirect: '/cyberspace'
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  const userData = store.state.userData;
  if (userData.isEdit && !confirm('Are you sure you want to cancel editing Cyberspace?')) {
    next(false);
    return;
  }
  if (to.matched.some(record => !record.meta.requiresAuth) || ((to.matched.some(record => !record.meta.requiresSuperuser) || userData.isSuperuser) && userData.isAuthed)) {
    if ((to.name === 'Login' && userData.isAuthed)) {
      next({ name: 'CyberspaceList' });
    } else {
      next();
    }
  } else if (userData.isAuthed) {
    next({ name: 'CyberspaceList' });
  } else {
    next({
      name: 'Login',
      query: { redirect: to.fullPath }
    });
  }
});

export default router;
