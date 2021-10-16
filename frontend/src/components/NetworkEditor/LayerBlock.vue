<template>
  <div class="layer-block d-flex">
    <v-sheet
      v-if="editMode && !selectMode"
      class="layer-block__reorder d-flex align-center"
    >
      <v-icon class="my-auto mx-2">mdi-reorder-horizontal</v-icon>
    </v-sheet>
    <div class="layer-block__contents">
      <v-sheet class="d-flex align-center pa-3 pl-5">
        <slot name="header">
          <span>{{ layer.id }}</span>
        </slot>
      </v-sheet>
      <v-sheet
        color="transparent"
        class="layer-block__blur"
      >
        <div class="layer-block__draggable-wrapper d-flex px-3">
          <draggable
            v-bind="dragOptions"
            :list="layer.nodes"
            :group="{ name: 'network' }"
            handle=".node__reorder"
            class="layer-block__draggable d-flex py-3"
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
              <group-block
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
</template>

<style lang="scss" scoped>
.layer-block {
  margin: 2px;
  outline: 2px solid #bdbdbd;

  .layer-block__reorder {
    outline: 2px solid #bdbdbd;
    cursor: move;
    z-index: 100;
  }
  .layer-block__reorder + .layer-block__contents {
    width: calc(100% - 40px) !important;
  }
  .layer-block__contents {
    width: 100%;

    .layer-block__blur {
      position: relative;

      .layer-block__draggable-wrapper {
        min-height: calc(100px + 24px);
        overflow-x: scroll;

        .layer-block__draggable {
          min-height: 100px;

          .network-editor__node-wrapper {
            height: fit-content;
          }
        }
      }
    }
    .layer-block__blur:before {
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
    .layer-block__blur:after {
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
    .theme--dark.layer-block__blur:before {
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
    .theme--dark.layer-block__blur:after {
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
</style>

<script>
import draggable from 'vuedraggable';
import NodeBlock from './NodeBlock.vue';
import GroupBlock from './GroupBlock.vue';

export default {
  name: 'LayerBlock',
  components: {
    draggable,
    NodeBlock,
    GroupBlock
  },
  props: {
    layer: {
      type: Object,
      required: true
    },
    openContextMenu: {
      type: Function,
      required: true
    },
    editMode: {
      type: Boolean,
      required: true
    },
    selectMode: {
      type: Boolean,
      default: false
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
    }
  }
};
</script>
