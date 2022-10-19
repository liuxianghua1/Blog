<template>
  <div>
    <v-list two-line>
      <v-list-item-group active-class="blue--text">
        <template v-for="(item, index) in articleList">
          <v-list-item @click="$router.push(`/article/${item.id}`)" :key="item.id">
            <template>
              <v-list-item-content>
                <v-list-item-title v-text="item.title"></v-list-item-title>

                <v-list-item-subtitle class="text--primary"> <v-icon color="grey lighten-1" class="mb-1"> mdi-eye </v-icon>浏览量:{{ item.clicks }} </v-list-item-subtitle>

                <v-list-item-subtitle> 发表时间:{{ item.createtime.split('T')[0] }} </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon color="grey lighten-1"> mdi-dots-horizontal </v-icon>
              </v-list-item-action>
            </template>
          </v-list-item>

          <v-divider v-if="index < articleList.length - 1" :key="index"></v-divider>
        </template>
      </v-list-item-group>
    </v-list>
  </div>
</template>

<script>
export default {
  props: ['id'],
  data: () => ({
    categoryList: [],
    articleList: []
  }),
  methods: {
    fetch() {
      // 标题 作者名 fabiaoshijian liulanliang yuantuqiuwenanniu
      this.$http
        .get(`api/category_list/${this.id}/`)
        .then(res => {
          this.articleList = res.data.articleList
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

<style></style>
