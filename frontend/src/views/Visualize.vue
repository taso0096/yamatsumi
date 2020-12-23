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
    this.network = await axios
      .get(`/networks/${this.$route.params.networkId}/`)
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
    this.socket = await this.$store.dispatch('connectSocket');
    this.socket.on('send_packet', data => {
      const srcNode = data.srcIsGlobal ? '.internet-nodes' : `#node-${Object.keys(routingTable)[Object.values(routingTable).findIndex(n => n.includes(data.srcIP))]}`;
      const dstNode = data.dstIsGlobal ? '.internet-nodes' : `#node-${Object.keys(routingTable)[Object.values(routingTable).findIndex(n => n.includes(data.dstIP))]}`;
      this.$refs.lineEntity.emit1(srcNode, dstNode);
    });
  },
  beforeDestroy() {
    this.socket.off('send_packet');
  }
};
</script>
