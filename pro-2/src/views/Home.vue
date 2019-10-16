<template>
  <div class="home">
    <Row type="flex">
      <Col :lg="12" :md="12" :sm="24" :xs="24">
        <Form :model="initNews" ref="newsForm" :label-width="0" :rules="newsRules">
          <FormItem prop="title">
            <Input v-model="initNews.title" placeholder="请输入新闻标题（选填）"/>
          </FormItem>
          <FormItem prop="text">
            <Input type="textarea" v-model="initNews.text" placeholder="请输入新闻正文（必填）" class="input-textarea"/>
          </FormItem>
        </Form>
      </Col>
      <Col :lg="12" :md="12" :sm="24" :xs="24">
        <Row type="flex">
          <Col class="btns" :lg="6" :md="6" :sm="24" :xs="24">
            <Row type="flex">
              <Col :lg="24" :md="24" :sm="6" :xs="12">
                <Tooltip placement="top" content="TextRank">
                  <Button type="primary" ghost class="btn oneline" :disabled="flags.indexOf(loadingText) !== -1 && flags.indexOf(loadingText) !== 0" :loading="loadingText === 'text_rank'" @click="submit('text_rank')">TextRank</Button>
                </Tooltip>
              </Col>
              <Col :lg="24" :md="24" :sm="6" :xs="12">
                <Tooltip placement="top" content="NaiveSentVec">
                  <Button type="primary" ghost class="btn oneline" :disabled="flags.indexOf(loadingText) !== -1 && flags.indexOf(loadingText) !== 1" :loading="loadingText === 'naive_sent_vec'" @click="submit('naive_sent_vec')">NaiveSentVec</Button>
                </Tooltip>
              </Col>
              <Col :lg="24" :md="24" :sm="6" :xs="12">
                <Tooltip placement="top" content="Word2Vec+WR">
                  <Button type="primary" ghost class="btn oneline" :disabled="flags.indexOf(loadingText) !== -1 && flags.indexOf(loadingText) !== 2" :loading="loadingText === 'w2v_wr'" @click="submit('w2v_wr')">Word2Vec+WR</Button>
                </Tooltip>
              </Col>
              <Col :lg="24" :md="24" :sm="6" :xs="12">
                <Tooltip placement="top" content="LDA">
                  <Button type="primary" ghost class="btn oneline" :disabled="flags.indexOf(loadingText) !== -1 && flags.indexOf(loadingText) !== 3" :loading="loadingText === 'lda'" @click="submit('lda')">LDA</Button>
                </Tooltip>
              </Col>
            </Row>
          </Col>
          <Col :lg="18" :md="18" :sm="24" :xs="24">
            <h4 class="head">{{summaryHead}}</h4>
            <div class="cont" v-if="summary">
              {{summary}}
            </div>
            <div class="cont" v-else>
              结果为空
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
      newsRules: {
        text: [
          {
            required: true, trigger: 'blur', type: 'string', message: '请输入新闻正文'
          }
        ]
      },
      initNews: {},
      loadingText: '',
      flags: ['text_rank', 'naive_sent_vec', 'w2v_wr', 'lda'],
      summaryHead: '',
      summary: '请在左侧输入新闻正文，并选择相应方法按钮进行自动摘要提取。'
    }
  },
  mounted () {

  },
  methods: {
    submit (flag) {
      console.log(flag)
      // 此处请求，提交initNewsHead和initNews，得到summaryHead和summary
      this.$refs['newsForm'].validate((valid) => {
        if (valid) {
          let postForm = {
            text: this.initNews.text,
            title: this.initNews.title ? this.initNews.title : '',
            type: flag
          }
          this.loadingText = flag
          this.$axios.post('/summary', postForm).then(res => {
            console.log(res)
            this.loadingText = ''
            this.summaryHead = this.initNews.title ? this.initNews.title : ''
            this.summary = res.data
          }).catch(e => {
            console.log(e)
            this.summaryHead = ''
            this.summary = '自动摘要未生成或请求超时'
            this.loadingText = ''
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
.btn {
  width: 80%;
  display: block;
  margin: 0 auto;
  padding: 0;
  height: 35px;
  line-height: 35px;
}
.oneline {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.head {
  text-align: center;
  margin-bottom: 10px;
}
@media (min-width: 768px){
  .ivu-col-span-lg-24 {
    margin-top: -10px;
  }
}
</style>
