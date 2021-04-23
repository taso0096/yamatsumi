<template>
  <v-card
    outlined
    width="100%"
  >
    <v-card-title class="subtitle-1">
      <span>{{ nodeData.label || nodeData.id }}</span>
      <v-spacer />
      <v-btn
        icon
        small
        @click="showDetails.childNodes.splice(nodeIndex, 1, !showDetails.childNodes[nodeIndex])"
      >
        <v-icon>
          {{ showDetails.childNodes[nodeIndex] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
        </v-icon>
      </v-btn>
    </v-card-title>
    <v-expand-transition>
      <div v-show="showDetails.childNodes[nodeIndex]">
        <v-card-text class="pt-0">
          <template v-if="isLayer">
            <v-row>
              <v-col class="py-0">
                <v-text-field
                  v-model="nodeData.id"
                  label="Layer ID"
                />
              </v-col>
              <v-col class="py-0">
                <v-text-field
                  v-model="nodeData.label"
                  label="Layer Label"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                <v-text-field
                  v-model.number="nodeData.depth"
                  label="Depth"
                  type="number"
                />
              </v-col>
              <v-col class="py-0">
                <v-text-field
                  v-model.number="nodeData.fixedDepth"
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
                  v-model="nodeData.id"
                  label="Node ID"
                />
              </v-col>
              <v-col class="py-0">
                <v-text-field
                  v-model="nodeData.label"
                  label="Node Label"
                />
              </v-col>
              <v-col class="py-0">
                <v-text-field
                  v-model="nodeData.parentId"
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
                  :input-value="!!nodeData.nodes"
                  class="mt-0 mb-3"
                  readonly
                  @click="updateGroupNode(nodeData)"
                />
              </v-col>
            </v-row>
          </template>

          <template v-if="!nodeData.nodes">
            <div v-if="editMode || nodeData.nodeOptions">
              <span class="subtitle-1 grey--text text--darken-1">Node Options</span>
            </div>
            <div
              v-if="editMode && !nodeData.nodeOptions"
              class="text-center mb-4"
            >
              <v-btn
                tile
                depressed
                small
                color="primary"
                @click="addNodeOptions(nodeData)"
              >
                <span>Add Node Options</span>
              </v-btn>
            </div>
            <template v-else-if="nodeData.nodeOptions">
              <v-row>
                <v-col class="py-0">
                  <v-select
                    v-model="nodeData.nodeOptions.type"
                    label="Type"
                    :items="nodeTypes"
                  />
                </v-col>
                <v-col class="py-0">
                  <v-text-field
                    v-model.number="nodeData.nodeOptions.size"
                    label="Size"
                    type="number"
                    min="0"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col class="py-0">
                  <v-text-field
                    v-model="nodeData.nodeOptions.nodeColor"
                    label="Node Color"
                  />
                </v-col>
                <v-col class="py-0">
                  <v-text-field
                    v-model="nodeData.nodeOptions.labelColor"
                    label="Label Color"
                  />
                </v-col>
              </v-row>
            </template>
          </template>
          <template v-else>
            <div v-if="editMode || nodeData.layoutOptions">
              <span class="subtitle-1 grey--text text--darken-1">Layout Options</span>
            </div>
            <div
              v-if="editMode && !nodeData.layoutOptions"
              class="text-center mb-4"
            >
              <v-btn
                tile
                depressed
                small
                color="primary"
                @click="addLayoutOptions(nodeData)"
              >
                <span>Add Layout Options</span>
              </v-btn>
            </div>
            <v-row v-else-if="nodeData.layoutOptions">
              <v-col class="py-0">
                <v-select
                  v-model="nodeData.layoutOptions.shape"
                  label="Shape"
                  :items="layoutShapes"
                />
              </v-col>
              <v-col class="py-0">
                <v-text-field
                  v-model.number="nodeData.layoutOptions.scale"
                  label="Scale"
                  type="number"
                  min="0"
                />
              </v-col>
              <v-col class="py-0">
                <v-text-field
                  v-model.number="nodeData.layoutOptions.fixedDistance"
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
              v-if="!(nodeData.nodes || []).length"
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
                @click="pushGroup(nodeData)"
              >
                <span>Show {{ nodeData.nodes.length }} Nodes</span>
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </div>
            <div
              v-if="editMode && !(nodeData.nodes || []).length"
              class="text-center mb-4"
            >
              <v-btn
                tile
                depressed
                small
                color="primary"
                @click="addNode(nodeData.nodes)"
              >
                <span>Add Node</span>
              </v-btn>
            </div>
          </template>
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script>
import cyberspaceSchema from '@/assets/CyberspaceSchema.json';

export default {
  name: 'NodeCard',
  props: {
    isLayer: {
      type: Boolean,
      default: false
    },
    nodeData: {
      type: Object,
      required: true
    },
    nodeIndex: {
      type: Number,
      required: true
    },
    showDetails: {
      type: Object,
      required: true
    },
    pushGroup: {
      type: Function,
      required: true
    },
    addNode: {
      type: Function,
      required: true
    }
  },
  computed: {
    schemaLayerProperties() {
      return cyberspaceSchema.properties.layers.items.properties;
    },
    layoutShapes() {
      return this.schemaLayerProperties.layoutOptions.properties.shape.enum;
    },
    nodeTypes() {
      return this.schemaLayerProperties.nodes.items.properties.nodeOptions.properties.type.enum;
    },
    editMode() {
      return this.$_userData.isEdit;
    }
  },
  methods: {
    async updateGroupNode(nodeData) {
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
      if (!nodeData.nodes) {
        this.$set(nodeData, 'nodes', []);
        this.$delete(nodeData, 'nodeOptions');
        return;
      }
      this.$delete(nodeData, 'nodes');
      this.$delete(nodeData, 'layoutOptions');
      if (nodeData.id === this.nextGroupData.id) {
        this.showNextGroup = false;
      }
    },
    addLayoutOptions(layer) {
      this.$set(layer, 'layoutOptions', {
        shape: 'circle',
        scale: 1,
        fixedDistance: ''
      });
    },
    addNodeOptions(nodeData) {
      this.$set(nodeData, 'nodeOptions', {
        type: 'sphere',
        size: 1,
        nodeColor: '#fff',
        labelColor: '#fff'
      });
    }
  }
};
</script>
