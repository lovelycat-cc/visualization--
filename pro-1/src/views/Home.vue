<template>
  <div class="home">
    <div class="tags"></div>
    <Carousel class="carousel" v-model="carousel" loop autoplay :autoplay-speed="5000">
      <CarouselItem v-for="(item, index) in groupList" :key="index">
        <div :class="`svg-${index}`" class="svg"></div>
      </CarouselItem>
    </Carousel>
    <Spin size="large" fix v-if="spinShow"></Spin>
  </div>
</template>

<script>
import * as d3 from 'd3'
import cloud from 'd3-cloud'
export default {
  name: 'home',
  data () {
    return {
      carousel: 0,
      groupList: [],
      initData: [],
      nodesObj: {},
      spinShow: true
    }
  },
  watch: {
    'carousel': {
      handler: function (val, oldVal) {
        if (val !== oldVal) {
          this.drawRect()
        }
      },
      deep: true
    }
  },
  mounted () {
    this.$emit('on-clear-search-key')
    this.$axios('http://localhost:31000/getAllInfo').then(res => {
      this.initData = res.data
      res.data.forEach((item, index) => {
        this.nodesObj[item.id] = item
      })
      let objRect = {}
      this.groupList = res.data.map((d, index) => {
        if (objRect.hasOwnProperty(d.group)) {
          return -1
        } else {
          objRect[d.group] = 1
          return d.group
        }
      }).filter((value) => value !== -1)
      this.$nextTick(() => {
        this.drawInit()
      })
    })
    // d3.json('https://gist.githubusercontent.com/mbostock/4062045/raw/5916d145c8c048a6e3086915a6be464467391c62/miserables.json').then((res) => {

    // })
  },
  methods: {
    drawInit () {
      this.drawRect()
      this.groupList.forEach((item, index) => {
        this.drawWords(item, index)
      })
    },
    drawRect () {
      d3.select('.tags').select('svg').remove()
      let svg = d3.select('.tags').append('svg')
      let _self_ = this
      svg.attr('height', 50).attr('width', `${this.groupList.length * 80}`)
      svg.append('g')
        .attr('class', 'labels')
        .attr('stroke', '#fff')
        .attr('stroke-width', 1.5)
        .selectAll('g')
        .data(_self_.groupList)
        .join('g')
        .attr('transform', function (d, i) { return `translate(${i * 70}, ${0})` })
        .style('cursor', 'pointer')
        .on('mouseenter', function (d, i) {
          if (_self_.carousel !== i) {
            _self_.carousel = i
          }
        })
      svg
        .select('.labels')
        .selectAll('g')
        .append('rect')
        .attr('width', 70)
        .attr('height', 40)
        .attr('rx', 10)
        .attr('ry', 10)
        .attr('fill', function (d, i) {
          if (i === _self_.carousel) {
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
        .attr('fill', '#333')
        .attr('stroke', '#fff')
        .attr('stroke-width', 0)
        .style('font-size', function (d) {
          return `${16}px`
        })
        .style('background', 'transparent')
        .style('color', '#333')
        .style('font-family', 'Impact')
        .attr('text-anchor', 'middle')
        .attr('transform', `translate(${35}, ${25})`)
    },
    drawWords (currentItem, currentIndex) {
      const width = 1000
      const height = 500

      let _self_ = this

      let colorWords = d3.scaleOrdinal(d3.schemeCategory10)

      let dataCurrent = this.initData.filter((item, index) => {
        return item.group === currentItem
      }).map((item, index) => {
        return {
          id: item.id,
          size: item.size
        }
      })
      let sizes = dataCurrent.map((item) => {
        return item.size
      })
      let maxSize = Math.max.apply(null, sizes)
      let minSize = Math.min.apply(null, sizes)
      let svg = d3.select(`.svg-${currentIndex}`).append('svg')
      svg.attr('width', width).attr('height', height)

      let words = dataCurrent.map(function (d) {
        return { text: d.id, size: 10 + (d.size - minSize) * 90 / (maxSize - minSize) }
      })

      let layoutWords = cloud()
        .size([width, height])
        .words(words)
        .padding(5)
        .rotate(function () {
          return Math.random() * 45
        })
        .font('Impact')
        .fontSize(function (d) {
          return d.size
        })
        .on('end', function () {
          _self_.draw(svg, words, this, colorWords)
          if (currentIndex === _self_.groupList.length - 1) {
            _self_.spinShow = false
          }
        })

      layoutWords.start()
    },
    draw (svg, words, layoutWords, colorWords) {
      let _self_ = this
      svg
        .append('g')
        .attr('transform', `translate(${layoutWords.size()[0] / 2},${layoutWords.size()[1] / 2})`)
        .selectAll('text')
        .data(words)
        .enter()
        .append('text')
        .attr('fill', (_, i) => colorWords(i))
        .style('font-size', function (d) {
          return `${d.size}px`
        })
        .style('font-family', 'Impact')
        .style('cursor', 'pointer')
        .attr('text-anchor', 'middle')
        .attr('transform', function (d) {
          return `translate(${[d.x, d.y]})rotate(${d.rotate})`
        })
        .text(function (d) {
          return d.text
        })
        .on('click', function (d, i) {
          _self_.$router.push({
            path: '/searchPage',
            query: {
              key: d.text
            }
          })
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.svg {
  display: flex;
  justify-content: center;
  align-items: center;
}
.tags {
  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
