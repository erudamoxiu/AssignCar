<template>
  <div>
    <Menu mode="horizontal" @on-select="selectName">
        <template v-for="(item,index) in menus">
            <MenuItem v-if="!item.children" :name="item.name">
                <Icon :type="item.icon"></Icon>
                <span v-text="item.alias"></span>
            </MenuItem>

            <Submenu v-if="item.children" :name="item.name">
                <template slot="title">
                    <Icon :type="item.icon"></Icon>
                    <span v-text="item.alias"></span>
                </template>
                <MenuGroup>
                    <MenuItem v-for="(item_sec,i) in item.children" :name="item_sec.name" >{{item_sec.alias}}</MenuItem>
                </MenuGroup>
            </Submenu>
        </template>
        
    </Menu>
  </div>
</template>

<script>
  let getUserInfoApi = '/user/getUserInfo'
  let getJSAPI = '/user/getJSAPI'
import { mapState, mapActions, mapGetters } from "vuex";
import { getMenu } from '@/common/js/menu.js'
import request from "@/common/js/request.js";
import "@/store/modules/menuModule";
export default {
    name: 'TopNavbar',
    data() {
        return {}
    },
    computed: {
        ...mapState('menu', {
            menus: "menus",
            tabs: 'tabs',
            nativeMenu: 'nativeMenu',
            activeItem: "activeItem"
        })
    },
    mounted() {
        this.login()

        let result = getMenu(0)
        this.getMenus(result.menus)
        this.getNativeMenu(result.nativeMenu)
        this.menuClick('apply')
    },
    methods: {
        ...mapActions('menu', {
            getMenus: "getMenus",
            menuClick: "menuClick",
            getNativeMenu: "getNativeMenu",
        }),
        selectName(name) {
            this.menuClick(name)
        },
        login() {
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
                        let result = getMenu(res.persona)
                        _this.getMenus(result.menus)
                        _this.getNativeMenu(result.nativeMenu)

                        switch (res.persona) {
                            case 0:
                                _this.menuClick('apply')
                                break;
                            case 1:
                                _this.menuClick('approvalApply')
                                break;
                            case 2:
                                _this.menuClick('approvalApply')
                                break;
                            case 3:
                                _this.menuClick('assignCar')
                                break;
                            case 4:
                                _this.menuClick('vehiclereturninfo')
                                break;
                        }
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
         firstPage(name) {
            this.menuClick(name)
        }
    }
};
</script>