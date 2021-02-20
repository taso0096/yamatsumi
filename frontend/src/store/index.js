import Vue from 'vue';
import Vuex from 'vuex';

import socket from './modules/socket';
import userData from './modules/userData';
import visualizeData from './modules/visualizeData';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    socket,
    userData,
    visualizeData
  }
});
