<template>
  <div>
    <v-card
      tile
      flat
      class="mb-3"
    >
      <v-card-title>
        <span>Network JSON</span>
        <v-spacer />
        <v-btn
          v-if="!editMode"
          color="warning"
          depressed
          tile
          small
          @click="editMode = true"
        >
          <span>Edit</span>
        </v-btn>
        <template v-else>
          <v-btn
            text
            tile
            small
            class="mr-2"
            @click="editMode = false"
          >
            <span>Cancel</span>
          </v-btn>
          <v-btn
            color="primary"
            depressed
            tile
            small
            @click="editMode = false"
          >
            <span>Save</span>
          </v-btn>
        </template>
      </v-card-title>
    </v-card>

    <v-form :readonly="!editMode">
      <v-card
        tile
        flat
        class="mb-3"
      >
        <v-card-title class="font-weight-regular">
          <span>Details</span>
          <v-spacer />
          <v-btn
            icon
            small
            @click="showAll.details = !showAll.details"
          >
            <v-icon>
              {{ showAll.details ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
            </v-icon>
          </v-btn>
        </v-card-title>
        <v-expand-transition>
          <v-card-text v-show="showAll.details">
            <v-text-field
              v-model="network.id"
              label="ID *"
              :rules="[rules.required]"
            />
            <v-text-field
              v-model="network.label"
              label="Label"
            />
            <v-text-field
              v-model="network.version"
              label="Version"
            />
            <v-textarea
              v-model="network.desc"
              label="Description"
            />
          </v-card-text>
        </v-expand-transition>
      </v-card>

      <v-card
        tile
        flat
        class="mb-3"
      >
        <v-card-title class="font-weight-regular">
          <span>Routing Table</span>
          <v-spacer />
          <v-btn
            icon
            small
            @click="showAll.routingTable = !showAll.routingTable"
          >
            <v-icon>
              {{ showAll.routingTable ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
            </v-icon>
          </v-btn>
        </v-card-title>
        <v-expand-transition>
          <v-card-text v-show="showAll.routingTable">
            <div
              v-for="(node, i) in routingTableArray"
              :key="`node-${i}`"
            >
              <v-text-field
                v-model="node[0]"
                :label="`Node ID - ${i + 1}`"
                hide-details
              />
              <v-combobox
                v-model="node[1]"
                :label="`IP addresses (${node[0]})`"
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
                  >
                    <span>
                      {{ item }}
                    </span>
                    <v-icon
                      v-if="editMode"
                      small
                      class="ml-2"
                      @click="parent.selectItem(item)"
                    >mdi-close</v-icon>
                  </v-chip>
                </template>
              </v-combobox>
            </div>
          </v-card-text>
        </v-expand-transition>
      </v-card>
    </v-form>
  </div>
</template>

<script>
export default {
  name: 'NetworkEditor',
  props: {
    network: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    editMode: false,
    showAll: {
      details: true,
      routingTable: false,
      layers: false
    },
    routingTableArray: []
  }),
  computed: {
    rules: () => ({
      required: v => !!v || 'Required.'
    })
  },
  mounted() {
    for (const key in this.network.routingTable) {
      this.routingTableArray.push([key, this.network.routingTable[key]]);
    }
  }
}
</script>
