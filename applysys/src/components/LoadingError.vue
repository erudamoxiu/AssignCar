<template>
  <div class="error-pnl">
      <Icon type="md-close-circle" />
      <Collapse v-model="value1" style="width:500px;margin:0 auto 20px">
        <Panel name="1">
            加载页面出现错误，展开查看错误详情！
            <p slot="content">{{errorDetails}}</p>
        </Panel>
    </Collapse>
      <!-- <el-button type="danger" @click="reload">点击重试</el-button> -->
       <Button :size="buttonSize" type="error" @click="dashed">点击重试</Button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      value1: '',
    }
  },
  methods: {
    reload() {
      this.$emit("reload");
    }
  },props:{
    errorDetails:String
  }
};
</script>

<style scoped>
.error-pnl {
  text-align: center;
}
.error-pnl > .el-button {
  margin-top: 2rem;
}
.error-pnl > i {
  font-size: 10rem;
  color: #ddd;
  margin: 2rem;
}
.error-pnl > .el-collapse {
  max-width: 30rem;
  margin: 0 auto;
}
</style>
