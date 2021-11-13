<template>
  <UserEntity
    v-if="validNode.users"
    :node="node"
    :users="validNode.users"
    :shape="validNode.shape"
  />
  <QuestionEntity
    v-else-if="validNode.questions"
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
    if (this.node.nodeOptions?.type === 'user') {
      const scores = this.$_visualizeData.exercise.scores;
      const users = [];
      for (const [teamId, team] of Object.entries(scores)) {
        users.push(
          ...Object.entries(team.users).map(([id, score]) => ({ id, score, teamId }))
        );
      }
      this.$set(this.validNode, 'users', users);
      this.$set(this.validNode, 'shape', this.node.id.split('__').slice(-1)[0] || 'circle');
      return;
    };
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
    this.$set(this.validNode, 'label', this.validNode.userId || this.node.label || this.node.id);
    this.$set(this.validNode, 'type', this.node.nodeOptions?.type || 'sphere');
    this.$set(this.validNode, 'size', this.node.nodeOptions?.size || 1);
    this.$set(this.validNode, 'nodeColor', this.node.nodeOptions?.nodeColor || '#fff');
    this.$set(this.validNode, 'labelColor', this.node.nodeOptions?.labelColor || '#fff');
  }
};
</script>
