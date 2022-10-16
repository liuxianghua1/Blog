<template>
  <el-container style="height: 100vh">
    <el-header style="text-align: right; font-size: 12px">
      <el-dropdown>
        <span> {{ username }}</span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="updated">修改密码</el-dropdown-item>
          <el-dropdown-item @click.native="exit()">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-header>

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
      role: localStorage.role
    }
  },
  methods: {
    exit() {
      localStorage.clear()
      this.$message('退出成功')
      this.$router.push('login')
    }
  }
}
</script>
