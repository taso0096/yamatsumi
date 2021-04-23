<template>
  <div class="group-card d-flex">
    <v-card
      tile
      flat
      min-width="500"
      width="500"
      height="100%"
      class="mb-3"
    >
      <v-card-title class="font-weight-regular">
        <span>{{ groupData.label || groupData.id || 'Layers' }}</span>
        <v-spacer />
        <v-btn
          v-if="isLayer"
          icon
          small
          @click="showDetails.parentNode = !showDetails.parentNode"
        >
          <v-icon>
            {{ showDetails.parentNode ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
          </v-icon>
        </v-btn>
        <v-btn
          v-else
          icon
          small
          @click="closeGroup()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-expand-transition>
        <div v-show="showDetails.parentNode">
          <v-card-text class="pt-0">
            <div
              v-if="!groupTopNodes.length"
              class="mb-4"
            >
              <span>No data available</span>
            </div>
            <div
              v-else
              v-for="(node, i) in groupTopNodes"
              :key="`layer-${i}`"
              class="d-flex mb-4"
            >
              <node-card
                :isLayer="isLayer"
                :nodeData="node"
                :nodeIndex="i"
                :showDetails="showDetails"
                :pushGroup="pushGroup"
                :addNode="addNode"
              />
              <div
                v-if="editMode"
                class="d-flex align-center ml-3"
              >
                <v-btn
                  icon
                  small
                  @click="deleteIndex(i)"
                >
                  <v-icon color="error">mdi-delete-outline</v-icon>
                </v-btn>
              </div>
            </div>
            <div
              v-if="editMode"
              class="text-center mb-4"
            >
              <v-btn
                v-if="isLayer"
                tile
                depressed
                small
                color="primary"
                @click="addLayer"
              >
                <span>Add Layer</span>
              </v-btn>
              <div
                v-else
                class="text-center mb-4"
              >
                <v-btn
                  tile
                  depressed
                  small
                  color="primary"
                  @click="addNode(groupData.nodes)"
                >
                  <span>Add Node</span>
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </div>
      </v-expand-transition>
    </v-card>

    <group-card
      v-if="showNextGroup"
      :groupData="nextGroupData"
      :closeGroup="closeNextGroup"
      class="ml-3"
    />
  </div>
</template>

<style lang="scss" scoped>
.group-card {
  height: 100%;
}
</style>

<script>
import GroupCard from './GroupCard.vue';
import NodeCard from './NodeCard.vue';

export default {
  name: 'GroupCard',
  components: {
    GroupCard,
    NodeCard
  },
  props: {
    isLayer: {
      type: Boolean,
      default: false
    },
    groupData: {
      type: [Array, Object],
      required: true
    },
    closeGroup: {
      type: Function
    }
  },
  data: () => ({
    showDetails: {
      parentNode: false,
      childNodes: []
    },
    nextGroupData: {},
    showNextGroup: false
  }),
  computed: {
    groupTopNodes() {
      return this.isLayer ? this.groupData : this.groupData.nodes;
    },
    editMode() {
      return this.$_userData.isEdit;
    }
  },
  watch: {
    'groupData.id'() {
      this.showDetails.parentNode = true;
      this.showDetails.childNodes = [];
      this.showDetails.childNodes = [...Array(this.groupTopNodes.length)].map(() => false);
    },
    '$_userData.isEdit'(val) {
      if (!val) {
        this.showNextGroup = false;
      }
    }
  },
  mounted() {
    if (this.groupData.id) {
      this.showDetails.parentNode = true;
    }
    this.showDetails.childNodes = [...Array(this.groupTopNodes.length)].map(() => false);
  },
  methods: {
    addLayer() {
      this.showDetails.childNodes.push(false);
      this.groupData.push({
        id: `layer${this.groupData.length + 1}`,
        label: '',
        depth: '',
        fixedDepth: '',
        nodes: []
      });
    },
    addNode(nodes) {
      if (nodes.length) {
        this.showDetails.childNodes.push(false);
      }
      nodes.push({
        id: `node${nodes.length + 1}`,
        label: '',
        parentId: ''
      });
    },
    pushGroup(data) {
      this.nextGroupData = data;
      this.showNextGroup = true;
    },
    async deleteIndex(i) {
      const nodeId = this.groupTopNodes[i].id;
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: `Are you sure you want to delete the "${nodeId}"?`,
        confirmText: 'Delete',
        color: 'error'
      });
      if (!isConfirmed) {
        return;
      }
      if (nodeId === this.nextGroupData.id) {
        this.closeNextGroup();
      }
      this.groupTopNodes.splice(i, 1);
      this.showDetails.childNodes.splice(i, 1);
    },
    closeNextGroup() {
      this.showNextGroup = false;
    }
  }
};
</script>
