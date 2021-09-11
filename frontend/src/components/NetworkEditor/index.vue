<template>
  <div>
    <v-row>
      <v-col>
        <v-btn
          depressed
          color="primary"
          @click="downloadNetwork"
        >
          <span>JSONダウンロード</span>
        </v-btn>
      </v-col>
    </v-row>
    <draggable
      :list="networkData"
      v-bind="dragOptions"
      handle=".network-editor__layer__reorder"
      class="network-editor__draggable"
    >
      <div
        v-for="layer, i in networkData"
        :key="`layer__${layer.id}_${i}`"
        class="network-editor__layer d-flex my-3"
        @contextmenu.stop="showObjectMenu($event, networkData, i)"
      >
        <div class="network-editor__layer__reorder d-flex align-center">
          <v-icon class="my-auto mx-2">mdi-reorder-horizontal</v-icon>
        </div>
        <div class="network-editor__layer__contents pl-3 pb-3">
          <div class="network-editor__layer__header d-flex mt-4 ml-3">
            <span>{{ layer.id }}</span>
          </div>
          <draggable
            v-bind="dragOptions"
            :list="layer.nodes"
            :group="{ name: 'network' }"
            handle=".node-block__reorder"
            class="network-editor__layer__draggable d-flex py-3"
          >
            <div
              v-for="node, j in layer.nodes"
              :key="`layer__${node.id}_${j}`"
              class="d-flex"
              @contextmenu.stop="showObjectMenu($event, layer.nodes, j)"
            >
              <node-block
                :nodeData="node"
                :showObjectMenu="showObjectMenu"
              />
            </div>
            <div
              slot="footer"
              class="network-editor__layer__footer d-flex pr-3"
            >
              <div class="my-auto">
                <v-btn
                  icon
                  class="d-flex"
                  @click="addNode(layer.nodes)"
                >
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
                <v-btn
                  icon
                  class="d-flex"
                  @click="addGroup(layer.nodes)"
                >
                  <v-icon>mdi-shape-square-plus</v-icon>
                </v-btn>
              </div>
            </div>
          </draggable>
        </div>
      </div>
      <div
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

    <v-menu
      v-model="objectMenu.show"
      :position-x="objectMenu.x"
      :position-y="objectMenu.y"
      absolute
      offset-y
    >
      <v-list class="py-0">
        <v-list-item>
          <v-list-item-title>{{ selectedObject.id }}</v-list-item-title>
        </v-list-item>
        <v-divider />
        <v-list-item @click="editObject">
          <v-list-item-title>編集</v-list-item-title>
        </v-list-item>
        <v-list-item @click="deleteObject">
          <v-list-item-title class="error--text">削除</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-dialog
      v-model="editDialog"
      :persistent="objectMenu.isChanged"
      width="500"
    >
      <v-card>
        <v-card-title>
          <span>詳細</span>
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="objectMenu.editObject.id"
            label="ID"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            depressed
            @click="editDialog = false"
          >
            <span>キャンセル</span>
          </v-btn>
          <v-btn
            depressed
            color="primary"
            @click="saveObject"
          >
            <span>保存</span>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.network-editor__layer {
  outline: 2px solid #000;
}
.network-editor__layer__reorder {
  outline: 2px solid #000;
  cursor: move;
  z-index: 100;
}
.network-editor__layer__draggable {
  min-width: 100%;
  min-height: calc(100px + 3rem);
  margin-top: 48px;
}
.network-editor__layer__contents {
  min-width: calc(100% - 42px);
  overflow-x: scroll;
}
.network-editor__layer__header {
  position: absolute;
  min-width: 300px;
}
.network-editor__layer__footer {
  margin-bottom: 30px;
}
</style>

<script>
import draggable from 'vuedraggable';
import NodeBlock from './NodeBlock.vue';

export default {
  name: 'NetworkEditor',
  components: {
    draggable,
    NodeBlock
  },
  props: {
    networkData: {
      type: Array,
      required: true
    }
  },
  data: () => ({
    objectMenu: {
      show: false,
      x: 0,
      y: 0,
      groupArray: [],
      index: 0,
      editObject: {},
      isChanged: false
    },
    editDialog: false
  }),
  computed: {
    dragOptions() {
      return {
        animation: 200,
        disabled: false,
        ghostClass: 'ghost'
      };
    },
    selectedObject() {
      return this.objectMenu.groupArray[this.objectMenu.index] || {};
    }
  },
  watch: {
    'objectMenu.show'(val) {
      if (!val) {
        this.objectMenu.isChanged = false;
        return;
      }
      this.objectMenu.editObject = {};
      for (const key in this.selectedObject) {
        if (typeof this.selectedObject[key] === 'object') {
          return;
        }
        this.$set(this.objectMenu.editObject, key, this.selectedObject[key]);
      }
    },
    'objectMenu.editObject': {
      handler() {
        this.objectMenu.isChanged = true;
      },
      deep: true
    }
  },
  methods: {
    addLayer() {
      this.networkData.push({
        id: `layer${this.networkData.length + 1}`,
        nodes: []
      });
    },
    addGroup(nodes) {
      nodes.push({
        id: `group${nodes.length + 1}`,
        nodes: []
      });
    },
    addNode(nodes) {
      nodes.push({
        id: `node${nodes.length + 1}`
      });
    },
    showObjectMenu(e, array, index) {
      e.preventDefault();
      this.objectMenu.show = false;
      this.objectMenu.x = e.clientX;
      this.objectMenu.y = e.clientY;
      this.objectMenu.groupArray = array;
      this.objectMenu.index = index;
      this.$nextTick(() => {
        this.objectMenu.show = true;
      });
    },
    editObject() {
      this.editDialog = true;
    },
    async deleteObject() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: `"${this.selectedObject.id}"を削除しますか?`,
        confirmText: '削除',
        color: 'error'
      });
      if (!isConfirmed) {
        return;
      }
      this.objectMenu.groupArray.splice(this.objectMenu.index, 1);
    },
    async saveObject() {
      const isConfirmed = await this.$_appRefs.confirmDialog.open({
        message: '変更を保存しますか?',
        confirmText: '保存'
      });
      if (!isConfirmed) {
        return;
      }
      for (const key in this.objectMenu.editObject) {
        this.$set(this.selectedObject, key, this.objectMenu.editObject[key]);
      }
      this.editDialog = false;
    },
    downloadNetwork() {
      const data = JSON.stringify(this.networkData, null, '  ');
      const link = document.createElement('a');
      link.href = `data:text/plain,${encodeURIComponent(data)}`;
      link.download = 'network.json';
      link.click();
    }
  }
};
</script>
