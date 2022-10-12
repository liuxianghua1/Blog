<template>
  <div>
    <el-table border :default-sort="{ prop: 'createtime', prop: 'lastlogintime' }" :data="tableData" stripe style="width: 100%">
      <el-table-column type="index" :index="table_index" width="50" label="序号"> </el-table-column>
      <el-table-column prop="id" label="id"> </el-table-column>
      <el-table-column prop="username" label="用户名">
        <template slot-scope="scope">
          <div slot="reference" class="name-wrapper">
            <el-tag size="medium">{{ scope.row.username }}</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="phone" label="手机号"> </el-table-column>
      <el-table-column sortable prop="createtime" label="创建时间">
        <template slot-scope="scope">
          <i class="el-icon-time"></i>
          <span style="margin-left: 10px">{{ scope.row.createtime }}</span>
        </template>
      </el-table-column>
      <el-table-column sortable prop="lastlogintime" label="最后登录时间">
        <template slot-scope="scope">
          {{ scope.row.lastlogintime ? scope.row.lastlogintime : '还没登陆过' }}
        </template>
      </el-table-column>
      <el-table-column
        prop="role"
        label="权限"
        :filters="[
          { text: '管理员', value: 0 },
          { text: '超级管理员', value: 1 }
        ]"
        :filter-method="filterRole"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag :type="scope.row.role === 1 ? 'primary' : 'success'">{{ scope.row.role === 1 ? '超级管理员' : '管理员' }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="status" label="状态">
        <template slot-scope="scope">
          <!-- <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">{{ scope.row.status === 1 ? '激活' : '禁用' }}</el-tag> -->
          <el-switch :value="scope.row.status === 1 ? true : false" active-color="#13ce66" inactive-color="#ff4949" active-text="激活" inactive-text="禁用" @change="statusChange(scope.row.id, scope.row.status)"> </el-switch>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="medium" type="primary" round @click="$router.push(`/home/user_updata/${scope.row.id}`)">编辑</el-button>
          <el-button size="medium" type="danger" round @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-row>
      <div style="text-align: center; margin-top: 10px">
        <el-pagination background @current-change="handleCurrentChange" :current-page.sync="paginations.page_index" :page-sizes="[10, 20, 30, 40, 50]" @size-change="handleSizeChange" :page-size="paginations.page_size" :layout="paginations.layout" :total="paginations.total"></el-pagination>
      </div>
    </el-row>
  </div>
</template>

<script>
// 每页最后一条数据删除时会报错、当分页超出数据库拥有最大条数时会报错
export default {
  data() {
    return {
      tableData: [],
      value2: true,
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
    // 状态更改方法 这个id是从scope.row.id中传过来的
    statusChange(id, status) {
      this.$http.put(`/api/users/${id}/updateuser/`, { status: status === 1 ? 0 : 1 }).then(() => {
        this.fetch(this.paginations.page_num, this.paginations.page_size)
      })
    },
    filterRole(value, row) {
      // 权限筛选功能
      return row.role === value
    },
    handleDelete(row) {
      // 删除方法
      this.$confirm(`此操作将永久删除 ${row.username} 该用户, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async () => {
          const res = await this.$http.delete(`/api/users/${row.id}/`)

          const loadingInstance = this.$loading()

          if (res.status === 204) {
            this.tableData = res.data.results
            this.$message({
              message: `${row.username} 用户删除成功`,
              type: 'warning'
            })
            // 执行数据获取 刷新表格
            this.fetch(this.paginations.page_num, this.paginations.page_size)
            loadingInstance.close()
          }
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    table_index(index) {
      // 分页自增
      return (this.paginations.page_index - 1) * this.paginations.page_size + index + 1
    },
    async fetch(page = 1, size = 10) {
      // 全屏loading开启
      const loadingInstance = this.$loading()

      // 数据获取
      const res = await this.$http.get(`/api/users/?page=${page}&size=${size}`)
      // 分页总数赋予
      this.paginations.total = res.data.count

      if (res.status === 200) {
        this.tableData = res.data.results
        // 数据赋予、全屏loading 关闭
        loadingInstance.close()
      }
    },
    async handleCurrentChange(page) {
      // 页码变化触发操作
      this.fetch(page, this.paginations.page_size)
      this.paginations.page_num = page
      // /api/users/?page=2&size=10
    },
    async handleSizeChange(size) {
      // 每页x条变化触发操作
      this.paginations.page_size = size
      this.fetch(this.paginations.page_num, size)
    }
  },
  created() {
    this.fetch()
  }
}
</script>
<style></style>
