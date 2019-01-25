<template>
  <div id="tableModel">
    <!-- 导入 -->
    <input
    type="file"
    ref="imFile"
    @change="importFile(this)"
    style="display: none"
    accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel">

    <Card class="search">
        <!-- <slot name="search"></slot> -->
        <searchModel ref="searchModel" :search="search" @searchData="queryData" @selectChecker="selectChecker"></searchModel>
    </Card>
    <Card class="table">
      <div slot="title" class="table_title">
        <div>
          <Icon type="ios-stats" /> {{tableTitle}}
          <slot name="message"></slot>
        </div>
        <div class="btn">
          <ButtonGroup>
            <slot name="addBtn"></slot>
            <Button v-if="upload" @click="uploadFile()">
              <Icon type="ios-cloud-upload-outline" /> 导入
            </Button>
            <Button v-if="downLoad" @click="downloadExl()">
              <Icon type="ios-cloud-download-outline" /> 导出
            </Button>
            <Button @click="refresh()">
              <Icon type="md-refresh" /> 刷新
            </Button>
          </ButtonGroup>
        </div>
      </div>

      <div class="table_content" ref="tableContent">
        <Table border ref="table" @on-selection-change="selectedColumns" :loading="loading" :columns="columns" :height="tableHeight" :data="tableData"></Table>
      </div>

      <div class="table_page">
           <Page @on-change="changePage" :current="pageOption.current" :total="pageOption.total" :page-size="pageOption.pageSize" show-total />
      </div>
    </Card>
  </div>
</template>

<script>
var XLSX = require('xlsx')

let factoryApi = ''
let departureApi = ''
let carModelApi = ''

import request from '@/common/js/request.js'
import searchModel from '@/components/model/searchModel'
export default {
  name: "tableModel",
  components: {
      searchModel
  },
  props: {
    search: {
        default() {     // 显示的搜索条件       
            return []
        }
    },
    upload: {           // 导入
        default: false
    },
    downLoad: {
        default: false   // 导出
    },
    pageOption: {
        default(){
            return {}
        }
    },
    columns: {
      default() {
          return []
      }
    },
    tableData: {
      default() {
          return []
      }
    },
    tableTitle: {    // 表格名称和导出的excel文件名称
        default: ''
    },
    idData: {
        default() {
            return []
        }
    }
  },
    data() {
      return {
        tableHeight: 0,
        loading: true
      }
    },
    mounted() {
        setTimeout(()=>{
            let tableHeight = this.$refs.tableContent.clientHeight
            this.tableHeight = tableHeight
        },20)
        let _this = this
        window.onresize = function() {
            let tableHeight = _this.$refs.tableContent.clientHeight
            let tableWrapper = document.querySelector('.ivu-table-wrapper')
            tableWrapper.style.height = tableHeight
            _this.tableHeight = tableHeight
        }

        // this.loading = true
        this._timeOut(8000)
    },
    computed: {
        // 监听页码的变化
        newPageIndex() {
            clearTimeout(this.timerId)  // 清空计时器
            return this.pageOption.pageIndex
        }
    },
  watch: {
    tableData(val) {
        this.loading = false
    },
    // 通过计算属性来监听pageOption.pageIndex值得变化
    newPageIndex() {
        this.loading = true
        this._timeOut(8000)
    }
  },
  methods: {
    // 改变当前页码
    changePage(current) {
        if (this.loading == false) {
            this.$emit('changePage',current)
        }
    },
    // 返回搜索的条件
    queryData(val) {
        this.$emit('queryData',val)
    },
    // 设置超时
    _timeOut(time) {
        this.timerId = setTimeout(()=>{
            if (this.loading === true) {
                console.log('tiemOut')
                this.loading = false
                this.$Message.warning('请求超时!')
            }
        },time)
    },
    // 点击导入按钮
    uploadFile() {
        this.$refs.imFile.click();
    },
    // 刷新
    refresh() {
        this.loading = true
        this.$emit('refresh')
    },
    // 返回选中的行
    selectedColumns(event) {
        // console.log(event)
        this.$emit('selectedRow',event)
    },
    // 显示所有检验员
    showAllChecker(){
        this.$refs.searchModel.showModel('checker')
    },
    // 返回选中的检验员
    selectChecker(val) {
        this.$emit('selectChecker',val)
    },
    // 导出excel
    downloadExl() {
        this.$refs.table.exportCsv({
            filename: this.tableTitle,
            columns: this.columns.filter((col,index) => index < this.columns.length-1 && index != 0),
            data: this.tableData.filter((data,index) => index < this.columns.length-1)
        })
    },
    // 导入excel
    importFile() {
        let obj = this.$refs.imFile
        if (!obj.files) {
            return 
        }
        let f = obj.files[0]
        let reader = new FileReader()
        let $t = this
        reader.onload = function(e) {
            let data = e.target.result
            if ($t.rABS) {
                $t.wb = XLSX.read(btoa(this.fixdata(data)), {  // 手动转化
                    type: 'base64'
                })
            }else {                
                $t.wb = XLSX.read(data, {
                    type: 'binary'
                })
            }
            let json = XLSX.utils.sheet_to_json($t.wb.Sheets[$t.wb.SheetNames[0]])
            $t.dealFile(json)
        }
        if (this.rABS) {
            reader.readAsArrayBuffer(f)
        } else {
            reader.readAsBinaryString(f)
        }
    },
    dealFile(data) {   // 处理导入的数据
        let newArr = []
        data.forEach( item => {
            this.idData.forEach( val => {
                if(val.name == item.factory) {
                    item.factoryId = val.id
                }
            })       
        })
        let url = '/driver/createMultipleData'
        request.post(url,data).then(res => {
            console.log(res)
        })

    },
    fixdata: function (data) {  // 文件流转BinaryString
        var o = ''
        var l = 0
        var w = 10240
        for (; l < data.byteLength / w; ++l) {
        o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w, l * w + w)))
        }
        o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w)))
        return o
    }
  }
};
</script>

<style lang="less" scoped>
#tableModel {
    height: 100%;
    display: flex;
    flex-direction: column;

    .search {
        min-height: 60px;
        margin-bottom: 5px;

    }
    .table {
        // height: 100%;
        flex: 1;
        background-color: #fff;       
        .table_title {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .table_content {
            flex: 1
        }
        .table_page {
            flex-basis: 40px;
            margin-top: 5px;
            margin-bottom: 5px;
        }
        
    }
}
</style>

<style>
#tableModel .table.ivu-card {
    display: flex;
    flex-direction: column;
}
#tableModel .table .ivu-card-body {
    flex: 1;
    height: 100%;
    padding: 0;
    display: flex;
    flex-direction: column;
}
/* #tableModel .table_content {
    border: 1px solid red;
} */
#tableModel .ivu-card-head {
    flex-basis: 50px;
    box-sizing: border-box;
    background-color: #58b1ec;
    padding: 10px 12px;
}
#tableModel .ivu-table-wrapper {
    border: none;
}

</style>
