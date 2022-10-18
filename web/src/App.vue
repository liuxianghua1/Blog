<template>
  <v-app id="inspire">
    <!-- 头部 -->
    <v-app-bar flat app color="#f5f5f5" class="d-flex justify-center">
      <v-container class="py-0 fill-height">
        <!-- <v-avatar class="mr-10" color="grey darken-1" size="32">
          <span class="white--text text-h5">刘翔華</span>
        </v-avatar> -->
        <div class="d-flex">
          <!-- LOGO -->
          <v-toolbar-title class="mr-2 headline grey--text text--darken-1">
            <span class="font-weight">刘翔華</span>
            <span>Blog</span>
          </v-toolbar-title>

          <v-btn v-for="i in links" :key="i.name" :to="i.url" text>
            {{ i.name }}
          </v-btn>

          <v-spacer></v-spacer>

          <v-responsive class="mt-1" max-width="250">
            <v-text-field light append-icon="mdi-magnify" dense flat hide-details label="搜索你想要找的博客" placeholder="输入文章标题" rounded></v-text-field>
          </v-responsive>
        </div>
      </v-container>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view :key="$route.path"></router-view>
      </v-container>
    </v-main>

    <!-- 页脚 -->
    <!-- <v-btn
        v-for="link in links"
        :key="link"
        color="white"
        text
        rounded
        class="my-2"
      >
        {{ link }}
      </v-btn> -->
    <!-- <v-footer dark padless>
      <v-card flat tile class="indigo lighten-1 white--text text-center">
        <v-card-text>
          <v-btn v-for="icon in icons" :key="icon" class="mx-4 white--text" icon>
            <v-icon size="24px">
              {{ icon }}
            </v-icon>
          </v-btn>
        </v-card-text>

        <v-card-text class="white--text pt-0"> 感谢我自己，写代码真累，谁也不感谢了，我最牛逼 </v-card-text>

        <v-divider></v-divider>

        <v-card-text class="white--text"> {{ new Date().getFullYear() }} — <strong>刘翔華</strong> </v-card-text>
      </v-card>
    </v-footer> -->
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
