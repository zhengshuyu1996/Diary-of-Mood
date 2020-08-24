<template>
  <div class="container-fluid" id="diary-detail">
    <div class="detail-container">
      <h3>{{diary.date}}</h3>
      <hr/>
      <pre class="diary-content text-monospace">{{diary.content}}</pre>
      <div class="btn-edit-group">
        <button type="button" class="btn btn-outline-info btn-margin" @click="editDiary">编辑</button>
        <button type="button" class="btn btn-outline-danger" @click="deleteDiary">删除</button>
      </div>
      <hr/>
    </div>
    <div class="comment-container">
      <p class="comment-title">评论区</p>
      <div
        class="comment-inner"
        v-for="(comment, idx) in comments"
        :key="idx">
<!--        <span :class="{'user-left': !comment.isOwner, 'user-right': comment.isOwner}">{{comment.userName}}</span>-->
        <div
          class="comment-item"
          :class="{'comment-left': !comment.isOwner, 'comment-right': comment.isOwner}">
          <span :class="{ 'bubble-corner-left': !comment.isOwner, 'bubble-corner-right': comment.isOwner }"></span>
          <p>{{comment.comment}}</p>
        </div>
      </div>
    </div>
    <div class="response-box">
      <el-input
        v-model="myResponse"
        type="textarea"
        :autosize="{ minRows: smallScreen ? 1 : 3, maxRows: smallScreen ? 4 : 6}"
        placeholder="评论"
        class="response-input">
      </el-input>
      <button type="button" class="btn response-btn">发送</button>
    </div>
    <div id="page-loader" v-show="showLoading">
      <div class="spinner">
        <div class="bounce1"></div>
        <div class="bounce2"></div>
        <div class="bounce3"></div>
      </div>
    </div>
  </div>
</template>

