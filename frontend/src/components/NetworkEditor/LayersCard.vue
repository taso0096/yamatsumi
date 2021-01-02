<template>
  <div class="layers-card d-flex">
    <v-card
      tile
      flat
      min-width="588"
      height="100%"
      class="mb-3"
    >
      <v-card-title class="font-weight-regular">
        <span>Layers</span>
        <v-spacer />
        <v-btn
          icon
          small
          @click="showAll.layers = !showAll.layers"
        >
          <v-icon>
            {{ showAll.layers ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
          </v-icon>
        </v-btn>
      </v-card-title>
      <v-expand-transition>
        <div v-show="showAll.layers">
          <v-card-text class="pt-0">
            <div
              v-if="!layers.length"
              class="mb-4"
            >
              <span>No data available</span>
            </div>
            <v-card
              v-else
              v-for="(layer, i) in layers"
              :key="`layer-${i}`"
              tile
              flat
            >
              <v-card-title class="subtitle-1 px-0">
                <span>{{ layer.label || layer.id }}</span>
                <v-spacer />
                <v-btn
                  icon
                  small
                  @click="showAll.layer.splice(i, 1, !showAll.layer[i])"
                >
                  <v-icon>
                    {{ showAll.layer[i] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                  </v-icon>
                </v-btn>
              </v-card-title>
              <v-expand-transition>
                <div v-show="showAll.layer[i]">
                  <v-card-text class="pt-0 px-0">
                    <v-row>
                      <v-col class="py-0">
                        <v-text-field
                          v-model="layer.id"
                          label="ID"
                        />
                      </v-col>
                      <v-col class="py-0">
                        <v-text-field
                          v-model="layer.label"
                          label="Label"
                        />
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col class="py-0">
                        <v-text-field
                          v-model="layer.depth"
                          label="Depth"
                        />
                      </v-col>
                      <v-col class="py-0">
                        <v-text-field
                          v-model="layer.fixedDepth"
                          label="Fixed Depth"
                        />
                      </v-col>
                    </v-row>

                    <div v-if="editMode || layer.layoutOptions">
                      <span class="subtitle-1 grey--text text--darken-1">Layout Options</span>
                    </div>
                    <div
                      v-if="editMode && !layer.layoutOptions"
                      class="text-center mb-4"
                    >
                      <v-btn
                        tile
                        depressed
                        small
                        color="primary"
                        @click="addLayoutOptions(layer)"
                      >
                        <span>Add Layout Options</span>
                      </v-btn>
                    </div>
                    <v-row v-else-if="layer.layoutOptions">
                      <v-col class="py-0">
                        <v-select
                          v-model="layer.layoutOptions.shape"
                          label="Shape"
                          :items="layoutShapes"
                        />
                      </v-col>
                      <v-col class="py-0">
                        <v-text-field
                          v-model="layer.layoutOptions.scale"
                          label="Scale"
                        />
                      </v-col>
                      <v-col class="py-0">
                        <v-text-field
                          v-model="layer.layoutOptions.fixedDistance"
                          label="Fixed Distance"
                        />
                      </v-col>
                    </v-row>

                    <div>
                      <span class="subtitle-1 grey--text text--darken-1">Nodes</span>
                    </div>
                    <div
                      v-if="!layer.nodes.length"
                      class="mb-4"
                    >
                      <span>No data available</span>
                    </div>
                    <div
                      v-else
                      class="text-center"
                      @click="pushMenu(0, layer)"
                    >
                      <v-btn>
                        <span>Show Nodes</span>
                      </v-btn>
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
                      >
                        <v-icon>mdi-plus</v-icon>
                      </v-btn>
                    </div>
                  </v-card-text>
                </div>
              </v-expand-transition>
            </v-card>
            <div
              v-if="editMode"
              class="text-center mb-4"
            >
              <v-btn
                fab
                depressed
                small
                color="primary"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </v-card-text>
        </div>
      </v-expand-transition>
    </v-card>

    <v-card
      v-for="(object, i) in detailMenus"
      :key="`object-${i}`"
      tile
      flat
      min-width="588"
      height="100%"
      class="ml-3 mb-3"
    >
      <v-card-title class="font-weight-regular">
        <span>{{ object.label || object.id }}</span>
        <v-spacer />
        <v-btn
          icon
          small
          @click="showAll.layers = !showAll.layers"
        >
          <v-icon>
            {{ showAll.layers ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
          </v-icon>
        </v-btn>
      </v-card-title>
      <v-expand-transition>
        <div v-show="showAll.layers">
          <v-card-text class="pt-0">
            <div
              v-for="(node, i) in object.nodes"
              :key="`node-${i}`"
            >
              <v-row>
                <v-col class="py-0">
                  <v-text-field
                    v-model="node.id"
                    label="ID"
                  />
                </v-col>
                <v-col class="py-0">
                  <v-text-field
                    v-model="node.label"
                    label="Label"
                  />
                </v-col>
                <v-col class="py-0">
                  <v-text-field
                    v-model="node.parentId"
                    label="Parent ID"
                  />
                </v-col>
              </v-row>

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
                      v-model="node.nodeOptions.size"
                      label="Size"
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
                    v-model="node.layoutOptions.scale"
                    label="Scale"
                  />
                </v-col>
                <v-col class="py-0">
                  <v-text-field
                    v-model="node.layoutOptions.fixedDistance"
                    label="Fixed Distance"
                  />
                </v-col>
              </v-row>
            </div>
          </v-card-text>
        </div>
      </v-expand-transition>
    </v-card>
  </div>
</template>

<style lang="scss" scoped>
.layers-card {
  overflow: scroll;
}
</style>

<script>
import networkSchema from '@/assets/NetworkSchema.json';

export default {
  name: 'LayersCard',
  props: {
    layers: {
      type: Array,
      required: true
    },
    editMode: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    showAll: {
      layers: false,
      layer: []
    },
    detailMenus: []
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
  mounted() {
    this.layers.forEach(() => {
      this.showAll.layer.push(false);
    });
  },
  methods: {
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
    pushMenu(index, object) {
      this.detailMenus.splice(index);
      this.detailMenus.push(object);
    }
  }
}
</script>
