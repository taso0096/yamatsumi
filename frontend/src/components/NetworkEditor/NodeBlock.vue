<template>
  <v-sheet
    :id="`node__${node.id}`"
    class="node-block pa-3"
    :class="{
      node__reorder: editMode
    }"
  >
    <span>{{ node.id }}</span>
  </v-sheet>
</template>

<style lang="scss" scoped>
.node-block {
  width: 100px;
  height: 100px;
  outline: 2px solid #bdbdbd;

  span {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    word-break: break-all;
  }
}
.node__reorder {
  cursor: move;
}
</style>

<script>
export default {
  name: 'NodeBlock',
  props: {
    node: {
      type: Object,
      required: true
    },
    editMode: {
      type: Boolean,
      required: true
    }
  }
};
</script>
