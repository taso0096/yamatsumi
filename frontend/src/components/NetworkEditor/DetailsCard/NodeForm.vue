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
          :placeholder="String(schemaNodeOptions.type.default || '')"
          :items="schemaNodeOptions.type.enum"
          @change="changeNodeType"
        />
      </v-col>
      <v-col class="py-0">
        <v-select
          v-model="node.nodeOptions.shape"
          label="Shape"
          :placeholder="String(schemaNodeOptions.shape.default || '')"
          :items="schemaNodeOptions.shape.enum"
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
    <v-row>
      <v-col class="py-0">
        <v-select
          v-model="node.nodeOptions.topLabel"
          label="Top Label"
          :placeholder="String(schemaNodeOptions.topLabel.default || '')"
          :items="schemaNodeOptions.topLabel.enum"
        />
      </v-col>
      <v-col class="py-0">
        <v-select
          v-model="node.nodeOptions.centerLabel"
          label="Center Label"
          :placeholder="String(schemaNodeOptions.centerLabel.default || '')"
          :items="schemaNodeOptions.centerLabel.enum"
        />
      </v-col>
      <v-col class="py-0">
        <v-select
          v-model="node.nodeOptions.bottomLabel"
          label="Bottom Label"
          :placeholder="String(schemaNodeOptions.bottomLabel.default || '')"
          :items="schemaNodeOptions.bottomLabel.enum"
        />
      </v-col>
    </v-row>
    <v-row>
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

    <template v-if="['user', 'question'].includes(node.nodeOptions.type)">
      <v-row
        v-for="option in nodeTypeOptions(node.nodeOptions.type)"
        :key="option"
      >
        <v-col class="py-0">
          <v-select
            v-model="node.nodeOptions[option]"
            :label="`Selected ${option[0].toUpperCase()}${option.slice(1)}`"
            :items="exercise[option]"
            item-text="label"
            item-value="id"
            multiple
          >
            <template v-slot:prepend-item>
              <v-list-item
                ripple
                @click="toggleSelectAll(option)"
              >
                <v-list-item-action>
                  <v-icon :color="node.nodeOptions[option].length > 0 ? 'primary' : ''">
                    {{ selectAllIcon(option) }}
                  </v-icon>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>
                    Select All
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-divider class="mt-2"></v-divider>
            </template>
          </v-select>
        </v-col>
      </v-row>
      <div>
        <span class="subtitle-1 grey--text text--darken-1">Layout Options</span>
      </div>
      <v-row v-if="node.nodeOptions.layoutOptions">
        <v-col class="py-0">
          <v-select
            v-model="node.nodeOptions.layoutOptions.shape"
            label="Shape"
            :items="schemaLayoutOptions.shape.enum"
          />
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model.number="node.nodeOptions.layoutOptions.scale"
            label="Scale"
            type="number"
            min="0"
            step="0.1"
            :placeholder="String(schemaLayoutOptions.scale.default || '')"
          />
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model.number="node.nodeOptions.layoutOptions.fixedDistance"
            label="Fixed Distance"
            type="number"
            min="0"
            step="0.1"
            :placeholder="String(schemaLayoutOptions.fixedDistance.default || '')"
          />
        </v-col>
      </v-row>
    </template>
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
    },
    schemaLayoutOptions() {
      return this.schemaLayer.layoutOptions.properties;
    },
    exercise() {
      return {
        users: Object.values(this.$_visualizeData.exercise.scores)
          .reduce((users, team) => {
            users.push(...Object.keys(team.users).map(id => ({ id, label: id })));
            return users;
          }, []),
        levels: this.$_visualizeData.exercise.levels,
        categories: this.$_visualizeData.exercise.categories
      };
    }
  },
  created() {
    if (!this.node.nodeOptions) {
      this.node.nodeOptions = {};
    }
  },
  methods: {
    changeNodeType(type) {
      delete this.node.nodeOptions.users;
      delete this.node.nodeOptions.levels;
      delete this.node.nodeOptions.categories;
      delete this.node.nodeOptions.layoutOptions;
      switch (type) {
        case 'user':
          this.node.nodeOptions.users = [];
          this.node.nodeOptions.layoutOptions = {};
          break;
        case 'question':
          this.node.nodeOptions.levels = [];
          this.node.nodeOptions.categories = [];
          this.node.nodeOptions.layoutOptions = {};
          break;
      }
    },
    selectAllIcon(option) {
      if (!this.node.nodeOptions[option] || !this.exercise[option]) {
        return 'mdi-checkbox-blank-outline';
      }
      switch (this.node.nodeOptions[option].length/this.exercise[option].length) {
        case 1:
          return 'mdi-close-box';
        case 0:
          return 'mdi-checkbox-blank-outline';
        default:
          return 'mdi-minus-box';
      }
    },
    toggleSelectAll(option) {
      if (!this.node.nodeOptions[option] || !this.exercise[option]) {
        return;
      }
      this.$nextTick(() => {
        if (this.node.nodeOptions[option].length/this.exercise[option].length === 1) {
          this.node.nodeOptions[option].splice(0, this.node.nodeOptions[option].length);
        } else {
          this.node.nodeOptions[option].splice(0, this.node.nodeOptions[option].length);
          this.node.nodeOptions[option].push(...this.exercise[option].map(v => v.id));
        }
      });
    },
    nodeTypeOptions(type) {
      switch (type) {
        case 'user':
          return ['users'];
        case 'question':
          return ['levels', 'categories'];
      }
    }
  }
};
</script>
