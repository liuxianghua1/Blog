<template>
  <v-card class="mx-auto">
    <v-card dark flat>
      <v-card-title class="pa-2 blue lighten-3">
        <h3 class="text-h6 font-weight text-center grow">网站归档</h3>
      </v-card-title>
      <v-img src="http://rjrujxhu3.bkt.clouddn.com/FrAcmcr-lBOUpXrw0iMifAQE43VR">
        <v-container class="fill-height">
          <v-row align="center">
            <strong class="text-h4 font-weight-regular mr-6">台湾新竹鸳鸯湖</strong>
            <v-row justify="end">
              <div class="text-h5 font-weight-light">摄于22年7月22日 我觉得我拍的最好的照片。<br />没有之一</div>
            </v-row>
          </v-row>
        </v-container>
      </v-img>
    </v-card>
    <v-card-text class="py-0">
      <v-timeline align-top dense>
        <v-timeline-item v-for="i in data" :key="i.id" color="grey" small>
          <v-row class="pt-1">
            <v-col cols="3">
              <strong>{{ i.createtime }}</strong>
            </v-col>
            <v-col>
              <strong class="a_hover" style="cursor: pointer" @click="$router.push(`/article/${i.id}`)">{{ i.title }}</strong>
            </v-col>
          </v-row>
        </v-timeline-item>

        <!-- <v-timeline-item color="grey" small>
          <v-row class="pt-1">
            <v-col cols="3">
              <strong>2022年10月13日</strong>
            </v-col>
            <v-col>
              <strong>我的一个标题i</strong>
            </v-col>
          </v-row>
        </v-timeline-item> -->
      </v-timeline>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      data: []
    }
  },
  methods: {
    async fetch() {
      this.$http
        .get('api/archiving/')
        .then(res => {
          this.data = res.data
        })
        .catch(err => {
          // this.$router.push('/home')
          console.log(err)
        })
    }
  },
  created() {
    this.fetch()
  }
}
</script>

<style>
.col .a_hover:hover {
  text-decoration: underline;
}
</style>
