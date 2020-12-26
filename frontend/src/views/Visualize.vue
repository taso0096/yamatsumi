<template>
  <a-scene embedded>
    <a-camera position='0 1.5 5'>
      <a-cursor color='#888' />
    </a-camera>
    <a-sky color='#00022d' />
    <a-entity oculus-touch-controls="hand: left"></a-entity>
    <a-entity oculus-touch-controls="hand: right"></a-entity>

    <network-entity v-if="Object.keys(network).length" :network="network" />
    <line-entity ref="lineEntity" />
  </a-scene>
</template>

<script>
import NetworkEntity from '@/components/Network/BaseNetworkEntity.vue';
import LineEntity from '@/components/LineEntity.vue';

import axios from '@/axios';

export default {
  name: 'Home',
  components: {
    NetworkEntity,
    LineEntity
  },
  data: () => ({
    socket: {
      status: null
    },
    network: {}
  }),
  async mounted() {
    const networkId = this.$route.params.networkId;
    this.network = await axios
      .get(`/networks/${networkId}/`)
      .then(res => res.data.data)
      .catch(err => {
        console.log(err);
        this.$_pushNotice('ネットワーク情報の取得に失敗しました。', 'error');
        return false;
      });
    if (!this.network.id) {
      return;
    }
    const routingTable = this.network.routingTable;
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
