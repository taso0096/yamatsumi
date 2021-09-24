<template>
  <v-card>
    <slot name="header">
      <v-card-title>
        <span>Details</span>
      </v-card-title>
    </slot>
    <v-card-text>
      <v-text-field
        v-model="node.id"
        label="ID"
      />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'DetailsCard',
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
