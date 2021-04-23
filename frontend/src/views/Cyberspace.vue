<template>
  <div class="exercise">
    <v-navigation-drawer
      v-model="editDrawer"
      app
      clipped
      floating
      right
      mobile-breakpoint="960"
      color="transparent"
      width="1024"
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
        <span v-if="!exercise">Exercise ID "{{ $route.params.exerciseId }}" does not exist.</span>
        <span v-else-if="!Object.keys(exercise).length">Loading</span>
        <template v-else>
          <span>{{ exercise.data.label || exercise.data.id }}</span>
          <span class="mx-2">-</span>
          <span>{{ exercise.username }}</span>
          <span class="ml-auto mr-3 subtitle-1">{{ $_convertDateFormat(exercise.updatedAt) }}</span>
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
.exercise {
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
  name: 'Cyberspace',
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
    network: {
      original: {},
      visualize: {},
      edit: {}
    },
    exercise: {},
    scoreData: {}
  }),
  watch: {
    $route() {
      this.$_createPageTitle({
        title: `${(this.network.original.label || this.network.original.id)} - YAMATSUMI`
      });
    }
  },
  async mounted() {
    const exerciseId = this.$route.params.exerciseId;
    this.exercise = await axios
      .get(`/exercises/${exerciseId}/`)
      .then(res => res.data)
      .catch(err => {
        console.log(err);
        return undefined;
      });
    if (!this.exercise) {
      return;
    }
    this.scoreData = await fetch(this.exercise.data.scoreUrl)
      .then(res => res.json())
      .catch(() => undefined);

    const originalNetwork = await axios
      .get(`/networks/${exerciseId}/`)
      .then(res => res.data.data)
      .catch(err => {
        console.log(err);
        return undefined;
      });
    if (!originalNetwork) {
      return;
    }
    this.network = {
      original: JSON.parse(JSON.stringify(originalNetwork)),
      visualize: JSON.parse(JSON.stringify(originalNetwork)),
      edit: JSON.parse(JSON.stringify(originalNetwork))
    };
    this.$_createPageTitle({
      title: `${(this.network.original.label || this.network.original.id)} - YAMATSUMI`
    });
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
    this.socket = await this.$store.dispatch('connectSocket', exerciseId);
    this.socket.on('packet', data => {
      const userId = data.userId;
      const port = lineColor.get(data.srcPort) || lineColor.get(data.dstPort);
      if (userId) {
        const user = this.$_visualizeData.exercise.users.find(u => u.id === userId);
        this.$refs.lineEntity.emit1(`#node-${user.nodeId}`, '.internet-nodes', port?.color || '#fff');
        return;
      }
      const routingTable = this.network.visualize.routingTable;
      const srcNodeId = Object.keys(routingTable)[Object.values(routingTable).findIndex(n => n.includes(data.srcIP))];
      const dstNodeId = Object.keys(routingTable)[Object.values(routingTable).findIndex(n => n.includes(data.dstIP))];
      const srcNode = srcNodeId ? `#node-${srcNodeId}` : data.srcIsGlobal ? '.internet-nodes' : '.intranet-nodes';
      const dstNode = dstNodeId ? `#node-${dstNodeId}` : data.dstIsGlobal ? '.internet-nodes' : '.intranet-nodes';
      this.$refs.lineEntity.emit1(srcNode, dstNode, port?.color || '#fff');
    });
    this.socket.on('answer', data => {
      this.$refs.lineEntity.emitAnswer(data.uid, data.qid, data.isCorrect, () => {
        if (!data.isCorrect) {
          return;
        }
        const levelId = (this.exercise.data.questions || []).find(q => String(q.id) === String(data.qid))?.levelId;
        const targetScore = this.scoreData.users[data.uid] + (this.exercise.data.levels || []).find(l => String(l.id) === String(levelId))?.score;
        if (!targetScore) {
          return;
        }
        const scoreIntervalId = setInterval(() => {
          const score = this.scoreData.users[data.uid];
          if (score < targetScore) {
            this.$set(this.scoreData.users, data.uid, score + 5);
          } else {
            clearInterval(scoreIntervalId);
          }
        }, 20);
      });
    });
    this.socket.on('notice', data => {
      this.$_pushNotice(data.text, data.type);
    });

    this.$refs.networkEntity.set({
      exercise: this.exercise.data,
      network: this.network.visualize,
      score: this.scoreData
    });
  },
  beforeDestroy() {
    if (this.socket.status === 'connect') {
      this.socket.off('answer');
      this.socket.off('packet');
      this.socket.off('notice');
      this.$store.dispatch('resetSocket');
      this.$store.dispatch('resetEvent');
    }
  },
  methods: {
    copyNetwork(src, dst) {
      this.$set(this.network, dst, JSON.parse(JSON.stringify(this.network[src])));
      if (dst === 'visualize') {
        this.$refs.networkEntity.set({
          exercise: this.exercise.data,
          network: this.network.visualize,
          score: this.scoreData
        });
      }
    }
  }
};
</script>
