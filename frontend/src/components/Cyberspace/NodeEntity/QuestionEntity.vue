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
      :look-center="`parentSelector: question-entity__${node.id}`"
    >
      <NodeShapeEntity
        :node="node"
        :centerLabel="question.id"
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

    const questionCount = this.questions.length;
    const questionRadius = this.sphereRadius*nodeOptions.layoutOptions.scale;
    for (const i of [...Array(questionCount).keys()]) {
      const theta = Math.acos(-1 + 2*(i + 1)/(questionCount + 1)); // 仰角
      const phi = Math.sqrt((questionCount + 1)*Math.PI)*theta; // 俯角
      const x = questionRadius*Math.sin(theta)*Math.cos(phi);
      const y = questionRadius*Math.sin(theta)*Math.sin(phi);
      const z = questionRadius*Math.cos(theta);
      this.$set(this.questions[i], 'position', new THREE.Vector3(x, y, z));
    }
  }
};
</script>
