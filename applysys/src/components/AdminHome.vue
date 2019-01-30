<template>
  <div id="AdminHome" class="layout" style="border: none; border-radius:0">
    <Header id="outside_navbar">
      <AppHeader></AppHeader>
    </Header>
    <div id="outside_main">
      <MainBody></MainBody>
    </div>
    <Footer class="layout-footer-center" id="outside_footer">{{date}} &copy; zuoyou</Footer>
  </div>
</template>

<script>


import { mapActions } from "vuex";

  import AppHeader from '@/components/adminHome/TopNavbar'
  import MainBody from '@/components/adminHome/MainBody';
  

  let dataTime = new Date().getFullYear();
  export default {
    name: 'AdminHome',
    data(){
      return {
        date: dataTime
      }
    },

  methods: {
  },
    components: {
      AppHeader,
      MainBody
    },
  }
</script>

<style scoped>
  .layout{
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
  }
  .layout-logo{
    width: 100px;
    height: 30px;
    background: #5b6270;
    border-radius: 3px;
    float: left;
    position: relative;
    top: 15px;
    left: 20px;
  }
  .layout-nav{
    width: 420px;
    margin: 0 auto;
    margin-right: 20px;
  }
  .layout-footer-center{
    text-align: center;
    font-family: 'Avenir' !important;
  }
  #outside_navbar{
    width: 100%;
    position: fixed;
    top: 0;
    height: 60px;
    z-index: 999;
    padding: 0;
  }
  #outside_main{
    width: 100%;
    box-sizing: border-box;
    position: fixed;
    top: 60px;
    left: 0;
    bottom: 30px;
    overflow-x: hidden;
    background: #eaeaea;
  }
  #outside_footer{
    position: fixed;
    height: 30px;
    width: 100%;
    bottom: 0;
    left: 0;
    font-size: 12px;
    background: white;
  }
  .ivu-layout-footer{
    padding: 0!important;
    line-height: 30px;
  }
</style>
