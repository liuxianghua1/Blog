import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Article from '../views/Article.vue'
import category from '../views/category.vue'

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
    component: category
  },
  {
    path: '/category/:id',
    name: 'category',
    component: category,
    props: true
  }
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
