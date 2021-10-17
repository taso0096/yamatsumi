<template>
  <div class="node-group">
    <v-sheet class="d-flex align-center pa-3">
      <v-icon
        v-if="editMode"
        class="node__reorder mr-3"
      >mdi-drag</v-icon>
      <span>{{ node.id }}</span>
    </v-sheet>
    <div class="d-flex px-3">
      <draggable
        v-bind="dragOptions"
        :list="node.nodes"
        :group="{ name: 'network' }"
        handle=".node__reorder"
        class="node-group__draggable d-flex my-3"
      >
        <div
          v-for="(childNode, i) in node.nodes"
          :key="`nodes-group__${node.id}_${i}`"
          class="node-group__node-wrapper d-flex mx-3 my-auto"
          @contextmenu.stop="openContextMenu($event, node.nodes, i)"
          @dblclick.stop="openDetails(node.nodes, i)"
        >
          <node-block
            v-if="!childNode.nodes"
            :node="childNode"
            :editMode="editMode"
          />
          <group-block
            v-else
            :node="childNode"
            :openContextMenu="openContextMenu"
            :openDetails="openDetails"
            :editMode="editMode"
          />
        </div>
      </draggable>
      <div
        v-if="editMode"
        class="my-auto ml-auto"
      >
        <v-btn
          icon
          class="d-flex"
          @click="addNode(node.nodes)"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
        <v-btn
          icon
          class="d-flex"
          @click="addGroup(node.nodes)"
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
import GroupBlock from './GroupBlock.vue';

export default {
  name: 'GroupBlock',
  components: {
    draggable,
    NodeBlock,
    GroupBlock
  },
  props: {
    node: {
      type: Object,
      required: true
    },
    openContextMenu: {
      type: Function,
      required: true
    },
    openDetails: {
      type: Function,
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
