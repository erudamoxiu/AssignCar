<template>
  <div id="MainBody" style="height: 100%">
    <Tabs id="main_tabs" style="height: 100%" type="card" :value="activeItem" :animated="false" :closable="tabs.length > 0" @on-tab-remove="remove">
      <TabPane label="首页" name="home" :closable="false">
        <async-component componentPath="components/home" ref="componentParent"></async-component>
      </TabPane>

      <TabPane id="tabPane" style="" v-for="(item,index) in tabs" :label="item.alias" :name="item.name" :key="item.id">
        <async-component :componentPath="item.components" ref="componentParent"></async-component>
      </TabPane>
    </Tabs>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import AsyncComponent from "@/components/AsyncComponent";
export default {
  name: 'MainBody',
  computed: {
    ...mapState("menu", {
      tabs: "tabs",
      activeItem: "activeItem"
    }),
  },
  components: {
    AsyncComponent
  },
  methods: {
    ...mapActions("menu", {
      menuClose: "menuClose"
    }),
    remove(e) {
      console.log('name',e)
      this.menuClose(e)
    }
  }
};
</script>

<style>
#MainBody #main_tabs {
  height: 100%;
  padding-top: 40px
}
#MainBody #main_tabs .ivu-tabs-bar {
  margin-top: -40px;
  margin-bottom: 5px;
}
#MainBody #main_tabs .ivu-tabs-content {
  padding: 0 5px;
  height: 100%;
}
#MainBody .ivu-tabs-tabpane {
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
}
#MainBody #main_tabs .ivu-tabs-tabpane>div {
  height: 100%;
 
}
</style>