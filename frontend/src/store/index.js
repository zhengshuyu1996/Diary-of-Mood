import Vue from 'vue'
import Vuex from 'vuex'
// import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

let store = new Vuex.Store({
  // plugins: [createPersistedState({
  //   key: 'offpay-admin',
  //   paths: ['username', 'uuid']
  // })],
  state: {
    user_info: {}
  },
  mutations: {
    SET_USERINFO: (state, userinfo) => {
      state.user_info = userinfo
      console.log('userinfo updated: ', state.user_info)
    }
  }
})

export default store
