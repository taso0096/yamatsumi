<template>
  <v-navigation-drawer
    v-model="drawer"
    app
    clipped
    floating
    right
    mobile-breakpoint="960"
    color="transparent"
    width="50%"
    class="cyberspace-drawer pt-3 pr-3"
  >
    <v-sheet>
      <v-toolbar flat color="transparent">
        <v-tabs v-model="drawerTab">
          <v-tab>Details</v-tab>
          <v-tab disabled>Exercise</v-tab>
          <v-tab>Network</v-tab>
          <v-spacer />

          <v-menu
            v-if="!editMode"
            bottom
            left
            offset-y
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                v-bind="attrs"
                v-on="on"
                class="my-auto mr-3"
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>

            <v-list class="pa-0">
              <v-list-item @click="enableEditMode">
                <v-list-item-title>Edit</v-list-item-title>
              </v-list-item>
              <v-list-item
                :disabled="isLoading.delete"
                @click="deleteCyberspace"
              >
                <v-list-item-title :class="{
                  'error--text': !isLoading.delete
                }">Delete</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
          <template v-else>
            <v-btn
              text
              tile
              class="my-auto mr-3"
              @click="disableEditMode(true)"
            >
              <span>Cancel</span>
            </v-btn>
            <v-btn
              color="primary"
              depressed
              tile
              :loading="isLoading.save"
              class="my-auto mr-3"
              @click="saveCyberspace"
            >
              <span>Save</span>
            </v-btn>
          </template>
        </v-tabs>
      </v-toolbar>
    </v-sheet>

    <v-form
      :readonly="!editMode"
      class="cyberspace-drawer__tab-items-wrapper mt-3"
    >
      <v-tabs-items
        v-model="drawerTab"
        class="cyberspace-drawer__tab-items"
      >
        <v-tab-item>
          <details-editor :cyberspace="cyberspace" />
        </v-tab-item>
        <v-tab-item>Exercise</v-tab-item>
        <v-tab-item>
          <network-editor
            :network="cyberspace.layers"
            :routingTable="cyberspace.routingTable"
            :editMode="editMode"
          />
        </v-tab-item>
      </v-tabs-items>
    </v-form>
  </v-navigation-drawer>
</template>

<style lang="scss" scoped>
.cyberspace-drawer {
  .cyberspace-drawer__tab-items-wrapper {
    height: calc(100% - 64px - 24px);

    .cyberspace-drawer__tab-items {
      height: 100%;
      background: transparent !important;
      overflow: scroll;

      div {
        height: 100%;
      }
    }
  }
}
</style>

<script>
import axios from '@/axios';

import DetailsEditor from '@/components/DetailsEditor.vue';
import NetworkEditor from '@/components/NetworkEditor';

export default {
  name: 'CyberspaceDrawer',
  components: {
    DetailsEditor,
    NetworkEditor
  },
  props: {
    drawer: {
      type: Boolean,
      default: false,
      required: true
    },
    cyberspace: {
      type: Object,
      required: true
    },
    copyCyberspace: {
      type: Function,
      required: true
    }
  },
  data: () => ({
    drawerTab: null,
    editMode: false,
    editIntervalId: null,
    isChangedForm: false,
    isLoading: {
      save: false,
      delete: false
    }
  }),
  watch: {
    'cyberspace.routingTable': {
      handler() {
        this.isChangedForm = true;
      },
      deep: true
    },
    'cyberspace.layers': {
      handler() {
        this.isChangedForm = true;
      },
      deep: true
    }
  },
  beforeDestroy() {
    this.$store.dispatch('updateEditState', false);
    clearInterval(this.editIntervalId);
  },
  methods: {
    async disableEditMode(needConfirm = false) {
      if (needConfirm) {
        const isConfirmed = await this.$_appRefs.confirmDialog.open({
          message: 'Are you sure you want to discard changes?',
          confirmText: 'Discard',
          color: 'error'
        });
        if (!isConfirmed) {
          return;
        }
      }
      this.editMode = false;
      this.$store.dispatch('updateEditState', false);
      this.copyCyberspace('original', 'visualize');
      this.copyCyberspace('original', 'edit');
      clearInterval(this.editIntervalId);
    },
    async enableEditMode() {
      this.editMode = true;
      this.$store.dispatch('updateEditState', true);
      this.editIntervalId = setInterval(() => {
        if (this.isChangedForm) {
          this.copyCyberspace('edit', 'visualize');
          this.isChangedForm = false;
        }
      }, 1000);
    },
    async saveCyberspace() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: 'Do you want to save the changes?',
        confirmText: 'Save'
      });
      if (!isConfirmed) {
        return;
      }
      this.isLoading.save = true;
      const id = this.$route.params.id;
      await axios
        .put(`/cyberspaces/${id}/`, {
          data: this.cyberspace
        },
        {
          validateStatus: status => status < 500
        })
        .then(res => {
          if (res.status !== 200) {
            this.$_pushNotice('This Cyberspace ID is already in use.', 'error');
            return;
          }
          this.copyCyberspace('edit', 'visualize');
          this.copyCyberspace('edit', 'original');
          this.disableEditMode();
          this.$_pushNotice('Saved the Cyberspace.', 'success');
          if (this.cyberspace.id !== id) {
            this.$router.push({
              name: 'Visualize',
              params: {
                id: this.cyberspace.id
              }
            });
          }
        })
        .catch(() => {
          this.$_pushNotice('An error occurred.', 'error');
        });
      this.isLoading.save = false;
    },
    async deleteCyberspace() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: 'Are you sure you want to delete this Cyberspace?',
        confirmText: 'Delete',
        color: 'error'
      });
      if (!isConfirmed) {
        return;
      }
      this.isLoading.delete = true;
      const id = this.$route.params.id;
      await axios
        .delete(`/cyberspaces/${id}/`)
        .then(() => {
          this.$_pushNotice('Deleted the Cyberspace.', 'success');
          this.$router.push({ name: 'Cyberspace' });
        })
        .catch(() => {
          this.$_pushNotice('An error occurred.', 'error');
        });
      this.isLoading.delete = false;
    }
  }
};
</script>
