<template>
  <a-entity>
    <template v-if="!validNode.label" />
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
    <node-shape-entity
      v-else
      :node="validNode"
    />
  </a-entity>
</template>

<script>
import UserEntity from './UserEntity.vue';
import QuestionEntity from './QuestionEntity.vue';
import SpacerEntity from './SpacerEntity.vue';
import NodeShapeEntity from './NodeShapeEntity';

export default {
  name: 'NodeEntity',
  components: {
    UserEntity,
    QuestionEntity,
    SpacerEntity,
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
        nodeColor: nodeOptions.nodeColor || '#fff',
        labelColor: nodeOptions.labelColor || '#fff'
      }
    };
  }
};
</script>
