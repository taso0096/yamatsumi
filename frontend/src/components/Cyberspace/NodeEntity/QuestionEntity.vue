<template>
  <a-entity
    :id="`question-entity__${node.id}`"
  >
    <a-text
      :value="node.label"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`0 ${-sphereRadius*node.nodeOptions.layoutOptions.scale - sphereRadius/2} 0`"
      wrap-count="50"
    />
    <a-entity
      v-for="question in questions"
      :key="question.id"
      :id="`question__${question.id}`"
      :position="question.position"
      :look-center="node.nodeOptions.layoutOptions.shape !== 'square' && `parentSelector: question-entity__${node.id}`"
    >
      <node-shape-entity
        :node="node"
        :detailsLabel="question.id"
      />
    </a-entity>
  </a-entity>
</template>

<script>
import NodeShapeEntity from './NodeShapeEntity';

export default {
  name: 'QuestionEntity',
  components: {
    NodeShapeEntity
  },
  props: {
    node: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    questions: []
  }),
  computed: {
    sphereRadius: () => 0.65
  },
  mounted() {
    const nodeOptions = this.node.nodeOptions;
    const allQuestions = JSON.parse(JSON.stringify(this.$_visualizeData.exercise.questions));
    nodeOptions.levels.forEach(levelId => {
      this.questions.push(...allQuestions.filter(q => q.levelId === levelId));
    });
    nodeOptions.categories.forEach(categoryId => {
      this.questions.push(...allQuestions.filter(q => q.categoryId === categoryId));
    });

    this.$set(nodeOptions, 'layoutOptions', {
      shape: nodeOptions.layoutOptions.shape || 'circle',
      scale: nodeOptions.layoutOptions.scale || 1,
      fixedDistance: nodeOptions.layoutOptions.fixedDistance
    });
    this.calcPosition(nodeOptions.layoutOptions.shape);
  },
  methods: {
    calcPosition(shape = 'circle') {
      const calcFunctions = {
        circle: this.calcCirclePosition,
        square: this.calcSquarePosition,
        sphere: this.calcSpherePosition
      };
      calcFunctions[shape]();
    },
    calcCirclePosition() {
      const questionCount = this.questions.length;
      const radius = questionCount === 1
        ? 1e-100
        : this.node.nodeOptions.layoutOptions.fixedDistance || (questionCount/5)*this.node.nodeOptions.layoutOptions.scale;
      this.questions.forEach((_, i) => {
        const theta = 2*Math.PI*i/questionCount + Math.PI/2;
        const x = radius*Math.cos(theta);
        const z = radius*Math.sin(theta);
        this.$set(this.questions[i], 'position', new THREE.Vector3(x, 0, z));
      });
    },
    calcSquarePosition() {
      const questionCount = this.questions.length;
      const edgeMaxLength = Math.ceil(Math.sqrt(questionCount)) - 1;
      const gap = this.node.nodeOptions.layoutOptions.fixedDistance || this.node.nodeOptions.layoutOptions.scale;
      this.questions.forEach((_, i) => {
        const x = (edgeMaxLength - i%(edgeMaxLength + 1))*gap - edgeMaxLength*gap/2;
        const z = (edgeMaxLength - Math.floor(i/(edgeMaxLength + 1)))*gap - (edgeMaxLength - (questionCount/(edgeMaxLength + 1) - 1)/2)*gap;
        this.$set(this.questions[i], 'position', new THREE.Vector3(x, 0, z));
      });
    },
    calcSpherePosition() {
      const questionCount = this.questions.length;
      const questionRadius = this.node.nodeOptions.layoutOptions.fixedDistance || this.sphereRadius*this.node.nodeOptions.layoutOptions.scale;
      this.questions.forEach((_, i) => {
        const theta = Math.acos(-1 + 2*(i + 1)/(questionCount + 1)); // 仰角
        const phi = Math.sqrt((questionCount + 1)*Math.PI)*theta; // 俯角
        const x = questionRadius*Math.sin(theta)*Math.cos(phi);
        const y = questionRadius*Math.sin(theta)*Math.sin(phi);
        const z = questionRadius*Math.cos(theta);
        this.$set(this.questions[i], 'position', new THREE.Vector3(x, y, z));
      });
    }
  }
};
</script>
