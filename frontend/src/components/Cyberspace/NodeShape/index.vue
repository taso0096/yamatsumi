<template>
  <CircleEntity
    v-if="node.nodeOptions.shape === 'circle'"
    :node="node"
    :topLabel="topLabel"
    :centerLabel="centerLabel"
    :bottomLabel="bottomLabel"
  />
  <SphereEntity
    v-else
    :node="node"
    :topLabel="topLabel"
    :bottomLabel="bottomLabel"
  />
</template>

<script>
import SphereEntity from './SphereEntity.vue';
import CircleEntity from './CircleEntity.vue';

export default {
  name: 'NodeShape',
  components: {
    SphereEntity,
    CircleEntity
  },
  props: {
    node: {
      type: Object
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
  }
};
</script>
