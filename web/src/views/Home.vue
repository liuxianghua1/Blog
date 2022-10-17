<template>
  <v-row>
    <v-col v-for="i in articleLit" :key="i.id" cols="12">
      <v-card outlined class="mx-auto">
        <v-img @click="$router.push(`/article/${i.id}`)" class="white--text align-end" style="cursor: pointer" height="auto" :src="i.image_url === '' ? 'http://localhost:8081/uploads/2022101710040245215.png' : 'http://localhost:8081/uploads/' + i.image_url"> </v-img>
        <v-card-title>
          <span class="text-h5" style="cursor: pointer" @click="$router.push(`/article/${i.id}`)">{{ i.title }}</span>
        </v-card-title>
        <v-card-subtitle class="pb-0 text--primary text-subtitle-1">作者：{{ i.author }}</v-card-subtitle>

        <v-card-text class="text--primary text-subtitle-1">
          <div>作者身份：{{ i.author_role === 0 ? '管理员' : '超级管理员' }}</div>
          <div>发表时间：{{ i.createtime }}</div>
          <div>
            分类：
            <v-chip v-for="k in i.categorys" :key="k.id" class="ma-1" color="blue" @click="readCategoryArticle(k.id)" label text-color="white">
              <v-icon left>mdi-code-tags </v-icon>
              {{ k.name }}
            </v-chip>
          </div>
        </v-card-text>
        <v-card-actions class="ml-2 pt-0">
          <v-btn outlined color="primary" @click="$router.push(`/article/${i.id}`)"> 阅读全文 <v-icon right>mdi-dots-horizontal</v-icon></v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
    <v-col cols="12">
      <div class="text-center">
        <span class="text-subtitle-2">共{{ pageCount }}篇文章</span>
        <v-pagination v-model="page" @input="onPageChange()" :length="pageLength" :total-visible="pageVisible" circle></v-pagination>
      </div>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    articleLit: [],
    page: 1, // 当前页码
    pageCount: 0,
    pageLimit: 5, // 每页展示数量
    pageLength: 0, // 总页码数 6/5 = 1余1 在向上取整
    pageVisible: 7 // 分页条中可见页面码数
  }),
  methods: {
    onPageChange() {
      this.fetch(this.page, this.pageLimit)
    },
    readArticle(id) {
      console.log('文章的' + id)
    },
    readCategoryArticle(id) {
      console.log('分类的id' + id)
    },
    fetch(page = 1, pageLimit = 5) {
      // page === 1 ? page : page - 1
      this.$http
        .get(`/api/article_list/?page=${page}&size=${pageLimit}/`)
        .then(res => {
          this.articleLit = res.data.results
          this.pageCount = res.data.count
          this.pageLength = Math.ceil(this.pageCount / this.pageLimit)
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  created() {
    this.fetch()
  }
}
</script>
