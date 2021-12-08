<template>
  <a-entity :position="`0 ${depth} 0`">
    <a-entity
      v-for="node in notParentNodes"
      :key="node.id"
      :id="`node-${node.id}`"
      :class="{
        'internet-nodes': isInternetNode(node),
        'intranet-nodes': isIntranetNode(node)
      }"
      :position="node.position"
      :look-center="(!group.layoutOptions || group.layoutOptions && group.layoutOptions.shape !== 'square') && (!group.parentId || `parentSelector: #node-${group.parentId}`)"
    >
      <a-entity>
        <a-entity
          :position="getTreeVecter((group.nodeOptions || {}).position)"
          :rotation="getTreeVecter((group.nodeOptions || {}).rotation)"
        >
          <group-entity
            v-if="node.nodes"
            :group="node"
          />
          <node-entity
            v-else
            :node="node"
          />
        </a-entity>
      </a-entity>
    </a-entity>
  </a-entity>
</template>

<script>
import Vue from 'vue';
import GroupEntity from './GroupEntity.vue';
import NodeEntity from './NodeEntity';

export default {
  name: 'GroupEntity',
  components: {
    GroupEntity,
    NodeEntity
  },
  props: {
    group: {
      type: Object
    },
    depth: {
      type: Number,
      default: 0
    },
    parentId: {
      type: String,
      default: ''
    }
  },
  data: () => ({
    notParentNodes: []
  }),
  computed: {
    sphereRadius: () => 0.65
  },
  mounted() {
    this.init();
  },
  methods: {
    async init() {
      if (!this.group.nodes) {
        this.notParentNodes.push(this.group);
        return;
      }
      this.notParentNodes = this.group.nodes.filter(n => !n.parentId);
      const hasParentNodes = this.group.nodes.filter(n => n.parentId);
      this.calcPosition(this.group.layoutOptions?.shape);
      await this.$_sleep(1000);
      hasParentNodes.forEach(node => {
        const parentEl = document.querySelector(`#node-${node.parentId}`);
        const GroupEntityConstructor = Vue.extend(GroupEntity);
        const groupEntityComponent = new GroupEntityConstructor({
          propsData: {
            group: node,
            depth: (this.depth || this.group.fixedDepth) - parentEl.object3D.parent.position.y,
            parentId: node.parentId
          }
        });
        const el = document.createElement('div');
        el.setAttribute('id', `node-${node.id}`);
        parentEl.append(el);
        groupEntityComponent.$mount(`#node-${node.id}`);
      });
    },
    isInternetNode(node) {
      return node.nodeOptions?.type === 'internet';
    },
    isIntranetNode(node) {
      return node.nodeOptions?.type === 'intranet';
    },
    calcPosition(shape = 'circle') {
      const calcFunctions = {
        circle: this.calcCirclePosition,
        square: this.calcSquarePosition,
        sphere: this.calcSpherePosition
      };
      calcFunctions[shape]();
    },
    calcCirclePosition() {
      const nodeCount = this.notParentNodes.length;
      const radius = nodeCount === 1
        ? 1e-100
        : this.group.layoutOptions?.fixedDistance || (nodeCount*(2 - !!this.group.parentId)/5)*(this.group.layoutOptions?.scale || 1);
      this.notParentNodes.forEach((_, i) => {
        const theta = 2*Math.PI*i/nodeCount + Math.PI/2;
        const x = radius*Math.cos(theta);
        const z = radius*Math.sin(theta);
        this.$set(this.notParentNodes[i], 'position', new THREE.Vector3(x, 0, z));
      });
    },
    calcSquarePosition() {
      const nodeCount = this.notParentNodes.length;
      const edgeMaxLength = Math.ceil(Math.sqrt(nodeCount)) - 1;
      const gap = this.group.layoutOptions?.fixedDistance || this.group.layoutOptions?.scale || 1;
      this.notParentNodes.forEach((_, i) => {
        const x = (edgeMaxLength - i%(edgeMaxLength + 1))*gap - edgeMaxLength*gap/2;
        const z = (edgeMaxLength - Math.floor(i/(edgeMaxLength + 1)))*gap - (edgeMaxLength - (nodeCount/(edgeMaxLength + 1) - 1)/2)*gap;
        this.$set(this.notParentNodes[i], 'position', new THREE.Vector3(x, 0, z));
      });
    },
    calcSpherePosition() {
      const nodeCount = this.notParentNodes.length;
      const radius = this.group.layoutOptions?.fixedDistance || this.sphereRadius*(this.group.layoutOptions?.scale || 1);
      this.notParentNodes.forEach((_, i) => {
        const theta = Math.acos(-1 + 2*(i + 1)/(nodeCount + 1)); // 仰角
        const phi = Math.sqrt((nodeCount + 1)*Math.PI)*theta; // 俯角
        const x = radius*Math.sin(theta)*Math.cos(phi);
        const y = radius*Math.sin(theta)*Math.sin(phi);
        const z = radius*Math.cos(theta);
        this.$set(this.notParentNodes[i], 'position', new THREE.Vector3(x, y, z));
      });
    },
    getTreeVecter(vecter) {
      return new THREE.Vector3(vecter?.x, vecter?.y, vecter?.z);
    }
  }
};
</script>
