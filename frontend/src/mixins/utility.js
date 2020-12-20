import Vue from 'vue';
import { mapState } from 'vuex';

Vue.mixin({
  computed: {
    ...mapState({
      $_userData: state => state.userData
    })
  }
});
