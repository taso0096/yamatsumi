<template>
  <a-circle
    :color="node.nodeOptions.nodeColor"
    side="double"
    :radius="circleRadius*node.nodeOptions.size"
  >
    <a-ring
      :color="node.nodeOptions.nodeColor"
      side="double"
      :radius-inner="circleRadius*node.nodeOptions.size*1.025"
      :radius-outer="circleRadius*node.nodeOptions.size*1.05"
    />
    <a-ring
      :color="node.nodeOptions.nodeColor"
      side="double"
      :radius-inner="circleRadius*node.nodeOptions.size*1.075"
      :radius-outer="circleRadius*node.nodeOptions.size*1.175"
    />
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
  </a-circle>
</template>

<script>
export default {
  name: 'CircleEntity',
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
    circleRadius: () => 0.2,
    labels() {
      const labelOptions = [
        {
          place: 'top',
          position: {
            x: 0,
            y: this.circleRadius*this.node.nodeOptions.size + this.circleRadius,
            z: 0
          }
        },
        {
          place: 'center',
          position: {
            x: 0,
            y: 0.01,
            z: 0.005
          }
        },
        {
          place: 'bottom',
          position: {
            x: 0,
            y: -this.circleRadius*this.node.nodeOptions.size - this.circleRadius,
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