<script>
// import $ from 'jquery'
import { Message } from 'element-ui'
export default {
  name: 'Diary',
  data () {
    return {
      defaultDiary: {
        title: '新日记',
        date: 'xxxx-xx-xx',
        content: ''
      },
      diary: {
        title: '新日记',
        date: '2020-08-09',
        content: '    大家好'
      },
      myResponse: '',
      comments: [
        {
          userName: 'Adviser',
          comment: '心情不好吗？',
          isOwner: false
        },
        {
          userName: 'owner',
          comment: '气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了气死了',
          isOwner: true
        },
        {
          userName: 'Adviser',
          comment: '我理解你的感受，考试前焦虑是正常的。',
          isOwner: false
        }
      ],
      showLoading: false
    }
  },
  props: {
    day: {
      type: String,
      default: '0'
    }
  },
  computed: {
    editingHTML () {
      return '<div>' + this.code + '</div>'
    },
    smallScreen () {
      return document.body.clientWidth < 768
    },
    id () {
      if (this.$store.state.user_info && this.$store.state.user_info.hasOwnProperty('id')) {
        return this.$store.state.user_info.id
      }
      return ''
    }
  },
  watch: {
    id () {
      this.getDiary()
      this.getComments()
    }
  },
  methods: {
    getDiary () {
      if (this.day === '0' || this.id === '') {
        this.diary = this.defaultDiary
        return
      }
      let that = this
      this.showLoading = true
      this.$axios.get('/diary?date=' + this.day + '&id=' + this.id)
        .then(res => {
          console.log('getDiary', res.data)
          if (res.data.status === 'OK') {
            that.diary = res.data.data
          }
        })
        .catch(err => {
          console.log(err)
        })
        .finally(() => {
          that.showLoading = false
        })
    },
    getComments () {
      if (this.day === '0') {
        this.diary = this.defaultDiary
        // return
      }
      // let that = this
      // this.$axios.post(this.$global.baseUrl + 'uploadHTML', {
      //   body: this.code,
      //   limit: this.limit
      // })
      //   .then(res => {
      //     console.log('StyleList', res.data)
      //     that.timestamp = res.data.timestamp
      //     that.original_html = that.$global.baseUrl + res.data.filepath
      //     that.styles = res.data.styles
      //   })
      //   .catch(err => {
      //     console.log(err)
      //   })
    },
    editDiary () {
      this.$router.push('/edit/' + this.day)
    },
    deleteDiary () {
      let that = this
      this.$confirm('确认要删除 ' + this.day + ' 的日记吗?', '删除日记', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      })
        .then(() => {
          that.showLoading = true
          that.$axios.get('/delete?date=' + this.day + '&id=' + this.id)
            .then(res => {
              if (res.data.status === 'OK') {
                Message.success('删除成功')
                that.$router.replace('/')
              } else {
                Message.error('删除失败')
              }
            })
            .catch(err => {
              Message.error('删除失败' + err)
            })
            .finally(() => {
              that.showLoading = false
            })
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  created () {
    this.getDiary()
    this.getComments()
  }
}
</script>

<style scoped>
  #diary-detail {
    height: calc(100vh - 80px);
  }
  .detail-container {
    width: 90%;
    margin-top: 80px;
    margin-left: auto;
    margin-right: auto;
    overflow: hidden;
    text-align: center;
  }
  .diary-content {
    text-align: left;
    font-size: 16px;
    color: #566270;
    min-height: 40vh;
  }
  .btn-edit-group {
    margin-top: 20px;
    margin-bottom: 20px;
  }
  .btn-margin {
    margin-right: 20px;
  }
  .response-box {
    float: right;
    margin: 20px 5% 40px auto;
    width: 60%;
    padding: 10px 0;
  }
  .response-input {
    width: 100%;
  }
  .response-btn {
    float: right;
    margin-top: 10px;
    width: 15%;
    background-color: #A593E0;
    color: #fffff3;
    max-width: 150px;
  }
  .comment-title {
    width: 100%;
    margin-left: 5%;
    font-size: 18px;
    font-weight: bold;
  }
  .comment-container {
    margin-top: 20px;
    width: 90%;
  }
  .comment-inner {
    width: 100%;
    margin-left: 5%;
    min-height: 40px;
    height: content-box;
    overflow: hidden;
    margin-bottom: 10px;
  }
  .user-left {
    width: 100%;
    text-align: left;
  }
  .user-right {
    width: 100%;
    text-align: right;
  }
  .comment-item {
    max-width: 60%;
    min-height: 40px;
    border-radius: 10px;
    padding: 15px;
    text-align: left;
    position: relative;
  }
  .comment-item p {
    margin-bottom: 0 !important;
  }
  .comment-left {
    float: left;
    margin-left: 10px;
    background-color: #F68657;
    color: #fffff3;
  }
  .comment-right {
    float: right;
    margin-right: 10px;
    background-color: #8CD790;
    color: #285943;
  }
  .bubble-corner-left {
    border-top: 8px solid transparent;
    border-left: 10px solid transparent;
    border-right: 10px solid #F68657;
    border-bottom: 8px solid transparent;
    position: absolute;
    left: -20px;
    top: 15px;
  }
  .bubble-corner-right {
    border-top: 8px solid transparent;
    border-left: 10px solid #8CD790;
    border-right: 10px solid transparent;
    border-bottom: 8px solid transparent;
    position: absolute;
    right: -20px;
    top: 15px;
  }
  @media (max-width: 768px) {
    .detail-container {
      width: 100%;
    }
    .response-box {
      width: 100vw;
      bottom: 0;
      left: 0;
      padding: 10px 0;
      position: fixed;
      background-color: #58C9B9;
      float: none;
      margin: 0 0 0 0;
    }
    .response-input {
      width: 80%;
    }
    .response-btn {
      display: inline;
      width: 15%;
      background-color: #A593E0;
      color: #fffff3;
      height: 33px;
      font-size: 0.9rem;
      max-width: 150px;
      margin-top: 0;
      float: none;
    }
    .comment-container {
      margin-bottom: 120px;
    }
  }
</style>
