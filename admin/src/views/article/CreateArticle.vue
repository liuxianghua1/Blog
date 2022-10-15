<template>
  <div>
    <!-- 表头区域 -->
    <el-page-header @back="$router.go(-1)" :content="id ? '修改文章' : '发布文章'" style="margin-bottom: 50px"></el-page-header>
    <el-form style="height: 100%" label-width="120px" @submit.native.prevent="create">
      <el-form-item label="标题">
        <el-input v-model="model.title"></el-input>
      </el-form-item>

      <el-form-item label="封面">
        <el-upload action="http://127.0.0.1:8000/api/articles/image_upload/" class="avatar-uploader" :on-success="afterUpload" :before-upload="beforeUpload" :headers="getAuthHeaders()" ref="upload" accept="image/jpeg,image/png,image/jpg" :show-file-list="false">
          <img v-if="model.image_url" :src="model.image_url" class="avatar" />
          <i v-else style="line-height: 178px" class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
      </el-form-item>

      <!-- 富文本编辑器 -->
      <el-form-item label="正文">
        <vue-editor id="editor" :editor-toolbar="customToolbar" useCustomImageHandler @image-added="handleImageAdded" v-model="model.body" />
      </el-form-item>

      <el-form-item label="分类">
        <el-select filterable clearable v-model="model.categorys" multiple placeholder="请选择文章分类">
          <el-option v-for="item in category" :key="item.id" :label="item.name" :value="item.id"> </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="状态">
        <el-switch :value="model.status === 1 ? true : false" active-color="#13ce66" inactive-color="#ff4949" active-text="展示" inactive-text="隐藏" @change="statusChange()"> </el-switch>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" native-type="submit">发布</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { VueEditor } from 'vue2-editor'

export default {
  props: {
    id: {}
  },
  data() {
    return {
      customToolbar: [['clean', 'link', 'video', 'image', 'code-block']],
      category: [
        { id: 1, name: 'python' },
        { id: 2, name: 'web' },
        { id: 3, name: 'vue' }
      ],
      model: {
        body: '',
        title: '',
        image_url: '',
        categorys: [],
        status: 1
      },
      image_name: ''
      // 用来存放图片文件名
      // http://127.0.0.1:8080/uploads/2022101506452378707.jpg 可以获取到
    }
  },
  methods: {
    // 封面上传    // 成功上传封面执行的方法
    // 图片上传的流程 先上传给后端 后端把路径返回给我 我在给model 然后随着表单一起传给数据库
    afterUpload(res) {
      this.image_name = res.filename
      this.$set(this.model, 'image_url', '/uploads/' + res.filename)
    },

    // 上传封面钱对类型做个限制
    beforeUpload(file) {
      const testmsg = file.name.substring(file.name.lastIndexOf('.') + 1)
      const extension = testmsg === 'jpg' || testmsg === 'jpeg' || testmsg === 'png'
      if (!extension) {
        this.$message({
          message: '上传图片类型不正确!',
          type: 'error'
        })
      }
      return extension
    },

    // 富文本编辑器上传图片的方法
    handleImageAdded(file, Editor, cursorLocation, resetUploader) {
      const flag = this.beforeUpload(file)
      if (flag) {
        const fm = new FormData()
        fm.append('file', file)
        this.$http
          .post('/api/articles/image_upload/', fm)
          .then(res => {
            Editor.insertEmbed(cursorLocation, 'image', '/uploads/' + res.data.filename)
            // 把光标移至图片后面
            Editor.setSelection(cursorLocation + 1)
            resetUploader()
          })
          .catch(err => {
            this.$message({
              type: 'error',
              message: err
            })
          })
      }
    },
    statusChange() {
      this.model.status === 1 ? (this.model.status = 0) : (this.model.status = 1)
    },
    async create() {
      const list = []
      for (let index = 0; index < this.category.length; index++) {
        if (this.model.categorys.indexOf(this.category[index].id) !== -1) {
          list.push(this.category[index])
        }
      }
      this.model.categorysList = list
      this.model.image_name = this.image_name
      const res = await this.$http.post('/api/articles/create_article/', this.model)
      if (res.data.code === 200) {
        // 创建成功
        this.$message({
          type: 'success',
          message: res.data.msg
        })
        this.$router.push('/home/article_list/')
      } else if (res.data.code === 500) {
        this.$message({
          type: 'error',
          message: res.data.msg
        })
      }
    }

    // 再写一个获取所有分类的方法
  },
  components: { VueEditor }
}
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
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
