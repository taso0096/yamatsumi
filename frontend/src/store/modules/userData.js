import axios from '@/axios/index';
import Cookies from 'js-cookie';

const beforeunloadHandler = e => {
  e.returnValue = 'Are you sure you want to cancel editing Cyberspace?';
};

const defaultState = {
  isLoaded: false,
  isAuthed: false,
  accessToken: null,
  username: null,
  isSuperuser: false,
  interceptorId: null,
  isEdit: false
};

const state = Object.assign({}, defaultState);

const mutations = {
  RESET_USER_DATA(state) {
    axios.interceptors.request.eject(state.interceptorId);
    Object.assign(state, defaultState);
    Cookies.remove('accessToken');
  },
  UPDATE_AUTH_STATE(state, { accessToken, username, isSuperuser }) {
    axios.interceptors.request.eject(state.interceptorId);
    Object.assign(state, defaultState);
    Cookies.remove('accessToken');
    state.isLoaded = true;
    if (accessToken) {
      state.isAuthed = true;
      Cookies.set('accessToken', accessToken);
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
  },
  UPDATE_EDIT_STATE(state, isEdit) {
    state.isEdit = isEdit;
    if (isEdit) {
      window.addEventListener('beforeunload', beforeunloadHandler);
    } else {
      window.removeEventListener('beforeunload', beforeunloadHandler);
    }
  }
};

const actions = {
  resetUserData: ({ commit }) => {
    commit('RESET_USER_DATA');
  },
  updateAuthState: ({ commit }, userData) => {
    commit('UPDATE_AUTH_STATE', userData);
  },
  updateEditState: ({ commit }, isEdit) => {
    commit('UPDATE_EDIT_STATE', isEdit);
  }
};

export default {
  state,
  mutations,
  actions
};
