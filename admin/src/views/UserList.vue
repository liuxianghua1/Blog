<template>
  <div>
    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column type="index" :index="table_index" width="50" label="序号"> </el-table-column>
      <el-table-column prop="id" label="id"> </el-table-column>
      <el-table-column prop="username" label="用户名"> </el-table-column>
      <el-table-column prop="phone" label="手机号"> </el-table-column>
      <el-table-column prop="createtime" label="创建时间"> </el-table-column>
      <el-table-column prop="lastlogintime" label="最近登录时间"> </el-table-column>
      <el-table-column prop="role" label="权限"> </el-table-column>
      <el-table-column prop="status" label="状态"> </el-table-column>
    </el-table>
    <el-row :span="24">
      <div style="text-align: center; margin-top: 1rem">
        <el-pagination background @current-change="handleCurrentChange" :current-page.sync="paginations.page_index" :layout="paginations.layout" :total="paginations.total"></el-pagination>
      </div>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
      paginations: {
        page_index: 1,
        total: 0,
        page_size: 10,
        layout: 'total, prev, pager, next, jumper'
      }
    }
  },
  methods: {
    table_index(index) {
      return (this.paginations.page_index - 1) * this.paginations.page_size + index + 1
    },
    async fetch(page) {
      const loadingInstance = this.$loading()
      let res
      if (page) {
        res = await this.$http.get(`/api/users/?page=${page}`)
      } else {
        res = await this.$http.get('/api/users/')
      }
      this.paginations.total = res.data.count
      if (res.status === 200) {
        this.tableData = res.data.results
        this.$message({
          message: '用户数据获取成功',
          type: 'success'
        })
        loadingInstance.close()
      }
    },
    handleCurrentChange(page) {
      this.fetch(page)
    }
  },
  created() {
    this.fetch()
  }
}
</script>
<style></style>
