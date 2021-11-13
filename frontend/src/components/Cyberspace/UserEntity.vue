<template>
  <a-entity>
    <a-entity
      v-for="user in users"
      :key="user.id"
      :id="`user-entity__${user.id}`"
      :position="user.position"
      :look-center="`parentSelector: #node-${node.id}`"
    >
      <a-sphere
        :radius="node.nodeOptions.size"
      >
        <a-text
          :value="user.id"
          align="center"
          :color="node.nodeOptions.labelColor"
          side="double"
          :position="`0 ${-node.nodeOptions.size - sphereRadius} 0`"
          wrap-count="50"
        />
        <a-text
          v-if="user.score !== null"
          :value="$_visualizeData.exercise.scores[user.teamId].users[user.id]"
          align="center"
          :color="node.nodeOptions.labelColor"
          side="double"
          :position="`0 ${node.nodeOptions.size + sphereRadius} 0`"
          wrap-count="50"
        />
      </a-sphere>
    </a-entity>
  </a-entity>
</template>

<script>
export default {
  name: 'LayerEntity',
  props: {
    node: {
      type: Object,
      required: true
    },
    users: {
      type: Array,
      required: true
    },
    shape: {
      type: String,
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
      this.calcPosition(this.shape);
    },
    calcPosition(shape = 'circle') {
      const calcFunctions = {
        square: this.calcSquarePosition,
        circle: this.calcCirclePosition
      };
      calcFunctions[shape]();
    },
    calcSquarePosition() {
      const nodeCount = this.users.length;
      const edgeMaxLength = Math.ceil(Math.sqrt(nodeCount)) - 1;
      const gap = 1;
      this.users.forEach((_, i) => {
        const x = (edgeMaxLength - i%(edgeMaxLength + 1))*gap - edgeMaxLength*gap/2;
        const z = (edgeMaxLength - Math.floor(i/(edgeMaxLength + 1)))*gap - (edgeMaxLength - (nodeCount/(edgeMaxLength + 1) - 1)/2)*gap;
        this.$set(this.users[i], 'position', new THREE.Vector3(x, 0, z));
      });
    },
    calcCirclePosition() {
      const nodeCount = this.users.length;
      const radius = nodeCount === 1 ? 1e-100 : this.node.nodeOptions.size*nodeCount*0.8;
      this.users.forEach((_, i) => {
        const theta = 2*Math.PI*i/nodeCount + Math.PI/2;
        const x = radius*Math.cos(theta);
        const z = radius*Math.sin(theta);
        this.$set(this.users[i], 'position', new THREE.Vector3(x, 0, z));
      });
    }
  }
};
</script>
