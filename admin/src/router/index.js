import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'
import UserList from '../views/UserList.vue'
import UserCreate from '../views/UserCreate.vue'
Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/home' },
  {
    path: '/home',
    name: 'Main',
    component: Main,
    children: [
      {
        path: 'user_list',
        component: UserList
      },
      {
        path: 'user_create',
        component: UserCreate
      },
      {
        path: 'user_updata/:id',
        component: UserCreate,
        props: true
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
