const defaultState = {
  cyberspace: {},
  exercise: {},
  score: {}
};

const state = Object.assign({}, defaultState);

const mutations = {
  RESET_VISUALIZE_DATA(state) {
    Object.assign(state, defaultState);
  },
  SET_VISUALIZE_DATA(state, visualizeData) {
    state.cyberspace = visualizeData.cyberspace || {};
    state.exercise = visualizeData.exercise || {};
    state.score = visualizeData.score || {};
  }
};

const actions = {
  resetVisualizeData({ commit }) {
    commit('RESET_VISUALIZE_DATA');
  },
  setVisualizeData({ commit }, visualizeData) {
    commit('SET_VISUALIZE_DATA', visualizeData);
  }
};

export default {
  state,
  mutations,
  actions
};
