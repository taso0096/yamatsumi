import Vue from 'vue';
import { mapState } from 'vuex';

Vue.mixin({
  computed: {
    ...mapState({
      $_userData: state => state.userData
    }),
    $_appRefs() {
      return this.$root.$children[0].$refs;
    }
  },
  methods: {
    $_sleep(msec) {
      return new Promise(resolve => setTimeout(resolve, msec));
    },
    $_pushNotice(text, type, icon, group = 'app') {
      this.$notify({
        group,
        text,
        type,
        duration: 5000,
        data: { icon }
      });
    },
    $_convertDateFormat(date) {
      if (!date) {
        return undefined;
      } else if (typeof date !== 'object') {
        date = new Date(date);
      }
      const dateFormat = date.getFullYear() + '/' +
             ('0' + (date.getMonth() + 1)).slice(-2) + '/' +
             ('0' + date.getDate()).slice(-2);
      return dateFormat + ' ' + `0${date.getHours()}`.slice(-2) + ':' + `0${date.getMinutes()}`.slice(-2);
    },
    $_createPageTitle(meta) {
      document.title = meta.title;
    }
  }
});
