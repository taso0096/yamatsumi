<template>
  <div class="layers-card d-flex">
    <v-card
      tile
      flat
      min-width="500"
      width="500"
      height="100%"
      class="mb-3"
    >
      <v-card-title class="font-weight-regular">
        <span>{{ menuObject.label || menuObject.id || 'Layers' }}</span>
        <v-spacer />
        <v-btn
          v-if="layers"
          icon
          small
          @click="showAll.parentNode = !showAll.parentNode"
        >
          <v-icon>
            {{ showAll.parentNode ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
          </v-icon>
        </v-btn>
        <v-btn
          v-else
          icon
          small
          @click="closeMenu()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-expand-transition>
        <div v-show="showAll.parentNode">
          <v-card-text class="pt-0">
            <div
              v-if="!(layers || menuObject.nodes).length"
              class="mb-4"
            >
              <span>No data available</span>
            </div>
            <div
              v-else
              v-for="(node, i) in (layers || menuObject.nodes)"
              :key="`layer-${i}`"
              class="d-flex mb-4"
            >
              <v-card
                outlined
                width="100%"
              >
                <v-card-title class="subtitle-1">
                  <span>{{ node.label || node.id }}</span>
                  <v-spacer />
                  <v-btn
                    icon
                    small
                    @click="showAll.childNodes.splice(i, 1, !showAll.childNodes[i])"
                  >
                    <v-icon>
                      {{ showAll.childNodes[i] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                    </v-icon>
                  </v-btn>
                </v-card-title>
                <v-expand-transition>
                  <div v-show="showAll.childNodes[i]">
                    <v-card-text class="pt-0">
                      <template v-if="layers">
                        <v-row>
                          <v-col class="py-0">
                            <v-text-field
                              v-model="node.id"
                              label="Layer ID"
                            />
                          </v-col>
                          <v-col class="py-0">
                            <v-text-field
                              v-model="node.label"
                              label="Layer Label"
                            />
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col class="py-0">
                            <v-text-field
                              v-model.number="node.depth"
                              label="Depth"
                              type="number"
                            />
                          </v-col>
                          <v-col class="py-0">
                            <v-text-field
                              v-model.number="node.fixedDepth"
                              label="Fixed Depth"
                              type="number"
                            />
                          </v-col>
                        </v-row>
                      </template>
                      <template v-else>
                        <v-row>
                          <v-col class="py-0">
                            <v-text-field
                              v-model="node.id"
                              label="Node ID"
                            />
                          </v-col>
                          <v-col class="py-0">
                            <v-text-field
                              v-model="node.label"
                              label="Node Label"
                            />
                          </v-col>
                          <v-col class="py-0">
                            <v-text-field
                              v-model="node.parentId"
                              label="Parent Node ID"
                            />
                          </v-col>
                        </v-row>

                        <v-row>
                          <v-col class="py-0">
                            <v-switch
                              label="Group Node"
                              inset
                              hide-details
                              :input-value="!!node.nodes"
                              class="mt-0 mb-3"
                              readonly
                              @click="updateGroupNode(node, index + 1)"
                            />
                          </v-col>
                        </v-row>
                      </template>

                      <template v-if="!node.nodes">
                        <div v-if="editMode || node.nodeOptions">
                          <span class="subtitle-1 grey--text text--darken-1">Node Options</span>
                        </div>
                        <div
                          v-if="editMode && !node.nodeOptions"
                          class="text-center mb-4"
                        >
                          <v-btn
                            tile
                            depressed
                            small
                            color="primary"
                            @click="addNodeOptions(node)"
                          >
                            <span>Add Node Options</span>
                          </v-btn>
                        </div>
                        <template v-else-if="node.nodeOptions">
                          <v-row>
                            <v-col class="py-0">
                              <v-select
                                v-model="node.nodeOptions.type"
                                label="Type"
                                :items="nodeTypes"
                              />
                            </v-col>
                            <v-col class="py-0">
                              <v-text-field
                                v-model.number="node.nodeOptions.size"
                                label="Size"
                                type="number"
                                min="0"
                              />
                            </v-col>
                          </v-row>
                          <v-row>
                            <v-col class="py-0">
                              <v-text-field
                                v-model="node.nodeOptions.nodeColor"
                                label="Node Color"
                              />
                            </v-col>
                            <v-col class="py-0">
                              <v-text-field
                                v-model="node.nodeOptions.labelColor"
                                label="Label Color"
                              />
                            </v-col>
                          </v-row>
                        </template>
                      </template>
                      <template v-else>
                        <div v-if="editMode || node.layoutOptions">
                          <span class="subtitle-1 grey--text text--darken-1">Layout Options</span>
                        </div>
                        <div
                          v-if="editMode && !node.layoutOptions"
                          class="text-center mb-4"
                        >
                          <v-btn
                            tile
                            depressed
                            small
                            color="primary"
                            @click="addLayoutOptions(node)"
                          >
                            <span>Add Layout Options</span>
                          </v-btn>
                        </div>
                        <v-row v-else-if="node.layoutOptions">
                          <v-col class="py-0">
                            <v-select
                              v-model="node.layoutOptions.shape"
                              label="Shape"
                              :items="layoutShapes"
                            />
                          </v-col>
                          <v-col class="py-0">
                            <v-text-field
                              v-model.number="node.layoutOptions.scale"
                              label="Scale"
                              type="number"
                              min="0"
                            />
                          </v-col>
                          <v-col class="py-0">
                            <v-text-field
                              v-model.number="node.layoutOptions.fixedDistance"
                              label="Fixed Distance"
                              type="number"
                              min="0"
                            />
                          </v-col>
                        </v-row>

                        <div>
                          <span class="subtitle-1 grey--text text--darken-1">Nodes</span>
                        </div>
                        <div
                          v-if="!(node.nodes || []).length"
                          class="mb-4"
                        >
                          <span>No data available</span>
                        </div>
                        <div
                          v-else
                          class="text-center"
                        >
                          <v-btn
                            tile
                            depressed
                            small
                            color="secondary"
                            @click="pushMenu(node)"
                          >
                            <span>Show {{ node.nodes.length }} Nodes</span>
                            <v-icon>mdi-chevron-right</v-icon>
                          </v-btn>
                        </div>
                        <div
                          v-if="editMode && !(node.nodes || []).length"
                          class="text-center mb-4"
                        >
                          <v-btn
                            tile
                            depressed
                            small
                            color="primary"
                            @click="addNode(node.nodes)"
                          >
                            <span>Add Node</span>
                          </v-btn>
                        </div>
                      </template>
                    </v-card-text>
                  </div>
                </v-expand-transition>
              </v-card>
              <div
                v-if="editMode"
                class="d-flex align-center ml-3"
              >
                <v-btn
                  icon
                  small
                  @click="deleteIndex(nodes, showAll.childNodes, i)"
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
                v-if="layers"
                tile
                depressed
                small
                color="primary"
                @click="addLayer"
              >
                <span>Add Layer</span>
              </v-btn>
              <div
                v-else
                class="text-center mb-4"
              >
                <v-btn
                  tile
                  depressed
                  small
                  color="primary"
                  @click="addNode(menuObject.nodes)"
                >
                  <span>Add Node</span>
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </div>
      </v-expand-transition>
    </v-card>

    <layers-card
      v-if="showNextMenu"
      :menuObject="nextMenuObject"
      :editMode="editMode"
      :closeMenu="closeNextMenu"
      class="ml-3"
    />
  </div>
</template>

<style lang="scss" scoped>
.layers-card {
  height: 100%;
}
</style>

<script>
import LayersCard from './LayersCard.vue';

import networkSchema from '@/assets/NetworkSchema.json';

export default {
  name: 'LayersCard',
  components: {
    LayersCard
  },
  props: {
    layers: {
      type: Array
    },
    menuObject: {
      type: Object,
      default: () => ({})
    },
    editMode: {
      type: Boolean,
      default: false
    },
    closeMenu: {
      type: Function
    }
  },
  data: () => ({
    showAll: {
      parentNode: false,
      childNodes: []
    },
    nextMenuObject: {},
    showNextMenu: false
  }),
  computed: {
    schemaLayerProperties() {
      return networkSchema.properties.layers.items.properties;
    },
    layoutShapes() {
      return this.schemaLayerProperties.layoutOptions.properties.shape.enum;
    },
    nodeTypes() {
      return this.schemaLayerProperties.nodes.items.properties.nodeOptions.properties.type.enum;
    }
  },
  watch: {
    'menuObject.id'() {
      this.showAll.parentNode = true;
      this.showAll.childNodes = [];
      this.showAll.childNodes = [...Array(this.menuObject.nodes.length)].map(() => false);
    }
  },
  mounted() {
    if (this.menuObject.id) {
      this.showAll.parentNode = true;
    }
    this.showAll.childNodes = [...Array((this.layers || this.menuObject).length)].map(() => false);
  },
  methods: {
    addLayer() {
      this.showAll.childNodes.push(false);
      this.layers.push({
        id: `layer${this.layers.length + 1}`,
        label: '',
        depth: '',
        fixedDepth: '',
        nodes: []
      });
    },
    addNode(nodes) {
      if (nodes.length) {
        this.showAll.childNodes.push(false);
      }
      nodes.push({
        id: `node${nodes.length + 1}`,
        label: '',
        parentId: ''
      });
    },
    async updateGroupNode(node, nextIndex) {
      if (!this.editMode) {
        return;
      } else {
        const isConfirmed = await this.$_appRefs.confirmDialog.open({
          message: 'Are you sure you want to change "Group Node" status?',
          confirmText: 'Change',
          color: 'error'
        });
        if (!isConfirmed) {
          return;
        }
      }
      if (!node.nodes) {
        this.$set(node, 'nodes', []);
        this.$delete(node, 'nodeOptions');
        return;
      }
      this.$delete(node, 'nodes');
      this.$delete(node, 'layoutOptions');
      if (node.id === this.detailMenus[nextIndex]?.id) {
        this.detailMenus.splice(nextIndex);
      }
    },
    addLayoutOptions(layer) {
      this.$set(layer, 'layoutOptions', {
        shape: 'circle',
        scale: 1,
        fixedDistance: ''
      });
    },
    addNodeOptions(node) {
      this.$set(node, 'nodeOptions', {
        type: 'sphere',
        size: 1,
        nodeColor: '#fff',
        labelColor: '#fff'
      });
    },
    pushMenu(object) {
      this.nextMenuObject = object;
      this.showNextMenu = true;
    },
    async deleteIndex(array, showAll, delIndex, nextMenuIndex = 0) {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: `Are you sure you want to delete the "${array[delIndex].id}"?`,
        confirmText: 'Delete',
        color: 'error'
      });
      if (!isConfirmed) {
        return;
      }
      if (array[delIndex].id === this.detailMenus[nextMenuIndex]?.id) {
        this.detailMenus.splice(nextMenuIndex);
      }
      array.splice(delIndex, 1);
      showAll.splice(delIndex, 1);
    },
    closeNextMenu() {
      this.showNextMenu = false;
    }
  }
};
</script>
