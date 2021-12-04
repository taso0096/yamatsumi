<template>
  <UserEntity
    v-if="(validNode.nodeOptions || {}).type === 'user'"
    :node="validNode"
  />
  <QuestionEntity
    v-else-if="(validNode.nodeOptions || {}).type === 'question'"
    :node="validNode"
  />
  <a-entity v-else-if="!validNode.label"></a-entity>
  <a-entity v-else>
    <SphereEntity :node="validNode" />
  </a-entity>
</template>

<script>
import UserEntity from './UserEntity.vue';
import QuestionEntity from './QuestionEntity.vue';
import SphereEntity from './NodeShape/SphereEntity.vue';

export default {
  name: 'NodeEntity',
  components: {
    UserEntity,
    QuestionEntity,
    SphereEntity
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
