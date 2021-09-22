<template>
  <div class="node-group">
    <v-sheet class="d-flex align-center pa-3">
      <v-icon class="node__reorder mr-3">mdi-drag</v-icon>
      <span>{{ nodeData.id }}</span>
    </v-sheet>
    <div class="d-flex px-3">
      <draggable
        v-bind="dragOptions"
        :list="nodeData.nodes"
        :group="{ name: 'network' }"
        handle=".node__reorder"
        class="node-group__draggable d-flex my-3"
      >
        <div
          v-for="(node, i) in nodeData.nodes"
          :key="`nodes-group__${node.id}_${i}`"
          class="node-group__node-wrapper d-flex mx-3 my-auto"
          @contextmenu.stop="openContextMenu($event, nodeData.nodes, i)"
        >
          <node-block
            v-if="!node.nodes"
            :nodeData="node"
          />
          <node-group
            v-else
            :nodeData="node"
            :openContextMenu="openContextMenu"
          />
        </div>
      </draggable>
      <div class="my-auto ml-auto">
        <v-btn
          icon
          class="d-flex"
          @click="addNode(nodeData.nodes)"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
        <v-btn
          icon
          class="d-flex"
          @click="addGroup(nodeData.nodes)"
        >
          <v-icon>mdi-shape-square-plus</v-icon>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.node-group {
  outline: 2px solid #bdbdbd;

  .node__reorder {
    cursor: move;
  }
  .node-group__draggable {
    min-width: calc(100px + 24px);
    min-height: 100px;

    .node-group__node-wrapper {
      height: fit-content;
    }
  }
}
</style>

<script>
import draggable from 'vuedraggable';
import NodeBlock from './NodeBlock.vue';
import NodeGroup from './NodeGroup.vue';

export default {
  name: 'NodeGroup',
  components: {
    draggable,
    NodeBlock,
    NodeGroup
  },
  props: {
    nodeData: {
      type: Object,
      required: true
    },
    openContextMenu: {
      type: Function,
      required: true
    }
  },
  computed: {
    dragOptions() {
      return {
        animation: 200,
        disabled: false,
        ghostClass: 'ghost'
      };
    }
  },
  methods: {
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
