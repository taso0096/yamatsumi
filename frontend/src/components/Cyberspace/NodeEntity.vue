<template>
  <UserEntity
    v-if="(validNode.nodeOptions || {}).type === 'user'"
    :node="validNode"
  />
  <QuestionEntity
    v-else-if="validNode.questions"
    :node="node"
    :questions="validNode.questions"
  />
  <a-entity v-else-if="!validNode.label"></a-entity>
  <a-entity v-else>
    <a-sphere
      :radius="sphereRadius*validNode.nodeOptions.size"
      :color="validNode.nodeColor"
    >
      <a-text
        :value="validNode.label"
        align="center"
        :color="validNode.nodeOptions.labelColor"
        side="double"
        :position="`0 ${-sphereRadius*validNode.nodeOptions.size - sphereRadius} 0`"
        wrap-count="50"
      />
    </a-sphere>
  </a-entity>
</template>

<script>
import UserEntity from './UserEntity.vue';
import QuestionEntity from './QuestionEntity.vue';

export default {
  name: 'NodeEntity',
  components: {
    UserEntity,
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
      const questions = JSON.parse(JSON.stringify(this.$_visualizeData.exercise.questions));
      const nodeQuestions = [];
      const tags = this.node.id.split('__');
      tags.forEach(tag => {
        const levelId = tag.split(/^level-/)[1];
        const categoryId = tag.split(/^category-/)[1];
        if (levelId) {
          nodeQuestions.push(...questions.filter(q => q.levelId === levelId));
        } else if (categoryId) {
          nodeQuestions.push(...questions.filter(q => q.categoryId === categoryId));
        }
      });
      this.$set(this.validNode, 'questions', nodeQuestions);
      return;
    };
    const nodeOptions = this.node.nodeOptions || {};
    this.validNode = {
      id: this.node.id,
      label: this.node.label || this.node.id,
      nodeOptions: {
        ...nodeOptions,
        type: nodeOptions.type || 'sphere',
        size: nodeOptions.size || 1,
        nodeColor: nodeOptions.nodeColor || '#fff',
        labelColor: nodeOptions.labelColor || '#fff'
      }
    };
  }
};
</script>
