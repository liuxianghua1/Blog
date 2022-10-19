import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Article from '../views/Article.vue'
import Category from '../views/category.vue'
import ArticleByCategory from '../views/ArticleByCategory.vue'
import Archiving from '../views/Archiving.vue'
import About from '../views/About.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: {
      title: '主页'
    }
  },
  {
    path: '/article/:id',
    name: 'Article',
    component: Article,
    props: true
  },
  {
    path: '/archiving',
    name: 'Archiving',
    component: Archiving,
    meta: {
      title: '归档'
    }
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: {
      title: '关于'
    }
  },
  {
    path: '/category',
    name: 'category',
    component: Category,
    meta: {
      title: '分类'
    },
    children: [
      {
        path: 'articlebycategory/:id',
        component: ArticleByCategory,
        props: true,
        meta: {
          title: '分类'
        }
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

router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

export default router
