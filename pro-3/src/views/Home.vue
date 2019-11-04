<template>
  <div class="home">
    <Row type="flex">
      <Col :lg="12" :md="12" :sm="24" :xs="24">
        <Form :model="initComments" ref="commentsForm" :label-width="0" :rules="commentsRules">
          <FormItem prop="text">
            <Input type="textarea" v-model="initComments.text" placeholder="请输入待分析的文本（必填）" class="input-textarea"/>
          </FormItem>
        </Form>
      </Col>
      <Col :lg="12" :md="12" :sm="24" :xs="24">
        <Row type="flex" class="right">
          <Col class="btns" :lg="6" :md="6" :sm="24" :xs="24">
            <div class="btn">
              <Button type="primary" @click="submit" ghost :loading="isLoading">情感分析</Button>
            </div>
          </Col>
          <Col :lg="18" :md="18" :sm="24" :xs="24">
            <div class="comments" v-if="comments.good.length > 0 || comments.bad.length > 0 || comments.middle.length > 0">
              <div class="comment">
                <h4 class="head"><img class="comment-icon" src="../assets/good.png"/></h4>
                <div class="cont">
                  <Tag v-for="(item, index) in comments.good" :key="index" :color="getColor(item.type)">{{item.comment}}</Tag>
                </div>
              </div>
              <div class="comment">
                <h4 class="head"><img class="comment-icon" src="../assets/middle.png"/></h4>
                <div class="cont">
                  <Tag v-for="(item, index) in comments.middle" :key="index" :color="getColor(item.type)">{{item.comment}}</Tag>
                </div>
              </div>
              <div class="comment">
                <h4 class="head"><img class="comment-icon" src="../assets/bad.png"/></h4>
                <div class="cont">
                  <Tag v-for="(item, index) in comments.bad" :key="index" :color="getColor(item.type)">{{item.comment}}</Tag>
                </div>
              </div>
            </div>
            <div class="comments-center" v-else>
              <span class="null-comment">请在左侧输入待分析文本并按情感分析按钮进行相应分析</span>
            </div>
          </Col>
        </Row>
      </Col>
    </Row>
  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      commentsRules: {
        text: [
          {
            required: true, trigger: 'blur', type: 'string', message: '请输入待分析文本'
          }
        ]
      },
      initComments: {},
      isLoading: false,
      comments: {
        good: [],
        bad: [],
        middle: []
      }
    }
  },
  mounted () {

  },
  methods: {
    getColor (flag) {
      switch (flag) {
        case 0:
          return 'red'
        case 1:
          return 'yellow'
        case 2:
          return 'lime'
        case 3:
          return 'green'
        case 4:
          return 'blue'
        case 5:
          return 'purple'
      }
    },
    submit () {
      // 此处请求，提交initCommentsHead和initComments，得到summaryHead和summary
      this.$refs['commentsForm'].validate((valid) => {
        if (valid) {
          let postForm = {
            text: this.initComments.text
          }
          this.isLoading = true
          this.$axios.post('/comments', postForm).then(res => {
            this.isLoading = false
            this.comments = {...this.comments, ...res.data}
          }).catch(e => {
            console.log(e)
            this.isLoading = false
            this.comments = {
              good: [],
              bad: [],
              middle: []
            }
          })
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.input-textarea >>> textarea{
  min-height: 400px;
  margin-top: 10px;
}
.home >>> .ivu-tooltip {
  width: 100%;
  margin-top: 10px;
  margin-bottom: 10px;
}
.right {
  height: 100%;
}
.btn {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  height: 100%
}
.oneline {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.comments {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.comment-icon {
  vertical-align: middle;
  height: 30px;
  width: auto;
}
.comments-center {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.comment {
  border-top: #999999 dashed 1px;
}
.comments .comment:first-child {
  border-top: none;
}
.comments .comment-icon {
  margin-top: 10px;
}
.comments .comment:first-child .comment-icon {
  margin-top: 0;
}
.null-comment {
  color: #999999;
}
.head {
  /* text-align: center; */
  margin-bottom: 10px;
}
.cont {
  /* text-align: center; */
  margin-bottom: 20px;
}
@media (min-width: 768px){
  .ivu-col-span-lg-24 {
    margin-top: -10px;
  }
}
</style>
