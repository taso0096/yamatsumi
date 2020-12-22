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
import networkSchema from '@/assets/NetworkSchema.json';

export default {
  name: 'BaseNetworkEntity',
  components: {
    LayerEntity
  },
  props: {
    network: {
      type: Object
    }
  },
  data: () => ({
    isValidNetwork: false,
    totalDepth: 0
  }),
  mounted() {
    const network = this.network;
    const networkValidate = validate(network, networkSchema);
    if (!networkValidate.valid) {
      console.error('JSON Schema Validate ERROR', networkValidate.errors);
      this.$_pushNotice('JSONのバリデーションに失敗しました。', 'error');
      return;
    }
    if (!network.layers.length) {
      return;
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
          console.warn(`FixedDepth is larger than totalDepth. (layerId: ${layer.id})`);
        } else {
          this.totalDepth = layer.fixedDepth;
        }
      }
    }
    this.isValidNetwork = true;
    AFRAME.registerComponent('look-center', {
      schema: {
        parentSelector: { type: 'string' }
      },
      init: function() {
        const targetEl = document.querySelector(this.data.parentSelector);
        const targetPosition = targetEl?.object3D.getWorldPosition(new THREE.Vector3());
        if (targetPosition) {
          targetPosition.y = this.el.object3D.getWorldPosition(new THREE.Vector3()).y;
        }
        this.el.object3D.lookAt(targetPosition || new THREE.Vector3(0, 0, 0));
        this.el.firstElementChild.object3D.rotation.set(0, Math.PI, 0);
      }
    });
  }
};
</script>
