<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top" style="background-color: #A593E0">
      <a class="navbar-brand" href="#">Diary of Mood</a>
      <div class="nav-content" id="navbarSupportedContent">
        <div class="content-item" v-if="!isEdit">
          <a class="btn nav-add shadow-sm rounded-circle" href="/#/edit/0"><i class="fa fa-pencil"></i></a>
        </div>
        <div class="content-item" v-if="isNotIndex">
          <a href="/#/"><i class="fa fa-home nav-icon"></i></a>
        </div>
        <div class="content-item">
          <a href="/#/user"><i class="fa fa-user-circle nav-icon"></i></a>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'yheader',
  data () {
    return {
      login_status: 0,
      username: ''
    }
  },
  methods: {
  },
  computed: {
    isNotIndex () {
      return this.$route.path.startsWith('/edit') || this.$route.path.startsWith('/diary') || this.$route.path.startsWith('/user')
    },
    isEdit () {
      return this.$route.path.startsWith('/edit')
    }
  },
  created () {
    // this.refreshHeader()
  }
}
</script>

<style scoped>
  #navbar-menu li {
    font-size: 16px !important;
  }
  .navbar-brand {
    color: #fffff3;
  }
  .nav-icon {
    font-size: 24px;
    margin-right: 20px;
    color: #fffff3;
    padding-top: 0.325em;
  }
  .nav-add {
    font-size: 16px;
    margin-top: -0.75em;
    margin-right: 40px;
    color: #fffff3;
    background-color: #58C9B9;
  }
  .nav-add:hover {
    background-color: #ef6c00;
  }
  .content-item {
    display: inline;
  }
  .nav-content {
    position: fixed;
    right: 0.2em;
    width: 100%;
    text-align: right;
  }
  @media (max-width: 768px) {
    .nav-add {
      margin-right: 20px;
    }
  }
</style>
