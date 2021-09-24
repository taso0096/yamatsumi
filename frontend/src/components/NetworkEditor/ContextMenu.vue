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
        <v-list-item @click="detailsDialog = true">
          <v-list-item-title>Details</v-list-item-title>
        </v-list-item>
        <v-list-item @click="deleteNode">
          <v-list-item-title class="error--text">Delete</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-dialog
      v-model="detailsDialog"
      :key="selectedNode.id"
      width="500"
    >
      <details-card
        :node="selectedNode"
        :isLayer="contextMenu.isLayer"
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
  </div>
</template>

<script>
import DetailsCard from './DetailsCard';

export default {
  name: 'ContextMenu',
  components: {
    DetailsCard
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
    detailsDialog: false
  }),
  computed: {
    selectedNode() {
      return this.contextMenu.array[this.contextMenu.index] || {};
    }
  },
  methods: {
    open(e, array, index, isLayer = false) {
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
      this.contextMenu.array.splice(this.contextMenu.index, 1);
    }
  }
};
</script>
