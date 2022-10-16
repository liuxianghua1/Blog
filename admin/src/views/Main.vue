<template>
  <el-container style="height: 100vh">
    <el-header style="text-align: right; font-size: 12px">
      <el-dropdown>
        <span> {{ username }}</span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="dialogFormVisible = true">修改密码</el-dropdown-item>
          <el-dropdown-item @click.native="exit()">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-header>

    <!-- 修改密码的 -->
    <el-dialog @close="closeDialog()" title="修改密码" :visible.sync="dialogFormVisible">
      <el-form :rules="rules" ref="form" :model="form">
        <el-form-item prop="oldPassword" label="原密码" label-width="120px">
          <el-input type="password" v-model="form.oldPassword" placeholder="请输入原密码"></el-input>
        </el-form-item>
        <el-form-item prop="password" label="新密码" label-width="120px">
          <el-input type="password" v-model="form.password" placeholder="请输入新密码"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click.prevent="updataPassword('form')">确 定</el-button>
      </div>
    </el-dialog>

    <el-container>
      <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
        <el-menu router unique-opened :default-active="$route.path">
          <el-menu-item index="/home"><i class="el-icon-house"></i>主页</el-menu-item>
          <el-submenu v-show="role == 1" index="1">
            <template slot="title"><i class="el-icon-user"></i>用户管理</template>
            <el-menu-item-group>
              <el-menu-item index="/home/user_create">新建用户</el-menu-item>
              <el-menu-item index="/home/user_list">用户列表</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-edit-outline"></i>文章管理</template>
            <el-menu-item-group>
              <el-menu-item index="/home/article_create">发布文章</el-menu-item>
              <el-menu-item index="/home/article_list">文章列表</el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-menu-item index="/home/category_list"><i class="el-icon-guide"></i>分类列表</el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view :key="$route.path"></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<style>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}
</style>

<script>
export default {
  data() {
    return {
      username: localStorage.username,
      role: localStorage.role,
      dialogFormVisible: false,
      form: {
        oldPassword: '',
        password: ''
      },
      rules: {
        oldPassword: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
        password: [{ required: true, message: '请输入新密码', trigger: 'blur' }]
      }
    }
  },
  methods: {
    exit() {
      localStorage.clear()
      this.$message.success('退出成功')
      this.$router.push('/login')
    },
    closeDialog() {
      this.form = {
        oldPassword: '',
        password: ''
      }
    },
    updataPassword(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          if (this.form.oldPassword === this.form.password) {
            this.$message.error('原密码不能和新密码一样')
          } else {
            this.$http.put('/api/update_pass/', this.form).then(res => {
              if (res.data.code === 200) {
                localStorage.clear()
                this.$router.push('/login')
                this.$message.success(res.data.msg + '请重新登录')
              } else {
                this.$message.error(res.data.msg)
              }
            })
          }
        } else {
          return false
        }
      })
    }
  }
}
</script>
