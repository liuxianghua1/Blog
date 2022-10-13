import Vue from 'vue'
import axios from 'axios'

// axios.defaults.baseURL = 'http://127.0.0.1:8000/'
// Vue.prototype.$http = axios
const http = axios.create({
  // 动态端口 不写死
  // baseURL: process.env.VUE_APP_API_URL || '/admin/api',

  baseURL: 'http://127.0.0.1:8000/'
})

http.interceptors.request.use(
  function (config) {
    if (localStorage.token) {
      // config.headers.Authorization = 'JWT ' + (localStorage.token || '')
      config.headers.Authorization =
        'JWT ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1NjgyMTY1LCJpYXQiOjE2NjU2Mzg5NjUsImp0aSI6IjFkMWY2NjgxNWQ0MTQwNmM5ZjI5Mzk4OWUyOTAzMDIyIiwidXNlcl9pZCI6MjczLCJuYW1lIjoibHhoIiwicm9sZSI6MCwic3RhdHVzIjoxfQ.smZNup22QkjSt5-h4VuFqnyzDA8T4mJPh6fjPVxltq4'
    }
    return config
  },
  function (error) {
    return Promise.reject(error)
  }
)

// 服务端返回错误 有message 就弹出
http.interceptors.response.use(
  res => {
    return res
  },
  err => {
    if (err) {
      const loadingInstance = Vue.prototype.$loading()
      Vue.prototype.$message({
        type: 'error',
        // 弹窗的内容 在status中的message定义
        message: err
      })
      loadingInstance.close()
      // if (err.response.status === 401) {
      //     router.push('/login')
      // }
    }
    return Promise.reject(err)
  }
)

export default http
