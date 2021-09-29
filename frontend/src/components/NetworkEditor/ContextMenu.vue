<template>
  <v-menu
    v-model="contextMenu"
    :position-x="position.x"
    :position-y="position.y"
    absolute
    offset-y
  >
    <v-list class="py-0">
      <v-list-item>
        <v-list-item-title>{{ selectedNode.id }}</v-list-item-title>
      </v-list-item>
      <v-divider />
      <v-list-item @click="openDetails(node.array, node.index, node.isLayer)">
        <v-list-item-title>Details</v-list-item-title>
      </v-list-item>
      <v-list-item
        v-if="editMode"
        @click="deleteNode"
      >
        <v-list-item-title class="error--text">Delete</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  name: 'ContextMenu',
  props: {
    openDetails: {
      type: Function,
      required: true
    },
    editMode: {
      type: Boolean,
      required: true
    }
  },
  data: () => ({
    resolve: null,
    contextMenu: false,
    position: {
      x: 0,
      y: 0
    },
    node: {
      array: [],
      index: 0,
      isLayer: false
    }
  }),
  computed: {
    selectedNode() {
      return this.node.array[this.node.index] || {};
    }
  },
  methods: {
    open(e, array, index, isLayer = false) {
      return new Promise(resolve => {
        this.resolve = resolve;
        e.preventDefault();
        this.contextMenu = false;
        this.position.x = e.clientX;
        this.position.y = e.clientY;
        this.node.array = array;
        this.node.index = index;
        this.node.isLayer = isLayer;
        this.$nextTick(() => {
          this.contextMenu = true;
        });
      });
    },
    async deleteNode() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: `Are you sure you want to delete the "${this.selectedNode.id}"?`,
        confirmText: 'delete',
        color: 'error'
      });
      if (!isConfirmed) {
        return;
      }
      delete this.routingTable[this.selectedNode.id];
      this.contextMenu.array.splice(this.contextMenu.index, 1);
      this.resolve();
    }
  }
};
</script>
