<template>
  <div>
    <!-- 表头区域 -->
    <el-page-header @back="$router.go(-1)" :content="id ? '修改用户' : '新建用户'" style="margin-bottom: 50px"></el-page-header>

    <!-- 表单区域 -->
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
      <el-form-item label="用户名" :prop="id ? '' : 'username'">
        <el-input :disabled="id ? true : false" placeholder="保存后无法修改,请谨慎填写。" v-model="ruleForm.username"></el-input>
      </el-form-item>
      <el-form-item label="手机号" :prop="id ? '' : 'phone'">
        <el-input :disabled="id ? true : false" placeholder="保存后无法修改,请谨慎填写。" v-model="ruleForm.phone"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="ruleForm.password" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="用户权限" prop="role">
        <el-radio v-model="ruleForm.role" :label="0">管理员</el-radio>
        <el-radio v-model="ruleForm.role" :label="1">超级管理员</el-radio>
      </el-form-item>
      <el-form-item label="用户状态" prop="status">
        <el-radio v-model="ruleForm.status" :label="0">禁用</el-radio>
        <el-radio v-model="ruleForm.status" :label="1">激活</el-radio>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        <el-button v-if="!this.id" @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
// 待实现功能 新建用户、修改用户
export default {
  props: {
    id: {}
  },
  data() {
    var validatePass = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请再次输入密码'))
      } else {
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    var validatePhone = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('手机号不能为空'))
      } else {
        const reg = /^1[3|4|5|7|8][0-9]\d{8}$/
        if (reg.test(value)) {
          callback()
        } else {
          return callback(new Error('请输入正确的手机号'))
        }
      }
    }
    return {
      ruleForm: {
        username: '',
        phone: '',
        password: '',
        checkPass: '',
        role: 0,
        status: 1
      },
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        phone: [{ required: true, validator: validatePhone, trigger: 'blur' }],
        password: [{ required: true, validator: validatePass, trigger: 'blur' }],
        checkPass: [{ required: true, validator: validatePass2, trigger: 'blur' }],
        role: [{ required: true, message: '请选择用户权限', trigger: 'change' }],
        status: [{ required: true, message: '请选择用户状态', trigger: 'change' }]
      }
    }
  },
  methods: {
    // 获取用户数据的方法
    async fetch() {
      const { data: res } = await this.$http.get(`/api/users/${this.id}/`)

      this.ruleForm = res
    },
    // 提交方法
    async create() {
      // admin 15000485500
      const res = await this.$http.post('/api/users/createuser/', this.ruleForm)
      if (res.data.code === 201) {
        // 创建成功
        this.$message({
          type: 'success',
          message: '创建成功'
        })
        this.$router.push('/home/user_list/')
      } else if (res.data.code === 500) {
        this.$message({
          type: 'error',
          message: res.data.msg
        })
      }
    },
    // 更新方法
    async update() {
      const res = await this.$http.put(`/api/users/${this.id}/updateuser/`, this.ruleForm)
      if (res.data.code === 201) {
        // 更新成功
        this.$message({
          type: 'success',
          message: '更新成功'
        })
        this.$router.push('/home/user_list/')
      }
    },
    // 提交方法
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          if (!this.id) {
            this.create()
          } else {
            this.update()
          }
        } else {
          return false
        }
      })
    },
    // 重置表单方法
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  },
  created() {
    // id得到后再接着获取用户信息
    this.id && this.fetch()
  }
}
</script>
