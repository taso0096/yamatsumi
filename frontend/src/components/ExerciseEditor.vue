<template>
  <div class="exercise-editor">
    <v-card
      tile
      flat
      class="exercise-editor__title-header mt-3"
    >
      <v-card-title>
        <span>Details</span>
        <v-spacer />
        <v-menu
          bottom
          left
          offset-y
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-bind="attrs"
              v-on="on"
              tile
              depressed
              small
              color="primary"
              :disabled="isLoading.upload"
            >
              <span>Upload JSON</span>
            </v-btn>
          </template>

          <v-list class="pa-0">
            <v-list-item @click="selectJSON('exercise')">
              <v-list-item-title>Exercise</v-list-item-title>
            </v-list-item>
            <v-list-item @click="selectJSON('network')">
              <v-list-item-title>Network</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-btn
          tile
          depressed
          small
          color="error"
          :disabled="isLoading.delete"
          class="ml-3"
          @click="deleteExercise"
        >Delete</v-btn>
      </v-card-title>
    </v-card>

    <v-form
      readonly
      class="exercise-editor__form"
    >
      <v-card
        tile
        flat
        class="mb-3"
      >
        <v-card-text>
          <v-text-field
            v-model="exercise.data.id"
            label="Exercise ID"
          />
          <v-text-field
            v-model="exercise.label"
            label="Exercise Label"
          />
          <v-text-field
            v-model="exercise.version"
            label="Version"
          />
          <v-textarea
            v-model="exercise.desc"
            label="Description"
          />
        </v-card-text>
      </v-card>
    </v-form>
  </div>
</template>

<style lang="scss" scoped>
.exercise-editor {
  height: calc(100% - 64px - 12px);
  margin-top: calc(64px + 12px);

  .exercise-editor__title-header {
    position: absolute;
    top: 0;
    width: calc(100% - 12px);
    z-index: 1;
  }
  .exercise-editor__form {
    height: 100%;
    overflow: scroll;
  }
}
</style>

<script>
import axios from '@/axios';
import { validate } from 'jsonschema';
import exerciseSchema from '@/assets/ExerciseSchema.json';
import networkSchema from '@/assets/NetworkSchema.json';

export default {
  name: 'ExerciseEditor',
  props: {
    exercise: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    isLoading: {
      upload: false,
      delete: false
    }
  }),
  computed: {
    schema: () => ({
      exercise: exerciseSchema,
      network: networkSchema
    })
  },
  methods: {
    selectJSON(type) {
      const inputEl = document.createElement('input');
      inputEl.type = 'file';
      inputEl.accept = '.json';
      inputEl.addEventListener('change', e => {
        const reader = new FileReader();
        reader.readAsText(e.target.files[0]);
        reader.addEventListener('load', () => {
          const data = JSON.parse(reader.result);
          const dataValidate = validate(data, this.schema[type]);
          if (!dataValidate.valid) {
            console.error('JSON Schema Validate ERROR', dataValidate.errors);
            this.$_pushNotice('An error occurred during JSON validation.', 'error');
            return;
          }
          this.updateJSON(type, data);
        });
      });
      inputEl.click();
    },
    async updateJSON(type, data) {
      this.isLoading.upload = true;
      const exerciseId = this.$route.params.exerciseId;
      await axios
        .put(`/${type}s/${exerciseId}/`, {
          data
        })
        .then(res => {
          this.$_pushNotice(`Saved the ${type.charAt(0).toUpperCase() + type.slice(1)}.`, 'success');
        })
        .catch(err => {
          console.log(err);
          this.$_pushNotice('An error occurred.', 'error');
        });
      this.isLoading.upload = false;
    },
    async deleteExercise() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: 'Are you sure you want to delete this Exercise?',
        confirmText: 'Delete',
        color: 'error'
      });
      if (!isConfirmed) {
        return;
      }
      this.isLoading.delete = true;
      const exerciseId = this.$route.params.exerciseId;
      await axios
        .delete(`/exercises/${exerciseId}/`)
        .then(() => {
          this.$_pushNotice('Deleted the Exercise', 'success');
          this.$router.push({ name: 'ExerciseList' });
        })
        .catch(err => {
          console.log(err);
          this.$_pushNotice('An error occurred.', 'error');
        });
      this.isLoading.delete = false;
    }
  }
};
</script>
