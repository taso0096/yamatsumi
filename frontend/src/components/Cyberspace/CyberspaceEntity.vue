<template>
  <a-entity v-if="!isValidCyberspace" />
  <a-entity
    v-else
    :position="`${cyberspaceOption.position.x || 0} ${-(totalDepth - cyberspace.layers[0].fixedDepth)/2} ${cyberspaceOption.position.z || 0}`"
    :rotation="`${cyberspaceOption.rotation.x || 0} ${cyberspaceOption.rotation.y || 0} ${cyberspaceOption.rotation.z || 0}`"
    :animation="`property: rotation; to: ${cyberspaceOption.animation.to || '0 0 0'}; dur: ${cyberspaceOption.animation.duration || 200000}; easing: linear; loop: true`"
  >
    <a-entity :position="`0 ${cyberspaceOption.position.y || 0} 0`">
      <layer-entity
        v-for="layer in cyberspace.layers"
        :key="layer.id"
        :layer="layer"
      />
    </a-entity>
  </a-entity>
</template>

<script>
import LayerEntity from './LayerEntity.vue';

import { validate } from 'jsonschema';
import cyberspaceSchema from '@/assets/CyberspaceSchema.json';
import exerciseSchema from '@/assets/ExerciseSchema.json';

export default {
  name: 'CyberspaceEntity',
  components: {
    LayerEntity
  },
  data: () => ({
    cyberspace: {},
    exercise: {},
    isValidCyberspace: false,
    totalDepth: 0
  }),
  computed: {
    cyberspaceOption() {
      const options = this.cyberspace.options;
      return {
        position: options.position || {},
        rotation: options.rotation || {},
        animation: options.animation || {}
      };
    }
  },
  methods: {
    async set(visualizeData) {
      const { cyberspace, exercise } = visualizeData;
      this.$store.dispatch('setVisualizeData', visualizeData);
      this.isValidCyberspace = false;
      await this.$_sleep(100);
      const cyberspaceValidate = validate(cyberspace, cyberspaceSchema);
      if (!cyberspaceValidate.valid) {
        console.error('JSON Schema Validate ERROR', cyberspaceValidate.errors);
        this.$_pushNotice('An error occurred during JSON validation.', 'error');
        return false;
      }
      if (!cyberspace.layers.length) {
        this.$_pushNotice('Layer does not exist.', 'warning');
        return false;
      }
      if (!cyberspace.layers[0].fixedDepth) {
        this.totalDepth = cyberspace.layers[0].depth || 0;
        cyberspace.layers[0].fixedDepth = this.totalDepth;
      }
      for (const layer of cyberspace.layers.slice(1)) {
        if (!layer.fixedDepth) {
          this.totalDepth -= 1.5*(layer.depth ?? 1);
          layer.fixedDepth = this.totalDepth;
        } else {
          if (layer.fixedDepth > this.totalDepth) {
            const warnMessage = `FixedDepth is larger than totalDepth. \n(Layer Id: ${layer.id})`;
            console.warn(warnMessage);
            this.$_pushNotice(warnMessage, 'warning');
          } else {
            this.totalDepth = layer.fixedDepth;
          }
        }
      }
      this.cyberspace = cyberspace;

      const exerciseValidate = validate(exercise, exerciseSchema);
      if (!exerciseValidate.valid) {
        console.error('JSON Schema Validate ERROR', exerciseValidate.errors);
        this.$_pushNotice('An error occurred during JSON validation.', 'error');
        return false;
      } else {
        this.exercise = exercise;
      }

      this.isValidCyberspace = true;
      return true;
    },
    reset() {
      this.isValidCyberspace = false;
      this.cyberspace = {};
    }
  }
};
</script>
