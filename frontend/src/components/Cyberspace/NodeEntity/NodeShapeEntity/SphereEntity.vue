<template>
  <a-sphere
    :radius="sphereRadius*node.nodeOptions.size"
    :color="node.nodeOptions.nodeColor"
    :wireframe="node.nodeOptions.wireframe"
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
  </a-sphere>
</template>

<script>
export default {
  name: 'SphereEntity',
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
    sphereRadius: () => 0.2,
    labels() {
      const labelOptions = [
        {
          place: 'top',
          position: {
            x: 0,
            y: this.sphereRadius*this.node.nodeOptions.size + this.sphereRadius,
            z: 0
          }
        },
        {
          place: 'center',
          position: {
            x: 0,
            y: 0.01,
            z: this.sphereRadius*this.node.nodeOptions.size*1.3
          }
        },
        {
          place: 'bottom',
          position: {
            x: 0,
            y: -this.sphereRadius*this.node.nodeOptions.size - this.sphereRadius,
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
