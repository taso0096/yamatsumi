const defaultState = {
  network: {},
  game: {}
};

const state = Object.assign({}, defaultState);

const mutations = {
  RESET_EVENT(state) {
    Object.assign(state, defaultState);
  },
  SET_EVENT(state, event) {
    state.network = event.network || {};
    state.game = event.game || {};
  }
};

const actions = {
  resetEvent({ commit }) {
    commit('RESET_EVENT');
  },
  setEvent({ commit }, event) {
    commit('SET_EVENT', event);
  }
};

export default {
  state,
  mutations,
  actions
};
