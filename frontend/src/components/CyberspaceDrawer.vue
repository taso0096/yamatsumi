<template>
  <v-navigation-drawer
    v-model="drawer"
    app
    clipped
    floating
    right
    mobile-breakpoint="960"
    color="transparent"
    width="50%"
    class="cyberspace-drawer pt-3 pr-3"
  >
    <v-toolbar flat>
      <v-tabs v-model="drawerTab">
        <v-tab>Details</v-tab>
        <v-tab disabled>Contest</v-tab>
        <v-tab>Network</v-tab>
        <v-spacer />
        <v-menu
          bottom
          left
          offset-y
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
              class="my-auto mr-3"
            >
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>

          <v-list class="pa-0">
            <v-list-item>
              <v-list-item-title>Edit</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-title color="error--text">Delete</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-tabs>
    </v-toolbar>

    <v-tabs-items
      v-model="drawerTab"
      class="cyberspace-drawer__tab-items"
    >
      <v-tab-item>Details</v-tab-item>
      <v-tab-item>Contest</v-tab-item>
      <v-tab-item>
        <network-editor
          :networkData="cyberspace.layers"
          class="ma-3"
        />
      </v-tab-item>
    </v-tabs-items>
  </v-navigation-drawer>
</template>

<style lang="scss" scoped>
.cyberspace-drawer {
  .cyberspace-drawer__tab-items {
    background: transparent !important;
  }
}
</style>

<script>
import NetworkEditor from '@/components/NetworkEditor';

export default {
  name: 'CyberspaceDrawer',
  components: {
    NetworkEditor
  },
  props: {
    drawer: {
      type: Boolean,
      default: false,
      required: true
    },
    cyberspace: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    drawerTab: null
  })
};
</script>
