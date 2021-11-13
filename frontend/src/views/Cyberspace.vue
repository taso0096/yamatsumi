<template>
  <div class="cyberspace-v2">
    <cyberspace-drawer
        v-if="cyberspace.original.id"
      :drawer="cyberspaceDrawer"
        :cyberspace="cyberspace.edit"
        :copyCyberspace="copyCyberspace"
      />

    <v-card
      tile
      flat
      :loading="isLoading.cyberspace"
    >
      <v-card-title>
        <span v-if="isLoading.cyberspace">Loading</span>
        <span v-else-if="!cyberspaceInfo.id">Cyberspace ID "{{ $route.params.id }}" does not exist.</span>
        <template v-else>
          <span>{{ cyberspaceInfo.label || cyberspaceInfo.id }}</span>
          <span class="mx-2">-</span>
          <span>{{ cyberspaceInfo.username }}</span>
          <span class="ml-auto mr-3 subtitle-1">{{ $_convertDateFormat(cyberspaceInfo.updatedAt) }}</span>
          <v-btn
            icon
            small
            :disabled="!cyberspace.original.id"
            @click="cyberspaceDrawer = !cyberspaceDrawer"
          >
            <v-icon v-if="!cyberspaceDrawer">mdi-settings</v-icon>
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
        <a-camera v-if="!isEditMode" position='0 1.5 5' />
        <a-camera
          v-else
          position='0 3 0'
          rotation="-90 0 0"
          look-controls="enabled: false"
          wasd-controls="enabled: false"
        />
        <a-sky color='#000' />
        <a-entity oculus-touch-controls="hand: left"></a-entity>
        <a-entity oculus-touch-controls="hand: right"></a-entity>

        <cyberspace-entity ref="cyberspaceEntity" />
        <line-entity ref="lineEntity" />
      </a-scene>
    </v-card>
  </div>
</template>

<style lang="scss" scoped>
.cyberspace-v2 {
  height: 100%;

  a-scene {
    height: 100%;
  }
}
</style>

<script>
import CyberspaceEntity from '@/components/Cyberspace/CyberspaceEntity.vue';
import LineEntity from '@/components/LineEntity.vue';
import CyberspaceDrawer from '@/components/CyberspaceDrawer.vue';

import axios from '@/axios';

