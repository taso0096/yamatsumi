<template>
  <v-card-text>
    <v-text-field
      v-model="node.id"
      label="Group ID"
    />
    <v-text-field
      v-model="node.label"
      label="Group Label"
    />
    <v-text-field
      v-model="node.parentId"
      label="Parent ID"
    />

    <div>
      <span class="subtitle-1 grey--text text--darken-1">Layout Options</span>
    </div>
    <v-row>
      <v-col class="py-0">
        <v-select
          v-model="node.layoutOptions.shape"
          label="Shape"
          :items="schemaLayoutOptions.shape.enum"
        />
      </v-col>
      <v-col class="py-0">
        <v-text-field
          v-model.number="node.layoutOptions.scale"
          label="Scale"
          type="number"
          min="0"
          step="0.1"
          :placeholder="String(schemaLayoutOptions.scale.default || '')"
        />
      </v-col>
      <v-col class="py-0">
        <v-text-field
          v-model.number="node.layoutOptions.fixedDistance"
          label="Fixed Distance"
          type="number"
          min="0"
          step="0.1"
          :placeholder="String(schemaLayoutOptions.fixedDistance.default || '')"
        />
      </v-col>
    </v-row>
  </v-card-text>
</template>

<script>
import cyberspaceSchema from '@/assets/CyberspaceSchema.json';

export default {
  name: 'GroupForm',
  props: {
    node: {
      type: Object,
      require: true
    }
  },
  computed: {
    schemaLayer() {
      return cyberspaceSchema.properties.layers.items.properties;
    },
    schemaLayoutOptions() {
      return this.schemaLayer.layoutOptions.properties;
    }
  },
  created() {
    if (!this.node.layoutOptions) {
      this.node.layoutOptions = {};
    }
  }
};
</script>
