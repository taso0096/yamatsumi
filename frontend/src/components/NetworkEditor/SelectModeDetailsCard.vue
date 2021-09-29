<template>
  <div>
    <details-card
      v-if="selectedNodeCopy.id"
      :node="selectedNodeCopy"
      :isLayer="isLayer"
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
    detailsDialog: false,
    selectedNode: {},
    selectedNodeCopy: {},
    isLayer: false,
    editIntervalId: null,
    isChangedForm: false
  }),
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
    open(array, index, isLayer) {
      clearInterval(this.editIntervalId);
      this.isLayer = isLayer;
      this.selectedNode = array[index];
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
