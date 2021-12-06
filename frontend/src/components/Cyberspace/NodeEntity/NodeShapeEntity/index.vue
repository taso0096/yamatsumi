<template>
  <a-entity
    :position="getTreeVecter(node.nodeOptions.position)"
    :rotation="getTreeVecter(node.nodeOptions.rotation)"
  >
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
  </a-entity>
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
  },
  methods: {
    getTreeVecter(vecter) {
      return new THREE.Vector3(vecter?.x, vecter?.y, vecter?.z);
    }
  }
};
</script>
