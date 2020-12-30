<template>
  <div>
    <v-navigation-drawer
      v-model="editDrawer"
      app
      clipped
      floating
      right
      mobile-breakpoint="960"
      color="transparent"
      width="600"
    >
    </v-navigation-drawer>

    <v-app-bar
      clipped-left
      clipped-right
      absolute
      color="white"
      elevation="0"
      class="ma-3"
    >
      <v-toolbar-title>
        <span>{{ network.label }}</span>
      </v-toolbar-title>
      <v-spacer />
      <v-btn
        icon
        @click="editDrawer = !editDrawer"
      >
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  name: 'NetworkEditor',
  props: {
    network: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    editDrawer: false
  })
}
</script>
