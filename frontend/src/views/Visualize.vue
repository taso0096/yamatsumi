<template>
  <div class="visualize">
    <v-navigation-drawer
      v-model="editDrawer"
      app
      clipped
      floating
      right
      mobile-breakpoint="960"
      color="transparent"
      width="600"
      class="pt-3 pr-3"
    >
      <network-editor
        v-if="network.original.id"
        :network="network.edit"
        :copyNetwork="copyNetwork"
      />
    </v-navigation-drawer>

    <v-card
      tile
      flat
      :loading="!Object.keys(network).length"
    >
      <v-card-title>
        <span v-if="!Object.keys(networkData).length">Loading</span>
        <span v-else-if="!network.original.id">Network ID "{{ $route.params.networkId }}" does not exist.</span>
        <template v-else>
          <span>{{ network.original.label || network.original.id }}</span>
          <span class="mx-2">-</span>
          <span>{{ networkData.username }}</span>
          <span class="ml-auto mr-3 subtitle-1">{{ $_convertDateFormat(networkData.updatedAt) }}</span>
          <v-btn
            icon
            small
            @click="editDrawer = !editDrawer"
          >
            <v-icon v-if="!editDrawer">mdi-settings</v-icon>
            <v-icon v-else>mdi-arrow-right</v-icon>
          </v-btn>
        </template>
      </v-card-title>
    </v-card>

    <v-card
      tile
      outlined
      width="100%"
      height="calc(100% - 64px)"
    >
      <a-scene embedded>
        <a-camera position='0 1.5 5' />
        <a-sky color='#000' />
        <a-entity oculus-touch-controls="hand: left"></a-entity>
        <a-entity oculus-touch-controls="hand: right"></a-entity>

        <network-entity ref="networkEntity" />
        <line-entity ref="lineEntity" />
      </a-scene>
    </v-card>
  </div>
</template>

<style lang="scss" scoped>
.visualize {
  height: 100%;

  a-scene {
    height: 100%;
  }
}
</style>

<script>
import NetworkEntity from '@/components/Network/BaseNetworkEntity.vue';
import LineEntity from '@/components/LineEntity.vue';
import NetworkEditor from '@/components/NetworkEditor/NetworkEditor.vue';

import axios from '@/axios';

export default {
  name: 'Visualize',
  components: {
    NetworkEntity,
    LineEntity,
    NetworkEditor
  },
  data: () => ({
    editDrawer: false,
    socket: {
      status: null
    },
    networkData: {},
    network: {
      original: {},
      visualize: {},
      edit: {}
    }
  }),
  async mounted() {
    const networkId = this.$route.params.networkId;
    this.networkData = await axios
      .get(`/networks/${networkId}/`)
      .then(res => res.data)
      .catch(err => {
        console.log(err);
        return { loaded: true };
      });
    if (!this.networkData.data) {
      return;
    }
    this.network = {
      original: JSON.parse(JSON.stringify(this.networkData.data)),
      visualize: JSON.parse(JSON.stringify(this.networkData.data)),
      edit: JSON.parse(JSON.stringify(this.networkData.data))
    };
    this.$refs.networkEntity.set(this.network.visualize);
    const lineColor = new Map([
      [22, {
        service: 'ssh',
        color: '#ff0000'
      }],
      [53, {
        service: 'dns',
        color: '#2ecc71'
      }],
      [80, {
        service: 'web',
        color: '#3498db'
      }],
      [443, {
        service: 'web',
        color: '#3498db'
      }],
      [8623, {
        service: 'yamatsumi',
        color: '#3498db'
      }],
      [445, {
        service: 'ntlm',
        color: '#f1c40f'
      }],
      [3389, {
        service: 'r_d',
        color: '#f36bff'
      }],
      [5432, {
        service: 'db',
        color: '#cdffb5'
      }]
    ]);
    this.socket = await this.$store.dispatch('connectSocket', networkId);
    this.socket.on('packet', data => {
      const routingTable = this.network.visualize.routingTable;
      const srcNodeId = Object.keys(routingTable)[Object.values(routingTable).findIndex(n => n.includes(data.srcIP))];
      const dstNodeId = Object.keys(routingTable)[Object.values(routingTable).findIndex(n => n.includes(data.dstIP))];
      const srcNode = srcNodeId ? `#node-${srcNodeId}` : data.srcIsGlobal ? '.internet-nodes' : '.intranet-nodes';
      const dstNode = dstNodeId ? `#node-${dstNodeId}` : data.dstIsGlobal ? '.internet-nodes' : '.intranet-nodes';
      const port = lineColor.get(data.srcPort) || lineColor.get(data.dstPort);
      if (['ssh', 'ntlm', 'r_d'].includes(port?.service)) {
        console.log(`${port.service}: ${srcNode === '#node-else' ? data.srcIP : srcNode} -> ${dstNode === '#node-else' ? data.dstIP : dstNode}`);
      }
      this.$refs.lineEntity.emit1(srcNode, dstNode, port?.color || '#fff');
    });
    this.socket.on('notice', data => {
      this.$_pushNotice(data.text, data.type);
    });
  },
  beforeDestroy() {
    if (this.socket.status === 'connect') {
      this.socket.off('packet');
      this.socket.off('notice');
      this.$store.dispatch('resetSocket');
    }
  },
  methods: {
    copyNetwork(src, dst) {
      this.$set(this.network, dst, JSON.parse(JSON.stringify(this.network[src])));
      if (dst === 'visualize') {
        this.$refs.networkEntity.set(this.network.visualize);
      }
    }
  }
};
</script>
