<template>
  <a-tetrahedron
    v-if="node.nodeOptions.facesNumber === 4"
    :radius="polyhedronSize*node.nodeOptions.size*1.5"
    :color="node.nodeOptions.nodeColor"
  >
    <a-text
      v-for="(label, i) in labels"
      :key="i"
      :value="label.value"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`${label.position.x} ${label.position.y} ${label.position.z}`"
      :wrap-count="50/node.nodeOptions.fontSize"
    />
  </a-tetrahedron>
  <a-octahedron
    v-else-if="node.nodeOptions.facesNumber === 8"
    :radius="polyhedronSize*node.nodeOptions.size"
    :color="node.nodeOptions.nodeColor"
  >
    <a-text
      v-for="(label, i) in labels"
      :key="i"
      :value="label.value"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`${label.position.x} ${label.position.y} ${label.position.z}`"
      :wrap-count="50/node.nodeOptions.fontSize"
    />
  </a-octahedron>
  <a-dodecahedron
    v-else-if="node.nodeOptions.facesNumber === 12"
    :radius="polyhedronSize*node.nodeOptions.size"
    :color="node.nodeOptions.nodeColor"
  >
    <a-text
      v-for="(label, i) in labels"
      :key="i"
      :value="label.value"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`${label.position.x} ${label.position.y} ${label.position.z}`"
      :wrap-count="50/node.nodeOptions.fontSize"
    />
  </a-dodecahedron>
  <a-icosahedron
    v-else-if="node.nodeOptions.facesNumber === 20"
    :radius="polyhedronSize*node.nodeOptions.size"
    :color="node.nodeOptions.nodeColor"
  >
    <a-text
      v-for="(label, i) in labels"
      :key="i"
      :value="label.value"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`${label.position.x} ${label.position.y} ${label.position.z}`"
      :wrap-count="50/node.nodeOptions.fontSize"
    />
  </a-icosahedron>
  <a-box
    v-else
    :width="polyhedronSize*node.nodeOptions.size*1.5"
    :height="polyhedronSize*node.nodeOptions.size*1.5"
    :depth="polyhedronSize*node.nodeOptions.size*1.5"
    :color="node.nodeOptions.nodeColor"
  >
    <a-text
      v-for="(label, i) in labels"
      :key="i"
      :value="label.value"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`${label.position.x} ${label.position.y} ${label.position.z}`"
      :wrap-count="50/node.nodeOptions.fontSize"
    />
  </a-box>
</template>

<script>
export default {
  name: 'PolyhedronEntity',
  props: {
    node: {
      type: Object,
      required: true
    },
    detailsLabel: {
      type: [String, Number],
      required: false
    },
    score: {
      type: Number,
      required: false
    }
  },
  computed: {
    polyhedronSize: () => 0.2,
    labels() {
      const labelOptions = [
        {
          place: 'top',
          position: {
            x: 0,
            y: this.polyhedronSize*this.node.nodeOptions.size + this.polyhedronSize,
            z: 0
          }
        },
        {
          place: 'center',
          position: {
            x: 0,
            y: 0.01,
            z: this.polyhedronSize*this.node.nodeOptions.size*1.3
          }
        },
        {
          place: 'bottom',
          position: {
            x: 0,
            y: -this.polyhedronSize*this.node.nodeOptions.size - this.polyhedronSize,
            z: 0
          }
        }
      ];
      const labels = [];
      labelOptions.forEach(option => {
        const labelType = this.node.nodeOptions[`${option.place}Label`] || (option.place === 'bottom' ? 'node_label' : '(none)');
        if (labelType !== '(none)') {
          labels.push({
            value: this.selectLabel(labelType),
            position: option.position
          });
        }
      });
      return labels;
    }
  },
  methods: {
    selectLabel(labelType) {
      switch (labelType) {
        case 'node_label':
          return this.node.label;
        case 'details_label':
          return this.detailsLabel;
        case 'score':
          return this.score;
      }
    }
  }
};
</script>
