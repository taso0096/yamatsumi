import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css';
import '@mdi/font/css/materialdesignicons.css';
import './mixins/utility';

import Notifications from 'vue-notification';
import velocity from 'velocity-animate';

import Cookies from 'js-cookie';
import axios from '@/axios/index';

import 'aframe';

Vue.config.productionTip = false;
Vue.config.ignoredElements = [
  'a-scene',
  'a-sky',
  'a-plane',
  'a-cylinder',
  'a-sphere',
  'a-circle',
  'a-entity',
  'a-camera',
  'a-tetrahedron',
  'a-octahedron',
  'a-dodecahedron',
  'a-icosahedron',
  'a-box',
  'a-ring',
  'a-asset-items',
  'a-assets',
  'a-cursor',
  'a-text',
  'a-light',
  'a-image',
  'a-triangle'
];

Vue.use(Notifications, { velocity });

const createApp = async() => {
  new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
  }).$mount('#app');
  const accessToken = Cookies.get('accessToken');
  if (!accessToken) {
    store.dispatch('updateAuthState', {});
  } else {
    await axios
      .get('/users/verify/',
        {
          headers: {
            Authorization: `JWT ${accessToken}`
          }
        }
      )
      .then(res => {
        store.dispatch('updateAuthState', {
          accessToken,
          ...res.data
        });
        if (router.app._route.name === 'Login') {
          router.push(router.app._route.query.redirect || { name: 'Network' });
        }
      })
      .catch(() => {
        store.dispatch('updateAuthState', {});
      });
  }
};

createApp();
