<template>
  <a-entity>
    <template v-if="!validNode.label" />
    <team-entity
      v-else-if="validNode.nodeOptions.type === 'team'"
      :node="validNode"
    />
    <user-entity
      v-else-if="validNode.nodeOptions.type === 'user'"
      :node="validNode"
    />
    <question-entity
      v-else-if="validNode.nodeOptions.type === 'question'"
      :node="validNode"
    />
    <spacer-entity
      v-else-if="validNode.nodeOptions.type === 'spacer'"
    />
    <timer-entity
      v-else-if="validNode.nodeOptions.type === 'timer'"
      :node="validNode"
      :startTime="$_visualizeData.exercise.extra.startTime"
      :endTime="$_visualizeData.exercise.extra.endTime"
    />
    <node-shape-entity
      v-else
      :node="validNode"
    />
  </a-entity>
</template>

<script>
import TeamEntity from './TeamEntity.vue';
import UserEntity from './UserEntity.vue';
import QuestionEntity from './QuestionEntity.vue';
import SpacerEntity from './SpacerEntity.vue';
import TimerEntity from './TimerEntity.vue';
import NodeShapeEntity from './NodeShapeEntity';

export default {
  name: 'NodeEntity',
  components: {
    TeamEntity,
    UserEntity,
    QuestionEntity,
    SpacerEntity,
    TimerEntity,
    NodeShapeEntity
  },
  props: {
    node: {
      type: Object
    }
  },
  data: () => ({
    validNode: {}
  }),
  mounted() {
    const nodeOptions = this.node.nodeOptions || {};
    this.validNode = {
      id: this.node.id,
      label: this.node.label || this.node.id,
      nodeOptions: {
        ...nodeOptions,
        type: nodeOptions.type || 'default',
        shape: nodeOptions.shape || 'sphere',
        size: nodeOptions.size || 1,
        fontSize: nodeOptions.fontSize || 1,
        nodeColor: nodeOptions.nodeColor || '#fff',
        labelColor: nodeOptions.labelColor || '#fff',
        wireframe: nodeOptions.wireframe || false
      }
    };
  }
};
</script>
