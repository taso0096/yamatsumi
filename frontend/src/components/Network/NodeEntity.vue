<template>
  <a-entity v-if="!validNode.label"></a-entity>
  <a-entity v-else>
    <a-sphere
      :radius="sphereRadius*validNode.size"
      :color="validNode.nodeColor"
    >
      <a-text
        :value="validNode.label"
        align="center"
        :color="validNode.labelColor"
        side="double"
        :position="`0 ${-sphereRadius*validNode.size - sphereRadius} 0`"
        wrap-count="50"
      />
    </a-sphere>
  </a-entity>
</template>

<script>
export default {
  name: 'NodeEntity',
  props: {
    node: {
      type: Object
    }
  },
  data: () => ({
    validNode: {}
  }),
  computed: {
    sphereRadius: () => 0.2
  },
  mounted() {
    this.$set(this.validNode, 'label', this.node.label || this.node.id);
    this.$set(this.validNode, 'type', this.node.nodeOptions?.type || 'sphere');
    this.$set(this.validNode, 'size', this.node.nodeOptions?.size || 1);
    this.$set(this.validNode, 'nodeColor', this.node.nodeOptions?.nodeColor || '#fff');
    this.$set(this.validNode, 'labelColor', this.node.nodeOptions?.labelColor || '#fff');
  }
};
</script>
