<template>
  <div class="cyberspace-editor">
    <v-card
      tile
      flat
      class="cyberspace-editor__title-header mt-3"
    >
      <v-card-title>
        <span>Cyberspace Settings</span>
        <v-spacer />
        <v-btn
          v-if="!mode.edit"
          icon
          class="mr-3"
          @click="downloadCyberspace"
        >
          <v-icon>mdi-download</v-icon>
        </v-btn>
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
            <v-list-item @click="editCyberspace">
              <v-list-item-title>Edit</v-list-item-title>
            </v-list-item>
            <v-list-item
              :disabled="isLoading.delete"
              @click="deleteCyberspace"
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
            @click="cancelEdit(true)"
          >
            <span>Cancel</span>
          </v-btn>
          <v-switch
            label="Preview Mode"
            inset
            hide-details
            class="mt-0 pt-0 mr-5"
            @click="previewCyberspace"
          />
          <v-btn
            color="primary"
            depressed
            tile
            small
            :loading="isLoading.save"
            @click="saveCyberspace"
          >
            <span>Save</span>
          </v-btn>
        </template>
      </v-card-title>
    </v-card>

    <v-form
      :readonly="!mode.edit"
      class="cyberspace-editor__form"
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
                v-model="cyberspace.id"
                label="Cyberspace ID"
              />
              <v-text-field
                v-model="cyberspace.label"
                label="Cyberspace Label"
              />
              <v-text-field
                v-model="cyberspace.version"
                label="Version"
              />
              <v-textarea
                v-model="cyberspace.desc"
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
                            v-if="mode.edit"
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
                  v-if="mode.edit"
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
                v-if="mode.edit"
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

      <div class="layers-block">
        <layers-card
          :isLayers="true"
          :menuData="cyberspace.layers"
          :editMode="mode.edit"
        />
      </div>
    </v-form>
  </div>
</template>

<style lang="scss" scoped>
.cyberspace-editor {
  height: calc(100% - 64px - 12px);
  margin-top: calc(64px + 12px);

  .cyberspace-editor__title-header {
    position: absolute;
    top: 0;
    width: calc(100% - 12px);
    z-index: 1;
  }
  .cyberspace-editor__form {
    height: 100%;
    overflow: scroll;
  }
  .layers-block {
    overflow: scroll;
  }
}
</style>

<script>
import axios from '@/axios';

import LayersCard from './LayersCard.vue';

export default {
  name: 'CyberspaceEditor',
  components: {
    LayersCard
  },
  props: {
    cyberspace: {
      type: Object,
      required: true
    },
    copyCyberspace: {
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
      details: false,
      routingTable: false
    },
    routingTableArray: [],
    isLoading: {
      save: false,
      delete: false
    },
    previewIntervalId: null,
    isChangedForm: false
  }),
  watch: {
    cyberspace: {
      handler(val, oldVal) {
        this.isChangedForm = true;
      },
      deep: true
    },
    routingTableArray: {
      handler() {
        this.applyRoutingTable();
      },
      deep: true
    }
  },
  mounted() {
    this.init();
  },
  destroyed() {
    this.$store.dispatch('updateEditState', false);
  },
  methods: {
    init() {
      this.routingTableArray = [];
      for (const key in this.cyberspace.routingTable) {
        this.routingTableArray.push({
          nodeId: key,
          ipaddresses: this.cyberspace.routingTable[key]
        });
      }
    },
    applyRoutingTable() {
      const routingTable = {};
      for (const item of this.routingTableArray) {
        routingTable[item.nodeId] = item.ipaddresses;
      }
      this.$set(this.cyberspace, 'routingTable', routingTable);
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
    async downloadCyberspace() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: 'Do you want to download the Cyberspace?',
        confirmText: 'Download'
      });
      if (!isConfirmed) {
        return;
      }
      const data = JSON.stringify(this.cyberspace, null, '  ');
      const link = document.createElement('a');
      link.href = `data:text/plain,${encodeURIComponent(data)}`;
      link.download = `${this.cyberspace.id}.json`;
      link.click();
    },
    editCyberspace() {
      this.mode.edit = true;
      this.$store.dispatch('updateEditState', true);
    },
    async cancelEdit(needConfirm) {
      if (needConfirm) {
        const isConfirmed = await this.$_appRefs.confirmDialog.open({
          message: 'Are you sure you want to cancel editing Cyberspace?',
          confirmText: 'Cancel',
          color: 'error'
        });
        if (!isConfirmed) {
          return;
        }
      }
      this.mode.edit = false;
      this.mode.preview = false;
      clearInterval(this.previewIntervalId);
      this.$store.dispatch('updateEditState', false);
      this.copyCyberspace('original', 'edit');
      this.copyCyberspace('original', 'visualize');
      await this.$_sleep(100);
      this.init();
    },
    previewCyberspace() {
      this.mode.preview = !this.mode.preview;
      if (!this.mode.preview) {
        this.copyCyberspace('original', 'visualize');
        clearInterval(this.previewIntervalId);
        return;
      }
      this.copyCyberspace('edit', 'visualize');
      this.previewIntervalId = setInterval(() => {
        if (this.isChangedForm) {
          this.copyCyberspace('edit', 'visualize');
          this.isChangedForm = false;
        }
      }, 1000);
    },
    async saveCyberspace() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: 'Do you want to save the changes?',
        confirmText: 'Save'
      });
      if (!isConfirmed) {
        return;
      }
      this.isLoading.save = true;
      const id = this.$route.params.id;
      await axios
        .put(`/cyberspaces/${id}/`, {
          data: this.cyberspace
        },
        {
          validateStatus: status => status < 500
        })
        .then(res => {
          if (res.status !== 200) {
            this.$_pushNotice('This Cyberspace ID is already in use.', 'error');
            return;
          }
          this.copyCyberspace('edit', 'visualize');
          this.copyCyberspace('edit', 'original');
          this.cancelEdit(false);
          this.$_pushNotice('Saved the Cyberspace', 'success');
          if (this.cyberspace.id !== id) {
            this.$router.push({
              name: 'Visualize',
              params: {
                id: this.cyberspace.id
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
    async deleteCyberspace() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: 'Are you sure you want to delete this Cyberspace?',
        confirmText: 'Delete',
        color: 'error'
      });
      if (!isConfirmed) {
        return;
      }
      this.isLoading.delete = true;
      const id = this.$route.params.id;
      await axios
        .delete(`/cyberspaces/${id}/`)
        .then(() => {
          this.$_pushNotice('Deleted the Cyberspace', 'success');
          this.$router.push({ name: 'Cyberspace' });
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
