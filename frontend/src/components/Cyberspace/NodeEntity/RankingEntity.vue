<template>
  <a-entity>
    <a-entity
      v-for="(team, i) in ranking"
      :key="i"
      :position="`0 ${(-i*node.nodeOptions.fontSize + (ranking.length/2)*node.nodeOptions.fontSize)/2} 0`"
    >
      <node-shape-entity
        :node="node"
        :detailsLabel="`${i + 1} - ${team.id} : ${team.score}`"
        textAlign="left"
      />
    </a-entity>
  </a-entity>
</template>

<script>
import NodeShapeEntity from './NodeShapeEntity';

export default {
  name: 'RankingEntity',
  components: {
    NodeShapeEntity
  },
  props: {
    node: {
      type: Object
    }
  },
  computed: {
    ranking() {
      return Object.entries(this.$_visualizeData.exercise.scores)
        .map(([teamId, team]) => ({ id: teamId, score: team.score }))
        .sort((a, b) => b.score - a.score);
    }
  }
};
</script>
