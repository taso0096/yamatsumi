<template>
  <a-entity
    :position="`0 ${layer.fixedDepth} 0`"
    :animation="`property: rotation; to: ${animationOption.to || '0 0 0'}; dur: ${animationOption.duration || 200000}; easing: linear; loop: true`"
  >
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
  },
  computed: {
    animationOption() {
      return this.layer.animation || {};
    }
  }
};
</script>
