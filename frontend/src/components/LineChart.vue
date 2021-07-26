<template class="container">
<div id = 'allchart' :style="{width: '100%', height: '78%', float:left}" style="padding-top:20px">
  <div id='timeseletor'>
      select the time gap：
      <el-radio-group v-model="timegap">
        <el-radio :label=360 border size="mini">6h</el-radio>
        <el-radio :label=720 border size="mini">12h</el-radio>
        <el-radio :label=1440 border size="mini">1d</el-radio>
        <el-radio :label=4320 border size="mini">3d</el-radio>
        <el-radio :label=10080 border size="mini">7d</el-radio>
        <el-button size="mini" @click="changezoomer" type="primary">select</el-button>
      </el-radio-group>
  </div>
  <div id="myChart" ref="chart" :style="{width: '100%', height: '100%'} "></div>
  <div id="selectshower"></div>
  <el-button size="mini" @click="clearselect" v-if="this.startpoint != 'None'">重选</el-button>
  
</div>
</template>
<script>
import axios from 'axios';
// 引入基本模板
let echarts = require('echarts/lib/echarts')
import { EventBus } from "../event-bus.js";
// 引入柱状图组件
require('echarts/lib/chart/bar')
// 引入提示框和title组件
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')
require('echarts/lib/component/visualMap')
export default {
  name: 'HelloWorld',
  data() {
    return {
      unmarking:false,
      timegap:144,
      current_file: 'None',
      mingap:5,
      mychart : 'null',
      startpoint: 'None',
      endpoint: 'None',
      selectedSeries:'None',
      currentVmap : [{
            type : 'piecewise',
            show:false,
            seriesIndex:0,
            dimension:0,
            pieces:[
              {min:-1,max:-1}
            ],
            inRange:{
              color:'red'
            },
            outOfRange:{
              color:'blue'
            }
          },
          {
            type: 'piecewise',
            show:false,
            seriesIndex:1,
            dimension:0,
            pieces:[
              {min:-1,max:-1}
            ],
            inRange:{
              color:'red',
            },
            outOfRange:{
              color:'Aquamarine'
            }},
          {
          type: 'piecewise',
          show:false,
          seriesIndex:2,
          dimension:0,
          pieces:[
            {min:-1,max:-1}
          ],
          inRange:{
            color:'red',
          },
          outOfRange:{
            color:'yellow'
          }},
          {
          type: 'piecewise',
          show:false,
          seriesIndex:3,
          dimension:0,
          pieces:[
            {min:-1,max:-1}
          ],
          inRange:{
            color:'red',
          },
          outOfRange:{
            color:'DarkViolet'
          }}]
    }
  },
  mounted() {
    window.onkeydown = this.start_unmark
    // window.onkeyup = this.stop_unmark
    this.drawLine();
    // document.getElementById('allchart').style.display = 'none';
    EventBus.$on('changeRow',msg => {
      document.getElementById('allchart').style.display = '';
      this.getData(msg)
      this.current_file = msg
    })
    EventBus.$on('Export',msg =>{
      console.log('Export:'+msg)
      var resdict = {}
      var top = this.mychart.getOption()
      // s1数组存储的即是多个分块的字典
      resdict['filename'] = msg
      var xAxis = top['xAxis']
      resdict['timestamp'] = xAxis[0]['data']
      for(var _k=0;_k<this.currentVmap.length;_k++){
        var s1 = this.currentVmap[_k].pieces
        console.log(s1)
        resdict[_k+'_'+'data'] = top['series'][_k]['data']
        var markdata = new Array(resdict[_k+'_'+'data'].length).fill(0)
        for(var _i=1;_i<s1.length;_i++){
          if(s1[_i].min == s1[_i].max){
            markdata[s1[_i].min] = 2;
          }
          for(var _j=s1[_i].min;_j<s1[_i].max;_j++){
              markdata[_j] = 1;
          }
      }
        resdict[_k+'_'+'markdata'] = markdata
      }
      console.log(resdict)
      axios.post('http://127.0.0.1:5000/post/export',resdict,
      {headers: {'Content-Type': 'application/json'}})
    })
    EventBus.$on('deleteRow', msg => {
      // this.option.data = []
      // this.option.series = []
      this.mychart.setOption({
        legend:{
            data:[]
          },
          series: [],
          xAxis:{
            type:'time',
            data: [],
          }
      })
    })
  },
  methods: {
    drawLine() {
      let that = this
      // 基于准备好的dom，初始化echarts实例
      let myChart = echarts.init(document.getElementById('myChart'))
      this.mychart = myChart
      // 绘制图表
      myChart.setOption({
        color:['blue','Aquamarine','yellow','DarkViolet'],
        title: {  },
        tooltip: {},
        xAxis: {
          data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
        },
        yAxis: {},
        series: [],
        dataZoom:[
          {
            type:'slider',
            start:10,
            end:20
          },
          {
            type:'inside',
          },
        ],
      });
      myChart.on('click', function(params){
        console.log(params.seriesName);
        console.log(params.dataIndex);
        if(that.unmarking == false)
          return;
          var s = that.currentVmap[params.seriesIndex].pieces
          for(var i = 0;i<s.length;i++){
            if(params.dataIndex>s[i].min && params.dataIndex<s[i].max)
              s.splice(i,1);
          that.currentVmap[params.seriesIndex].pieces = s
          console.log('s:',s)
          that.mychart.setOption({
          visualMap:that.currentVmap
         })
        }

      });
      myChart.on('dblclick', function(params){
        console.log(that.selectedSeries)
        if(that.selectedSeries  == 'None'){
          that.selectedSeries = params.seriesIndex
          that.startpoint = params.dataIndex
          document.getElementById('selectshower').innerHTML = "current KPI：KPI_" + that.selectedSeries 
          + "\nstart point："+that.startpoint + "  " + "end point："+that.endpoint
        }
        else{
          if(params.seriesIndex != that.selectedSeries){
            alert('The KPI curves of the two choices were inconsistent!')
            that.selectedSeries = 'None'
            that.startpoint = 'None'
            that.endpoint = 'None'
            document.getElementById('selectshower').innerHTML = " "
            return
          }
          that.endpoint = params.dataIndex
          if(that.startpoint > that.endpoint){
            var tpoint = that.endpoint
            that.endpoint = that.startpoint
            that.startpoint = tpoint
          }
          that.handlemark(that.selectedSeries,that.startpoint,that.endpoint)
          document.getElementById('selectshower').innerHTML = "current KPI：KPI_" + that.selectedSeries 
          + "\nstart point："+that.startpoint + "  " + "end point："+that.endpoint
          that.selectedSeries = 'None'
          that.startpoint = 'None'
          that.endpoint = 'None'
        }
      });
      document.getElementById('allchart').style.display = 'none';
    },
    start_unmark(event){
      console.log('down')
      if(event.ctrlKey){
        if(this.unmarking == false){
          this.$message({
            message:'cancel the label',
            type:'success'
          })
          this.unmarking = true
        }
        else{
          this.$message({
            message:'stop cancel the label',
            type:'success'
          })
          this.unmarking = false
        }
      }
    },
    stop_unmark(event){
      if(event.ctrlKey){
        this.$message({
          message:'stop cancel the label',
          type:'success'
        })
        this.unmarking = false
      }
    },
    getData(file_name){
      let that = this
      axios.get('http://127.0.0.1:5000/get/'+file_name).then(response => {
        // this.writeObj(response.data[file_name])
        this.mingap = response.data.mingap
        var temp_x_date = [],namelist = [],serieslist =[]
        for(var j = 0;j<response.data['datas'].length;j++){
          var temp_name = 'kpi'+ j
          var temp_dict = {}
          temp_dict['name'] = temp_name
          temp_dict['type'] = 'line'
          var temp_data = []
          for(var i = 0;i<response.data['datas'][j].length;i++){
            temp_data.push(response.data['datas'][j][i]);
          }
          
          temp_dict['data'] = temp_data
          namelist.push(temp_name)
          serieslist.push(temp_dict)
        }
        for(var l=0;l<response.data['timestamp'].length;l++){
          temp_x_date.push(response.data['timestamp'][l])
        }
        this.mychart.setOption({
          legend:{
            data:namelist
          },
          series: serieslist,
          xAxis:{
            data: temp_x_date,
          },
          visualMap : [{
            type : 'piecewise',
            show:false,
            seriesIndex:0,
            dimension:0,
            pieces:[
              {min:-1,max:-1}
            ],
            inRange:{
              color:'red'
            },
            outOfRange:{
              color:'blue'
            }
          },
          {
            type: 'piecewise',
            show:false,
            seriesIndex:1,
            dimension:0,
            pieces:[
              {min:-1,max:-1}
            ],
            inRange:{
              color:'red',
            },
            outOfRange:{
              color:'Aquamarine'
            }},
          {
          type: 'piecewise',
          show:false,
          seriesIndex:2,
          dimension:0,
          pieces:[
            {min:-1,max:-1}
          ],
          inRange:{
            color:'red',
          },
          outOfRange:{
            color:'yellow'
          }},
          {
          type: 'piecewise',
          show:false,
          seriesIndex:3,
          dimension:0,
          pieces:[
            {min:-1,max:-1}
          ],
          inRange:{
            color:'red',
          },
          outOfRange:{
            color:'DarkViolet'
          }}]
        })
      })
    },
    writeObj(obj){ 
      var description = ""; 
      for(var i in obj){ 
      var property=obj[i]; 
      description+=i+" = "+property+"\n"; 
      }
      console.log(description)
    },
    changezoomer(){
      var zoomerlen = parseInt(this.timegap/this.mingap)
      var tempoption = {
        dataZoom:[
          {
            type:'slider',
            startValue:this.mychart.getOption().dataZoom[0].startValue,
            endValue:this.mychart.getOption().dataZoom[0].startValue + zoomerlen
          }
        ]
      }
      this.mychart.setOption(tempoption)
      // this.$refs["echart"].getOp()
    },
    handlemark(seriesIndex, sIndex, eIndex){
      let that = this
      console.log(this.currentVmap[seriesIndex].pieces)
      var s = this.currentVmap[seriesIndex].pieces
      s = this.mergeList(s,{min:sIndex,max:eIndex})
      this.currentVmap[seriesIndex].pieces = s
      this.mychart.setOption({
        visualMap:this.currentVmap
      })
    },
    clearselect(){
      let that = this
      that.selectedSeries = 'None'
      that.startpoint = 'None'
      that.endpoint = 'None'
      document.getElementById('selectshower').innerHTML = ''
    },
    mergeList(tlist,ndict){
      var spoint = -1,epoint = -1,spos = -1,epos = -1,pos = 1;
      for(var i=1;i<tlist.length;i++){
        // 如果不需要合并
        if(ndict.min>tlist[i].max || ndict.max < tlist[i].min){
          if(ndict.min>tlist[i].max)
            pos++
          continue
        }
        else{
          if(ndict.min<tlist[i].max&&spoint == -1){
            spoint = Math.min(tlist[i].min,ndict.min)
            spos = i
            if(ndict.max<tlist[i].max&&epoint == -1){
              epoint = tlist[i].max
              epos = i
              break
            }
            else
              continue
          }
          if(ndict.max>tlist[i].min&&epoint == -1){
            epoint = Math.max(tlist[i].max,ndict.max)
            epos = i
            break
          }
        }
      }
      // 不需要和数组的任意一项合并，直接添加
      if(spoint == -1){
        tlist.splice(pos,0,ndict)
        return tlist
      }
      console.log('points:',spoint,epoint)
      console.log('pos:',spos,epos) 
      for(var j=epos-spos;j>=0;j--){
        tlist.splice(spos,1)
      }
      var tdict = {min:spoint,max:epoint}
      tlist.splice(spos,0,tdict)
      return tlist
    }
  }
}
</script>
