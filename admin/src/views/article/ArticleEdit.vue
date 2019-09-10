<template>
  <Form ref="formInline" :model="formInline" :rules="ruleInline" inline>
    <h1>{{ id ? "编辑" : "新建" }}文章</h1>
    <br />
    <FormItem prop="title" label="标题">
      <Input
        type="text"
        v-model="formInline.title"
        placeholder="请输入文章标题"
      />
    </FormItem>
    <FormItem label="内容">
      <Input
        type="text"
        v-model="formInline.body"
      />
    </FormItem>
    <FormItem label="封面">
      <el-upload
  class="avatar-uploader"
  :action="$http.defaults.baseURL+'/upload'"
  :show-file-list="false"
  :on-success="afterUpload"
  >
  <img v-if="formInline.icon" :src="formInline.icon" class="avatar">
  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
</el-upload>
    </FormItem>
    <br>
    <FormItem>
      <Button type="primary" @click="handleSubmit('formInline')">确定</Button>
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
        title: "",
        body: "",
        icon: ''
      },
      ruleInline: {
        title: [
          {
            required: true,
            message: "Please fill in the title name",
            trigger: "blur"
          }
        ]
      }
    };
  },
  methods: {
    afterUpload(res) {
      this.$set(this.formInline, 'icon', res.url)
      // this.formInline.icon = res.url
    },

    handleSubmit(name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          this.save();
          this.$Message.success("修改成功!");
        } else {
          this.$Message.error("请输入标题名称!");
        }
      });
    },

    async save() {
      if (this.id) {
        await this.$http.put(`rest/article/${this.id}`, this.formInline);
      } else {
        await this.$http.post("rest/article", this.formInline);
      }
      this.$router.push("/article/list");
    },
    async fetch() {
      const res = await this.$http.get(`rest/article/${this.id}`, this.formInline);
      this.formInline = res.data;
    }
  },
  created() {
    this.id && this.fetch();
  }
};
</script>
<style>
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
  .el-icon-plus:before {
    position: absolute;
    top: 77px;
    left: 77px;
  }
</style>