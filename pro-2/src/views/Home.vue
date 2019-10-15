<template>
  <div class="home">
    <Row type="flex">
      <Col :lg="12" :md="12" :sm="24" :xs="24">
        <Input v-model="initNewsHead" placeholder="请输入新闻标题"/>
        <Input type="textarea" v-model="initNews" placeholder="请输入新闻原文" class="input-textarea"/>
      </Col>
      <Col :lg="12" :md="12" :sm="24" :xs="24">
        <Row type="flex">
          <Col class="btns" :lg="6" :md="6" :sm="24" :xs="24">
            <Row type="flex">
              <Col :lg="24" :md="24" :sm="6" :xs="12">
                <Button type="primary" ghost class="btn" text="textrank">textrank</Button>
              </Col>
              <Col :lg="24" :md="24" :sm="6" :xs="12">
                <Button type="primary" ghost class="btn" text="textrank">textrank</Button>
              </Col>
              <Col :lg="24" :md="24" :sm="6" :xs="12">
                <Button type="primary" ghost class="btn" text="textrank">textrank</Button>
              </Col>
              <Col :lg="24" :md="24" :sm="6" :xs="12">
                <Button type="primary" ghost class="btn" text="textrank">textrank</Button>
              </Col>
            </Row>
          </Col>
          <Col :lg="18" :md="18" :sm="24" :xs="24">
            <h4 class="head">{{reviewHead}}</h4>
            <div class="cont">
              {{review}}
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
      initNewsHead: '',
      initNews: '',
      reviewHead: '我是标题我是标题',
      review: '我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要我是摘要'
    }
  },
  mounted () {

  },
  methods: {

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.input-textarea >>> textarea{
  min-height: 400px;
  margin-top: 10px;
}
.btn {
  width: 80%;
  display: block;
  margin: 10px auto;
  padding: 0;
  height: 35px;
  line-height: 35px;
}
.head {
  text-align: center;
  margin-bottom: 10px;
}
@media (min-width: 992px){
  .ivu-col-span-lg-24 {
    margin-top: -10px;
  }
}
</style>
