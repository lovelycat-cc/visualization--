<template>
<div>
  <div class="search content">
    <div class="left"></div>
    <div class="right">
    <Spin size="large" v-if="spinRightShow"></Spin>
      <p v-if="newsList.length === 0" class="tip">点击左侧点出现点的具体信息</p>
      <div v-if="newsList.length > 0">
        <div class ="tags hidden">
          <Tag class="tag" :class="groupClicked">{{keyClicked}}</Tag>
          <Tag class="tag" :class="groupClicked">{{labelsObj[groupClicked]}}</Tag>
          <span class="more">>>更多文章</span>
        </div>
        <div v-for="(item, index) in newsList" :key="index" class="card">
          <Card v-if="index < 2">
            <p slot="title">{{ item.title}}</p>
            <p class="author">{{item.source}}  {{item.author}}</p>
            <p v-for="(i,idx) in getOpinion(item.opinion)" :key="idx">
              <Alert v-if="idx < 4">{{i[0]}}: {{i[2]}}</Alert>
            </p>
            <p v-if="getOpinion(item.opinion).length === 0">
              <Alert type="warning">暂无观点内容</Alert>
            </p>
            <p class="hidden">
              <span class="more" @click="showMoreContent(item)">>>更多内容</span>
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
      moreContentModal: {}
    }
  },
  mounted () {
    if (this.$route.query.key) {
      this.spinShow = true
      this.getConnectedWords(this.$route.query.key)
    } else {
      this.$Message.info('请在搜索框输入关键词进行搜索')
    }
  },
  methods: {
    getConnectedWords (keyword) {
      this.$axios.get(`http://localhost:31000/getNodesByKeyword?keyword=${keyword}`).then(res => {
        this.initData = res.data
        this.drawInit(res.data)
        res.data.nodes.forEach((item, index) => {
          this.nodesObj[item.id] = item
        })
      })
    },
    getDetail (keyword, label) {
      this.spinRightShow = true
      this.keyClicked = keyword
      this.groupClicked = label
      this.$axios.get(`http://localhost:31000/getInfoByKeyword?keyword=${keyword}&label=${label}`).then(res => {
        this.newsList = res.data
        this.spinRightShow = false
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
      this.$set(this.moreContentModal, 'content', item.content.replace(/\\n/g, '<br>'))
    },
    okModal () {
      this.moreContentModal = {}
      this.$set(this.moreContentModal, 'show', false)
    },
    cancelModal () {
      this.moreContentModal = {}
      this.$set(this.moreContentModal, 'show', false)
    },
    drawInit (data) {
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
        .attr('fill', function (d) {
          return _self_.scale[d.group]
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
    },
    drawRect (data) {
      let _self_ = this
      let objRect = {}

      const rectNodes = data.nodes.map((d, index) => {
        if (objRect.hasOwnProperty(d.group)) {
          return -1
        } else {
          objRect[d.group] = 1
          return d.group
        }
      }).filter((value) => value !== -1)

      const svg = d3.select('svg')

      svg.append('g')
        .attr('class', 'labels')
        .attr('stroke', '#fff')
        .attr('stroke-width', 1.5)
        .selectAll('g')
        .data(rectNodes)
        .join('g')
        .attr('transform', function (d, i) {
          return `translate(${10}, ${i * 30})`
        })
        .style('cursor', 'pointer')
        .on('click', function (d, i) {
          if (objRect[d] === 1) { // 此时为选中状态
            d3.select(this).select('rect').style('fill', '#ddd')
            d3.select(this).select('text').style('fill', '#333')
            objRect[d] = -1
            let currentNodes = rectNodes.filter((item, index) => {
              return objRect[item] === 1
            })
            let data = _self_.initData.nodes.filter((item, index) => {
              return currentNodes.indexOf(item.group) !== -1
            })
            let links = _self_.initData.links.filter((item, index) => {
              return currentNodes.indexOf(_self_.nodesObj[item.source.id].group) !== -1 && currentNodes.indexOf(_self_.nodesObj[item.target.id].group) !== -1
            })

            d3.select('.links').remove()
            d3.select('.nodes').remove()

            _self_.draw({ links: links, nodes: data })
          } else {
            objRect[d] = 1
            d3.select(this).select('rect').style('fill', _self_.scale[d])
            d3.select(this).select('text').style('fill', '#fff')
            let currentNodes = rectNodes.filter((item, index) => {
              return objRect[item] === 1
            })
            let data = _self_.initData.nodes.filter((item, index) => {
              return currentNodes.indexOf(item.group) !== -1
            })
            let links = _self_.initData.links.filter((item, index) => {
              return currentNodes.indexOf(_self_.nodesObj[item.source.id].group) !== -1 && currentNodes.indexOf(_self_.nodesObj[item.target.id].group) !== -1
            })
            d3.select('.links').remove()
            d3.select('.nodes').remove()
            _self_.draw({ links: links, nodes: data })
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
          return _self_.scale[d]
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
        .style('fill', '#fff')
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
.right {
  width: 50%;
  overflow: visible;
  word-break: break-word;
  position: relative;
}
.tip {
  text-align: center;
}
.tags {
  margin-bottom: 10px
}
.tag.civilization>>>span {
  color: #ff7f0e !important;
}
.tag.economy>>>span {
  color: #2ca02c !important;
}
.tag.education>>>span {
  color: #d62728 !important;
}
.tag.military>>>span {
  color: #9467bd !important;
}
.tag.polity>>>span {
  color: #1f77b4 !important;
}
.tag.society>>>span {
  color: #e377c2 !important;
}
.tag.sports>>>span {
  color: #7f7f7f !important;
}
.tag.other>>>span {
  color: #bcbd22 !important;
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
</style>
