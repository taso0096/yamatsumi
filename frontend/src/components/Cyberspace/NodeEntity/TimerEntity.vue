<template>
  <node-shape-entity
    :node="node"
    :detailsLabel="remainingTime"
  />
</template>

<script>
import NodeShapeEntity from './NodeShapeEntity';

export default {
  name: 'TimerEntity',
  components: {
    NodeShapeEntity
  },
  props: {
    node: {
      type: Object
    },
    startTime: {
      type: Number,
      required: true
    },
    endTime: {
      type: Number,
      required: true
    }
  },
  data: () => ({
    timerId: null,
    remainingTime: ''
  }),
  mounted() {
    if (!(this.startTime || this.endTime)) {
      this.remainingTime = 'ERROR';
      return;
    }
    this.timerId = setInterval(() => this.count(), 1000);
  },
  methods: {
    count() {
      const diffTime = this.endTime - Date.now();
      if (diffTime <= 0) {
        this.remainingTime = '00:00:00';
        clearInterval(this.timerId);
        return;
      }
      const rTime = {
        hour: ('0' + Math.floor(diffTime/(60*60*1000))).slice(-2),
        min: ('0' + Math.floor(diffTime/(60*1000)%60)).slice(-2),
        sec: ('0' + Math.floor(diffTime/1000%60)).slice(-2)
      };
      this.remainingTime = `${rTime.hour}:${rTime.min}:${rTime.sec}`;
    }
  }
};
</script>
