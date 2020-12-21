<template>
  <div class="Logout">
    <v-card
      flat
      color="rgba(0, 0, 0, 0)"
    >
      <v-card-text class="text-center">
        <div class="body-1 mb-3">
          Logging out
        </div>
        <v-progress-circular
          indeterminate
          color="primary"
        />
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'Logout',
  async mounted() {
    await new Promise(resolve => setTimeout(resolve, 500));
    this.$store.dispatch('updateAuthState', {});
    this.$router.push({ name: 'Login' });
  }
};
</script>
