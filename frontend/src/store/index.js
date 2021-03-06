import Vue from 'vue';
import Vuex from 'vuex';

import socket from './modules/socket';
import userData from './modules/userData';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    socket,
    userData
  }
});
