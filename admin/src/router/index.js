import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'
import UserList from '../views/user/UserList.vue'
import UserCreate from '../views/user/UserCreate.vue'
import Login from '../views/login/Login.vue'

Vue.use(VueRouter)

// 超级用户的
const routes = [
  { path: '/login', name: 'login', component: Login, meta: { isPublic: true } },
  { path: '/', redirect: '/home' },
  {
    path: '/home',
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
      }
    ]
  }
]

const router = new VueRouter({
  routes
})
// 路由限制 if 判断 不是isPublic：true 也没有token 则跳转
router.beforeEach((to, from, next) => {
  window.addEventListener('storage', function (e) {
    localStorage.setItem(e.newValue, e.oldValue)
  })

  if (!to.meta.isPublic && !localStorage.token) {
    return next('/login')
  } else if (to.meta.role === 1 && Number(localStorage.role) === 0) {
    return next('/home')
  }
  next()
})

export default router
