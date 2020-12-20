import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css';
import '@mdi/font/css/materialdesignicons.css';
import './mixins/utility';

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

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app');
