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

    <confirm-dialog ref="confirmDialog" />

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
      <v-sheet class="ma-3 mr-0">
        <v-list
          v-if="$_userData.isAuthed"
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
      <v-sheet class="ma-3 mr-0">
        <v-list
          v-if="$_userData.isLoaded"
          class="py-0"
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
            >
              <v-list-item-icon>
                <v-icon size="20">{{ tab.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{ tab.title }}</v-list-item-title>
            </v-list-item>
          </template>
          <v-divider />
          <v-switch
            v-model="$vuetify.theme.dark"
            label="Dark Mode"
            inset
            hide-details
            class="mt-2 mb-3 ml-4"
          />
          <v-divider />
          <div class="py-3 pl-4">
            <div class="subtitle-2">©YAMATSUMI v{{ version }}</div>
            <div class="subtitle-2">Develop by <a href="https://github.com/taso0096" target="_blank">@taso0096</a></div>
          </div>
        </v-list>
      </v-sheet>
    </v-navigation-drawer>

    <v-app-bar
      app
      clipped-left
      clipped-right
      :color="$vuetify.theme.dark ? '#1e1e1e' : 'white'"
      flat
    >
      <v-app-bar-nav-icon
        v-if="$route.name !== 'Logout'"
        @click="appDrawer = !appDrawer"
      />

      <v-toolbar-title>
        <span>YAMATSUMI</span>
      </v-toolbar-title>
    </v-app-bar>

    <v-main
      :style="{
        background: $vuetify.theme.dark ? '#303030' : '#eee'
      }"
    >
      <v-container
        :style="{
          height: ['Cyberspace', 'CyberspaceV2'].includes($route.name) && '100%'
        }"
      >
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<style lang="scss">
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
import ConfirmDialog from '@/components/ConfirmDialog.vue';

import appPackage from '../package.json';

export default {
  name: 'App',
  components: {
    ConfirmDialog
  },
  data: () => ({
    appDrawer: window.innerWidth >= 960,
    drawerTabs: [
      {
        title: 'Cyberspaces',
        icon: 'mdi-wan',
        route: {
          name: 'CyberspaceList'
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
  }),
  computed: {
    version: () => appPackage.version
  },
  watch: {
    $route(to) {
      this.$_createPageTitle(to.meta);
    },
    '$vuetify.theme.dark'(val) {
      if (val) {
        localStorage.setItem('darkMode', val);
      } else {
        localStorage.removeItem('darkMode');
      }
    }
  },
  mounted() {
    this.$_createPageTitle(this.$route.meta);
    this.$vuetify.theme.dark = !!localStorage.getItem('darkMode');
    AFRAME.registerComponent('look-center', {
      schema: {
        parentSelector: { type: 'string' }
      },
      init: function() {
        const targetEl = document.querySelector(this.data.parentSelector);
        const targetPosition = targetEl?.object3D.getWorldPosition(new THREE.Vector3());
        if (targetPosition) {
          targetPosition.y = this.el.object3D.getWorldPosition(new THREE.Vector3()).y;
        }
        this.el.object3D.lookAt(targetPosition || new THREE.Vector3(0, 0, 0));
        this.el.firstElementChild.object3D.rotation.set(0, Math.PI, 0);
      }
    });
  }
};
</script>
