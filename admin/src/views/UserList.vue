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
    <el-row>
      <div style="text-align: center">
        <el-pagination background @current-change="handleCurrentChange" :current-page.sync="paginations.page_index" :page-sizes="[10, 20, 30, 40, 50]" @size-change="handleSizeChange" :page-size="paginations.page_size" :layout="paginations.layout" :total="paginations.total"></el-pagination>
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
        page_index: 1, // 序号
        total: 0,
        page_size: 10, // 一页显示几条
        page_num: 1, // 页码
        layout: 'total, prev, sizes, pager, next, jumper'
      }
    }
  },
  methods: {
    table_index(index) {
      // 分页自增
      return (this.paginations.page_index - 1) * this.paginations.page_size + index + 1
    },
    async fetch() {
      // 全屏loading开启
      const loadingInstance = this.$loading()
      const res = await this.$http.get(`/api/users/?page=${this.paginations.page_num}&size=${this.paginations.page_size}`)

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
    async handleCurrentChange(page) {
      // 页码变化触发操作
      const res = await this.$http.get(`/api/users/?page=${page}&size=${this.paginations.page_size}`)
      this.paginations.total = res.data.count
      this.tableData = res.data.results
    },
    async handleSizeChange(val) {
      // 每页x条变化触发操作
      this.paginations.page_size = val
      const res = await this.$http.get(`/api/users/?page=${this.paginations.page_num}&size=${this.paginations.page_size}`)
      this.paginations.total = res.data.count
      this.tableData = res.data.results
    }
  },
  created() {
    this.fetch()
  }
}
</script>
<style></style>
