<template>
<div>
  <div class="search content">
    <div class="left"></div>
    <div class="right">点击左侧点出现点的具体信息</div>
  </div>
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
      spinShow: false
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
          document.querySelector('.right').innerHTML = `<span style='color: ${_self_.scale[d.group]}'>[${d.group}][${d.index}-${d.id}]${JSON.stringify(d)}</span>`
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
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
