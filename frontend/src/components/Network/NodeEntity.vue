<template>
  <QuestionEntity
    v-if="validNode.questions"
    :node="node"
    :questions="validNode.questions"
  />
  <a-entity v-else-if="!validNode.label"></a-entity>
  <a-entity v-else>
    <a-sphere
      :radius="sphereRadius*validNode.size"
      :color="validNode.nodeColor"
    >
      <a-text
        :value="validNode.label"
        align="center"
        :color="validNode.labelColor"
        side="double"
        :position="`0 ${-sphereRadius*validNode.size - sphereRadius} 0`"
        wrap-count="50"
      />
    </a-sphere>
  </a-entity>
</template>

<script>
import QuestionEntity from './QuestionEntity.vue';

export default {
  name: 'NodeEntity',
  components: {
    QuestionEntity
  },
  props: {
    node: {
      type: Object
    }
  },
  data: () => ({
    validNode: {}
  }),
  computed: {
    sphereRadius: () => 0.2
  },
  mounted() {
    if (this.node.nodeOptions?.type === 'question') {
      const questions = JSON.parse(JSON.stringify(this.$_event.game.questions));
      const tags = this.node.id.split('__');
      tags.forEach(tag => {
        const levelId = tag.split(/^level-/)[1];
        const categoryId = tag.split(/^category-/)[1];
        const tmpQuestions = JSON.parse(JSON.stringify(questions));
        if (levelId) {
          questions.length = 0;
          questions.push(...tmpQuestions.filter(q => q.levelId === levelId));
        } else if (categoryId) {
          questions.length = 0;
          questions.push(...tmpQuestions.filter(q => q.categoryId === categoryId));
        }
      });
      this.$set(this.validNode, 'questions', questions);
      return;
    };
    this.$set(this.validNode, 'label', this.node.label || this.node.id);
    this.$set(this.validNode, 'type', this.node.nodeOptions?.type || 'sphere');
    this.$set(this.validNode, 'size', this.node.nodeOptions?.size || 1);
    this.$set(this.validNode, 'nodeColor', this.node.nodeOptions?.nodeColor || '#fff');
    this.$set(this.validNode, 'labelColor', this.node.nodeOptions?.labelColor || '#fff');
  }
};
</script>
