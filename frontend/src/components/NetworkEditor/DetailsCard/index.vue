<template>
  <v-card>
    <slot name="header">
      <v-card-title>
        <span>Details</span>
      </v-card-title>
    </slot>
    <layer-form
      v-if="isLayer"
      :node="node"
    />
  </v-card>
</template>

<script>
import LayerForm from './LayerForm.vue'

export default {
  name: 'DetailsCard',
  components: {
    LayerForm
  },
  props: {
    node: {
      type: Object,
      require: true
    },
    isLayer: {
      type: Boolean,
      default: false,
      require: true
    }
  }
};
</script>
