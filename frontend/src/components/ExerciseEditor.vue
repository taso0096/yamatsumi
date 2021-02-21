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
          v-if="!mode.edit"
          bottom
          left
          offset-y
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>

          <v-list class="pa-0">
            <v-list-item
              :disabled="isLoading.delete"
              @click="deleteExercise"
            >
              <v-list-item-title :class="{
                'error--text': !isLoading.delete
              }">Delete</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-card-title>
    </v-card>

    <v-form
      :readonly="!mode.edit"
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

export default {
  name: 'ExerciseEditor',
  props: {
    exercise: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    mode: {
      edit: false
    },
    isLoading: {
      delete: false
    }
  }),
  methods: {
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
          this.$router.push({ name: 'Exercise' });
        })
        .catch(err => {
          console.log(err);
          this.$_pushNotice('An error occurred.', 'error');
        });
      this.isLoading.delete = false;
    }
  }
}
</script>
