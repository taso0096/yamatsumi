<template>
  <div>
    <v-sheet rounded="lg">
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
      getNetworks: false
    }
  }),
  async mounted() {
    await this.getNetworks();
  },
  methods: {
    async getNetworks() {
      this.isLoading.getNetworks = true;
      await axios
        .get('/networks/')
        .then(res => {
          this.networks = res.data;
        })
        .catch(err => {
          console.log(err);
          this.$_pushNotice('ネットワーク一覧の取得に失敗しました。', 'error');
        });
      this.isLoading.getNetworks = false;
    }
  }
}
</script>
