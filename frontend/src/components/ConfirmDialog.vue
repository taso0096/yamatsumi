<template>
  <div class="confirm-dialog">
    <v-dialog
      v-model="dialog"
      max-width="400"
      :persistent="data.persistent"
    >
      <v-card>
        <v-card-title>{{ data.title || 'Confirm' }}</v-card-title>
        <v-card-text class="confirm-dialog__text">
          {{ data.message }}
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            tile
            text
            @click="cancel"
          >
            <span>Cancel</span>
          </v-btn>
          <v-btn
            :color="data.color || 'primary'"
            tile
            depressed
            @click="confirm"
          >
            {{ data.confirmText || 'OK' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style lang="scss" scoped>
.confirm-dialog__text {
  white-space: pre-line;
}
</style>

<script>
export default {
  name: 'ConfirmDialog',
  data: () => ({
    dialog: false,
    resolve: null,
    data: {}
  }),
  watch: {
    dialog(val) {
      if (!val) {
        this.resolve(false);
      }
    }
  },
  methods: {
    open(data) {
      return new Promise(resolve => {
        this.data = data;
        this.resolve = resolve;
        this.dialog = true;
      });
    },
    confirm() {
      this.dialog = false;
      this.resolve(true);
    },
    cancel() {
      this.dialog = false;
      this.resolve(false);
    }
  }
};
</script>
