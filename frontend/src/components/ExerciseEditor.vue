<template>
  <v-card
    flat
    tile
    height="auto"
  >
    <v-card-text>
      <v-text-field
        v-model="cyberspace.scoresUrl"
        label="Score URL"
        :placeholder="scoresUrlExample"
      />
      <v-text-field
        v-model="cyberspace.questionsUrl"
        label="Questions URL"
        :placeholder="questionsUrlExample"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import cyberspaceSchema from '@/assets/CyberspaceSchema.json';

export default {
  name: 'ExerciseEditor',
  props: {
    cyberspace: {
      type: Object,
      required: true
    }
  },
  computed: {
    scoresUrlExample() {
      return String(cyberspaceSchema.properties.scoresUrl.examples[0]) || '';
    },
    questionsUrlExample() {
      return String(cyberspaceSchema.properties.questionsUrl.examples[0]) || '';
    }
  }
};
</script>
