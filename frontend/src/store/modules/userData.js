import axios from '@/axios/index';
import Cookies from 'js-cookie';

const defaultState = {
  isLoaded: false,
  isAuthed: false,
  accessToken: null,
  username: null,
  isSuperuser: false,
  interceptorId: null
};

const state = Object.assign({}, defaultState);

const mutations = {
  RESET_USER_DATA(state) {
    axios.interceptors.request.eject(state.interceptorId);
    Object.assign(state, defaultState);
    Cookies.remove('accessToken');
  },
  UPDATE_AUTH_STATE(state, { accessToken, username, isSuperuser }) {
    Object.assign(state, defaultState);
    Cookies.remove('accessToken');
    state.isLoaded = true;
    if (accessToken) {
      state.isAuthed = true;
      Cookies.set('accessToken', accessToken);
      axios.interceptors.request.eject(state.interceptorId);
      state.interceptorId = axios.interceptors.request.use(config => {
        config.headers.Authorization = `JWT ${accessToken}`;
        return config;
      }, err => {
        return Promise.reject(err);
      });
    }
    state.accessToken = accessToken;
    state.username = username;
    state.isSuperuser = !!isSuperuser;
  }
};

const actions = {
  resetUserData: ({ commit }) => {
    commit('RESET_USER_DATA');
  },
  updateAuthState: ({ commit }, userData) => {
    commit('UPDATE_AUTH_STATE', userData);
  }
};

export default {
  state,
  mutations,
  actions
};