export default {
  name: 'Cyberspace',
  components: {
    CyberspaceEntity,
    LineEntity,
    CyberspaceDrawer
  },
  data: () => ({
    socket: {
      status: null
    },
    cyberspaceInfo: {},
    cyberspace: {
      original: {},
      visualize: {},
      edit: {}
    },
    exercise: {},
    scoreData: {},
    isLoading: {
      cyberspace: true
    },
    cyberspaceDrawer: false,
    isEditMode: false
  }),
  watch: {
    $route() {
      this.$_createPageTitle({
        title: `${(this.cyberspace.original.label || this.cyberspace.original.id)} - YAMATSUMI`
      });
    }
  },
  async mounted() {
    const id = this.$route.params.id;
    // cyberspace読み込み
    const originalCyberspace = await axios
      .get(`/cyberspaces/${id}/`)
      .then(res => {
        this.cyberspaceInfo = {
          id,
          label: res.data.data.label,
          username: res.data.username,
          updatedAt: res.data.updatedAt
        };
        return res.data.data;
      })
      .catch(() => undefined);
    this.isLoading.cyberspace = false;
    if (!originalCyberspace) {
      return;
    }
    // 編集等で使用するcyberspaceのコピー
    this.cyberspace = {
      original: JSON.parse(JSON.stringify(originalCyberspace)),
      visualize: JSON.parse(JSON.stringify(originalCyberspace)),
      edit: JSON.parse(JSON.stringify(originalCyberspace))
    };
    this.$_createPageTitle({
      title: `${(this.cyberspace.original.label || this.cyberspace.original.id)} - YAMATSUMI`
    });
    // exercise読み込み
    this.exercise = await axios
      .get(`/exercises/${id}/`)
      .then(res => res.data)
      .catch(() => undefined);
    if (this.exercise?.scoreUrl) {
      this.scoreData = await fetch(this.exercise.scoreUrl)
        .then(res => res.json())
        .catch(() => undefined);
    }

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
    this.socket = await this.$store.dispatch('connectSocket', id);
    this.socket.on('packet', data => {
      const userId = data.userId;
      const port = lineColor.get(data.srcPort) || lineColor.get(data.dstPort);
      if (userId) {
        const user = this.$_visualizeData.exercise.users.find(u => u.id === userId);
        this.$refs.lineEntity.emit3(`#node-${user.nodeId}`, '.internet-nodes', port?.color || '#fff');
        return;
      }
      const routingTable = this.cyberspace.visualize.routingTable;
      const usersRoutingTable = this.exercise.routingTable;
      const srcNodeId = Object.keys(routingTable)[Object.values(routingTable).findIndex(n => n.includes(data.srcIP))] || Object.keys(usersRoutingTable)[Object.values(usersRoutingTable).findIndex(n => n.includes(data.srcIP))];
      const dstNodeId = Object.keys(routingTable)[Object.values(routingTable).findIndex(n => n.includes(data.dstIP))] || Object.keys(usersRoutingTable)[Object.values(usersRoutingTable).findIndex(n => n.includes(data.dstIP))];
      const srcNode = srcNodeId ? `#node-${srcNodeId}` : data.srcIsGlobal ? '.internet-nodes' : '.intranet-nodes';
      const dstNode = dstNodeId ? `#node-${dstNodeId}` : data.dstIsGlobal ? '.internet-nodes' : '.intranet-nodes';
      this.$refs.lineEntity.emit3(srcNode, dstNode, port?.color || '#fff');
    });
    this.socket.on('answer', data => {
      const answerData = JSON.parse(data);
      Object.entries(answerData.scores.teams).forEach(([teamId, targetScore]) => {
        this.$refs.lineEntity.emitAnswer(teamId, answerData.questionId, answerData.isSuccess, () => {
          if (!answerData.isSuccess) {
            return;
          }
          const scoreIntervalId = setInterval(() => {
            const score = this.exercise.scores[teamId].score;
            if (score < targetScore) {
              this.$set(this.exercise.scores[teamId], 'score', score + 5);
            } else {
              clearInterval(scoreIntervalId);
            }
          }, 20);
        });
      });
      Object.entries(answerData.scores.users).forEach(([userId, targetScore]) => {
        this.$refs.lineEntity.emitAnswer(userId, answerData.questionId, answerData.isSuccess, () => {
          if (!answerData.isSuccess) {
            return;
          }
          const scoreIntervalId = setInterval(() => {
            const score = this.exercise.scores[answerData.teamId].users[userId];
            if (score < targetScore) {
              this.$set(this.exercise.scores[answerData.teamId].users, userId, score + 5);
            } else {
              clearInterval(scoreIntervalId);
            }
          }, 20);
        });
      });
    });
    this.socket.on('notice', data => {
      this.$_pushNotice(data.text, data.type);
    });

    this.$refs.cyberspaceEntity.set({
      cyberspace: this.cyberspace.visualize,
      exercise: this.exercise,
      score: this.scoreData
    });
  },
  beforeDestroy() {
    if (this.socket.status === 'connect') {
      this.socket.off('answer');
      this.socket.off('packet');
      this.socket.off('notice');
      this.$store.dispatch('resetSocket');
      this.$store.dispatch('resetVisualizeData');
    }
  },
  methods: {
    copyCyberspace(src, dst) {
      this.$set(this.cyberspace, dst, JSON.parse(JSON.stringify(this.cyberspace[src])));
      if (dst === 'visualize') {
        this.$refs.cyberspaceEntity.set({
          cyberspace: this.cyberspace.visualize,
          exercise: this.exercise,
          score: this.scoreData
        });
      }
    }
  }
};
</script>
