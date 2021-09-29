<template>
  <div>
    <v-menu
      v-model="contextMenu.isOpened"
      :position-x="contextMenu.x"
      :position-y="contextMenu.y"
      absolute
      offset-y
    >
      <v-list class="py-0">
        <v-list-item>
          <v-list-item-title>{{ selectedNode.id }}</v-list-item-title>
        </v-list-item>
        <v-divider />
        <v-list-item @click="setNode">
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

    <details-card
      v-if="selectedNodeCopy.id"
      :node="selectedNodeCopy"
      :isLayer="contextMenu.isLayer"
      :editMode="editMode"
    >
      <template #header>
        <v-card-title>
          <span>Details</span>
        </v-card-title>
      </template>
    </details-card>
  </div>
</template>

<script>
import DetailsCard from './DetailsCard';

export default {
  name: 'SelectModeDetailsCard',
  components: {
    DetailsCard
  },
  props: {
    routingTable: {
      type: Object,
      required: true
    },
    editMode: {
      type: Boolean,
      required: true
    }
  },
  data: () => ({
    contextMenu: {
      isOpened: false,
      x: 0,
      y: 0,
      array: [],
      index: 0,
      isLayer: false
    },
    selectedNodeCopy: {},
    editIntervalId: null,
    isChangedForm: false
  }),
  computed: {
    selectedNode() {
      return this.contextMenu.array[this.contextMenu.index] || {};
    }
  },
  watch: {
    selectedNodeCopy: {
      handler() {
        this.isChangedForm = true;
      },
      deep: true
    }
  },
  beforeDestroy() {
    clearInterval(this.editIntervalId);
  },
  methods: {
    init(network, index) {
      this.contextMenu.array = network;
      this.contextMenu.index = index;
      this.setNode(this.selectedNode);
    },
    openMenu(e, array, index, isLayer = false) {
      e.preventDefault();
      this.contextMenu.isOpened = false;
      this.contextMenu.x = e.clientX;
      this.contextMenu.y = e.clientY;
      this.contextMenu.array = array;
      this.contextMenu.index = index;
      this.contextMenu.isLayer = isLayer;
      this.$nextTick(() => {
        this.contextMenu.isOpened = true;
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
    },
    setNode() {
      clearInterval(this.editIntervalId);
      this.selectedNodeCopy = JSON.parse(JSON.stringify(this.selectedNode));
      this.selectedNodeCopy.ipaddresses = [...(this.routingTable[this.selectedNode.id] || [])];
      this.editIntervalId = setInterval(() => {
        if (this.isChangedForm) {
          this.updateNode();
          this.isChangedForm = false;
        }
      }, 1000);
    },
    updateNode() {
      if (this.selectedNode.id !== this.selectedNodeCopy.id) {
        delete this.routingTable[this.selectedNode.id];
      }
      for (const key in this.selectedNodeCopy) {
        if (key !== 'ipaddresses') {
          this.$set(this.selectedNode, key, this.selectedNodeCopy[key]);
          continue;
        }
        if (!this.selectedNodeCopy[key].length) {
          delete this.routingTable[this.selectedNodeCopy.id];
          continue;
        }
        this.routingTable[this.selectedNodeCopy.id] = [];
        this.routingTable[this.selectedNodeCopy.id].push(...this.selectedNodeCopy[key]);
      }
    }
  }
};
</script>
