<template>
  <div class="layout">
    <Layout>
      <Header>
        <Menu mode="horizontal" theme="dark" active-name="1">
          <div class="layout-logo"><img src="./assets/logo.png"></div>
          <div class="layout-nav">
            <MenuItem name="1">
              <router-link to="/"><Icon type="ios-navigate"></Icon>首页</router-link>
            </MenuItem>
            <MenuItem name="2">
              <router-link to="/searchPage" :class="{'router-link-exact-active': searchActive}"><Icon type="md-search"></Icon>关键词搜索</router-link>
            </MenuItem>
            <MenuItem name="2">
              <router-link to="/newsList" :class="{'router-link-exact-active': newsListActive}"><Icon type="ios-keypad"></Icon>新闻列表</router-link>
            </MenuItem>
            <MenuItem name="3">
              <Icon type="md-help-circle" size="18" class="help-btn" @click="helpModal = true"></Icon>
            </MenuItem>
          </div>
        </Menu>
      </Header>
      <Content :style="{padding: '0 50px'}">
        <div class="flex-box">
          <Breadcrumb :style="{margin: '20px 0'}">
            <BreadcrumbItem>WORDANCE</BreadcrumbItem>
            <BreadcrumbItem>{{ currentPage }}</BreadcrumbItem>
          </Breadcrumb>
          <div class="search-box">
            <div class="keyword circle" v-if="searchActive"></div>
            <span class="text" style="padding-right:10px" v-if="searchActive">关键词</span>
            <Input style="width:150px" v-model="searchKey" placeholder="请输入关键词" @on-keyup.enter="goSearch">
              <Icon type="ios-search" slot="suffix" class="search-btn" @click="goSearch"/>
            </Input>
          </div>
        </div>
        <Card>
          <div style="min-height: calc(100vh - 230px);">
            <router-view :key="$route.fullPath" @on-clear-search-key="clearSearchKey" @on-get-search-key="getSearchKey"/>
          </div>
        </Card>
      </Content>
      <Footer class="layout-footer-center">wordance &copy; more than you know</Footer>
    </Layout>
    <Modal
        v-model="helpModal"
        title="帮助文档"
        @on-ok="okModal"
        :scollable="true"
        @on-cancel="cancelModal">
        <p>- 首页词云为各类型数据聚合。</p>
        <p>- 点击词云里的词语可进入关键词搜索页。</p>
        <p>- 右上角输入框中可以输入词语进行搜索，也可以进入关键词搜索页，效果和点词云的词语进入的情况一样。</p>
        <p>- 关键词搜索页可以看关键词关联的词形成的力导图，同时可以看选中点对应的详细信息。</p>
        <p>- 关键词搜索页点更多文章可以进入新闻列表页</p>
        <p>- 也可直接进入新闻列表页，输入关键词，查看关键词对应的各类型文章，切换类型，可以看到不同文章。</p>
        <div slot="footer">
          <Button type="primary">确定</Button>
        </div>
    </Modal>
  </div>
</template>
<script>
export default {
  data () {
    return {
      helpModal: false,
      searchKey: ''
    }
  },
  mounted () {
    this.searchKey = this.$route.query.key
  },
  methods: {
    okModal () {
      this.helpModal = false
    },
    cancelModal () {
      this.helpModal = false
    },
    goSearch () {
      if (!this.searchKey) {
        this.$Message.error('请输入搜索的关键词')
        return false
      }
      console.log(this.$route.path)
      if (this.$route.path !== '/newsList') {
        this.$router.push({
          path: '/searchPage',
          query: {
            key: this.searchKey
          }
        })
      } else {
        this.$router.push({
          path: '/newsList',
          query: {
            key: this.searchKey
          }
        })
      }
    },
    clearSearchKey () {
      this.searchKey = ''
    },
    getSearchKey () {
      this.searchKey = this.$route.query.key
    }
  },
  computed: {
    currentPage () {
      let res = ''
      switch (this.$route.path) {
        case '/':
          res = '首页'
          break
        case '/searchPage':
          res = '关键词搜索'
          break
        case '/newsList':
          res = '新闻列表'
          break
      }
      return res
    },
    searchActive () {
      return this.$route.path.includes('/searchPage')
    },
    newsListActive () {
      return this.$route.path.includes('/newsList')
    }
  }
}
</script>
<style scoped>
.layout {
  border: 1px solid #d7dde4;
  background: #f5f7f9;
  position: relative;
  border-radius: 4px;
  overflow: hidden;
}
.layout-logo {
  float: left;
  position: relative;
}
.layout-nav {
  float: right;
  overflow: hidden;
}
.layout-footer-center {
  text-align: center;
}
.help-btn, .search-btn {
  cursor: pointer;
}
.flex-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.layout >>> .ivu-menu-item a {
  color: rgba(255,255,255,.7) !important;
  display: block;
}
.layout >>> .ivu-menu-dark.ivu-menu-horizontal .ivu-menu-item-active {
  color: rgba(255,255,255,.7) !important;
}
.layout >>> .ivu-menu-item a.router-link-exact-active {
  color: rgba(255,255,255) !important;
}
.layout >>>.ivu-layout-header {
  min-width: 920px;
}
.layout .circle.keyword {
  background: #2d8cf0;
  width: 10px;
  height:10px;
  border-radius: 50%;
  /* animation: keyword 1s ease infinite; */
  margin-right: 10px;
}
.search-box {
  display: flex;
  align-items: center;
}
@keyframes keyword {
  0% {
    width: 10px;
    height: 10px;
  }
  50% {
    width: 20px;
    height: 20px;
  }
  100% {
    width: 10px;
    height: 10px;
  }
}
</style>
