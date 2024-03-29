<template>
  <div>
    <!-- 表头区域 -->
    <el-page-header @back="$router.go(-1)" :content="id ? '修改文章' : '发布文章'" style="margin-bottom: 50px"></el-page-header>
    <el-form style="height: 100%" label-width="120px" @submit.native.prevent="create">
      <el-form-item label="标题">
        <el-input v-model="model.title"></el-input>
      </el-form-item>

      <el-form-item label="封面">
        <el-upload action="http://upload-cn-east-2.qiniup.com" class="avatar-uploader" :auto-upload="true" :on-success="afterUpload" :before-upload="beforeUpload" :data="upload_data" ref="upload" accept="image/jpeg,image/png,image/jpg" :show-file-list="false">
          <img v-if="model.image_url" :src="model.image_url" class="avatar" />
          <i v-else style="line-height: 178px" class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
        <el-button icon="el-icon-delete" @click="deleteImage()" type="text">删除封面</el-button>
      </el-form-item>

      <!-- 富文本编辑器 -->
      <el-form-item label="正文">
        <el-button @click="changeEditorTheme()" type="text">切换编辑器风格,当前配置为:{{ editorOption.theme }}。</el-button>

        <quill-editor :key="editorOption.theme" ref="myQuillEditor" v-model="model.body" :options="editorOption" />
        <el-upload v-show="false" :before-upload="beforeUpload" drag multiple :data="upload_data" class="quill-upload" :on-success="quillSuccess" :on-error="quillError" action="http://upload-cn-east-2.qiniup.com">
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
    const toolbarOptions = [
      ['bold', 'italic', 'underline', 'strike'], // 加粗，斜体，下划线，删除线
      ['blockquote', 'code-block'], // 引用，代码块
      [{ header: 1 }, { header: 2 }], // 标题，键值对的形式；1、2表示字体大小
      [{ list: 'ordered' }, { list: 'bullet' }], // 列表
      [{ script: 'sub' }, { script: 'super' }], // 上下标
      [{ indent: '-1' }, { indent: '+1' }], // 缩进
      [{ direction: 'rtl' }], // 文本方向
      [{ size: ['small', false, 'large', 'huge'] }], // 字体大小
      [{ header: [1, 2, 3, 4, 5, 6, false] }], // 几级标题
      [{ color: [] }, { background: [] }], // 字体颜色，字体背景颜色
      [{ font: [] }], // 字体
      [{ align: [] }], // 对齐方式
      ['clean'], // 清除字体样式
      ['link', 'image', 'video'] // 上传图片、上传视频
    ]
    return {
      editorOption: {
        // 编辑器配置
        placeholder: '请在这里写点什么吧！',
        theme: localStorage.EditorTheme ? localStorage.EditorTheme : 'snow',
        modules: {
          toolbar: {
            container: toolbarOptions,
            handlers: {
              image: function (value) {
                document.querySelector('.quill-upload .el-icon-upload').click()
              }
            }
          }
        }
      },
      category: [],
      upload_data: {
        token: ''
      },
      model: {
        body: '',
        title: '',
        image_url: '',
        categorys: [],
        status: 1
      },
      imgBaseUrl: 'http://rjrujxhu3.bkt.clouddn.com/'
    }
  },
  methods: {
    // 获取oss的token
    getUploadToken() {
      this.$http
        .get('/api/articles/get_token/')
        .then(res => {
          this.upload_data.token = res.data.uptoken
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 删除封面的方法
    deleteImage() {
      this.model.image_url = ''
    },
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
      fm.append('token', this.upload_data.token)
      this.$http
        .post('http://upload-cn-east-2.qiniup.com', fm)
        .then(res => {
          const quill = this.$refs.myQuillEditor.quill
          // 获取光标位置
          const pos = quill.getSelection().index
          // 插入图片到光标位置
          quill.insertEmbed(pos, 'image', this.imgBaseUrl + res.data.key)
        })
        .catch(err => {
          this.$message({
            type: 'error',
            message: err.data
          })
        })
    },

    // if (res.data.code === 200) {
    //   const quill = this.$refs.myQuillEditor.quill
    //   const pos = quill.getSelection().index
    //   // 插入图片到光标位置
    //   quill.insertEmbed(pos, 'image', '/uploads/' + res.data.filename)
    // } else {
    //   this.$message({
    //     type: 'error',
    //     message: res.data.msg
    //   })
    // }

    // 富文本上传图片失败的方法
    quillError() {
      this.$message({
        message: '上传图片类型不正确!',
        type: 'error'
      })
    },

    // 富文本编辑器上传图片的方法(不是粘贴图片)
    quillSuccess(res) {
      // 获取文本编辑器
      const quill = this.$refs.myQuillEditor.quill
      // 获取光标位置
      const pos = quill.getSelection().index
      // 插入图片到光标位置
      quill.insertEmbed(pos, 'image', this.imgBaseUrl + res.key)
    },

    // 成功上传封面执行的方法 封面传给后端后 后端返回给我文件名 然后我在复制给表单 路径+文件名 在一起传送给数据库
    afterUpload(res) {
      this.$set(this.model, 'image_url', this.imgBaseUrl + res.key)
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
      if (this.id) {
        var res = await this.$http.put(`/api/articles/${this.id}/update_article/`, this.model)
      } else {
        res = await this.$http.post('/api/articles/create_article/', this.model)
      }
      if (res.data.code === 200) {
        // 创建成功
        this.$message({
          type: 'success',
          message: res.data.msg
        })
        this.$router.push('/admin/article_list')
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
        .get('api/categorys/')
        .then(res => {
          this.category = res.data
        })
        .catch(err => {
          this.$message({
            type: 'error',
            message: err
          })
        })
    },

    // 获取文章数据的方法
    fetchArticle() {
      this.$http
        .get(`api/articles/${this.id}/`)
        .then(res => {
          this.model = res.data
          const list = []
          res.data.categorys.forEach(elem => {
            list.push(elem.id)
          })

          this.model.categorys = list
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
    this.getUploadToken()
  },
  created() {
    this.fetchCategorys()
    this.id && this.fetchArticle()
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
