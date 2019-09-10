<template>
  <Form ref="formInline" :model="formInline" :rules="ruleInline" inline>
    <h1>{{ id ? "编辑" : "新建" }}分类</h1>
    <br />
    <FormItem prop="category">
      <Input
        type="text"
        v-model="formInline.category"
        placeholder="请输入分类名称"
      />
    </FormItem>
    <FormItem>
      <Button type="primary" @click="handleSubmit('formInline')">Signin</Button>
    </FormItem>
  </Form>
</template>
<script>
export default {
  props: {
    id: {}
  },
  data() {
    return {
      formInline: {
        category: ""
      },
      ruleInline: {
        category: [
          {
            required: true,
            message: "Please fill in the category name",
            trigger: "blur"
          }
        ]
      }
    };
  },
  methods: {
    handleSubmit(name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          this.save();
          this.$Message.success("修改成功!");
        } else {
          this.$Message.error("请输入分类名称!");
        }
      });
    },

    async save() {
      if (this.id) {
        await this.$http.put(`category/${this.id}`, this.formInline);
      } else {
        await this.$http.post("category", this.formInline);
      }
      this.$router.push("/category/list");
    },
    async fetch() {
      const res = await this.$http.get(`category/${this.id}`, this.formInline);
      this.formInline = res.data;
    }
  },
  created() {
    this.id && this.fetch();
  }
};
</script>
