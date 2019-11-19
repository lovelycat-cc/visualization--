<template>
  <div class="home">
    <div class="container">
      <div class="content">
        <div class="item" v-for="(item, index) in msgList" :key="index">
          <div class="robot" v-if="item.type === 'robot'">
            <img src="../assets/robot.png"/> <div class="text">{{item.msg}}</div>
          </div>
          <div class="user" v-if="item.type === 'user'">
            <div class="text">{{item.msg}}</div><img src="../assets/user.png"/>
          </div>
        </div>
      </div>
      <div class="input-box">
        <Input type="textarea" v-model="sentMsg" placeholder="按右边发送按钮发送消息..."/>
        <Button type="primary" @click="sendMsg">
          发送
        </Button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      ws: null,
      msgList: [],
      sentMsg: ''
    }
  },
  mounted () {
    if ('WebSocket' in window) {
      console.log('您的浏览器支持 WebSocket!')
      // eslint-disable-next-line
      this.ws = new WebSocket(wsURL)
      this.ws.onopen = () => {
        console.log('websocket 已连接上')
      }
      this.ws.onmessage = (evt) => {
        let dataReceive = evt.data
        let type = dataReceive.split(':')[0] === 'robot' ? 'robot' : 'user'
        this.msgList.push({
          type: type,
          msg: dataReceive.split(':')[1]
        })
        this.$forceUpdate()
        console.log(this.msgList)
      }
      this.ws.onclose = () => {
        console.log('连接已关闭...')
      }
    } else {
      console.log('您的浏览器不支持 WebSocket!')
    }
  },
  beforeDestroy () {
    this.ws.close()
  },
  methods: {
    sendMsg () {
      this.ws.send(this.sentMsg)
      this.msgList.push({
        type: 'user',
        msg: this.sentMsg
      })
      this.$forceUpdate()
      this.sentMsg = ''
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home {
  background: #f5f7f9;
  margin: 0 -15px;
}
.container {
  width: 600px;
  margin: -15px auto;
  height: calc(100vh - 200px);
  position: relative
}
.content {
  height: calc(100% - 50px);
  overflow-y: auto;
  overflow-x: hidden;
}
.content::-webkit-scrollbar {/*滚动条整体样式*/
  width: 4px;     /*高宽分别对应横竖滚动条的尺寸*/
  height: 4px;
}
.content::-webkit-scrollbar-thumb {/*滚动条里面小方块*/
  border-radius: 5px;
  -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
  box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
  background: rgba(0,0,0,0.2);
}
.content::-webkit-scrollbar-track {/*滚动条里面轨道*/
  -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
  box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
  border-radius: 0;
  background: rgba(0,0,0,0.1);
}
.input-box {
  display: flex;
  flex-wrap: nowrap;
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
}
.input-box>>>textarea {
  resize: none;
}
.robot, .user {
  display: flex;
  margin: 5px 0;
}
.robot img, .user img {
  width: 30px;
  height: 30px;
  margin-top: 5px;
}
.user {
  justify-content: flex-end;
}
.user .text {
  background: #b2e281;
  padding: 5px;
  width: 150px;
  position: relative;
  float: right;
  overflow: visible;
  margin-left: 6px;
  border-radius: 4px;
  border: 1px solid #dcdee2;
  word-break: break-word;
}
.user .text::before {
  content: '';
  width: 0px;
  height: 0px;
  border-left: #b2e281 5px solid;
  border-right: transparent 5px solid;
  border-top: transparent 5px solid;
  border-bottom: transparent 5px solid;
  position: absolute;
  right: -10px;
  top: 15px;
  z-index: 20;
}
.user .text::after {
  content: '';
  width: 0px;
  height: 0px;
  border-left: #dcdee2 6px solid;
  border-right: transparent 6px solid;
  border-top: transparent 6px solid;
  border-bottom: transparent 6px solid;
  position: absolute;
  right: -12px;
  top: 14px;
  z-index: 0;
}
.robot .text {
  background: #ffffff;
  padding: 5px;
  width: 150px;
  position: relative;
  overflow: visible;
  margin-left: 6px;
  border-radius: 4px;
  border: 1px solid #dcdee2;
  word-break: break-word;
}
.robot .text::before {
  content: '';
  width: 0px;
  height: 0px;
  border-right: #ffffff 5px solid;
  border-left: transparent 5px solid;
  border-top: transparent 5px solid;
  border-bottom: transparent 5px solid;
  position: absolute;
  left: -10px;
  top: 15px;
  z-index: 20;
}
.robot .text::after {
  content: '';
  width: 0px;
  height: 0px;
  border-right: #dcdee2 6px solid;
  border-left: transparent 6px solid;
  border-top: transparent 6px solid;
  border-bottom: transparent 6px solid;
  position: absolute;
  left: -12px;
  top: 14px;
  z-index: 0;
}
</style>
