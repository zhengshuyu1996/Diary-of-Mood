import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import User from '@/components/User'
import Diary from '@/components/Diary'
import DiaryEdit from '@/components/DiaryEdit'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/user',
      name: 'User',
      component: User
    },
    {
      path: '/diary/:day',
      component: Diary,
      props: true
    },
    {
      path: '/edit/:day',
      name: 'DiaryEdit',
      component: DiaryEdit,
      props: true
    }
  ]
})
