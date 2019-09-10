<template>
  <Table :columns="columns1" :data="category"> </Table>
</template>
<script>
export default {
  data() {
    return {
      category: [],
      columns1: [
        {
          title: "Id",
          key: "_id"
        },
        {
          title: "分类名称",
          key: "category"
        },
        {
          title: "添加时间",
          key: "createdAt"
        },
        {
          title: "操作",
          render: (h, params) => {
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small"
                  },
                  style: {
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.$router.push(`/category/edit/${params.row._id}`);
                    }
                  }
                },
                "编辑"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "error",
                    size: "small"
                  },
                  on: {
                    click: () => {
                      this.$Notice.success({
                        title: "删除成功"
                      });
                      this.$http.delete(`/category/delete/${params.row._id}`);
                      this.remove(params.index);
                    }
                  }
                },
                "删除"
              )
            ]);
          }
        }
      ]
    };
  },
  methods: {
    async fetch() {
      const res = await this.$http.get("category");
      this.category = res.data;
    },
    remove(index) {
      this.category.splice(index, 1);
    }
  },
  created() {
    this.fetch();
  }
};
</script>
