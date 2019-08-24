<template>
<div>
  <div class="search content">
    <div class="left"></div>
    <div class="right">
    <Spin size="large" v-if="spinRightShow"></Spin>
      <p v-if="(initData.nodes && initData.nodes.length === 0) || initData.nodes === undefined" class="tip">点击左侧点出现点的具体信息, 没有出现力导图则请输入适当关键词进行搜索</p>
      <div class="tag-wrap">
        <div class ="tags hidden">
          <Tag class="tag" v-if="keyClicked"></Tag>{{currentLabelIndex}}
          <Tag
            class="tag"
            v-for="(item, index) in groupClicked"
            :key="index"
            :class="item"
            :name="item"
            :checkable="index !== currentLabelIndex"
            :checked="index === currentLabelIndex"
            @on-change="changeLabelIndex">
            <span :class="{current: index === currentLabelIndex}">{{labelsObj[item]}}</span>
          </Tag>
          <Button type="primary" ghost class="more" @click="moreNews">更多新闻</Button>
        </div>
      </div>
      <div v-if="newsList.length > 0">
        <div v-for="(item, index) in newsList" :key="index" class="card">
          <Card v-if="index < 2">
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
        </div>
      </div>
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
      <Button type="primary" @click="okModal">确定</Button>
    </div>
  </Modal>
  <Spin size="large" fix v-if="spinShow"></Spin>
</div>
</template>

