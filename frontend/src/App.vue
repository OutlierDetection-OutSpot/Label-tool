<template>
  <!-- <div id="app">
    <img src="./assets/logo.png">
    <div>
      <p>
        If Element is successfully added to this project, you'll see an
        <code v-text="'<el-button>'"></code>
        below
      </p>
      <el-button>el-button</el-button>
    </div>
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div> -->
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <el-container>
      <el-header class="title"><Title></Title></el-header>
      <el-container>
        <el-aside width=220px class="side-bar">
          <side-bar></side-bar>
        </el-aside>
        <el-main style="padding: 0;">
          <information></information>
          <line-chart></line-chart>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import Title from "./components/Title.vue";
import SideBar from "./components/SideBar.vue";
import Information from './components/Information.vue';
import LineChart from './components/LineChart';

export default {
  name: "app",
  components: {
    Title,
    SideBar,
    Information,
    LineChart,
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  border: black 1px solid;
  box-shadow: 4px 4px 2px #888888;
}
.title {
  background-color: #B3C0D1;
  color: #333;
  text-align: left;
  line-height: 60px;
}
.side-bar {
  height: 520px;
  background-color: #D3DCE6;
  color: #333;
  
}
.information {
  background-color: #E9EEF3;
  color: #333;
  text-align: left;
  line-height: 30px;
}
</style>
