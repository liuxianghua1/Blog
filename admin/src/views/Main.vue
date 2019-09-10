<style scoped>
.layout {
  border: 1px solid #d7dde4;
  background: #f5f7f9;
  position: relative;
  border-radius: 4px;
  overflow: hidden;
}
.layout-nav {
  float: right;
}
.layout-header-bar {
  background: #fff;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
}
.menu-item span {
  display: inline-block;
  overflow: hidden;
  width: 69px;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: bottom;
  transition: width 0.2s ease 0.2s;
}
.menu-item i {
  transform: translateX(0px);
  transition: font-size 0.2s ease, transform 0.2s ease;
  vertical-align: middle;
  font-size: 16px;
}
.collapsed-menu span {
  width: 0px;
  transition: width 0.2s ease;
}
.collapsed-menu i {
  transform: translateX(5px);
  transition: font-size 0.2s ease 0.2s, transform 0.2s ease 0.2s;
  vertical-align: middle;
  font-size: 22px;
}
</style>
<template>
  <div class="layout">
    <Layout>
      <Sider
        breakpoint="md"
        collapsible
        :collapsed-width="78"
        v-model="isCollapsed"
      >
        <Menu router theme="dark" width="auto" :class="menuitemClasses">
          <MenuGroup title="内容管理">
            <MenuItem to="/category/list" name="1">
              <Icon type="md-document" />
              分类管理
            </MenuItem>
            <MenuItem to="/category/create" name="2">
              <Icon type="md-document" />
              新建分类
            </MenuItem>
            <MenuItem to="/article/list" name="3">
              <Icon type="md-document" />
              文章管理
            </MenuItem>
            <MenuItem to="/article/create" name="4">
              <Icon type="md-chatbubbles" />
              文章发布
            </MenuItem>
          </MenuGroup>
          <MenuGroup title="统计分析">
            <MenuItem name="3">
              <Icon type="md-heart" />
              用户留存
            </MenuItem>
            <MenuItem name="4">
              <Icon type="md-leaf" />
              流失用户
            </MenuItem>
          </MenuGroup>
        </Menu>
        <div slot="trigger"></div>
      </Sider>
      <Layout>
        <Header class="layout-header-bar">
          <div class="layout-nav">
            <MenuItem name="1">
              <Icon type="ios-contact" size="20" />
              用户
            </MenuItem>
          </div>
        </Header>
        <Content
          :style="{ margin: '20px', background: '#fff', minHeight: '100vh' }"
        >
          <router-view></router-view>
        </Content>
      </Layout>
    </Layout>
  </div>
</template>
<script>
export default {
  data() {
    return {
      isCollapsed: false
    };
  },
  computed: {
    menuitemClasses: function() {
      return ["menu-item", this.isCollapsed ? "collapsed-menu" : ""];
    }
  }
};
</script>
