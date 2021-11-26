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
          @change="changeNodeType"
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
    <v-row v-if="node.nodeOptions.type === 'user'">
      <v-col class="py-0">
        <v-select
          v-model="node.nodeOptions.users"
          label="Selected Users"
          :items="users"
          multiple
        >
          <template v-slot:prepend-item>
            <v-list-item
              ripple
              @click="toggleSelectAll('users')"
            >
              <v-list-item-action>
                <v-icon :color="node.nodeOptions.users.length > 0 ? 'primary' : ''">
                  {{ selectAllIcon('users') }}
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
    <template v-if="node.nodeOptions.type === 'question'">
      <v-row>
        <v-col class="py-0">
          <v-select
            v-model="node.nodeOptions.levels"
            label="Selected Levels"
            :items="levels"
            multiple
            item-text="label"
            item-value="id"
          >
            <template v-slot:prepend-item>
              <v-list-item
                ripple
                @click="toggleSelectAll('levels')"
              >
                <v-list-item-action>
                  <v-icon :color="node.nodeOptions.levels.length > 0 ? 'primary' : ''">
                    {{ selectAllIcon('levels') }}
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
      <v-row>
        <v-col class="py-0">
          <v-select
            v-model="node.nodeOptions.categories"
            label="Selected Categories"
            :items="categories"
            multiple
            item-text="label"
            item-value="id"
          >
            <template v-slot:prepend-item>
              <v-list-item
                ripple
                @click="toggleSelectAll('categories')"
              >
                <v-list-item-action>
                  <v-icon :color="node.nodeOptions.categories.length > 0 ? 'primary' : ''">
                    {{ selectAllIcon('categories') }}
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
    users() {
      return Object.values(this.$_visualizeData.exercise.scores).reduce((users, team) => {
        users.push(...Object.keys(team.users).map((id) => (id)));
        return users;
      }, []);
    },
    levels() {
      return this.$_visualizeData.exercise.levels;
    },
    categories() {
      return this.$_visualizeData.exercise.categories;
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
      switch (type) {
        case 'user':
          this.node.nodeOptions.users = [];
          break;
        case 'question':
          this.node.nodeOptions.levels = [];
          this.node.nodeOptions.categories = [];
          break;
      }
    },
    selectAllIcon(item) {
      if (!this.node.nodeOptions[item] || !this[item]) {
        return 'mdi-checkbox-blank-outline';
      }
      switch (this.node.nodeOptions[item].length/this[item].length) {
        case 1:
          return 'mdi-close-box';
        case 0:
          return 'mdi-checkbox-blank-outline';
        default:
          return 'mdi-minus-box';
      }
    },
    toggleSelectAll(item) {
      if (!this.node.nodeOptions[item] || !this[item]) {
        return;
      }
      this.$nextTick(() => {
        if (this.node.nodeOptions[item].length/this[item].length === 1) {
          this.node.nodeOptions[item].splice(0, this.node.nodeOptions[item].length);
        } else {
          this.node.nodeOptions[item].splice(0, this.node.nodeOptions[item].length);
          this.node.nodeOptions[item].push(...this[item]);
        }
      });
    }
  }
};
</script>
