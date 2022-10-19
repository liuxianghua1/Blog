import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Article from '../views/Article.vue'
import Category from '../views/category.vue'
import ArticleByCategory from '../views/ArticleByCategory.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/article/:id',
    name: 'Article',
    component: Article,
    props: true
  },
  {
    path: '/category',
    name: 'category',
    component: Category,
    children: [
      {
        path: 'articlebycategory/:id',
        component: ArticleByCategory,
        props: true
      }
    ]
  }
  // {
  //   path: '/category/:id',
  //   name: 'category',
  //   component: category,
  //   props: true
  // }
  // {
  //   path: '/about',
  //   name: 'About',
  //   component: About
  // }
]

const router = new VueRouter({
  routes
})

export default router
