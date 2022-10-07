import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'
import UserList from '../views/UserList.vue'
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
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
