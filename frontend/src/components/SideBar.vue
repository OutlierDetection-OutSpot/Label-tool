<template>
  <div>
    <el-upload
      class="upload-demo"
      ref="upload"
      action="string"
      :limit="10"
      :multiple="false"
      :show-file-list="false"
      :http-request="uploadFile"
      :on-exceed="handleExceed"
    >
      <el-button slot="trigger" type="primary" class="upload"
        ><i class="el-icon-upload el-icon--left"></i>Add Data</el-button
      >
    </el-upload>
    <p>{{ fileName }}</p>
    <el-table
      ref="machineList"
      :data="fileList"
      highlight-current-row
      @current-change="handleCurrentChange"
      style="width: 100%"
    >
      <el-table-column type="index" width="50"> </el-table-column>
      <el-table-column property="name" label="fileList"> </el-table-column>
      <el-table-column label="opration">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleExport(scope.$index, scope.row)" style="width:60px;margin-bottom:5px"
            >Save</el-button>
          <br/>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)" 
          style="width:60px;padding-left:8px"
          >ReMove</el-button>

        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
import axios from "axios";
import { EventBus } from "../event-bus.js";
export default {
  data() {
    return {
      fileName: "KPI data",
      fileList: [],
      currentRow: null,
    };
  },
  methods: {
    // handleExceed(files, fileList) {
    handleExceed() {
      // this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
      this.$message.warning("you can only select 10 files");
    },
    uploadFile(fileObj) {
      // let formData = new FormData();
      let that = this;
      console.log(fileObj.file.name);
      // 把这行放到response200里
      that.fileList.push({ name: fileObj.file.name });
      // formData.set("file", fileObj.file);
      axios
        .post("http://127.0.0.1:5000/upload", fileObj.file.name, {
          headers: {
            "Content-Type": "text/plain",
          },
        })
        .then((response) => {
          if (response.status === 200) {
            // 提交成功将要执行的代码
            console.log('upload success')
            this.$message({
              message:'upload success',
              type:'success'
            })
          }
        })
        .catch(function (error) {
          console.log(error);
          this.$message({
              message:'upload failed',
              type:'error'
          })
        });
    },
    handleCurrentChange(Row) {
      if(Row != null && this.nameinList(Row.name,this.fileList)){
        console.log('handle change')
        let that = this;
        that.currentRow = Row;
        EventBus.$emit('changeRow',that.currentRow.name)
      }
    },
    handleExport(index, row) {
      let that = this;
      console.log(index, row);
      EventBus.$emit('Export',that.currentRow.name)
    },
    handleDelete(index, row) {
      console.log('handle delete')
      axios.post("http://127.0.0.1:5000/del/"+row.name,row.name).then((response)=>{

      })
      let that = this;
      // that.currentRow = null
      this.fileList.splice(index,1);
      EventBus.$emit('deleteRow')
    },
    getData() {
      axios
        .get("/get")
        .then((response) => {
          if (response.code === 200) {
            // 接受成功将要执行的代码
            console.log(response.data);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    nameinList(t_str,t_list){
      for(var i=0;i<t_list.length;i++){
        if(t_str == t_list[i].name)
        return true
      }
      return false
    },
    writeObj(obj){ 
      var description = ""; 
      for(var i in obj){ 
      var property=obj[i]; 
      description+=i+" = "+property+"\n"; 
      alert(description);
      } 
    } 
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.upload {
  margin: 20px;
}
</style>