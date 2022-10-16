<template>
  <div>
    <el-input v-model="createCategory" ref="createCategory" style="margin-bottom: 20px; width: 250px" placeholder="在这里输入新分类名" @keyup.enter.native="createCategoryMethods" @blur="createCategoryMethods"> </el-input>

    <el-table ref="filterTable" border :data="tableData" style="width: 100%">
      <el-table-column type="index" width="50" label="序号"> </el-table-column>
      <el-table-column prop="id" label="id"> </el-table-column>
      <el-table-column prop="name" label="分类">
        <template slot-scope="scope">
          <div slot="reference" class="name-wrapper">
            <el-tag>{{ scope.row.name }}</el-tag>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-popover placement="top" width="250" height="40" trigger="click">
            <el-input placeholder="在这里更新你的分类名" v-model="updateCategory" ref="updateCategory" @keyup.enter.native="createCategoryMethods(scope.row)" @blur="createCategoryMethods(scope.row)"> </el-input>
            <el-button slot="reference" size="medium" type="primary" round style="margin-right: 10px">编辑</el-button>
          </el-popover>

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
              this.$message({
                message: res.data.msg,
                type: 'info'
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
              if (res) {
                this.$message({
                  message: res.data.msg,
                  type: 'info'
                })
                this.fetch()
                this.createCategory = ''
              }
            })
            .catch(() => {
              this.createCategory = ''
            })
        }
      }
    },
    addCategory() {},
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
              type: 'warning'
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
