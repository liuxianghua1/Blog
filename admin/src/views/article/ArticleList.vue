<template>
  <Table :columns="columns1" :data="article">
  </Table>
</template>
<script>
export default {
  data() {
    return {
      article: [],
      columns1: [
        {
          title: "Id",
          key: "_id"
        },
        {
          title: "文章名称",
          key: "title"
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
                      this.$router.push(`/article/edit/${params.row._id}`);
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
                      this.$http.delete(`rest/article/delete/${params.row._id}`);
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
      const res = await this.$http.get("rest/article");
      this.article = res.data;
    },
    remove(index) {
      this.article.splice(index, 1);
    }
  },
  created() {
    this.fetch();
  }
};
</script>
