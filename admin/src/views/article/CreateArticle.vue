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
        <el-button @click="changeEditorTheme()" type="text">切换编辑器风格,当前配置为:{{ editorOption.theme }}。</el-button>

        <quill-editor :key="editorOption.theme" ref="myQuillEditor" v-model="model.body" :options="editorOption" />
        <el-upload v-show="false" drag multiple :headers="getAuthHeaders()" class="quill-upload" :on-success="quillSuccess" action="http://127.0.0.1:8000/api/articles/image_upload/">
          <i class="el-icon-upload"></i>
        </el-upload>
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
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import { quillEditor } from 'vue-quill-editor'

export default {
  components: {
    quillEditor
  },
  props: {
    id: {}
  },
  data() {
    return {
      editorOption: {
        // 编辑器配置
        placeholder: '请在这里写点什么吧！',
        theme: localStorage.EditorTheme ? localStorage.EditorTheme : 'snow',
        modules: {
          toolbar: {
            container: [['blockquote', 'code-block', 'clean', 'video', 'image', { header: 1 }, { header: 2 }, { color: [] }]],
            handlers: {
              image: function (value) {
                document.querySelector('.quill-upload .el-icon-upload').click()
              }
            }
          }
        }
      },
      category: [],
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
    // 切换富文本编辑器的风格
    changeEditorTheme() {
      if (this.editorOption.theme === 'bubble') {
        this.editorOption.theme = 'snow'
        localStorage.EditorTheme = 'snow'
      } else {
        this.editorOption.theme = 'bubble'
        localStorage.EditorTheme = 'bubble'
      }
    },
    // 监听富文本编辑器的图片粘贴事件
    init() {
      const quill = this.$refs.myQuillEditor.quill
      quill.root.addEventListener(
        'paste',
        evt => {
          if (evt.clipboardData && evt.clipboardData.files && evt.clipboardData.files.length) {
            evt.preventDefault()
            ;[].forEach.call(evt.clipboardData.files, file => {
              if (!file.type.match(/^image\/(gif|jpe?g|a?png|bmp)/i)) {
                return this.$message.error('格式错误')
              }
              this.uploadToServer(file)
            })
          }
        },
        false
      )
    },

    // 富文本编辑器粘贴图片为上传到服务器
    uploadToServer(file) {
      const fm = new FormData()
      fm.append('file', file)
      this.$http
        .post('/api/articles/image_upload/', fm)
        .then(res => {
          if (res.data.code === 200) {
            const quill = this.$refs.myQuillEditor.quill
            const pos = quill.getSelection().index
            // 插入图片到光标位置
            quill.insertEmbed(pos, 'image', '/uploads/' + res.data.filename)
          } else {
            this.$message({
              type: 'error',
              message: res.data.msg
            })
          }
        })
        .catch(err => {
          this.$message({
            type: 'error',
            message: err
          })
        })
    },

    // 富文本编辑器上传图片的方法(不是粘贴图片)
    quillSuccess(res) {
      if (res) {
        // 获取文本编辑器
        const quill = this.$refs.myQuillEditor.quill
        // 获取光标位置
        const pos = quill.getSelection().index
        // 插入图片到光标位置
        quill.insertEmbed(pos, 'image', '/uploads/' + res.filename)
      } else {
        this.$essage.error('图片插入失败')
      }
    },

    // 成功上传封面执行的方法 封面传给后端后 后端返回给我文件名 然后我在复制给表单 路径+文件名 在一起传送给数据库
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
    // 改变状态
    statusChange() {
      this.model.status === 1 ? (this.model.status = 0) : (this.model.status = 1)
    },
    // 发布文章
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
    },

    // 再写一个获取所有分类的方法
    fetchCategorys() {
      this.$http
        .get('api/category/')
        .then(res => {
          this.category = res.data
        })
        .catch(err => {
          this.$message({
            type: 'error',
            message: err
          })
        })
    }
  },
  mounted() {
    this.init()
  },
  created() {
    this.fetchCategorys()
  }
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
.quill-editor .ql-container {
  height: 500px;
}
body .el-table::before {
  z-index: inherit;
}
.quill-editor {
  line-height: normal;
}
</style>
