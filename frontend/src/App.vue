<template>
  <v-app>
    <router-view/>
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

  </v-app>
</template>

<style lang="scss">
body {
  margin: 0;
  background: #00022d;
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
