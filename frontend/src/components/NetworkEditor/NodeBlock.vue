<template>
  <v-card
    :id="`node__${nodeData.id}`"
    class="node-block node__reorder"
  >
    <v-card-title>{{ nodeData.id }}</v-card-title>
  </v-card>
</template>

<style scoped>
.node-block {
  width: 100px;
  height: 100px;
}
.node__reorder {
  outline: 2px solid #bdbdbd;
  cursor: move;
}
</style>

<script>
export default {
  name: 'NodeBlock',
  props: {
    nodeData: {
      type: Object,
      required: true
    },
    showObjectMenu: {
      type: Function,
      required: true
    }
  }
};
</script>
