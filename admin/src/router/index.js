import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'

import UserList from '../views/user/UserList.vue'
import UserCreate from '../views/user/UserCreate.vue'

import Login from '../views/login/Login.vue'

import ArticleList from '../views/article/ArticleList.vue'
import CreateArticle from '../views/article/CreateArticle.vue'

import CategoryList from '../views/category/category.vue'

Vue.use(VueRouter)

// 超级用户的
const routes = [
  { path: '/login', name: 'login', component: Login, meta: { isPublic: true } },
  // { path: '/admin/', redirect: '/admin' },
  {
    path: '/admin',
    name: 'Main',
    component: Main,

    children: [
      {
        path: 'user_list',
        component: UserList,
        meta: { role: 1 }
      },
      {
        path: 'user_create',
        component: UserCreate,
        meta: { role: 1 }
      },
      {
        path: 'user_updata/:id',
        component: UserCreate,
        props: true,
        meta: { role: 1 }
      },
      {
        path: 'article_list',
        component: ArticleList
      },
      {
        path: 'article_create',
        component: CreateArticle
      },
      {
        path: 'article_update/:id',
        component: CreateArticle,
        props: true
      },
      {
        path: 'category_list',
        component: CategoryList
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location, onResolve, onReject) {
  if (onResolve || onReject) return originalPush.call(this, location, onResolve, onReject)
  return originalPush.call(this, location).catch(err => err)
}

// 路由限制 if 判断 不是isPublic：true 也没有token 则跳转
router.beforeEach((to, from, next) => {
  window.addEventListener('storage', function (e) {
    localStorage.setItem(e.newValue, e.oldValue)
  })
  if (!to.meta.isPublic && !localStorage.token) {
    return next('/login')
  } else if (to.meta.role === 1 && Number(localStorage.role) === 0) {
    return next('/admin')
  }

  next()
})

export default router
