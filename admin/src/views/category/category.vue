<template>
  <div>
    <el-input v-model="createCategory" ref="createCategory" style="margin-bottom: 20px; width: 250px" placeholder="在这里输入新分类名" @keyup.enter.native="createCategoryMethods" @blur="createCategoryMethods"> </el-input>

    <el-table ref="filterTable" border :data="tableData" style="width: 100%">
      <el-table-column type="index" width="50" label="序号"> </el-table-column>
      <el-table-column prop="id" label="id"> </el-table-column>
      <el-table-column prop="name" label="分类">
        <template slot-scope="scope">
          <el-popover transition="el-zoom-in-top" :visible-arrow="false" placement="top" width="250" height="40" trigger="click">
            <el-input placeholder="在这里更新你的分类名" v-model="updateCategory" @keyup.enter.native="createCategoryMethods(scope.row)" @blur="createCategoryMethods(scope.row)"> </el-input>
            <el-tag slot="reference">{{ scope.row.name }}</el-tag>
          </el-popover>
        </template>
      </el-table-column>

      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="medium" type="danger" round @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
      createCategory: '',
      updateCategory: ''
    }
  },
  methods: {
    // 新建方法
    createCategoryMethods(row) {
      if (row.id) {
        if (this.updateCategory.trim() !== '') {
          this.$http
            .put(`api/categorys/${row.id}/update_category/`, { name: this.updateCategory })
            .then(res => {
              let flag = ''
              res.data.code === 200 ? (flag = 'success') : (flag = 'error')
              this.$message({
                message: res.data.msg,
                type: flag
              })
              this.fetch()
              this.updateCategory = ''
            })
            .catch(() => {
              this.updateCategory = ''
            })
        }
      } else {
        // 查重
        if (this.createCategory.trim() !== '') {
          this.$http
            .post('api/categorys/create_category/', { name: this.createCategory })
            .then(res => {
              let flag = ''
              res.data.code === 200 ? (flag = 'success') : (flag = 'error')
              this.$message({
                message: res.data.msg,
                type: flag
              })
              this.fetch()
              this.createCategory = ''
            })
            .catch(() => {
              this.createCategory = ''
            })
        }
      }
    },
    handleDelete(row) {
      this.$confirm(`此操作将永久删除 ${row.name} 该分类, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async () => {
          const res = await this.$http.delete(`/api/categorys/${row.id}/`)

          if (res.status === 204) {
            this.tableData = res.data.results
            this.$message({
              message: `${row.name} 分类删除成功`,
              type: 'success'
            })
            this.fetch()
          } else {
            this.$message({
              message: `${row.name} 分类删除失败`,
              type: 'error'
            })
          }
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    async fetch() {
      const res = await this.$http.get('/api/categorys/')
      if (res.status === 200) {
        this.tableData = res.data
      }
    }
  },
  created() {
    this.fetch()
  }
}
</script>
<style></style>
