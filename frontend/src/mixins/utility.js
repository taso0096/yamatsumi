import Vue from 'vue';
import { mapState } from 'vuex';

Vue.mixin({
  computed: {
    ...mapState({
      $_userData: state => state.userData
    })
  },
  methods: {
    $_pushNotice(text, type, icon, group = 'app') {
      this.$notify({
        group,
        text,
        type,
        duration: 5000,
        data: { icon }
      });
    }
  }
});
