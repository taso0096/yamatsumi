<template>
  <div>
    <v-card
      tile
      flat
      class="mb-3"
    >
      <v-card-title>
        <span>Network JSON</span>
        <v-spacer />
        <v-btn
          v-if="!editMode"
          color="warning"
          depressed
          tile
          small
          @click="editMode = true"
        >
          <span>Edit</span>
        </v-btn>
        <template v-else>
          <v-btn
            text
            tile
            small
            class="mr-2"
            @click="editMode = false"
          >
            <span>Cancel</span>
          </v-btn>
          <v-btn
            color="primary"
            depressed
            tile
            small
            @click="editMode = false"
          >
            <span>Save</span>
          </v-btn>
        </template>
      </v-card-title>
    </v-card>

    <v-form :readonly="!editMode">
      <v-card
        tile
        flat
        class="mb-3"
      >
        <v-card-title class="font-weight-regular">
          <span>Details</span>
          <v-spacer />
          <v-btn
            icon
            small
            @click="showAll.details = !showAll.details"
          >
            <v-icon>
              {{ showAll.details ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
            </v-icon>
          </v-btn>
        </v-card-title>
        <v-expand-transition>
          <div v-show="showAll.details">
            <v-card-text class="pt-0">
              <v-text-field
                v-model="network.id"
                label="Network ID"
              />
              <v-text-field
                v-model="network.label"
                label="Network Label"
              />
              <v-text-field
                v-model="network.version"
                label="Version"
              />
              <v-textarea
                v-model="network.desc"
                label="Description"
              />
            </v-card-text>
          </div>
        </v-expand-transition>
      </v-card>

      <v-card
        tile
        flat
        class="mb-3"
      >
        <v-card-title class="font-weight-regular">
          <span>Routing Table</span>
          <v-spacer />
          <v-btn
            icon
            small
            @click="showAll.routingTable = !showAll.routingTable"
          >
            <v-icon>
              {{ showAll.routingTable ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
            </v-icon>
          </v-btn>
        </v-card-title>
        <v-expand-transition>
          <div v-show="showAll.routingTable">
            <v-card-text class="pt-0">
              <div
                v-if="!routingTableArray.length"
                class="mb-4"
              >
                <span>No data available</span>
              </div>
              <div
                v-else
                v-for="(node, i) in routingTableArray"
                :key="`node-${i}`"
                class="d-flex mb-5"
              >
                <div class="network-editor__routing-table-field">
                  <v-text-field
                    v-model="node[0]"
                    :label="`Node ID (${i + 1})`"
                    hide-details
                  />
                  <v-combobox
                    v-model="node[1]"
                    :label="`IP addresses (${node[0] || i + 1})`"
                    hide-selected
                    single-line
                    hide-details
                    multiple
                    append-icon=""
                    class="pt-0"
                  >
                    <template v-slot:selection="{ attrs, item, parent, selected }">
                      <v-chip
                        v-bind="attrs"
                        :input-value="selected"
                        label
                        small
                        :color="$vuetify.theme.dark ? 'grey darken-3' : 'grey lighten-3'"
                      >
                        <span>{{ item }}</span>
                        <v-icon
                          v-if="editMode"
                          small
                          class="ml-2"
                          @click="parent.selectItem(item)"
                        >mdi-close</v-icon>
                      </v-chip>
                    </template>
                  </v-combobox>
                </div>
                <div
                  v-if="editMode"
                  class="d-flex align-center ml-3"
                >
                  <v-btn
                    icon
                    small
                    @click="deleteRoutingTable(i)"
                  >
                    <v-icon color="error">mdi-delete-outline</v-icon>
                  </v-btn>
                </div>
              </div>
              <div
                v-if="editMode"
                class="text-center mb-4"
              >
                <v-btn
                  fab
                  depressed
                  small
                  color="primary"
                  @click="addRoutingTable"
                >
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </div>
            </v-card-text>
          </div>
        </v-expand-transition>
      </v-card>

      <layers-card
        :layers="network.layers"
        :editMode="editMode"
      />
    </v-form>
  </div>
</template>

<style lang="scss" scoped>
.network-editor__routing-table-field {
  width: 100%;
}
</style>

<script>
import LayersCard from './LayersCard.vue';

export default {
  name: 'NetworkEditor',
  components: {
    LayersCard
  },
  props: {
    network: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    editMode: false,
    showAll: {
      details: true,
      routingTable: false
    },
    routingTableArray: []
  }),
  mounted() {
    for (const key in this.network.routingTable) {
      this.routingTableArray.push([key, this.network.routingTable[key]]);
    }
  },
  methods: {
    addRoutingTable() {
      this.routingTableArray.push(['', []]);
    },
    deleteRoutingTable(i) {
      this.routingTableArray.splice(i, 1);
    }
  }
}
</script>
