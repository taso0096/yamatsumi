import io from 'socket.io-client';

const defaultState = {
  socket: null
};

const state = Object.assign({}, defaultState);

const mutations = {
  async RESET_SOCKET(state) {
    console.log('RESET_SOCKET');
    await state.socket?.disconnect();
    Object.assign(state, defaultState);
  },
  CONNECT_SOCKET(state, socket) {
    state.socket = socket;
  }
};

const actions = {
  async resetSocket({ commit }) {
    await commit('RESET_SOCKET');
  },
  async connectSocket({ commit }, networkId) {
    if (state.isConnected) {
      return false;
    }
    const socket = await io.connect(process.env.VUE_APP_SOCKETIO_BASE_URL, {
      query: {
        network_id: networkId
      }
    });
    socket.status = null;
    socket.on('connect', () => {
      console.log('CONNECT');
      socket.status = 'connect';
      commit('CONNECT_SOCKET', socket);
    });
    socket.on('connect_error', err => {
      console.log('CONNECT_ERROR:', err);
      socket.disconnect();
      socket.status = 'disconnect';
      commit('RESET_SOCKET');
    });
    return socket;
  }
};

export default {
  state,
  mutations,
  actions
};
