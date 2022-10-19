<template>
  <div>
    <v-card flat class="mx-auto">
      <v-card-title>
        <span class="text-h4 mx-auto">{{ articleData.title }}</span>
      </v-card-title>
      <v-img class="white--text align-end" height="auto" :src="articleData.image_url"> </v-img>

      <v-card-subtitle class="text-h6">
        <div style="text-align: center">
          <span class="mr-2">作者：{{ articleData.author }}</span>
          <span class="mr-2">作者身份：{{ articleData.author_role === 0 ? '管理员' : '超级管理员' }} </span>
          <span class="mr-2">发表时间：{{ articleData.createtime }}</span>
          <span> 分类：</span>
          <v-chip v-for="k in articleData.categorys" :key="k.id" @click="$router.push(`/category/articlebycategory/${k.id}`)" class="mr-2 text-primary text-subtitle-1" color="#f0f0f0" label text-color="black">
            {{ k.name }}
          </v-chip>
          <span> <v-icon class="mb-1">mdi-eye</v-icon> 浏览量：{{ articleData.clicks }}</span>
        </div>
      </v-card-subtitle>

      <v-card-text>
        <div class="ql-container ql-snow mx-auto HTMLCSS" v-if="articleData.body">
          <div class="ql-editor" v-html="articleData.body"></div>
        </div>
        <div v-else style="text-align: center" class="text-h3">啥也没发、空空如也</div>
      </v-card-text>
    </v-card>
    <div style="text-align: center">
      <span class="text-h5">全文完...</span>
    </div>
    <v-card-actions>
      <v-container fluid>
        <v-row dense>
          <v-col style="text-align: left" cols="6"
            ><v-btn :disabled="pre.id ? false : true" color="black" @click="pre.id ? $router.push(`/article/${pre.id}`) : ''" text> 上一篇：{{ pre.title ? pre.title : '没有上一篇了' }} </v-btn></v-col
          >
          <v-col style="text-align: right" cols="6"
            ><v-btn :disabled="next.id ? false : true" color="black" @click="next.id ? $router.push(`/article/${next.id}`) : ''" text>
              <span>下一篇：{{ next.title ? next.title : '没有下一篇了' }} </span></v-btn
            ></v-col
          >
        </v-row>
      </v-container>
    </v-card-actions>
  </div>
</template>

<script>
import '../css/quill.core.css'
import '../css/quill.snow.css'

export default {
  props: {
    id: {}
  },
  data() {
    return {
      articleData: [],
      next: [],
      pre: []
    }
  },
  methods: {
    async fetch() {
      this.$http
        .get(`api/article_list/${this.id}/?page=5`)
        .then(res => {
          this.articleData = res.data.serializer
          document.title = res.data.serializer.title
          this.next = res.data.next
          this.pre = res.data.pre
        })
        .catch(() => {
          this.$router.push('/home')
        })
    }
  },
  created() {
    // id得到后再接着获取用户信息
    this.id && this.fetch()
  }
}
</script>

<style scoped>
/*防止图片宽度超出*/
.HTMLCSS >>> img {
  max-width: 100%;
  margin-top: 20px;
}
.HTMLCSS >>> h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: 'PT Sans', 'SF UI Display', '.PingFang SC', 'PingFang SC', 'Neue Haas Grotesk Text Pro', 'Arial Nova', 'Segoe UI', 'Microsoft YaHei', 'Microsoft JhengHei', 'Helvetica Neue', 'Source Han Sans SC', 'Noto Sans CJK SC', 'Source Han Sans CN', 'Noto Sans SC', 'Source Han Sans TC',
    'Noto Sans CJK TC', 'Hiragino Sans GB', sans-serif;
  text-rendering: optimizelegibility;
  margin-bottom: 1em;
  font-weight: bold;
  line-height: 1.8rem;
}
/* .HTMLCSS  */
</style>
