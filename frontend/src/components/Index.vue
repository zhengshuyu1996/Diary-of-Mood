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
      dayMood: {},
      colors: {
        'happy': {
          r: 239,
          g: 108,
          b: 0
        },
        'angry': {
          r: 183,
          g: 28,
          b: 28
        },
        'disguested': {
          r: 88,
          g: 201,
          b: 185
        },
        'depressed': {
          r: 96,
          g: 125,
          b: 139
        }
      }
    }
  },
  computed: {
    id () {
      if (this.$store.state.user_info && this.$store.state.user_info.hasOwnProperty('id')) {
        return this.$store.state.user_info.id
      }
      return ''
    }
  },
  watch: {
    id () {
      this.fetchCalendar()
    }
  },
  methods: {
    rgbaToString (r, g, b, a = 1) {
      return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')'
    },
    calcColor (day) {
      if (this.dayMood.hasOwnProperty(day)) {
        if (this.dayMood[day].hasOwnProperty('emotion_class')) {
          let rgb = this.colors[this.dayMood[day].emotion_class]
          return this.rgbaToString(rgb.r, rgb.g, rgb.b, this.dayMood[day].emotion_score)
        }
        let score = this.dayMood[day].point
        if (score < 0) {
          score = -score
          return this.rgbaToString(88, 201, 185, score)
        }
        return this.rgbaToString(239, 108, 0, score)
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
    fetchCalendar () {
      let that = this
      if (this.id === '') {
        return
      }
      this.showLoading = true
      this.$axios.get('/calendar?id=' + this.id)
        .then(res => {
          console.log('Calendar:', res.data)
          if (res.data.status === 'OK') {
            let data = res.data.data
            let calendar = {}
            for (let i = 0; i < data.length; i += 1) {
              calendar[data[i].date] = {
                point: data[i].point,
                words: data[i].words,
                responseNum: data[i].responseNum,
                hasNew: data[i].hasNew
              }
            }
            that.dayMood = calendar
          }
        })
        .catch(err => {
          console.log(err)
        })
        .finally(() => {
          that.showLoading = false
        })
    }
  },
  mounted () {
    console.log(this.$store.state)
    this.fetchCalendar()
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
