<template>
  <a-entity>
    <a-entity
      :position="getTreeVecter(node.nodeOptions.position)"
      :rotation="getTreeVecter(node.nodeOptions.rotation)"
    >
      <circle-entity
        v-if="node.nodeOptions.shape === 'circle'"
        :node="node"
        :detailsLabel="detailsLabel"
        :score="score"
        :percentage="percentage"
      />
      <text-entity
        v-else-if="node.nodeOptions.shape === 'text'"
        :node="node"
        :detailsLabel="detailsLabel"
        :score="score"
      />
      <polyhedron-entity
        v-else-if="node.nodeOptions.shape === 'polyhedron'"
        :node="node"
        :detailsLabel="detailsLabel"
        :score="score"
        :percentage="percentage"
      />
      <sphere-entity
        v-else
        :node="node"
        :detailsLabel="detailsLabel"
        :score="score"
        :percentage="percentage"
      />
    </a-entity>
  </a-entity>
</template>

<script>
import SphereEntity from './SphereEntity.vue';
import CircleEntity from './CircleEntity.vue';
import TextEntity from './TextEntity.vue';
import PolyhedronEntity from '@/components/Cyberspace/NodeEntity/NodeShapeEntity/PolyhedronEntity.vue';

export default {
  name: 'NodeShapeEntity',
  components: {
    SphereEntity,
    CircleEntity,
    TextEntity,
    PolyhedronEntity
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
    },
    percentage: {
      type: Number,
      default: 0
    }
  },
  methods: {
    getTreeVecter(vecter) {
      return new THREE.Vector3(vecter?.x, vecter?.y, vecter?.z);
    }
  }
};
</script>
