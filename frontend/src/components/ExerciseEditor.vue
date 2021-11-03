<template>
  <v-card
    flat
    tile
    height="auto"
  >
    <v-card-text>
      <v-text-field
        v-model="cyberspace.scoreUrl"
        label="Score URL"
        :placeholder="scoreUrlExample"
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
    scoreUrlExample() {
      return String(cyberspaceSchema.properties.scoreUrl.examples[0]) || '';
    },
    questionsUrlExample() {
      return String(cyberspaceSchema.properties.questionsUrl.examples[0]) || '';
    }
  }
};
</script>
