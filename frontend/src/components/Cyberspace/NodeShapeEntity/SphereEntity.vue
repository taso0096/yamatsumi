<template>
  <a-sphere
    :radius="sphereRadius*node.nodeOptions.size"
    :color="node.nodeOptions.nodeColor"
  >
    <a-text
      v-if="topLabel !== null"
      :value="topLabel"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`0 ${sphereRadius*node.nodeOptions.size + sphereRadius} 0`"
      wrap-count="50"
    />
    <a-text
      v-if="bottomLabel !== null"
      :value="bottomLabel || node.label"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`0 ${-sphereRadius*node.nodeOptions.size - sphereRadius} 0`"
      wrap-count="50"
    />
  </a-sphere>
</template>

<script>
export default {
  name: 'SphereEntity',
  props: {
    node: {
      type: Object,
      required: true
    },
    topLabel: {
      type: [String, Number],
      required: false
    },
    bottomLabel: {
      type: [String, Number],
      required: false
    }
  },
  computed: {
    sphereRadius: () => 0.2
  }
};
</script>
