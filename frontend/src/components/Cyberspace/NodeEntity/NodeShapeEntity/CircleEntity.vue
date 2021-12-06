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
      :position="`0 ${label.positionY} 0`"
      wrap-count="50"
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
          positionY: this.circleRadius*this.node.nodeOptions.size + this.circleRadius
        },
        {
          place: 'center',
          positionY: 0.01
        },
        {
          place: 'bottom',
          positionY: -this.circleRadius*this.node.nodeOptions.size - this.circleRadius
        }
      ];
      const labels = [];
      labelOptions.forEach(option => {
        const labelType = this.node.nodeOptions[`${option.place}Label`] || (option.place === 'bottom' ? 'node_label' : '(none)');
        if (labelType !== '(none)') {
          labels.push({
            value: this.selectLabel(labelType),
            positionY: option.positionY
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
