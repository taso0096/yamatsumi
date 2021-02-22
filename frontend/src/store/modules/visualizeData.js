const defaultState = {
  exercise: {},
  network: {},
  score: {}
};

const state = Object.assign({}, defaultState);

const mutations = {
  RESET_VISUALIZE_DATA(state) {
    Object.assign(state, defaultState);
  },
  SET_VISUALIZE_DATA(state, visualizeData) {
    state.exercise = visualizeData.exercise || {};
    state.network = visualizeData.network || {};
    state.score = visualizeData.score || {};
  }
};

const actions = {
  resetEvent({ commit }) {
    commit('RESET_VISUALIZE_DATA');
  },
  setEvent({ commit }, visualizeData) {
    commit('SET_VISUALIZE_DATA', visualizeData);
  }
};

export default {
  state,
  mutations,
  actions
};
