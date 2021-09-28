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
    <node-form
      v-else-if="!node.nodes"
      :node="node"
      :editMode="editMode"
    />
    <group-form
      v-else
      :node="node"
    />
  </v-card>
</template>

<script>
import LayerForm from './LayerForm.vue';
import NodeForm from './NodeForm.vue';
import GroupForm from './GroupForm.vue';

export default {
  name: 'DetailsCard',
  components: {
    LayerForm,
    NodeForm,
    GroupForm
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
    },
    editMode: {
      type: Boolean,
      require: true
    }
  }
};
</script>
