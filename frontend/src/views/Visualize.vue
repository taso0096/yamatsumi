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
        v-if="originalNetwork.id"
        :network="network.data"
      />
    </v-navigation-drawer>

    <v-card
      tile
      flat
      :loading="!Object.keys(network).length"
    >
      <v-card-title>
        <span v-if="!Object.keys(network).length">Loading</span>
        <span v-else-if="!network.data">Network ID "{{ $route.params.networkId }}" does not exist.</span>
        <template v-else>
          <span>{{ network.data.label || network.data.id }}</span>
          <span class="mx-2">-</span>
          <span>{{ network.username }}</span>
          <span class="ml-auto mr-3 subtitle-1">{{ $_convertDateFormat(network.updatedAt) }}</span>
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

        <template v-if="originalNetwork.id">
          <network-entity :network="network.data" />
          <line-entity ref="lineEntity" />
        </template>
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
  name: 'Home',
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
    originalNetwork: {},
    network: {}
  }),
  async mounted() {
    const networkId = this.$route.params.networkId;
    this.network = await axios
      .get(`/networks/${networkId}/`)
      .then(res => res.data)
      .catch(err => {
        console.log(err);
        return { loaded: true };
      });
    if (!this.network.data) {
      return;
    }
    this.originalNetwork = JSON.parse(JSON.stringify(this.network.data));
    const routingTable = this.network.data.routingTable;
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
      const srcNodeId = Object.keys(routingTable)[Object.values(routingTable).findIndex(n => n.includes(data.srcIP))];
      const dstNodeId = Object.keys(routingTable)[Object.values(routingTable).findIndex(n => n.includes(data.dstIP))];
      const srcNode = data.srcIsGlobal ? '.internet-nodes' : srcNodeId ? `#node-${srcNodeId}` : '.intranet-nodes';
      const dstNode = data.dstIsGlobal ? '.internet-nodes' : dstNodeId ? `#node-${dstNodeId}` : '.intranet-nodes';
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
  }
};
</script>
