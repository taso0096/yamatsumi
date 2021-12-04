<template>
  <a-entity>
    <a-entity
      v-for="user in (node.nodeOptions.users || [])"
      :key="user.id"
      :id="`node-${user.id}`"
      :position="user.position"
      :look-center="node.nodeOptions.layoutOptions.shape !== 'square' && `parentSelector: #node-${node.id}`"
    >
      <SphereEntity
        :node="node"
        :bottomLabel="user.id"
        :topLabel="getUserScore(user)"
      />
    </a-entity>
  </a-entity>
</template>

<script>
import SphereEntity from './NodeShape/SphereEntity.vue';

export default {
  name: 'LayerEntity',
  components: {
    SphereEntity
  },
  props: {
    node: {
      type: Object,
      required: true
    }
  },
  computed: {
    sphereRadius: () => 0.2
  },
  mounted() {
    this.init();
  },
  methods: {
    async init() {
      const nodeOptions = this.node.nodeOptions;
      const scores = this.$_visualizeData.exercise.scores;
      const users = [];
      for (const [teamId, team] of Object.entries(scores)) {
        users.push(
          ...Object.entries(team.users)
            .filter(([id]) => nodeOptions?.users.includes(id))
            .map(([id, score]) => ({ id, score, teamId }))
        );
      }
      this.$set(nodeOptions, 'users', users);
      this.$set(nodeOptions, 'layoutOptions', {
        shape: nodeOptions.layoutOptions.shape || 'circle',
        scale: nodeOptions.layoutOptions.scale || 1,
        fixedDistance: nodeOptions.layoutOptions.fixedDistance
      });
      this.calcPosition(nodeOptions.layoutOptions.shape);
    },
    calcPosition(shape) {
      const calcFunctions = {
        square: this.calcSquarePosition,
        circle: this.calcCirclePosition
      };
      calcFunctions[shape]();
    },
    calcSquarePosition() {
      const nodeCount = this.node.nodeOptions.users.length;
      const edgeMaxLength = Math.ceil(Math.sqrt(nodeCount)) - 1;
      const gap = 1.5;
      this.node.nodeOptions.users.forEach((_, i) => {
        const x = (edgeMaxLength - i%(edgeMaxLength + 1))*gap - edgeMaxLength*gap/2;
        const z = (edgeMaxLength - Math.floor(i/(edgeMaxLength + 1)))*gap - (edgeMaxLength - (nodeCount/(edgeMaxLength + 1) - 1)/2)*gap;
        this.$set(this.node.nodeOptions.users[i], 'position', new THREE.Vector3(x, 0, z));
      });
    },
    calcCirclePosition() {
      const nodeCount = this.node.nodeOptions.users.length;
      const radius = nodeCount === 1 ? 1e-100 : this.node.nodeOptions.layoutOptions.scale*nodeCount*0.8;
      this.node.nodeOptions.users.forEach((_, i) => {
        const theta = 2*Math.PI*i/nodeCount + Math.PI/2;
        const x = radius*Math.cos(theta);
        const z = radius*Math.sin(theta);
        this.$set(this.node.nodeOptions.users[i], 'position', new THREE.Vector3(x, 0, z));
      });
    },
    getUserScore(user) {
      return this.$_visualizeData.exercise.scores[user.teamId]?.users[user.id];
    }
  }
};
</script>
