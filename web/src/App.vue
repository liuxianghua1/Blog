<template>
  <v-app id="inspire">
    <!-- 头部 -->
    <v-app-bar flat app color="#f5f5f5" class="d-flex">
      <v-container class="py-0 fill-height">
        <div class="d-flex">
          <!-- LOGO -->
          <v-toolbar-title class="mr-2 headline grey--text text--darken-1 float-left">
            <span class="font-weight">刘翔華</span>
            <span>Blog</span>
          </v-toolbar-title>

          <v-btn v-for="i in links" :key="i.name" :to="i.url" text>
            {{ i.name }}
          </v-btn>

          <v-spacer></v-spacer>

          <v-responsive class="mt-1">
            <v-text-field light append-icon="mdi-magnify" dense flat hide-details label="搜索博客" placeholder="输入标题" rounded></v-text-field>
          </v-responsive>
        </div>
      </v-container>
    </v-app-bar>

    <!-- <v-navigation-drawer clipped-left>左边</v-navigation-drawer> -->
    <!-- <v-navigation-drawer clipped-right>右边</v-navigation-drawer> -->

    <v-main>
      <!-- fluid -->
      <v-container class="justify-center">
        <router-view :key="$route.path"></router-view>
      </v-container>
    </v-main>

    <v-footer padless>
      <v-col cols="12" class="text-center black--text">谁也不感谢了，就感谢我自己，写代码好累，我好牛蛙！ </v-col>
      <v-col class="text-center" cols="12"> {{ new Date().getFullYear() }} — <strong>刘翔華</strong> </v-col>
    </v-footer>
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
