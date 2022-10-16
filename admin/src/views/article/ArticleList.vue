<template>
  <div>
    <el-button @click="clearFilter" style="margin-bottom: 20px">清除所有过滤条件</el-button>
    <el-table ref="filterTable" border :row-class-name="tableRowClassName" :data="tableData.filter(data => !search || data.title.toLowerCase().includes(search.toLowerCase()))" style="width: 100%">
      <el-table-column type="index" :index="table_index" width="50" label="序号"> </el-table-column>
      <el-table-column prop="id" label="id" width="50"></el-table-column>
      <el-table-column prop="title" label="标题"></el-table-column>
      <el-table-column prop="image_url" label="封面">
        <template slot-scope="scope">
          <el-image v-if="scope.row.image_url" :src="'/uploads/' + scope.row.image_url" :preview-src-list="['/uploads/' + scope.row.image_url]"> </el-image>
          <span v-else>未传封面</span>
          <!-- <el-empty v-else :image-size="50" description="未上传图片"></el-empty> -->
        </template>
      </el-table-column>
      <el-table-column prop="categorys" label="分类">
        <template slot-scope="scope">
          <el-tag style="margin: 0 5px 5px 0" v-for="i in scope.row.categorys" :key="i.id">
            {{ i.name }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="author" label="作者"></el-table-column>
      <el-table-column prop="author_role" label="作者身份">
        <template slot-scope="scope">
          <el-tag :type="scope.row.author_role === 1 ? 'success' : 'primary'">{{ scope.row.author_role === 1 ? '超级管理员' : '管理员' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="clicks" label="点击数"></el-table-column>
      <el-table-column sortable prop="createtime" label="发表时间"> </el-table-column>

      <el-table-column
        prop="status"
        :filters="[
          { text: '隐藏', value: 0 },
          { text: '展示', value: 1 }
        ]"
        :filter-method="filterStatus"
        label="状态"
      >
        <template slot-scope="scope">
          <el-switch :value="scope.row.status === 1 ? true : false" active-color="#13ce66" inactive-color="#ff4949" active-text="展示" inactive-text="隐藏" @change="statusChange(scope.row.id, scope.row.status)"> </el-switch>
        </template>
      </el-table-column>
      <el-table-column width="173" align="right">
        <template slot="header" slot-scope="{}">
          <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
        </template>
        <template slot-scope="scope">
          <el-button size="medium" type="primary" round @click="$router.push(`/home/article_update/${scope.row.id}`)">编辑</el-button>
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
      search: '',
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
    clearFilter() {
      this.$refs.filterTable.clearFilter()
    },
    tableRowClassName({ row }) {
      if (row.status === 0) {
        return 'danger-row'
        // 文章隐藏会让这行变色
      }
    },
    // 文章状态更改方法 这个id是从scope.row.id中传过来的
    statusChange(id, status) {
      this.$http.put(`/api/articles/${id}/update_article/`, { status: status === 1 ? 0 : 1 }).then(() => {
        this.fetch(this.paginations.page_num, this.paginations.page_size)
      })
    },
    filterStatus(value, row) {
      // 权限筛选功能
      return row.status === value
    },
    handleDelete(row) {
      // 删除方法
      this.$confirm(`此操作将永久删除 ${row.title} 该文章, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async () => {
          const res = await this.$http.delete(`/api/articles/${row.id}/`)

          if (res.status === 204) {
            this.tableData = res.data.results
            this.$message({
              message: `${row.title} 文章删除成功`,
              type: 'success'
            })
            // 执行数据获取 刷新表格
            this.fetch(this.paginations.page_num, this.paginations.page_size)
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
      // 数据获取
      const res = await this.$http.get(`/api/articles/?page=${page}&size=${size}`)
      // 分页总数赋予
      this.paginations.total = res.data.count
      if (res.status === 200) {
        this.tableData = res.data.results
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
<style>
.el-table .danger-row {
  background: #f8e2e1;
}
</style>
