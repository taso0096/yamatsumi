<template>
  <v-menu
    v-model="contextMenu.isOpened"
    :position-x="contextMenu.x"
    :position-y="contextMenu.y"
    absolute
    offset-y
  >
    <v-list class="py-0">
      <v-list-item>
        <v-list-item-title>{{ selectedObject.id }}</v-list-item-title>
      </v-list-item>
      <v-divider />
      <v-list-item>
        <v-list-item-title>Edit</v-list-item-title>
      </v-list-item>
      <v-list-item @click="deleteObject">
        <v-list-item-title class="error--text">Delete</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  name: 'ContextMenu',
  data: () => ({
    contextMenu: {
      isOpened: false,
      x: 0,
      y: 0,
      array: [],
      index: 0
    }
  }),
  computed: {
    selectedObject() {
      return this.contextMenu.array[this.contextMenu.index] || {};
    }
  },
  methods: {
    open(e, array, index) {
      e.preventDefault();
      this.contextMenu.isOpened = false;
      this.contextMenu.x = e.clientX;
      this.contextMenu.y = e.clientY;
      this.contextMenu.array = array;
      this.contextMenu.index = index;
      this.$nextTick(() => {
        this.contextMenu.isOpened = true;
      });
    },
    async deleteObject() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: `Are you sure you want to delete the "${this.selectedObject.id}"?`,
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
