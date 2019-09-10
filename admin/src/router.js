import Vue from 'vue'
import Router from 'vue-router'
import Main from './views/Main.vue'
import ArticleCategory from './views/article/ArticleCategory.vue'
import ArticleCategoryList from './views/article/ArticleCategoryList.vue'
import Article from './views/article/ArticleEdit.vue'
import ArticleList from './views/article/ArticleList.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/', name: 'Main', component: Main, children: [
        { path: '/category/create', name: 'articleedit', component: ArticleCategory },
        { path: '/category/edit/:id', name: 'articleedit', component: ArticleCategory, props: true },
        { path: '/category/list', name: 'articleCategorylist', component: ArticleCategoryList },

        { path: '/article/create', name: 'article', component: Article },
        { path: '/article/edit/:id', name: 'article', component: Article, props: true },
        { path: '/article/list', name: 'articleList', component: ArticleList },




        // { path: '/article/list', name: 'articleedit', component: ArticleEdit },
      ]
    },





    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    // }
  ]
})
