<template>
  <a-entity :position="`0 ${layer.fixedDepth} 0`">
    <group-entity :group="layer" />
  </a-entity>
</template>

<script>
import GroupEntity from './GroupEntity.vue';

export default {
  name: 'LayerEntity',
  components: {
    GroupEntity
  },
  props: {
    layer: {
      type: Object
    }
  }
};
</script>
