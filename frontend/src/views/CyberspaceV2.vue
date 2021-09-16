<template>
  <div class="cyberspace-v2">
    <v-navigation-drawer
      v-model="editDrawer"
      app
      clipped
      floating
      right
      mobile-breakpoint="960"
      color="transparent"
      width="50%"
      class="pt-3 pr-3"
    >
      <network-editor
        v-if="cyberspace.original.id"
        :networkData="cyberspace.edit.layers"
        class="ma-3"
      />
    </v-navigation-drawer>

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
import NetworkEditor from '@/components/NetworkEditor';

import axios from '@/axios';

export default {
  name: 'Cyberspace',
  components: {
    CyberspaceEntity,
    LineEntity,
    NetworkEditor
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
    editDrawer: false,
    isEditMode: false
  }),
  watch: {
    $route() {
      this.$_createPageTitle({
        title: `${(this.cyberspace.original.label || this.cyberspace.original.id)} - YAMATSUMI`
      });
    },
    'cyberspace.edit': {
      handler() {
        this.copyCyberspace('edit', 'visualize');
      },
      deep: true
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
      .then(res => res.data.data)
      .catch(() => undefined);
    if (this.exercise?.scoreUrl) {
      this.scoreData = await fetch(this.exercise.scoreUrl)
        .then(res => res.json())
        .catch(() => undefined);
    }

    this.$refs.cyberspaceEntity.set({
      cyberspace: this.cyberspace.visualize,
      exercise: this.exercise,
      score: this.scoreData
    });
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
