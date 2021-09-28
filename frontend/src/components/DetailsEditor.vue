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
  }
};
</script>
