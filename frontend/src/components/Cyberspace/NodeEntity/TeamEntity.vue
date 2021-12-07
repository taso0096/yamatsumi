<template>
  <a-entity :id="`team-${teamId}`">
    <node-shape-entity
      :node="node"
      :detailsLabel="teamId"
      :score="teamScore"
    />
  </a-entity>
</template>

<script>
import NodeShapeEntity from './NodeShapeEntity';

export default {
  name: 'TeamEntity',
  components: {
    NodeShapeEntity
  },
  props: {
    node: {
      type: Object,
      required: true
    }
  },
  computed: {
    sphereRadius: () => 0.2,
    teamId() {
      return this.node.nodeOptions.teamId;
    },
    teamScore() {
      return this.$_visualizeData.exercise.scores[this.teamId]?.score;
    }
  }
};
</script>
