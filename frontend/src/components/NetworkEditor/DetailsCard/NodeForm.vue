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
    <template v-if="node.nodeOptions.type === 'user'">
      <v-row>
        <v-col class="py-0">
          <v-select
            v-model="node.nodeOptions.users"
            :items="users"
            label="Selected Users"
            multiple
          >
            <template v-slot:prepend-item>
              <v-list-item
                ripple
                @click="toggleSelectAllUsers"
              >
                <v-list-item-action>
                  <v-icon :color="node.nodeOptions.users.length > 0 ? 'primary' : ''">
                    {{ userSelectAllIcon() }}
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
    }
  },
  created() {
    if (!this.node.nodeOptions) {
      this.node.nodeOptions = {};
    }
  },
  methods: {
    changeNodeType(type) {
      if (type === 'user') {
        this.node.nodeOptions.users = [];
      } else if (this.node.nodeOptions.users) {
        delete this.node.nodeOptions.users;
      }
    },
    userSelectAllIcon () {
      switch (this.node.nodeOptions.users.length/this.users.length) {
        case 1:
          return 'mdi-close-box';
        case 0:
          return 'mdi-checkbox-blank-outline';
        default:
          return 'mdi-minus-box';
      }
    },
    toggleSelectAllUsers () {
      this.$nextTick(() => {
        if (this.node.nodeOptions.users.length/this.users.length === 1) {
          this.node.nodeOptions.users.splice(0, this.node.nodeOptions.users.length);
        } else {
          this.node.nodeOptions.users.splice(0, this.node.nodeOptions.users.length);
          this.node.nodeOptions.users.push(...this.users);
        }
      })
    }
  }
};
</script>
