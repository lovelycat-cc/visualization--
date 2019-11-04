<template>
  <div class="layout">
    <Layout>
      <Header>
        <Menu mode="horizontal" theme="dark" active-name="1">
          <div class="layout-logo"><img src="./assets/logo.png" style="width:55px;"><img src="./assets/logo-2.png"></div>
          <div class="layout-nav">
            <MenuItem name="1">
              <router-link to="/"><Icon type="ios-navigate"></Icon>情感分析</router-link>
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
        </div>
        <Card>
          <div style="min-height: calc(100vh - 230px);">
            <router-view :key="$route.fullPath"/>
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
        <p>- 本项目功能：情感分析。</p>
        <div slot="footer">
          <Button type="primary" @click="okModal">确定</Button>
        </div>
    </Modal>
  </div>
</template>
<script>
export default {
  data () {
    return {
      helpModal: false
    }
  },
  mounted () {
    window.onbeforeunload = function (e) {
      e = e || window.event
      // 兼容IE8和Firefox 4之前的版本
      if (e) {
        e.returnValue = '程序运行状态刷新页面将影响后台程序的运行。'
      }
      // Chrome, Safari, Firefox 4+, Opera 12+ , IE 9+
      return '程序运行状态刷新页面将影响后台程序的运行。'
    }
    sessionStorage.setItem('loading', '')
  },
  destroyed () {
    window.onbeforeunload = null
  },
  methods: {
    okModal () {
      this.helpModal = false
    },
    cancelModal () {
      this.helpModal = false
    }
  },
  computed: {
    currentPage () {
      let res = ''
      switch (this.$route.path) {
        case '/':
          res = '情感分析'
          break
      }
      return res
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
