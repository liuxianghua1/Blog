<template>
  <div class="login-container">
    <el-card header="请先登录" class="login-card">
      <el-form :model="model" :rules="rules" ref="model" class="demo-ruleForm">
        <el-form-item label="用户名" prop="username">
          <el-input placeholder="请输入账户" prefix-icon="el-icon-user" v-model="model.username"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input type="password" prefix-icon="el-icon-unlock" placeholder="请输入密码" show-password v-model="model.password"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" native-type="“submit”" @click.prevent="submitForm('model')">提交</el-button>
          <el-button @click="resetForm('model')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script>
export default {
  data() {
    return {
      model: {
        username: '',
        password: ''
      },
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.login()
        } else {
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    async login() {
      const res = await this.$http.post('/api/login/', this.model)
      // 窗口关闭需重新登录
      // sessionStorage.token = res.data.token

      // 窗口关闭可继续使用

      if (res.data.code === 200) {
        localStorage.token = res.data.token
        localStorage.id = res.data.id
        localStorage.username = res.data.username
        localStorage.role = res.data.role
        localStorage.EditorTheme = 'bubble'

        this.$router.push('/admin')

        this.$message({
          type: 'success',
          message: res.data.msg
        })
      } else {
        this.$message({
          type: 'error',
          message: res.data.msg
        })
      }
      // // localStorage.setItem('username', this.model.username)
    }
  }
}
</script>

<style>
.login-card {
  width: 25rem;
  margin: 8rem auto;
}
</style>
