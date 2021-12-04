<template>
  <a-entity v-if="!validNode.label"></a-entity>
  <UserEntity
    v-else-if="validNode.nodeOptions.type === 'user'"
    :node="validNode"
  />
  <QuestionEntity
    v-else-if="validNode.nodeOptions.type === 'question'"
    :node="validNode"
  />
  <SpacerEntity
    v-else-if="validNode.nodeOptions.type === 'spacer'"
  />
  <NodeShapeEntity
    v-else
    :node="validNode"
  />
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
