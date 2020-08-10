<template>
  <div class="container-fluid" id="diary-edit">
    <div class="edit-container">
      <div class="title-container">
        <h3>新日记</h3>
        <div class="diary-date">
          <el-date-picker
            style="width: 150px;"
            v-model="diaryDate"
            type="date"
            :clearable="false"
            :disabled="isEdit"
            placeholder="选择日期">
          </el-date-picker>
          <div class="edit-button">
            <button class="btn btn-outline-secondary" type="button" @click="clearDiary">清空</button>
            <button class="btn btn-save" type="button" @click="saveDiary">保存</button>
          </div>
        </div>
      </div>
      <codemirror
        ref="myCM"
        v-model="diary"
        :options="cmOptions"
        class="code-mirror">
      </codemirror>
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
import { codemirror } from 'vue-codemirror'
import 'codemirror/mode/htmlmixed/htmlmixed.js'
import 'codemirror/theme/3024-day.css'
export default {
  name: 'DiaryEdit',
  data () {
    return {
      diary: '',
      showLoading: false,
      diaryDate: Date.now(),
      cmOptions: {
        // codemirror options
        tabSize: 2,
        mode: 'text/html',
        theme: '3024-day',
        lineNumbers: true,
        line: true,
        lineWrapping: true,
        // viewportMargin: Infinity,
        smartIndent: true,
        spellcheck: true
        // more codemirror options, 更多 codemirror 的高级配置...
      }
    }
  },
  components: {
    codemirror
  },
  props: {
    day: {
      type: String,
      default: '0'
    }
  },
  computed: {
    isEdit () {
      return this.day !== '0'
    }
  },
  methods: {
    getDiaryContent (day) {
      if (day === '0') {
        this.diary = ''
        return
      }
      this.diaryDate = Date.parse(day)
      this.showLoading = true
      let that = this
      this.$axios.get(this.$global.baseUrl + 'uploadHTML')
        .then(res => {
          that.diary = res.data
        })
        .catch(err => {
          console.log(err)
        })
        .finally(() => {
          that.showLoading = false
        })
    },
    clearDiary () {
      this.diary = ''
    },
    saveDiary () {
      console.log(this.diary)
      this.$router.go(-1)
      // this.showLoading = true
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
      //     that.showResult = true
      //     that.showLoading = false
      //   })
      //   .catch(err => {
      //     console.log(err)
      //   })
    }
  },
  created () {
    this.getDiaryContent(this.day)
  }
}
</script>

<style scoped>
  .edit-container {
    width: 100%;
    margin-top: 80px;
    overflow: hidden;
    text-align: center;
  }
  .title-container {
    width: 90%;
    left: auto;
    margin-left: auto;
    right: auto;
    margin-right: auto;
    text-align: left;
  }
  .title-container h3 {
    width: 100px;
    display: inline;
  }
  .diary-date {
    display: inline;
    margin-top: 0;
    margin-left: 30px;
  }
  .edit-button {
    display: inline;
    float: right;
  }
  .edit-button button {
    margin-left: 10px;
  }
  .btn-save {
    background-color: #4caf50;
    color: #ffffff;
  }
  .btn-save:hover {
    background-color: #81c784;
  }
  .code-mirror {
    margin-top: 18px;
    height: calc(100vh - 160px);
    width: 90%;
    left: auto;
    margin-left: auto;
    right: auto;
    margin-right: auto;
    text-align: left;
    border: solid 1px #E0E3DA;
    font-size: 16px;
  }
  @media (max-width: 768px) {
    .diary-date {
      margin-top: 10px;
      display: block;
      margin-left: 0;
      width: 100%;
    }
    .code-mirror {
      margin-top: 8px;
      height: calc(100vh - 180px);
    }
  }
</style>
