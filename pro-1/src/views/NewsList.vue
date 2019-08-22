<template>
<div>
  <div class="search content">
    <div v-if="newsList.length > 0">
      <div class ="tags hidden">
        <Tag class="tag">{{$route.query.key}}</Tag>
        <!-- <Tag class="tag" :class="groupClicked[0]">{{}}</span></Tag> -->
        <div class="btns">
          <Button type="primary" @click="prev" ghost :disabled="btnDisable">上一页</Button>
          <Button type="primary" @click="next" ghost :disabled="btnDisable">下一页</Button>
        </div>
      </div>
      <Row :gutter="20">
        <Col v-for="(item, index) in newsList" :key="index" class="card card-item" span="12">
          <Card>
            <p slot="title" class="hidden">
              {{ item.title}}
              <span class="more" @click="showMoreContent(item)">
                <span>more</span>
                <svg t="1566372115510" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1113" width="200" height="200"><path d="M512 42.666667c258.133333 0 469.333333 211.2 469.333333 469.333333s-211.2 469.333333-469.333333 469.333333S42.666667 770.133333 42.666667 512 253.866667 42.666667 512 42.666667z m0 853.333333c211.2 0 384-172.8 384-384S723.2 128 512 128 128 300.8 128 512s172.8 384 384 384z" fill="#2d8cf0" p-id="1114"></path><path d="M512 448c-36.266667 0-64 27.733333-64 64s27.733333 64 64 64 64-27.733333 64-64-27.733333-64-64-64M725.333333 448c-36.266667 0-64 27.733333-64 64s27.733333 64 64 64 64-27.733333 64-64-27.733333-64-64-64M298.666667 448c-36.266667 0-64 27.733333-64 64s27.733333 64 64 64 64-27.733333 64-64-27.733333-64-64-64" fill="#2d8cf0" p-id="1115"></path></svg>
              </span>
            </p>
            <p class="author">{{item.source}}  {{item.author}}</p>
            <p v-for="(i,idx) in getOpinion(item.opinion)" :key="idx">
              <Alert v-if="idx < 4">{{i[0]}}: {{i[2]}}</Alert>
            </p>
            <p v-if="getOpinion(item.opinion).length === 0">
              <Alert type="warning">暂无观点内容</Alert>
            </p>
          </Card>
        </Col>
      </Row>
    </div>
  </div>
  <Modal
    v-model="moreContentModal.show"
    :title="moreContentModal.title"
    @on-ok="okModal"
    :width="800"
    :scollable="true"
    class="contentModal"
    @on-cancel="cancelModal">
    <div v-html="moreContentModal.content"></div>
    <div slot="footer">
      <Button type="primary">确定</Button>
    </div>
  </Modal>
  <Spin size="large" fix v-if="spinShow"></Spin>
</div>
</template>

<script>
export default {
  name: 'news-list',
  data () {
    return {
      newsList: [],
      spinShow: false,
      btnDisable: false,
      moreContentModal: {},
      page: {
        size: 10,
        index: 1
      }
    }
  },
  mounted () {
    if (this.$route.query.key) {
      this.$emit('on-get-search-key')
      this.getDetail(this.$route.query.key, -1, this.page.index, this.page.size, 'spinShow')
    } else {
      this.$emit('on-clear-search-key')
      this.$Message.info('请在搜索框输入关键词进行搜索')
    }
  },
  methods: {
    getDetail (keyword, label, index, size, disableKey) {
      this[disableKey] = true
      this.$axios.get(`http://localhost:31000/getInfoByKeyword?keyword=${keyword}&label=${label}&page_size=${size}&page_index=${index}`).then(res => {
        this.newsList = res.data
        this[disableKey] = false
      })
    },
    getOpinion (opinions) {
      return opinions.filter((item, index) => {
        return item[2] && item[2].length >= 4
      })
    },
    showMoreContent (item) {
      this.$set(this.moreContentModal, 'show', true)
      this.$set(this.moreContentModal, 'title', item.title)
      this.$set(this.moreContentModal, 'content', item.content.trim().replace(/\\n/g, '<br>'))
    },
    okModal () {
      this.moreContentModal = {}
      this.$set(this.moreContentModal, 'show', false)
    },
    cancelModal () {
      this.moreContentModal = {}
      this.$set(this.moreContentModal, 'show', false)
    },
    prev () {
      if (this.page.index === 1) {
        this.$Message.error('没有上一页')
        return false
      }
      this.page.index--
      this.getDetail(this.$route.query.key, -1, this.page.index, this.page.size, 'btnDisable')
    },
    next () {
      this.btnDisable = true
      this.$axios.get(`http://localhost:31000/getInfoByKeyword?keyword=${this.$route.query.key}&label=${-1}&page_size=${10}&page_index=${this.page.index + 1}`).then(res => {
        this.btnDisable = false
        if (res.data.length > 0) {
          this.newsList = res.data
          this.page.index++
        } else {
          this.$Message.error('没有下一页了')
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.content {
  display: flex;
}
.tags {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
}
.author {
  text-align: right;
  padding-bottom: 10px;
}
.hidden {
  overflow: hidden;
}
.more {
  float: right;
  color: #2d8cf0;
  cursor: pointer;
}
.content>>>.ivu-card-head p span {
  vertical-align: top;
}
.more svg {
  width: 20px;
  height: 20px;
}
.card {
  margin-bottom: 15px;
}
.contentModal>>>.ivu-modal-body {
  max-height: 400px;
  overflow: auto;
}
.card-item>>>.ivu-card-bordered {
    height: 400px;
    overflow: auto;
    background-image: url('../assets/water_mark.png');
    background-position: right bottom;
    background-repeat: no-repeat;
}
</style>
