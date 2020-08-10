<template>
  <div class="container-fluid" id="calendar">
    <div class="calender-container">
      <el-calendar v-model="today" :first-day-of-week="7">
        <template
          slot="dateCell"
          slot-scope="{date, data}">
          <div :style="{'background-color': calcColor(data.day)}" style="width: 100%; height: 100%;" @click="openDiary(data.day)">
            {{ parseInt(data.day.split('-')[2]) }}
            <div v-if="hasDiary(data.day)" class="diary-tag">
              {{ getWordCnt(data.day) }} 字 <br/>
              {{ getResponseNum(data.day) }} 评论 <span class="badge badge-light" v-if="hasNewResponse(data.day)">new</span>
            </div>
          </div>
        </template>
      </el-calendar>
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
export default {
  name: 'index',
  data () {
    return {
      code: '',
      showLoading: false,
      showResult: false,
      showMatch: false,
      today: new Date(),
      dayMood: {
        '2020-08-09': {
          point: 0.9,
          words: 100,
          responseNum: 0,
          hasNew: false
        },
        '2020-08-08': {
          point: 0.1,
          words: 200,
          responseNum: 1,
          hasNew: true
        }
      }
    }
  },
  methods: {
    rgbaToString (r, g, b, a = 1) {
      return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')'
    },
    calcColor (day) {
      if (this.dayMood.hasOwnProperty(day)) {
        let r = 255 * (1 - this.dayMood[day].point)
        let g = 255 * this.dayMood[day].point
        let b = 100 * this.dayMood[day].point / 2
        return this.rgbaToString(r, g, b)
      }
      return '#ffffff'
    },
    hasDiary (day) {
      return this.dayMood.hasOwnProperty(day)
    },
    getWordCnt (day) {
      if (this.dayMood.hasOwnProperty(day)) {
        return this.dayMood[day].words
      }
      return 0
    },
    hasNewResponse (day) {
      if (this.dayMood.hasOwnProperty(day)) {
        return this.dayMood[day].hasNew
      }
      return false
    },
    getResponseNum (day) {
      if (this.dayMood.hasOwnProperty(day)) {
        return this.dayMood[day].responseNum
      }
      return 0
    },
    openDiary (day) {
      this.$router.push('/diary/' + day)
    },
    fetchCalender () {
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
    },
    mounted () {
      this.fetchCalender()
    }
  }
}
</script>

<style scoped>
  .calender-container {
    margin-top: 70px;
    overflow: hidden;
  }
  .diary-tag {
    margin-top: 10px;
    width: 100%;
    padding: 2px;
    font-size: 12px;
    font-weight: 400;
  }
  @media (max-width: 768px) {
    .diary-tag {
      margin-top: 0;
    }
  }
</style>
