<template>
  <div>
    <v-dialog
      v-model="networkCreateDialog"
      max-width="400"
    >
      <v-card>
        <v-card-title>Create Network{{ newNetwork.data.id ? ' (Upload JSON)' : '' }}</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="newNetwork.id"
            label="Network ID"
            placeholder="If empty, UUID will be set."
            hide-details
          />
          <v-text-field
            v-model="newNetwork.label"
            label="Label"
            hide-details
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            tile
            text
            @click="networkCreateDialog = false"
          >
            <span>Cancel</span>
          </v-btn>
          <v-btn
            tile
            depressed
            :loading="isLoading.createNetwork"
            color="primary"
            @click="createNetwork"
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
            @click:append="searchNetwork"
            @keyup.enter="searchNetwork"
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
                <span>Create Network</span>
              </v-btn>
            </template>

            <v-list class="pa-0">
              <v-list-item @click="networkCreateDialog = true">
                <v-list-item-title>Create New</v-list-item-title>
              </v-list-item>
              <v-list-item @click="uploadNetwork">
                <v-list-item-title>Upload JSON</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-col>
      </v-row>
      <v-data-table
        :headers="headers"
        :items="networks"
        :items-per-page="10"
        :loading="isLoading.getNetworks"
      >
        <template v-slot:[`item.label`]="{ item }">
          <router-link
            :to="{ name: 'Visualize', params: { networkId: item.networkId } }"
            class="text-decoration-none"
          >
            {{ item.label || item.networkId }}
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
import axios from '@/axios'
import { validate } from 'jsonschema';
import networkSchema from '@/assets/NetworkSchema.json';

export default {
  name: 'Network',
  data: () => ({
    headers: [
      { text: 'Label', value: 'label', sortable: false },
      { text: 'Layers', value: 'layerCount', sortable: false, align: 'center' },
      { text: 'Nodes', value: 'nodeCount', sortable: false, align: 'center' },
      { text: 'Username', value: 'username', sortable: false, align: 'center' },
      { text: 'UpdatedAt', value: 'updatedAt', align: 'center' }
    ],
    networks: [],
    isLoading: {
      getNetworks: false,
      createNetwork: false
    },
    searchWord: '',
    networkCreateDialog: false,
    newNetwork: {
      id: '',
      label: '',
      data: {}
    }
  }),
  watch: {
    $route() {
      this.getNetworks();
    },
    networkCreateDialog(val) {
      if (!val) {
        this.newNetwork.id = '';
        this.newNetwork.label = '';
        this.newNetwork.data = {};
      }
    }
  },
  mounted() {
    this.getNetworks();
  },
  methods: {
    async getNetworks() {
      this.isLoading.getNetworks = true;
      this.searchWord = this.$route.query.search;
      await axios
        .get('/networks/', {
          params: {
            search: this.searchWord
          }
        })
        .then(res => {
          this.networks = res.data;
        })
        .catch(err => {
          console.log(err);
          this.$_pushNotice('Failed to retrieve network list.', 'error');
        });
      this.isLoading.getNetworks = false;
    },
    searchNetwork() {
      if (this.searchWord === this.$route.query.search) {
        this.getNetworks();
        return;
      }
      this.$router.push({
        query: {
          search: this.searchWord
        }
      });
    },
    async createNetwork() {
      if (!this.newNetwork.id) {
        const isConfirmed = await this.$_appRefs.confirmDialog.open({
          message: 'The Network ID was not set.\nDo you want to set UUID automatically?'
        });
        if (!isConfirmed) {
          return;
        }
      }
      this.isLoading.createNetwork = true;
      await axios
        .post('/networks/', {
          data: {
            layers: [],
            ...this.newNetwork.data,
            id: this.newNetwork.id,
            label: this.newNetwork.label
          }
        },
        {
          validateStatus: status => status < 500
        })
        .then(res => {
          if (res.status !== 201) {
            this.$_appRefs.confirmDialog.open({
              isAlert: true,
              title: 'Alert',
              message: 'This Network ID is already in use.'
            });
            return;
          }
          this.$_pushNotice('Created a new network.', 'success');
          this.$router.push({
            name: 'Visualize',
            params: {
              networkId: res.data.networkId
            }
          });
        })
        .catch(err => {
          console.log(err);
          this.$_pushNotice('An error occurred.', 'error');
        })
      this.isLoading.createNetwork = false;
    },
    uploadNetwork() {
      const inputEl = document.createElement('input');
      inputEl.type = 'file';
      inputEl.accept = '.json';
      inputEl.addEventListener('change', e => {
        const reader = new FileReader();
        reader.readAsText(e.target.files[0]);
        reader.addEventListener('load', () => {
          const network = JSON.parse(reader.result);
          const networkValidate = validate(network, networkSchema);
          if (!networkValidate.valid) {
            console.error('JSON Schema Validate ERROR', networkValidate.errors);
            this.$_pushNotice('An error occurred during JSON validation.', 'error');
            return;
          }
          this.newNetwork.id = network.id;
          this.newNetwork.label = network.label;
          this.newNetwork.data = network;
          this.networkCreateDialog = true;
        });
      });
      inputEl.click();
    }
  }
}
</script>
