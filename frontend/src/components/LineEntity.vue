<template>
  <a-entity id="line-group" position="0 0 0" />
</template>

<script>
export default {
  name: 'LineEntity',
  data: () => ({
    animationFunctions: {},
    lineGroup: null,
    frame: 0
  }),
  computed: {
    lineLength: () => 3
  },
  async mounted() {
    this.lineGroup = document.querySelector('#line-group').object3D;
    setInterval(() => {
      this.animationRender();
    }, 20);
  },
  methods: {
    animationRender() {
      for (const func of Object.values(this.animationFunctions)) {
        func();
      }
    },
    emit1(source, target, color = '#fff', endFunc = () => {}, isAnswer = false) {
      if (Object.keys(this.animationFunctions).length > 100) {
        return;
      }
      const sourceEl = document.querySelector(source);
      const targetEl = document.querySelector(target);
      if (!(sourceEl && targetEl)) {
        return;
      }
      const sourceP = sourceEl.object3D.getWorldPosition(new THREE.Vector3());
      const targetP = targetEl.object3D.getWorldPosition(new THREE.Vector3());
      const diffP = {
        x: targetP.x - sourceP.x,
        y: targetP.y - sourceP.y,
        z: targetP.z - sourceP.z
      };
      const points = [];
      const length = Math.sqrt((-diffP.x)**2 + (-diffP.y)**2 + (-diffP.z)**2);
      const curveTopHeight = length/5;
      const curveBottomHeight = length/8;
      const sign = targetP.y - sourceP.y < -curveTopHeight ? -1 : 1;
      points.push(sourceP);
      points.push(new THREE.Vector3(
        sourceP.x + diffP.x/5,
        sourceP.y + diffP.y/5 + curveBottomHeight*sign,
        sourceP.z + diffP.z/5
      ));
      points.push(new THREE.Vector3(
        sourceP.x + diffP.x/2,
        sourceP.y + diffP.y/2 + curveTopHeight*sign,
        sourceP.z + diffP.z/2
      ));
      points.push(new THREE.Vector3(
        sourceP.x + diffP.x*4/5,
        sourceP.y + diffP.y*4/5 + curveBottomHeight*sign,
        sourceP.z + diffP.z*4/5
      ));
      points.push(targetP);
      const linePoints = new THREE.CatmullRomCurve3(points).getPoints(isAnswer ? 40 : 15);
      const path = new THREE.CatmullRomCurve3(linePoints.slice(0, this.lineLength));
      const geometry = new THREE.TubeBufferGeometry(path, isAnswer ? 5 : 20, isAnswer ? 0.03 : 0.01);
      const material = new THREE.MeshBasicMaterial({ color });
      const lineMesh = new THREE.Mesh(geometry, material);
      this.lineGroup.add(lineMesh);
      const lineId = source + target + Date.now();
      let index = 0;
      this.animationFunctions[lineId] = () => {
        if (index >= linePoints.length - 2) {
          delete this.animationFunctions[lineId];
          this.lineGroup.remove(lineMesh);
          geometry.dispose();
          material.dispose();
          endFunc();
          return;
        };
        index++;
        const nextPath = new THREE.CatmullRomCurve3(linePoints.slice(index, index + this.lineLength));
        const nextGeometry = new THREE.TubeBufferGeometry(nextPath, isAnswer ? 5 : 20, isAnswer ? 0.03 : 0.01);
        const nowP = geometry.attributes.position;
        nowP.array = nextGeometry.attributes.position.array;
        nowP.needsUpdate = true;
        nextGeometry.dispose();
      };
    },
    emit2(source, target, color = '#fff', endFunc = () => {}) {
      if (Object.keys(this.animationFunctions).length > 100) {
        return;
      }
      const sourceEl = document.querySelector(source);
      const targetEl = document.querySelector(target);
      if (!(sourceEl && targetEl)) {
        return;
      }
      const sourceP = sourceEl.object3D.getWorldPosition(new THREE.Vector3());
      const linePoints = [];
      [...Array(5)].forEach(() => {
        linePoints.push(sourceP);
      });
      const path = new THREE.CatmullRomCurve3(linePoints);
      const geometry = new THREE.TubeBufferGeometry(path, 20, 0.01);
      const material = new THREE.MeshBasicMaterial({ color });
      const lineMesh = new THREE.Mesh(geometry, material);
      this.lineGroup.add(lineMesh);
      const lineId = source + target + Date.now();
      this.animationFunctions[lineId] = () => {
        const lineP = [linePoints.slice(-1)[0], linePoints[0]];
        const targetP = targetEl.object3D.getWorldPosition(new THREE.Vector3());
        const diffP = [
          {
            x: Math.abs(targetP.x - lineP[0].x),
            y: Math.abs(targetP.y - lineP[0].y),
            z: Math.abs(targetP.z - lineP[0].z)
          },
          {
            x: Math.abs(targetP.x - lineP[1].x),
            y: Math.abs(targetP.y - lineP[1].y),
            z: Math.abs(targetP.z - lineP[1].z)
          }
        ];
        const sumDiffP = diffP[1].x + diffP[1].y + diffP[1].z;
        const moveP = 0.3;
        if (sumDiffP < moveP*2) {
          delete this.animationFunctions[lineId];
          this.lineGroup.remove(lineMesh);
          geometry.dispose();
          material.dispose();
          endFunc();
          return;
        }
        const sign = {
          x: lineP[0].x < targetP.x ? 1 : -1,
          y: lineP[0].y < targetP.y ? 1 : -1,
          z: lineP[0].z < targetP.z ? 1 : -1
        };
        const nextP = {
          x: lineP[0].x + (diffP[0].x >= moveP)*sign.x*moveP,
          y: lineP[0].y + (diffP[0].y >= moveP)*sign.y*moveP,
          z: lineP[0].z + (diffP[0].z >= moveP)*sign.z*moveP
        };
        linePoints.shift();
        linePoints.push(new THREE.Vector3(nextP.x, nextP.y, nextP.z));
        const nextPath = new THREE.CatmullRomCurve3(linePoints);
        const nextGeometry = new THREE.TubeBufferGeometry(nextPath, 20, 0.01);
        const nowP = geometry.attributes.position;
        nowP.array = nextGeometry.attributes.position.array;
        nowP.needsUpdate = true;
        nextGeometry.dispose();
      };
    },
    emitAnswer(uid, qid, isCorrect, endFunc = () => {}) {
      const user = this.$_visualizeData.exercise.users.find(u => u.id === uid);
      this.emit1(`#node-${user.nodeId}`, `#question__${qid}`, isCorrect ? '#00ff00' : '#ff0000', endFunc, true);
    },
    emit3(source, target, color = '#fff', endFunc = () => {}, isAnswer = false) {
      if (Object.keys(this.animationFunctions).length > 100) {
        return;
      }
      const sourceEl = document.querySelector(source);
      const targetEl = document.querySelector(target);
      if (!(sourceEl && targetEl)) {
        return;
      }
      const sourceP = sourceEl.object3D.getWorldPosition(new THREE.Vector3());
      const targetP = targetEl.object3D.getWorldPosition(new THREE.Vector3());
      const diffP = {
        x: targetP.x - sourceP.x,
        y: targetP.y - sourceP.y,
        z: targetP.z - sourceP.z
      };
      const length = Math.sqrt((-diffP.x)**2 + (-diffP.y)**2 + (-diffP.z)**2);
      const curveTopHeight = length/5;
      const curveBottomHeight = length/8;
      const sign = targetP.y - sourceP.y < -curveTopHeight ? -1 : 1;
      const points = [
        sourceP,
        new THREE.Vector3(
          sourceP.x + diffP.x/5,
          sourceP.y + diffP.y/5 + curveBottomHeight*sign,
          sourceP.z + diffP.z/5
        ),
        new THREE.Vector3(
          sourceP.x + diffP.x/2,
          sourceP.y + diffP.y/2 + curveTopHeight*sign,
          sourceP.z + diffP.z/2
        ),
        new THREE.Vector3(
          sourceP.x + diffP.x*4/5,
          sourceP.y + diffP.y*4/5 + curveBottomHeight*sign,
          sourceP.z + diffP.z*4/5
        ),
        targetP
      ];

      const linePoints = new THREE.CatmullRomCurve3(points).getPoints(isAnswer ? 80 : 30);
      const coneGeometry = new THREE.CylinderGeometry(0, 0.05, 0.2, 4);
      const coneMaterial = new THREE.MeshBasicMaterial({ color });
      const coneMesh = new THREE.Mesh(coneGeometry, coneMaterial);
      const coneWrapperMesh = new THREE.Mesh();
      coneWrapperMesh.add(coneMesh);
      this.lineGroup.add(coneWrapperMesh);
      coneMesh.rotation.x = Math.PI/2;
      coneWrapperMesh.position = sourceP;
      coneWrapperMesh.lookAt(linePoints[1]);

      let lineId = `${source}->${target}__${Date.now() + Math.random()}`;
      while (this.animationFunctions[lineId]) {
        lineId += Math.random();
      }
      let index = 0;
      this.animationFunctions[lineId] = () => {
        if (index >= linePoints.length - 2) {
          delete this.animationFunctions[lineId];
          this.lineGroup.remove(coneMesh);
          this.lineGroup.remove(coneWrapperMesh);
          coneGeometry.dispose();
          coneMaterial.dispose();
          endFunc();
          return;
        };
        index++;
        coneWrapperMesh.position = linePoints[index];
        coneWrapperMesh.lookAt(linePoints[index + 1]);
      };
    }
  }
};
</script>
