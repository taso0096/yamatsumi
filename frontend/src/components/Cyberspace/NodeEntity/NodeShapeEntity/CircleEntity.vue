<template>
  <a-circle
    :color="node.nodeOptions.nodeColor"
    side="double"
    :radius="circleRadius*node.nodeOptions.size"
  >
    <a-ring
      :color="node.nodeOptions.nodeColor"
      side="double"
      :radius-inner="circleRadius*node.nodeOptions.size*1.025"
      :radius-outer="circleRadius*node.nodeOptions.size*1.05"
    />
    <a-ring
      :color="node.nodeOptions.nodeColor"
      side="double"
      :radius-inner="circleRadius*node.nodeOptions.size*1.075"
      :radius-outer="circleRadius*node.nodeOptions.size*1.175"
    />
    <a-text
      v-if="topLabel !== null"
      :value="topLabel"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`0 ${circleRadius*node.nodeOptions.size + circleRadius} 0`"
      wrap-count="50"
    />
    <a-text
      v-if="centerLabel !== null"
      :value="centerLabel || node.label"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      position="0 0.01 0"
      wrap-count="50"
    />
    <a-text
      v-if="bottomLabel !== null"
      :value="bottomLabel"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`0 ${-circleRadius*node.nodeOptions.size - circleRadius} 0`"
      wrap-count="50"
    />
  </a-circle>
</template>

<script>
export default {
  name: 'CircleEntity',
  props: {
    node: {
      type: Object,
      required: true
    },
    topLabel: {
      type: [String, Number],
      required: false
    },
    centerLabel: {
      type: [String, Number],
      required: false
    },
    bottomLabel: {
      type: [String, Number],
      required: false
    }
  },
  computed: {
    circleRadius: () => 0.2
  }
};
</script>
