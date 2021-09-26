<template>
  <v-card
    :id="`node__${node.id}`"
    class="node-block"
    :class="{
      node__reorder: editMode
    }"
  >
    <v-card-title>{{ node.id }}</v-card-title>
  </v-card>
</template>

<style lang="scss" scoped>
.node-block {
  width: 100px;
  height: 100px;
  outline: 2px solid #bdbdbd;
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
