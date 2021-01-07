<template>
  <div>
    <v-dialog
      v-model="networkCreateDialog"
      max-width="400"
    >
      <v-card>
        <v-card-title>Create Network</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="newNetwork.id"
            label="Network ID"
            placeholder="If empty, uuid will be set."
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
          <v-btn
            tile
            depressed
            small
            color="primary"
            @click="networkCreateDialog = true"
          >
            <span>Create Network</span>
          </v-btn>
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
      label: ''
    }
  }),
  watch: {
    $route() {
      this.getNetworks();
    },
    networkCreateDialog() {
      this.newNetwork.id = '';
      this.newNetwork.label = '';
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
            id: this.newNetwork.id,
            label: this.newNetwork.label,
            layers: []
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
    }
  }
}
</script>
