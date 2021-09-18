<template>
  <div class="node-group pr-3 d-flex">
    <div class="node__reorder d-flex align-center">
      <v-icon class="my-auto mx-2">mdi-reorder-horizontal</v-icon>
    </div>
    <div class="node-group__contents ml-3">
      <div class="node-group__header d-flex mt-3 ml-3">
        <span>{{ nodeData.id }}</span>
      </div>
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
          @contextmenu.stop="showObjectMenu($event, nodeData.nodes, i)"
        >
          <node-block
            v-if="!node.nodes"
            :nodeData="node"
            :showObjectMenu="showObjectMenu"
          />
          <node-group
            v-else
            :nodeData="node"
            :showObjectMenu="showObjectMenu"
          />
        </div>
      </draggable>
    </div>
    <div class="d-flex">
      <div class="my-auto">
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
.node__reorder {
  outline: 2px solid #999;
  cursor: move;
}

.node-group {
  outline: 2px solid #999;
}
.node-group__contents {
  width: 100%;
}
.node-group__header {
  min-width: calc(100px + 12px);
}
.node-group__draggable {
  min-height: 100px;

  .node-group__node-wrapper {
    height: fit-content;
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
    showObjectMenu: {
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
