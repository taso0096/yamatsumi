<template>
  <div class="network-editor d-flex flex-column">
    <context-menu
      ref="contextMenu"
      :openDetails="selectedLayerIndex === null ? openDetailsDialog : openDetailsCard"
      :routingTable="routingTable"
      :editMode="editMode"
    />

    <template v-if="selectedLayerIndex === null">
      <details-dialog
        ref="detailsDialog"
        :routingTable="routingTable"
        :editMode="editMode"
      />
      <draggable
        :list="network"
        v-bind="dragOptions"
        handle=".layer-block__reorder"
        class="network-editor__draggable"
      >
        <div
          v-for="(layer, i) in network"
          :key="`layer__${layer.id}_${i}`"
          class="mb-3"
          @contextmenu.stop="openContextMenu($event, network, i, true)"
        >
          <layer-block
            :layer="layer"
            :openContextMenu="openContextMenu"
            :editMode="editMode"
          >
            <template #header>
              <v-badge
                :content="i + 1"
                overlap
                bottom
                color="secondary"
                class="mr-5"
              >
                <v-icon>mdi-layers</v-icon>
              </v-badge>
              <span>{{ layer.id }}</span>
              <v-spacer />
              <v-btn
                icon
                @click="selectLayer(i)"
              >
                <v-icon>mdi-crosshairs</v-icon>
              </v-btn>
            </template>
          </layer-block>
        </div>
        <div
          v-if="editMode"
          slot="footer"
          class="d-flex justify-center"
        >
          <v-btn
            depressed
            color="secondary"
            class="ma-3"
            @click="addLayer"
          >
            <span>Add Layer</span>
          </v-btn>
        </div>
      </draggable>
    </template>

    <template v-else-if="selectedLayer">
      <select-mode-details-card
        ref="selectModeDetailsCard"
        :routingTable="routingTable"
        :editMode="editMode"
      />
      <div
        class="mt-auto"
        @contextmenu.stop="openContextMenu($event, network, selectedLayerIndex, true)"
      >
        <layer-block
          :layer="network[selectedLayerIndex]"
          :openContextMenu="openContextMenu"
          :editMode="editMode"
          :selectMode="true"
        >
          <template #header>
            <v-badge
              :content="selectedLayerIndex + 1"
              overlap
              bottom
              color="secondary"
              class="mr-5"
            >
              <v-icon>mdi-layers</v-icon>
            </v-badge>
            <span>{{ network[selectedLayerIndex].id }}</span>
            <v-spacer />
            <v-btn
              icon
              @click="deselectLayer"
            >
              <v-icon>mdi-crosshairs-gps</v-icon>
            </v-btn>
          </template>
        </layer-block>
      </div>
    </template>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import LayerBlock from './LayerBlock.vue';
import ContextMenu from './ContextMenu.vue';
import DetailsDialog from './DetailsDialog.vue';
import SelectModeDetailsCard from './SelectModeDetailsCard.vue';

export default {
  name: 'NetworkEditor',
  components: {
    draggable,
    LayerBlock,
    ContextMenu,
    DetailsDialog,
    SelectModeDetailsCard
  },
  props: {
    network: {
      type: Array,
      required: true
    },
    routingTable: {
      type: Object,
      required: true
    },
    editMode: {
      type: Boolean,
      required: true
    }
  },
  data: () => ({
    selectedLayerIndex: null
  }),
  computed: {
    dragOptions() {
      return {
        animation: 200,
        disabled: !this.editMode,
        ghostClass: 'ghost'
      };
    },
    selectedLayer() {
      return this.network[this.selectedLayerIndex];
    }
  },
  watch: {
    editMode() {
      if (this.selectedLayer) {
        this.openDetailsCard(this.network, this.selectedLayerIndex, true);
      }
    },
    selectedLayer(layer, beforeLayer) {
      if (beforeLayer?.id && layer?.id !== beforeLayer?.id) {
        this.deselectLayer();
      }
    }
  },
  methods: {
    addLayer() {
      this.network.push({
        id: `layer${this.network.length + 1}`,
        nodes: []
      });
    },
    openContextMenu(e, array, index, isLayer = false) {
      this.$refs.contextMenu.open(e, array, index, isLayer);
    },
    openDetailsDialog(array, index, isLayer = false) {
      this.$refs.detailsDialog.open(array, index, isLayer);
    },
    openDetailsCard(array, index, isLayer = false) {
      this.$refs.selectModeDetailsCard.open(array, index, isLayer);
    },
    selectLayer(i) {
      this.selectedLayerIndex = i;
      this.$nextTick(() => {
        this.openDetailsCard(this.network, i, true);
      });
    },
    deselectLayer() {
      this.selectedLayerIndex = null;
    }
  }
};
</script>
