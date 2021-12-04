<template>
  <a-sphere
    :radius="sphereRadius*node.nodeOptions.size"
  >
    <a-text
      v-if="labelBottom !== null"
      :value="labelBottom || node.label"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`0 ${-sphereRadius*node.nodeOptions.size - sphereRadius} 0`"
      wrap-count="50"
    />
    <a-text
      v-if="labelTop !== null"
      :value="labelTop"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`0 ${sphereRadius*node.nodeOptions.size + sphereRadius} 0`"
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
    labelBottom: {
      type: [String, Number],
      required: false
    },
    labelTop: {
      type: [String, Number],
      required: false
    }
  },
  computed: {
    sphereRadius: () => 0.2
  }
};
</script>
