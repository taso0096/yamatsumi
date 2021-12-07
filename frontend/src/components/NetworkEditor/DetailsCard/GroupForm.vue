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
      <span class="subtitle-1 grey--text text--darken-1">Group Options</span>
    </div>
    <v-row>
      <v-col class="py-0">
        <v-text-field
          v-model="node.nodeOptions.position.x"
          label="Position X"
          type="number"
          step="0.1"
          :placeholder="String(0)"
        />
      </v-col>
      <v-col class="py-0">
        <v-text-field
          v-model="node.nodeOptions.position.y"
          label="Position Y"
          type="number"
          step="0.1"
          :placeholder="String(0)"
        />
      </v-col>
      <v-col class="py-0">
        <v-text-field
          v-model="node.nodeOptions.position.z"
          label="Position Z"
          type="number"
          step="0.1"
          :placeholder="String(0)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col class="py-0">
        <v-text-field
          v-model="node.nodeOptions.rotation.x"
          label="Rotation X"
          type="number"
          step="0.1"
          :placeholder="String(0)"
        />
      </v-col>
      <v-col class="py-0">
        <v-text-field
          v-model="node.nodeOptions.rotation.y"
          label="Rotation Y"
          type="number"
          step="0.1"
          :placeholder="String(0)"
        />
      </v-col>
      <v-col class="py-0">
        <v-text-field
          v-model="node.nodeOptions.rotation.z"
          label="Rotation Z"
          type="number"
          step="0.1"
          :placeholder="String(0)"
        />
      </v-col>
    </v-row>

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
    },
    schemaNode() {
      return this.schemaLayer.nodes.items.properties;
    },
    schemaNodeOptions() {
      return this.schemaNode.nodeOptions.properties;
    }
  },
  created() {
    if (!this.node.layoutOptions) {
      this.node.layoutOptions = {};
    }
    if (!this.node.nodeOptions) {
      this.node.nodeOptions = {};
    }
    if (!this.node.nodeOptions.position) {
      this.node.nodeOptions.position = {};
    }
    if (!this.node.nodeOptions.rotation) {
      this.node.nodeOptions.rotation = {};
    }
  }
};
</script>
