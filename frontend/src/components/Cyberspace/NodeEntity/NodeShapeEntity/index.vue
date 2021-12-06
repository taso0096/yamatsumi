<template>
  <circle-entity
    v-if="node.nodeOptions.shape === 'circle'"
    :node="node"
    :detailsLabel="detailsLabel"
    :score="score"
  />
  <sphere-entity
    v-else
    :node="node"
    :detailsLabel="detailsLabel"
    :score="score"
  />
</template>

<script>
import SphereEntity from './SphereEntity.vue';
import CircleEntity from './CircleEntity.vue';

export default {
  name: 'NodeShapeEntity',
  components: {
    SphereEntity,
    CircleEntity
  },
  props: {
    node: {
      type: Object
    },
    detailsLabel: {
      type: [String, Number],
      required: false
    },
    score: {
      type: Number,
      required: false
    }
  }
};
</script>
