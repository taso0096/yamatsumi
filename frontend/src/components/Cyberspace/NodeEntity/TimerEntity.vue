<template>
  <a-entity>
    <node-shape-entity
      :node="node"
      :detailsLabel="remainingTime"
    />
    <a-text
      :value="`${formatedTime(startTime)} --> ${formatedTime(endTime)}`"
      align="center"
      :color="node.nodeOptions.labelColor"
      side="double"
      :position="`0 ${-node.nodeOptions.fontSize*3/25} 0`"
      :wrap-count="50/node.nodeOptions.fontSize*3"
    />
  </a-entity>
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
      this.remainingTime = this.formatedRemaminingTime(diffTime);
    },
    formatedRemaminingTime(time) {
      const rTime = {
        hour: ('0' + Math.floor(time/(60*60*1000))).slice(-2),
        min: ('0' + Math.floor(time/(60*1000)%60)).slice(-2),
        sec: ('0' + Math.floor(time/1000%60)).slice(-2)
      };
      return `${rTime.hour}:${rTime.min}:${rTime.sec}`;
    },
    formatedTime(time) {
      const date = new Date(time);
      const rTime = {
        hour: ('0' + date.getHours()).slice(-2),
        min: ('0' + date.getMinutes()).slice(-2),
        sec: ('0' + date.getSeconds()).slice(-2)
      };
      return `${rTime.hour}:${rTime.min}:${rTime.sec}`;
    }
  }
};
</script>
