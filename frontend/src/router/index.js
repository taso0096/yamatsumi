import Vue from 'vue';
import VueRouter from 'vue-router';
import Visualize from '@/views/Visualize.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/visualize',
    name: 'Visualize',
    component: Visualize
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

export default router;
