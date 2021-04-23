<template>
  <a-entity v-if="!isValidNetwork" />
  <a-entity v-else :position="`0 ${-(totalDepth - network.layers[0].fixedDepth)/2} 0`">
    <layer-entity
      v-for="layer in network.layers"
      :key="layer.id"
      :layer="layer"
    />
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
    network: {},
    exercise: {},
    isValidNetwork: false,
    totalDepth: 0
  }),
  methods: {
    async set(visualizeData) {
      const { exercise, network } = visualizeData;
      this.$store.dispatch('setEvent', visualizeData);
      this.isValidNetwork = false;
      await this.$_sleep(100);
      const networkValidate = validate(network, cyberspaceSchema);
      if (!networkValidate.valid) {
        console.error('JSON Schema Validate ERROR', networkValidate.errors);
        this.$_pushNotice('An error occurred during JSON validation.', 'error');
        return false;
      }
      if (!network.layers.length) {
        this.$_pushNotice('Layer does not exist.', 'warning');
        return false;
      }
      if (!network.layers[0].fixedDepth) {
        this.totalDepth = network.layers[0].depth || 0;
        network.layers[0].fixedDepth = this.totalDepth;
      }
      for (const layer of network.layers.slice(1)) {
        if (!layer.fixedDepth) {
          this.totalDepth -= 1.5*(layer.depth || 1);
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
      this.network = network;

      const exerciseValidate = validate(exercise, exerciseSchema);
      if (!exerciseValidate.valid) {
        console.error('JSON Schema Validate ERROR', exerciseValidate.errors);
        this.$_pushNotice('An error occurred during JSON validation.', 'error');
        return false;
      } else {
        this.exercise = exercise;
      }

      this.isValidNetwork = true;
      return true;
    },
    reset() {
      this.isValidNetwork = false;
      this.network = {};
    }
  }
};
</script>
