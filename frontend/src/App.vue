<template>
  <v-app>
    <notifications
      group="app"
      animation-type="velocity"
    >
      <template
        slot="body"
        slot-scope="props"
      >
        <v-alert
          :type="props.item.type"
          :icon="props.item.data.icon"
          width="400"
          class="my-notification ma-3 mb-0"
        >
          <div class="d-flex align-center ml-3">
            <div class="my-notification__text body-2 mr-auto">
              {{ props.item.text }}
            </div>
            <v-btn
              icon
              x-small
              class="ml-0"
              @click="props.close"
            >
              <v-icon small>mdi-close</v-icon>
            </v-btn>
          </div>
        </v-alert>
      </template>
    </notifications>

    <v-navigation-drawer
      v-if="$route.name !== 'Logout'"
      v-model="appDrawer"
      app
      clipped
      floating
      mobile-breakpoint="960"
      color="transparent"
      width="300"
    >
      <v-sheet
        v-if="$_userData.isAuthed"
        rounded="lg"
        class="ma-3 mr-0"
      >
        <v-list
          color="transparent"
          class="py-0"
        >
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>{{ $_userData.username }}</v-list-item-title>
              <v-list-item-subtitle v-if="$_userData.isSuperuser">superuser</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-sheet>
      <v-sheet
        v-if="$_userData.isLoaded"
        rounded="lg"
        class="ma-3 mr-0"
      >
        <v-list
          nav
          dense
          color="transparent"
        >
          <v-list-item
            v-if="!$_userData.isAuthed"
            :to="{ name: 'Login' }"
          >
            <v-list-item-icon>
              <v-icon size="20">mdi-login</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Login</v-list-item-title>
          </v-list-item>
          <template v-for="tab in drawerTabs">
            <v-list-item
              v-if="!tab.requiresAuth || (!tab.requiresSuperuser || $_userData.isSuperuser) && $_userData.isAuthed"
              :key="tab.title"
              :to="tab.route"
              exact
              class="mb-2"
            >
              <v-list-item-icon>
                <v-icon size="20">{{ tab.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{ tab.title }}</v-list-item-title>
            </v-list-item>
          </template>
          <v-divider class="my-2" />
          <div class="subtitle-2 ml-1">©YAMATSUMI</div>
          <div class="subtitle-2 ml-1">Develop by <a href="https://github.com/taso0096" target="_blank">@taso0096</a></div>
        </v-list>
      </v-sheet>
    </v-navigation-drawer>

    <v-app-bar
      app
      clipped-left
      clipped-right
      color="white"
      elevation="0"
    >
      <v-app-bar-nav-icon
        v-if="$route.name !== 'Logout'"
        @click="appDrawer = !appDrawer"
      />

      <v-toolbar-title>
        <span>YAMATSUMI</span>
      </v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container
        :style="{
          height: $route.name === 'Visualize' && '100%'
        }"
      >
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<style lang="scss">
.v-main {
  background: #F3F4F6;
}
.vue-notification-group {
    width: auto !important;

    .my-notification {
      @media (max-width:524px) {
        width: calc(100vw - 24px) !important;
      }
      .my-notification__text {
        white-space: pre-line;
      }
    }
  }
</style>

<script>
export default {
  name: 'App',
  data: () => ({
    appDrawer: window.innerWidth >= 960,
    drawerTabs: [
      {
        title: 'Network',
        icon: 'mdi-wan',
        route: {
          name: 'Network'
        },
        requiresAuth: true
      },
      {
        title: 'Logout',
        icon: 'mdi-logout',
        route: {
          name: 'Logout'
        },
        requiresAuth: true
      }
    ]
  })
}
</script>
