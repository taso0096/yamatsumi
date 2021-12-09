<template>
  <a-entity v-if="!isValidCyberspace" />
  <a-entity
    v-else
    :class="`delay__${delay}`"
    :position="`${cyberspaceOption.position.x || 0} ${-(totalDepth - cyberspace.layers[0].fixedDepth)/2} ${cyberspaceOption.position.z || 0}`"
    :rotation="`${cyberspaceOption.rotation.x || 0} ${cyberspaceOption.rotation.y || 0} ${cyberspaceOption.rotation.z || 0}`"
    :animation="`delay: ${delay}; property: rotation; to: ${cyberspaceOption.animation.to || '0 0 0'}; dur: ${cyberspaceOption.animation.duration || 200000}; easing: linear; loop: true`"
  >
    <a-entity :position="`0 ${cyberspaceOption.position.y || 0} 0`">
      <layer-entity
        v-for="layer in cyberspace.layers"
        :key="layer.id"
        :layer="layer"
        :delay="delay"
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
  props: {
    delay: {
      type: Number,
      default: 0
    }
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
      if (!this.delay) {
        this.$store.dispatch('setVisualizeData', visualizeData);
      }
      this.isValidCyberspace = false;
      await this.$_sleep(100);
      if (!this.delay) {
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
      }
      if (!cyberspace.layers[0].fixedDepth) {
        this.totalDepth = cyberspace.layers[0].depth || 0;
        cyberspace.layers[0].fixedDepth = this.totalDepth;
      }
      for (const layer of cyberspace.layers.slice(1)) {
        if (!layer.fixedDepth) {
          this.totalDepth -= 1.5*(layer.depth !== '' ? layer.depth ?? 1 : 1);
          layer.fixedDepth = this.totalDepth;
        } else {
          if (layer.fixedDepth > this.totalDepth) {
            if (!this.delay) {
              const warnMessage = `FixedDepth is larger than totalDepth. \n(Layer Id: ${layer.id})`;
              console.warn(warnMessage);
              this.$_pushNotice(warnMessage, 'warning');
            }
          } else {
            this.totalDepth = layer.fixedDepth;
          }
        }
      }
      this.cyberspace = cyberspace;

      const exerciseValidate = validate(exercise, exerciseSchema);
      if (!exerciseValidate.valid) {
        if (!this.delay) {
          console.error('JSON Schema Validate ERROR', exerciseValidate.errors);
          this.$_pushNotice('An error occurred during JSON validation.', 'error');
        }
        return false;
      } else {
        this.exercise = exercise;
      }

      this.isValidCyberspace = true;
      this.$nextTick(() => {
        if (this.delay === 0 && document.querySelector('.delay__0')) {
          document.querySelector('.delay__0').object3D.visible = false;
        }
      });
      return true;
    },
    reset() {
      this.isValidCyberspace = false;
      this.cyberspace = {};
    }
  }
};
</script>
