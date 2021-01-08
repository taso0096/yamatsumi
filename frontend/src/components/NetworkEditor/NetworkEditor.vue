<template>
  <div class="network-editor">
    <v-card
      tile
      flat
      class="network-editor__title-header mt-3"
    >
      <v-card-title>
        <span>Network Settings</span>
        <v-spacer />
        <v-menu
          v-if="!mode.edit"
          bottom
          left
          offset-y
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>

          <v-list class="pa-0">
            <v-list-item @click="mode.edit = true">
              <v-list-item-title>Edit</v-list-item-title>
            </v-list-item>
            <v-list-item
              :disabled="isLoading.delete"
              @click="deleteNetwork"
            >
              <v-list-item-title :class="{
                'error--text': !isLoading.delete
              }">Delete</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <template v-else>
          <v-btn
            text
            tile
            small
            class="mr-2"
            @click="cancelEdit"
          >
            <span>Cancel</span>
          </v-btn>
          <v-btn
            color="info"
            depressed
            :outlined="mode.preview"
            tile
            small
            class="mr-3"
            @click="previewNetwork"
          >
            <span v-if="!mode.preview">Preview</span>
            <span v-else>Original</span>
          </v-btn>
          <v-btn
            color="primary"
            depressed
            tile
            small
            :loading="isLoading.save"
            @click="saveNetwork"
          >
            <span>Save</span>
          </v-btn>
        </template>
      </v-card-title>
    </v-card>

    <v-form
      :readonly="!mode.edit || mode.preview"
      class="network-editor__form"
    >
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
                <v-card
                  outlined
                  width="100%"
                >
                  <v-card-text>
                    <v-text-field
                      v-model="node.nodeId"
                      :label="`Node ID (${i + 1})`"
                      hide-details
                    />
                    <v-combobox
                      v-model="node.ipaddresses"
                      :label="`IP addresses (${node.nodeId || i + 1})`"
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
                            v-if="mode.edit && !mode.preview"
                            small
                            class="ml-2"
                            @click="parent.selectItem(item)"
                          >mdi-close</v-icon>
                        </v-chip>
                      </template>
                    </v-combobox>
                  </v-card-text>
                </v-card>
                <div
                  v-if="mode.edit && !mode.preview"
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
                v-if="mode.edit && !mode.preview"
                class="text-center mb-4"
              >
                <v-btn
                  tile
                  depressed
                  small
                  color="primary"
                  @click="addRoutingTable"
                >
                  <span>Add Routing</span>
                </v-btn>
              </div>
            </v-card-text>
          </div>
        </v-expand-transition>
      </v-card>

      <layers-card
        :layers="network.layers"
        :editMode="mode.edit && !mode.preview"
      />
    </v-form>
  </div>
</template>

<style lang="scss" scoped>
.network-editor {
  height: calc(100% - 64px - 12px);
  margin-top: calc(64px + 12px);

  .network-editor__title-header {
    position: absolute;
    top: 0;
    width: calc(100% - 12px);
    z-index: 1;
  }
  .network-editor__form {
    height: 100%;
    overflow: scroll;
  }
}
</style>

<script>
import axios from '@/axios';

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
    },
    copyNetwork: {
      type: Function,
      required: true
    }
  },
  data: () => ({
    mode: {
      edit: false,
      preview: false
    },
    showAll: {
      details: true,
      routingTable: false
    },
    routingTableArray: [],
    isLoading: {
      save: false,
      delete: false
    }
  }),
  mounted() {
    this.init();
  },
  methods: {
    init() {
      this.routingTableArray = [];
      for (const key in this.network.routingTable) {
        this.routingTableArray.push({
          nodeId: key,
          ipaddresses: this.network.routingTable[key]
        });
      }
    },
    applyRoutingTable() {
      const routingTable = {};
      for (const item of this.routingTableArray) {
        routingTable[item.nodeId] = item.ipaddresses;
      }
      this.$set(this.network, 'routingTable', routingTable);
    },
    addRoutingTable() {
      this.routingTableArray.push({
        nodeId: '',
        ipaddresses: []
      });
    },
    async deleteRoutingTable(i) {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: `Are you sure you want to delete the "${this.routingTableArray[i].nodeId}" routing?`,
        confirmText: 'Delete',
        color: 'error'
      });
      if (!isConfirmed) {
        return;
      }
      this.routingTableArray.splice(i, 1);
    },
    cancelEdit() {
      this.mode.edit = false;
      this.mode.preview = false;
      this.copyNetwork('original', 'edit');
      this.copyNetwork('original', 'visualize');
      this.init();
    },
    previewNetwork() {
      this.mode.preview = !this.mode.preview;
      if (this.mode.preview) {
        this.copyNetwork('edit', 'visualize');
        this.applyRoutingTable();
        return;
      }
      this.copyNetwork('original', 'visualize');
    },
    async saveNetwork() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: 'Do you want to save the changes?',
        confirmText: 'Save'
      });
      if (!isConfirmed) {
        return;
      }
      this.applyRoutingTable();
      this.isLoading.save = true;
      const networkId = this.$route.params.networkId;
      await axios
        .put(`/networks/${networkId}/`, {
          data: this.network
        })
        .then(() => {
          this.copyNetwork('edit', 'visualize');
          this.copyNetwork('edit', 'original');
          this.cancelEdit();
          this.$_pushNotice('Saved the Network', 'success');
          if (this.network.id !== networkId) {
            this.$router.push({
              name: 'Visualize',
              params: {
                networkId: this.network.id
              }
            });
          }
        })
        .catch(err => {
          console.log(err);
          this.$_pushNotice('An error occurred.', 'error');
        });
      this.isLoading.save = false;
    },
    async deleteNetwork() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: 'Are you sure you want to delete this Network?',
        confirmText: 'Delete',
        color: 'error'
      });
      if (!isConfirmed) {
        return;
      }
      this.isLoading.delete = true;
      const networkId = this.$route.params.networkId;
      await axios
        .delete(`/networks/${networkId}/`)
        .then(() => {
          this.$_pushNotice('Deleted the Network', 'success');
          this.$router.push({ name: 'Network' });
        })
        .catch(err => {
          console.log(err);
          this.$_pushNotice('An error occurred.', 'error');
        });
      this.isLoading.delete = false;
    }
  }
}
</script>
