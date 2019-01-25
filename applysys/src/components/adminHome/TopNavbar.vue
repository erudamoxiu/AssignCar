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
import { mapState, mapActions, mapGetters } from "vuex";
import { menus, nativeMenu } from '@/common/js/menu.js'
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
        this.getMenus(menus)
        this.getNativeMenu(nativeMenu)
    },
    methods: {
        ...mapActions('menu', {
            getMenus: "getMenus",
            menuClick: "menuClick",
            getNativeMenu: "getNativeMenu",
        }),
        selectName(name) {
            // console.log('name',name)
            this.menuClick(name)
        }
    }
};
</script>