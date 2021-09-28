<template>
  <div class="network-editor d-flex flex-column">
    <context-menu
      ref="contextMenu"
      :routingTable="routingTable"
      :editMode="editMode"
    />

    <draggable
      v-if="selectedLayerIndex === null"
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
    <template v-else>
      <layer-block
        :layer="network[selectedLayerIndex]"
        :openContextMenu="openContextMenu"
        :editMode="editMode"
        class="mt-auto"
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
            @click="selectLayer"
          >
            <v-icon>mdi-crosshairs</v-icon>
          </v-btn>
        </template>
      </layer-block>
    </template>
  </div>
</template>

<style lang="scss" scoped>
.network-editor {
}
</style>

<script>
import draggable from 'vuedraggable';
import LayerBlock from './LayerBlock.vue';
import ContextMenu from './ContextMenu.vue';

export default {
  name: 'NetworkEditor',
  components: {
    draggable,
    LayerBlock,
    ContextMenu
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
    selectLayer(i) {
      if (this.selectedLayerIndex !== null) {
        this.selectedLayerIndex = null;
        return;
      }
      this.selectedLayerIndex = i;
    }
  }
};
</script>
