<template>
  <div class="network-editor">
    <draggable
      :list="network"
      v-bind="dragOptions"
      handle=".network-editor__layer__reorder"
      class="network-editor__draggable"
    >
      <div
        v-for="(layer, i) in network"
        :key="`layer__${layer.id}_${i}`"
        class="network-editor__layer d-flex my-3"
        @contextmenu.stop="openContextMenu($event, network, i, true)"
      >
        <v-sheet
          v-if="editMode"
          class="network-editor__layer__reorder d-flex align-center"
        >
          <v-icon class="my-auto mx-2">mdi-reorder-horizontal</v-icon>
        </v-sheet>
        <div class="network-editor__layer__contents">
          <v-sheet class="d-flex align-center pa-3 pl-5">
            <span>{{ layer.id }}</span>
          </v-sheet>
          <v-sheet
            color="transparent"
            class="network-editor__layer__blur"
          >
            <div class="network-editor__layer__draggable-wrapper d-flex px-3">
              <draggable
                v-bind="dragOptions"
                :list="layer.nodes"
                :group="{ name: 'network' }"
                handle=".node__reorder"
                class="network-editor__layer__draggable d-flex py-3"
              >
                <div
                  v-for="(node, j) in layer.nodes"
                  :key="`layer__${node.id}_${j}`"
                  class="network-editor__node-wrapper d-flex mx-3 my-auto"
                  @contextmenu.stop="openContextMenu($event, layer.nodes, j)"
                >
                  <node-block
                    v-if="!node.nodes"
                    :node="node"
                    :editMode="editMode"
                  />
                  <node-group
                    v-else
                    :node="node"
                    :openContextMenu="openContextMenu"
                    :editMode="editMode"
                  />
                </div>
              </draggable>
              <div
                v-if="editMode"
                class="my-auto mr-auto"
              >
                <v-btn
                  icon
                  class="d-flex"
                  @click="addNode(layer.nodes)"
                >
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
                <v-btn
                  icon
                  class="d-flex"
                  @click="addGroup(layer.nodes)"
                >
                  <v-icon>mdi-shape-square-plus</v-icon>
                </v-btn>
              </div>
            </div>
          </v-sheet>
        </div>
      </div>
      <div
        v-if="editMode"
        slot="footer"
        class="d-flex justify-center"
      >
        <v-btn
          depressed
          color="secondary"
          class="ma-3"
          @click="addLayer"
        >
          <span>Add Layer</span>
        </v-btn>
      </div>
    </draggable>

    <context-menu
      ref="contextMenu"
      :editMode="editMode"
    />
  </div>
</template>

<style lang="scss" scoped>
.network-editor {
  .network-editor__layer {
    outline: 2px solid #bdbdbd;

    .network-editor__layer__reorder {
      outline: 2px solid #bdbdbd;
      cursor: move;
      z-index: 100;
    }
    .network-editor__layer__reorder + .network-editor__layer__contents {
      width: calc(100% - 40px) !important;
    }
    .network-editor__layer__contents {
      width: 100%;

      .network-editor__layer__blur {
        position: relative;

        .network-editor__layer__draggable-wrapper {
          min-height: calc(100px + 24px);
          overflow-x: scroll;

          .network-editor__layer__draggable {
            min-height: 100px;

            .network-editor__node-wrapper {
              height: fit-content;
            }
          }
        }
      }
      .network-editor__layer__blur:before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 25px;
        height: 100%;
        background: linear-gradient(to left, rgba(0, 0, 0, 0), #eee 90%);
        pointer-events: none;
        z-index: 1;
      }
      .network-editor__layer__blur:after {
        content: '';
        position: absolute;
        bottom: 0;
        right: 0;
        width: 25px;
        height: 100%;
        background: linear-gradient(to right, rgba(0, 0, 0, 0), #eee 90%);
        pointer-events: none;
        z-index: 1;
      }
      .theme--dark.network-editor__layer__blur:before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 25px;
        height: 100%;
        background: linear-gradient(to left, rgba(0, 0, 0, 0), #303030 90%);
        pointer-events: none;
        z-index: 1;
      }
      .theme--dark.network-editor__layer__blur:after {
        content: '';
        position: absolute;
        bottom: 0;
        right: 0;
        width: 25px;
        height: 100%;
        background: linear-gradient(to right, rgba(0, 0, 0, 0), #303030 90%);
        pointer-events: none;
        z-index: 1;
      }
    }
  }
}
</style>

<script>
import draggable from 'vuedraggable';
import NodeBlock from './NodeBlock.vue';
import NodeGroup from './NodeGroup.vue';
import ContextMenu from './ContextMenu.vue';

export default {
  name: 'NetworkEditor',
  components: {
    draggable,
    NodeBlock,
    NodeGroup,
    ContextMenu
  },
  props: {
    network: {
      type: Array,
      required: true
    },
    editMode: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    dragOptions() {
      return {
        animation: 200,
        disabled: !this.editMode,
        ghostClass: 'ghost'
      };
    }
  },
  methods: {
    addLayer() {
      this.network.push({
        id: `layer${this.network.length + 1}`,
        nodes: []
      });
    },
    addGroup(nodes) {
      nodes.push({
        id: `group${nodes.length + 1}`,
        nodes: []
      });
    },
    addNode(nodes) {
      nodes.push({
        id: `node${nodes.length + 1}`
      });
    },
    openContextMenu(e, array, index, isLayer = false) {
      this.$refs.contextMenu.open(e, array, index, isLayer);
    }
  }
};
</script>
