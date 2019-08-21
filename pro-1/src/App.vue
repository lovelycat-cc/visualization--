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
              <router-link to="/searchPage" :class="{'router-link-exact-active': searchActive}"><Icon type="ios-keypad"></Icon>关键词搜索</router-link>
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
          <Input style="width:150px;" v-model="searchKey" placeholder="请输入关键词" @on-keyup.enter="goSearch">
            <Icon type="ios-search" slot="suffix" class="search-btn" @click="goSearch"/>
          </Input>
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
      this.$router.push({
        path: '/searchPage',
        query: {
          key: this.searchKey
        }
      })
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
      }
      return res
    },
    searchActive () {
      return this.$route.path.includes('/searchPage')
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
</style>
