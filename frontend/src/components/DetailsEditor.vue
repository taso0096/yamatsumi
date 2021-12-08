<template>
  <v-card
    flat
    tile
    height="auto"
  >
    <v-card-text>
      <v-text-field
        v-model="cyberspace.id"
        label="Cyberspace ID"
      />
      <v-text-field
        v-model="cyberspace.label"
        label="Cyberspace Label"
      />
      <v-text-field
        v-model="cyberspace.version"
        label="Version"
      />
      <v-textarea
        v-model="cyberspace.desc"
        label="Description"
      />

      <div>
        <span class="subtitle-1 grey--text text--darken-1">Options</span>
      </div>
      <v-row>
        <v-col class="py-0">
          <v-text-field
            v-model="cyberspace.options.position.x"
            label="Position X"
            type="number"
            step="0.1"
            :placeholder="String(0)"
          />
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model="cyberspace.options.position.y"
            label="Position Y"
            type="number"
            step="0.1"
            :placeholder="String(0)"
          />
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model="cyberspace.options.position.z"
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
            v-model="cyberspace.options.rotation.x"
            label="Rotation X"
            type="number"
            step="0.1"
            :placeholder="String(0)"
          />
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model="cyberspace.options.rotation.y"
            label="Rotation Y"
            type="number"
            step="0.1"
            :placeholder="String(0)"
          />
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model="cyberspace.options.rotation.z"
            label="Rotation Z"
            type="number"
            step="0.1"
            :placeholder="String(0)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0">
          <v-text-field
            v-model="cyberspace.options.animation.to"
            label="Animation To"
            type="string"
            placeholder="0 0 0"
          />
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model="cyberspace.options.animation.duration"
            label="Animation Duration"
            type="number"
            step="1"
            placeholder="200000"
          />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'DetailsEditor',
  props: {
    cyberspace: {
      type: Object,
      required: true
    }
  },
  created() {
    if (!this.cyberspace.options.position) {
      this.cyberspace.options.position = {};
    }
    if (!this.cyberspace.options.rotation) {
      this.cyberspace.options.rotation = {};
    }
    if (!this.cyberspace.options.animation) {
      this.cyberspace.options.animation = {};
    }
  }
};
</script>
