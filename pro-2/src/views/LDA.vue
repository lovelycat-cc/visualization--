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
                <Tooltip placement="top" content="LDA">
                  <Button type="primary" ghost class="btn oneline" :loading="loadingText === 'lda'" @click="submit('lda')">LDA</Button>
                </Tooltip>
              </Col>
              <Col :lg="24" :md="24" :sm="6" :xs="12">
                <Tooltip placement="top" content="Word2Vec+WR">
                  <router-link to="/"><Button type="primary" ghost class="btn oneline" :disabled="flags.indexOf(loadingText) !== -1">更多</Button></router-link>
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
    <Modal
        v-model="tipModal.show"
        title="帮助文档"
        @on-ok="okModal"
        :scollable="true"
        @on-cancel="cancelModal">
        <p>LDA方法比较慢，请耐心等待！等待过程请谨慎刷新，刷新可能会影响服务端运行。</p>
        <p v-if="loadingText === 'lda'">程序正在运行中，请等待…</p>
        <div slot="footer">
          <Button type="primary" :loading="loadingText === 'lda'" @click="okModal">确定</Button>
        </div>
    </Modal>
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
      flags: ['lda'],
      summaryHead: '',
      summary: '请在左侧输入新闻正文，并选择相应方法按钮进行自动摘要提取。',
      tipModal: {
        show: false
      }
    }
  },
  mounted () {

  },
  methods: {
    okModal () {
      let postForm = {
        text: this.initNews.text,
        title: this.initNews.title ? this.initNews.title : '',
        type: 'lda'
      }
      sessionStorage.setItem('loading', 'true')
      this.loadingText = 'lda'
      // eslint-disable-next-line
      this.$axios.post(`${LDA_URL}/summary`, postForm).then(res => {
        sessionStorage.setItem('loading', '')
        this.loadingText = ''
        this.summaryHead = this.initNews.title ? this.initNews.title : ''
        this.summary = res.data
        this.tipModal.show = false
      }).catch(e => {
        console.log(e)
        sessionStorage.setItem('loading', '')
        this.summaryHead = ''
        this.summary = '自动摘要未生成'
        this.loadingText = ''
      })
    },
    cancelModal () {
      this.tipModal.show = false
    },
    submit (flag) {
      // 此处请求，提交initNewsHead和initNews，得到summaryHead和summary
      this.$refs['newsForm'].validate((valid) => {
        if (valid) {
          this.tipModal.show = true
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