<script>
import * as d3 from 'd3'
export default {
  name: 'search',
  data () {
    return {
      initData: [],
      nodesObj: {},
      height: 600,
      width: 600,
      spinShow: false,
      newsList: [],
      keyClicked: '',
      groupClicked: '',
      spinRightShow: false,
      moreContentModal: {},
      currentGroupList: [],
      objRect: {},
      initGroupList: [],
      groupOfKeyWord: [],
      currentLabelIndex: 0,
      init: 0
    }
  },
  mounted () {
    if (this.$route.query.key) {
      this.spinShow = true
      this.$emit('on-get-search-key')
      this.getConnectedWords(this.$route.query.key)
    } else {
      this.$emit('on-clear-search-key')
      this.$Message.info('请在搜索框输入关键词进行搜索')
    }
  },
  methods: {
    getConnectedWords (keyword) {
      this.$axios.get(`/getNodesByKeyword?keyword=${keyword}`).then(res => {
        this.initData = res.data
        let objRect = {}
        res.data.nodes.forEach((d, index) => {
          d.group.forEach((i, idx) => {
            if (!objRect.hasOwnProperty(i)) {
              objRect[i] = 1
            }
          })
        })
        let rectNodes = Object.keys(objRect)
        this.currentGroupList = rectNodes.concat([])
        this.drawInit(res.data)
        res.data.nodes.forEach((item, index) => {
          this.nodesObj[item.id] = item
        })
      })
    },
    changeLabelIndex (checked, name) {
      this.currentLabelIndex = this.groupClicked.indexOf(name)
      this.getDetail(this.$route.query.key, this.groupClicked)
    },
    getDetail (keyword, label) {
      this.spinRightShow = true
      this.keyClicked = keyword
      let index = label.indexOf('other')
      if (index !== -1) {
        label.splice(index, 1)
        this.groupClicked = label.concat(['other']) // 把其他放到最后面
      } else {
        this.groupClicked = label.concat([])
      }
      if (this.groupClicked.indexOf(this.$route.query.label) !== -1 && this.init === 0) {
        this.currentLabelIndex = this.groupClicked.indexOf(this.$route.query.label)
        this.init++
      }
      this.$axios.get(`/getInfoByKeyword?keyword=${keyword.toLowerCase()}&label=${this.groupClicked[this.currentLabelIndex]}&page_size=2&page_index=1`).then(res => {
        this.newsList = res.data.data
        this.spinRightShow = false
      })
    },
    getOpinion (opinions) {
      return opinions.filter((item, index) => {
        return item[2] && item[2].length >= 4
      })
    },
    moreNews () {
      this.$router.push({
        path: '/newsList',
        query: {
          key: this.keyClicked,
          label: this.groupClicked[this.currentLabelIndex]
        }
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
    getLabels (labels) {
      let res = labels.map((item, index) => {
        return this.labelsObj[item]
      })
      return res.join(',')
    },
    getInitData () {
      this.initData.nodes.forEach((d, index) => {
        d.group.forEach((i, idx) => {
          if (!this.objRect.hasOwnProperty(i)) {
            this.objRect[i] = 1
          }
        })
      })
      let rectNodes = Object.keys(this.objRect)
      this.currentGroupList = rectNodes.concat([])
      this.initGroupList = rectNodes.concat([])
    },
    drawInit (data) {
      this.getInitData()
      this.draw(data, true)
      this.drawRect(data)
    },
    drag (simulation) {
      function dragstarted (d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart()
        d.fx = d.x
        d.fy = d.y
      }
      function dragged (d) {
        d.fx = d3.event.x
        d.fy = d3.event.y
      }
      function dragended (d) {
        if (!d3.event.active) simulation.alphaTarget(0)
        d.fx = null
        d.fy = null
      }
      return d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended)
    },
    draw (data, first) {
      this.spinShow = true
      let links = data.links
      let nodes = data.nodes
      let _self_ = this
      const simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id))
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      let svg
      if (first) {
        svg = d3.select('.left').append('svg')
      } else {
        svg = d3.select('svg')
      }
      svg.attr('viewBox', [0, 0, this.width, this.height])
      const link = svg.append('g')
        .attr('class', 'links')
        .attr('stroke', '#999')
        .attr('stroke-opacity', 0.6)
        .selectAll('line')
        .data(links)
        .join('line')
        .attr('stroke-width', d => 1) // 后续再看value怎么算
      const node = svg.append('g')
        .attr('class', 'nodes')
        .attr('stroke', '#fff')
        .attr('stroke-width', 1.5)
        .selectAll('circle')
        .data(nodes)
        .join('circle')
        .attr('r', 5)
        .attr('class', function (d, i) {
          if (d.id.toLowerCase() === _self_.$route.query.key.toLowerCase()) {
            _self_.groupOfKeyWord = d.group
            return 'keyword'
          }
        })
        .attr('fill', function (d) {
          let color = ''
          for (let i = 0; i < d.group.length; i++) {
            if (_self_.currentGroupList.indexOf(d.group[i]) !== -1) {
              color = d.group[i]
              break
            }
          }
          return _self_.scale[color]
        })
        .on('click', function (d) {
          _self_.getDetail(d.id, d.group)
        })
        .call(this.drag(simulation))
      node.append('title')
        .text(d => d.id)
      simulation.on('tick', () => {
        link
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y)
        node
          .attr('cx', d => d.x)
          .attr('cy', d => d.y)
      })
      this.spinShow = false
      if (this.groupOfKeyWord.length > 0) {
        this.getDetail(this.$route.query.key, this.groupOfKeyWord)
      }
    },
    redraw (rectNodes, objRect) {
      let currentNodes = rectNodes.filter((item, index) => {
        return objRect[item] === 1
      })
      this.currentGroupList = currentNodes.concat([])
      let data = this.initData.nodes.filter((item, index) => {
        let groupCurrent = item.group.filter((i, idx) => {
          return currentNodes.indexOf(i) !== -1
        })
        return groupCurrent.length > 0
      })
      let links = this.initData.links.filter((item, index) => {
        let sourceGroup = this.nodesObj[item.source.id].group.filter((i, idx) => {
          return currentNodes.indexOf(i) !== -1
        })
        let targetGroup = this.nodesObj[item.target.id].group.filter((i, idx) => {
          return currentNodes.indexOf(i) !== -1
        })
        return sourceGroup.length > 0 && targetGroup.length > 0
      })
      d3.select('.links').remove()
      d3.select('.nodes').remove()
      d3.select('.labels').remove()
      this.draw({ links: links, nodes: data })
      this.drawRect({ nodes: data })
    },
    drawRect (data) {
      let _self_ = this
      const svg = d3.select('svg')

      svg.append('g')
        .attr('class', 'labels')
        .attr('stroke', '#fff')
        .attr('stroke-width', 1.5)
        .selectAll('g')
        .data(_self_.initGroupList)
        .join('g')
        .attr('transform', function (d, i) {
          return `translate(${10}, ${i * 30})`
        })
        .style('cursor', 'pointer')
        .on('click', function (d, i) {
          if (_self_.objRect[d] === 1) { // 此时为选中状态
            _self_.objRect[d] = -1
            _self_.redraw(_self_.initGroupList, _self_.objRect)
          } else {
            _self_.objRect[d] = 1
            _self_.redraw(_self_.initGroupList, _self_.objRect)
          }
        })

      svg
        .select('.labels')
        .selectAll('g')
        .append('rect')
        .attr('width', 30)
        .attr('height', 15)
        .attr('rx', 3)
        .attr('ry', 3)
        .attr('fill', function (d) {
          if (_self_.objRect[d] === 1) {
            return _self_.scale[d]
          } else {
            return '#ddd'
          }
        })

      svg.select('.labels')
        .selectAll('g')
        .append('text')
        .text(function (d) {
          return _self_.labelsObj[d]
        })
        .attr('stroke-width', 0)
        .style('font-size', function (d) {
          return `${10}px`
        })
        .style('background', 'transparent')
        .style('fill', function (d) {
          if (_self_.objRect[d] === 1) {
            return '#fff'
          } else {
            return '#333'
          }
        })
        .style('font-family', 'Impact')
        .attr('text-anchor', 'middle')
        .attr('transform', `translate(${15}, ${11})`)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.content {
  display: flex;
}
.left {
  width: 50%
}
.left >>> circle.keyword {
  fill: #2d8cf0;
  stroke: #2d8cf0;
  stroke-width: 20px;
  animation: keyword 1s ease infinite;
}
.right {
  width: 50%;
  overflow: visible;
  word-break: break-word;
  position: relative;
}
.tip {
  text-align: center;
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate3d(-50%, -50%, 0);
}
.tags {
  margin-bottom: 10px
}
.tag.civilization>>>span {
  color: #ff7f0e;
}
.tag.economy>>>span {
  color: #2ca02c;
}
.tag.education>>>span {
  color: #d62728;
}
.tag.military>>>span {
  color: #9467bd;
}
.tag.polity>>>span {
  color: #1f77b4;
}
.tag.society>>>span {
  color: #e377c2;
}
.tag.sports>>>span {
  color: #7f7f7f;
}
.tag.other>>>span {
  color: #bcbd22;
}
.tag.ivu-tag-checked.civilization {
  background: #ff7f0e !important;
}
.tag.ivu-tag-checked.economy {
  background: #2ca02c !important;
}
.tag.ivu-tag-checked.education {
  background: #d62728 !important;
}
.tag.ivu-tag-checked.military {
  background: #9467bd !important;
}
.tag.ivu-tag-checked.polity {
  background: #1f77b4 !important;
}
.tag.ivu-tag-checked.society {
  background: #e377c2 !important;
}
.tag.ivu-tag-checked.sports {
  background: #7f7f7f !important;
}
.tag.ivu-tag-checked.other {
  background: #bcbd22 !important;
}
.tag.ivu-tag-checked span {
  color: #ffffff !important;
}
.search >>> .ivu-tag:not(.ivu-tag-border):not(.ivu-tag-dot):not(.ivu-tag-checked) {
  border: 1px solid #e8eaec;
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
.right>>>.ivu-card-head p span {
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
.right >>>.ivu-spin {
    width: 100%;
    height: 100%;
    position: absolute;
    background: #fff;
    display: flex;
    z-index: 20;
    justify-content: center;
    padding-top: 200px;
}
@keyframes keyword {
  0% {
    stroke-width: 10px;
  }
  50% {
    stroke-width: 20px;
  }
  100% {
    stroke-width: 10px;
  }
}
</style>
