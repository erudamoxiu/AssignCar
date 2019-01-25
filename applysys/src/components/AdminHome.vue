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

  let getUserInfoApi = '/user/getUserInfo'
  let getJSAPI = '/user/getJSAPI'

  import AppHeader from '@/components/adminHome/TopNavbar'
  import MainBody from '@/components/adminHome/MainBody';
  import request from "@/common/js/request.js";

  let dataTime = new Date().getFullYear();
  export default {
    name: 'AdminHome',
    data(){
      return {
        date: dataTime
      }
    },
      // let userInfo = res
      // sessionStorage.setItem('zyUerInfo',JSON.stringify(userInfo))
    mounted() {
    let _this = this;

    request.get("/user/getJSAPI").then(res => {

      sessionStorage.setItem('zyCorpId',res.data.corpId)
      DingTalkPC.config({
        agentId: res.data.agentId, // 必填，微应用ID
        corpId: res.data.corpId, //必填，企业ID
        timeStamp: res.data.timeStamp, // 必填，生成签名的时间戳
        nonceStr: res.data.nonceStr, // 必填，生成签名的随机串
        signature: res.data.signature, // 必填，签名
        jsApiList: [
          "runtime.info",
          "biz.contact.choose",
          "device.notification.confirm",
          "device.notification.alert",
          "device.notification.prompt",
          "biz.ding.post",
          "biz.util.openLink"
        ]
      });
      DingTalkPC.ready(function() {
        DingTalkPC.runtime.permission.requestAuthCode({
          corpId: res.data.corpId,
          onSuccess: function(result) {
            let url = '/user/getUserInfo?code='+result.code
            request.get(url).then(res => {
              
              if (res) {
                _this.admin = true
                sessionStorage.setItem('zyUserInfo',JSON.stringify(res))
              }else {
                _this.message = "没有权限"
              }           
            })
          }
        });
      });
    });


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
