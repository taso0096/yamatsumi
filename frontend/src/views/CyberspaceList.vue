<template>
  <div>
    <v-dialog
      v-model="cyberspaceCreateDialog"
      max-width="400"
    >
      <v-card>
        <v-card-title>Create Cyberspace{{ newCyberspace.data.id ? ' (Upload JSON)' : '' }}</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="newCyberspace.id"
            label="Cyberspace ID"
            placeholder="If empty, UUID will be set."
            hide-details
          />
          <v-text-field
            v-model="newCyberspace.label"
            label="Label"
            hide-details
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            tile
            text
            @click="cyberspaceCreateDialog = false"
          >
            <span>Cancel</span>
          </v-btn>
          <v-btn
            tile
            depressed
            :loading="isLoading.createCyberspace"
            color="primary"
            @click="createCyberspace"
          >
            <span>Create</span>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-sheet>
      <v-row class="mx-1">
        <v-col class="col-12 col-sm-4">
          <v-text-field
            v-model="searchWord"
            append-icon="mdi-magnify"
            label="Search"
            hide-details
            clearable
            @click:append="searchCyberspace"
            @keyup.enter="searchCyberspace"
          />
        </v-col>
        <v-spacer />
        <v-col
          cols="auto"
          class="d-flex align-center"
        >
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
              >
                <span>Create Cyberspace</span>
              </v-btn>
            </template>

            <v-list class="pa-0">
              <v-list-item @click="cyberspaceCreateDialog = true">
                <v-list-item-title>Create New</v-list-item-title>
              </v-list-item>
              <v-list-item @click="uploadCyberspace">
                <v-list-item-title>Upload JSON</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-col>
      </v-row>
      <v-data-table
        :headers="headers"
        :items="cyberspaces"
        :items-per-page="10"
        :loading="isLoading.getCyberspaces"
      >
        <template v-slot:[`item.label`]="{ item }">
          <router-link
            :to="{ name: 'Cyberspace', params: { id: item.id } }"
            class="text-decoration-none"
          >
            {{ item.label || item.id }}
          </router-link>
        </template>
        <template v-slot:[`item.updatedAt`]="{ item }">
          <div>
            {{ $_convertDateFormat(item.updatedAt) }}
          </div>
        </template>
      </v-data-table>
    </v-sheet>
  </div>
</template>

<style lang="scss" scoped>
.v-data-table {
    background: transparent !important;
}
</style>

<script>
import axios from '@/axios';
import { validate } from 'jsonschema';
import cyberspaceSchema from '@/assets/CyberspaceSchema.json';

export default {
  name: 'CyberspaceList',
  data: () => ({
    headers: [
      { text: 'Label', value: 'label', sortable: false },
      { text: 'Username', value: 'username', sortable: false, align: 'center' },
      { text: 'UpdatedAt', value: 'updatedAt', align: 'center' }
    ],
    cyberspaces: [],
    isLoading: {
      getCyberspaces: false,
      createCyberspace: false
    },
    searchWord: '',
    cyberspaceCreateDialog: false,
    newCyberspace: {
      id: '',
      label: '',
      data: {}
    }
  }),
  watch: {
    $route() {
      this.getCyberspaces();
    },
    cyberspaceCreateDialog(val) {
      if (!val) {
        this.newCyberspace.id = '';
        this.newCyberspace.label = '';
        this.newCyberspace.data = {};
      }
    }
  },
  mounted() {
    this.getCyberspaces();
  },
  methods: {
    async getCyberspaces() {
      this.isLoading.getCyberspaces = true;
      this.searchWord = this.$route.query.search;
      await axios
        .get('/cyberspaces/', {
          params: {
            search: this.searchWord
          }
        })
        .then(res => {
          this.cyberspaces = res.data;
        })
        .catch(err => {
          console.log(err);
          this.$_pushNotice('Failed to retrieve cyberspace list.', 'error');
        });
      this.isLoading.getCyberspaces = false;
    },
    searchCyberspace() {
      if (this.searchWord === this.$route.query.search) {
        this.getCyberspaces();
        return;
      }
      this.$router.push({
        query: {
          search: this.searchWord
        }
      });
    },
    async createCyberspace() {
      if (!this.newCyberspace.id) {
        const isConfirmed = await this.$_appRefs.confirmDialog.open({
          message: 'The Cyberspace ID was not set.\nDo you want to set UUID automatically?'
        });
        if (!isConfirmed) {
          return;
        }
      }
      this.isLoading.createCyberspace = true;
      await axios
        .post('/cyberspaces/', {
          data: {
            layers: [],
            ...this.newCyberspace.data,
            id: this.newCyberspace.id,
            label: this.newCyberspace.label
          }
        },
        {
          validateStatus: status => status < 500
        })
        .then(res => {
          if (res.status !== 201) {
            this.$_pushNotice('This Cyberspace ID is already in use.', 'error');
            return;
          }
          this.$_pushNotice('Created a new cyberspace.', 'success');
          this.$router.push({
            name: 'Cyberspace',
            params: {
              id: res.data.id
            }
          });
        })
        .catch(err => {
          console.log(err);
          this.$_pushNotice('An error occurred.', 'error');
        });
      this.isLoading.createCyberspace = false;
    },
    uploadCyberspace() {
      const inputEl = document.createElement('input');
      inputEl.type = 'file';
      inputEl.accept = '.json';
      inputEl.addEventListener('change', e => {
        const reader = new FileReader();
        reader.readAsText(e.target.files[0]);
        reader.addEventListener('load', () => {
          const cyberspace = JSON.parse(reader.result);
          const cyberspaceValidate = validate(cyberspace, cyberspaceSchema);
          if (!cyberspaceValidate.valid) {
            console.error('JSON Schema Validate ERROR', cyberspaceValidate.errors);
            this.$_pushNotice('An error occurred during JSON validation.', 'error');
            return;
          }
          this.newCyberspace.id = cyberspace.id;
          this.newCyberspace.label = cyberspace.label;
          this.newCyberspace.data = cyberspace;
          this.cyberspaceCreateDialog = true;
        });
      });
      inputEl.click();
    }
  }
};
</script>
