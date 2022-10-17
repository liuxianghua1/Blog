<template>
  <v-app id="inspire">
    <!-- 头部 -->
    <v-app-bar app color="white" flat>
      <v-container class="py-0 fill-height">
        <v-avatar class="mr-10" color="grey darken-1" size="32">
          <span class="white--text text-h5">刘翔華</span>
        </v-avatar>

        <v-btn v-for="i in links" :key="i.name" :to="i.url" text>
          {{ i.name }}
        </v-btn>

        <v-spacer></v-spacer>

        <!-- 搜索款 -->
        <v-responsive max-width="260">
          <v-text-field dense flat hide-details rounded solo-inverted></v-text-field>
        </v-responsive>
      </v-container>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view :key="$route.path"></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      links: [
        {
          name: '主页',
          url: '/home'
        },
        {
          name: '分类',
          url: '/category'
        },
        {
          name: '关于',
          url: '/about'
        },
        {
          name: '归档',
          url: '/archiving'
        }
      ]
    }
  }
  // methods: {
  //   demo() {
  //     console.log('!')
  //   }
  // },
  // created() {
  //   this.demo()
  // }
}
</script>
