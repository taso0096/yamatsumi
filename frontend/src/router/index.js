import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store';

import Login from '@/views/Login.vue';
import Logout from '@/views/Logout.vue';
import Network from '@/views/Network.vue';
import Visualize from '@/views/Visualize.vue';

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
    path: '/network',
    name: 'Network',
    component: Network,
    meta: {
      title: appName,
      requiresAuth: true
    }
  },
  {
    path: '/network/:networkId',
    name: 'Visualize',
    component: Visualize,
    meta: {
      title: `Visualize - ${appName}`,
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
