<template>
  <v-card-text>
    <v-text-field
      v-model="node.id"
      label="Node ID"
    />
    <v-text-field
      v-model="node.label"
      label="Node Label"
    />
    <v-text-field
      v-model="node.parentId"
      label="Parent ID"
    />
    <v-combobox
      v-model="node.ipaddresses"
      label="IP addresses"
      hide-selected
      multiple
      append-icon=""
    >
      <template v-slot:selection="{ attrs, item, parent, selected }">
        <v-chip
          v-bind="attrs"
          :input-value="selected"
          label
          small
          :color="$vuetify.theme.dark ? 'grey darken-3' : 'grey lighten-3'"
        >
          <span>{{ item }}</span>
          <v-icon
            v-if="editMode"
            small
            class="ml-2"
            @click="parent.selectItem(item)"
          >mdi-close</v-icon>
        </v-chip>
      </template>
    </v-combobox>

    <div>
      <span class="subtitle-1 grey--text text--darken-1">Node Options</span>
    </div>
    <v-row>
      <v-col class="py-0">
        <v-select
          v-model="node.nodeOptions.type"
          label="Type"
          :items="schemaNodeOptions.type.enum"
        />
      </v-col>
      <v-col class="py-0">
        <v-text-field
          v-model.number="node.nodeOptions.size"
          label="Size"
          type="number"
          min="0"
          step="0.1"
          :placeholder="String(schemaNodeOptions.size.default || '')"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col class="py-0">
        <v-text-field
          v-model="node.nodeOptions.nodeColor"
          label="Node Color"
          :placeholder="String(schemaNodeOptions.nodeColor.default || '')"
        />
      </v-col>
      <v-col class="py-0">
        <v-text-field
          v-model="node.nodeOptions.labelColor"
          label="Label Color"
          :placeholder="String(schemaNodeOptions.labelColor.default || '')"
        />
      </v-col>
    </v-row>
  </v-card-text>
</template>

<script>
import cyberspaceSchema from '@/assets/CyberspaceSchema.json';

export default {
  name: 'NodeForm',
  props: {
    node: {
      type: Object,
      require: true
    },
    editMode: {
      type: Boolean,
      require: true
    }
  },
  computed: {
    schemaLayer() {
      return cyberspaceSchema.properties.layers.items.properties;
    },
    schemaNode() {
      return this.schemaLayer.nodes.items.properties;
    },
    schemaNodeOptions() {
      return this.schemaNode.nodeOptions.properties;
    }
  },
  created() {
    if (!this.node.nodeOptions) {
      this.node.nodeOptions = {};
    }
  }
};
</script>
