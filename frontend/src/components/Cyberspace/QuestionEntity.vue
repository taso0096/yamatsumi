<template>
  <a-entity
    :id="`question-entity__${node.id}`"
    :scale="`${node.nodeOptions.size} ${node.nodeOptions.size} ${node.nodeOptions.size}`"
  >
    <a-text
      :value="node.label"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`0 ${-sphereRadius*node.nodeOptions.size - sphereRadius} 0`"
      wrap-count="50"
    />
    <a-circle
      v-for="question in questions"
      :key="question.id"
      :id="`question__${question.id}`"
      :color="node.nodeOptions.nodeColor"
      side="double"
      radius="0.2"
      :position="question.position"
      :look-center="`parentSelector: question-entity__${node.id}`"
    >
      <a-ring
        :color="node.nodeOptions.nodeColor"
        side="double"
        radius-inner="0.205"
        radius-outer="0.21"
      />
      <a-ring
        :color="node.nodeOptions.nodeColor"
        side="double"
        radius-inner="0.215"
        radius-outer="0.235"
      />
      <a-text
        :value="question.id"
        align="center"
        :color="node.nodeOptions.labelColor"
        side="double"
        position="0 0.01 0"
        rotation="0 180 0"
      />
    </a-circle>
  </a-entity>
</template>

<script>
export default {
  name: 'QuestionEntity',
  props: {
    node: {
      type: Object,
      required: true
    },
    questions: {
      type: Array,
      required: true
    }
  },
  computed: {
    sphereRadius: () => 0.45
  },
  mounted() {
    const questionCount = this.questions.length;
    const questionRadius = 0.65;
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
