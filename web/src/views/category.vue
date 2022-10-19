<template>
  <div>
    <div class="text-h5 text-center">共有{{ this.count }}个分类</div>
    <div>
      <v-btn v-for="i in categoryList" :key="i.id" :to="`/category/articlebycategory/${i.id}`" text>
        {{ i.name }}
      </v-btn>
    </div>
    <router-view :key="$route.path"></router-view>
  </div>
</template>

<script>
export default {
  data: () => ({
    categoryList: [],
    count: ''
  }),
  methods: {
    fetch() {
      this.$http
        .get('api/category_list/')
        .then(res => {
          this.categoryList = res.data
          this.count = this.categoryList.length
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
