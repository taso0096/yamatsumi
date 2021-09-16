<template>
  <v-card
    v-if="!nodeData.nodes"
    :id="`node__${nodeData.id}`"
    class="node-block node-block__card node-block__reorder my-auto mx-3"
  >
    <v-card-title>{{ nodeData.id }}</v-card-title>
  </v-card>
  <div
    v-else
    class="node-block node-block__nodes-group my-auto mx-3 pr-3 d-flex"
  >
    <div class="node-block__reorder d-flex align-center">
      <v-icon class="my-auto mx-2">mdi-reorder-horizontal</v-icon>
    </div>
    <div class="node-block__nodes-group__contents ml-3">
      <div class="node-block__nodes-group__header d-flex mt-3 ml-3">
        <span>{{ nodeData.id }}</span>
      </div>
      <draggable
        v-bind="dragOptions"
        :list="nodeData.nodes"
        :group="{ name: 'network' }"
        handle=".node-block__reorder"
        class="node-block__nodes-group__draggable d-flex my-3"
      >
        <div
          v-for="(node, i) in nodeData.nodes"
          :key="`nodes-group__${node.id}_${i}`"
          class="d-flex"
          @contextmenu.stop="showObjectMenu($event, nodeData.nodes, i)"
        >
          <node-block
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

<style scoped>
.node-block__reorder {
  outline: 2px solid #999;
  cursor: move;
}

.node-block__card {
  width: 100px;
  height: 100px;
}

.node-block__nodes-group {
  outline: 2px solid #999;
}
.node-block__nodes-group__contents {
  width: 100%;
}
.node-block__nodes-group__header {
  min-width: calc(100px + 12px);
}
.node-block__nodes-group__draggable {
  min-height: 100px;
}
</style>

<script>
import draggable from 'vuedraggable';
import NodeBlock from './NodeBlock.vue';

export default {
  name: 'NodeBlock',
  components: {
    draggable,
    NodeBlock
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
