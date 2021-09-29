<template>
  <v-dialog
    v-model="detailsDialog"
    :key="selectedNode.id"
    width="500"
  >
    <details-card
      :node="selectedNodeCopy"
      :isLayer="isLayer"
      :editMode="editMode"
    >
      <template #header>
        <v-card-title>
          <span>Details</span>
          <v-spacer />
          <v-btn
            icon
            @click="detailsDialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
      </template>
    </details-card>
  </v-dialog>
</template>

<script>
import DetailsCard from './DetailsCard';

export default {
  name: 'DetailsDialog',
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
    isLayer: false
  }),
  watch: {
    detailsDialog(val) {
      if (!val) {
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
  },
  methods: {
    open(array, index, isLayer = false) {
      this.detailsDialog = false;
      this.isLayer = isLayer;
      this.selectedNode = array[index];
      this.selectedNodeCopy = JSON.parse(JSON.stringify(this.selectedNode));
      this.selectedNodeCopy.ipaddresses = [...(this.routingTable[this.selectedNode.id] || [])];
      this.detailsDialog = true;
    }
  }
};
</script>
