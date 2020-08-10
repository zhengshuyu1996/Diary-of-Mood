<template>
  <div id="app" class="site-wrapper">
    <div class="site-wrapper-inner">
      <div class="cover-container">
        <my-header :key="key"></my-header>
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import myHeader from '@/components/Header.vue'

export default {
  components: {
    myHeader
  },
  name: 'App',
  computed: {
    key () {
      return this.$route.name !== undefined ? this.$route.name + new Date() : this.$route + new Date()
    }
  }
}
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    text-align: center;
    color: #566270;
  }
  .site-wrapper-inner {
    background-color: #ffffff;
  }
</style>
