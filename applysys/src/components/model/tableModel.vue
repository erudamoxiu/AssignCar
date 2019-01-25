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
       <slot name="search"></slot>
    </Card>

    <Card class="table">
      <div slot="title" class="table_title">
        <div>
          <Icon type="ios-stats" /> {{tableTitle}}
        </div>
        <div class="btn">
          <ButtonGroup>
            <slot name="addBtn"></slot>
            <Button @click="uploadFile()">
              <Icon type="ios-cloud-upload-outline" /> 导入
            </Button>
            <Button @click="downloadExl()">
              <Icon type="ios-cloud-download-outline" /> 导出
            </Button>
          </ButtonGroup>
        </div>
      </div>

      <div class="table_content" ref="tableContent">
        <Table border ref="table" @on-selection-change="selectedRow" :columns="columns" :height="tableHeight" :data="tableData"></Table>
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
export default {
  name: "tableModel",
  props: {
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
        tableHeight: 0
      }
  },
  mounted() {
      let tableHeight = this.$refs.tableContent.clientHeight
      this.tableHeight = tableHeight
    //   console.log('tableHeight',tableHeight)
        let _this = this
        window.onresize = function() {
            let tableHeight = _this.$refs.tableContent.clientHeight
            let tableWrapper = document.querySelector('.ivu-table-wrapper')
            tableWrapper.style.height = tableHeight
            _this.tableHeight = tableHeight
            console.log('111',document.querySelector('.ivu-tabs-content').clientHeight)
        }
  },
  methods: {
    // 改变当前页码
    changePage(current) {
        this.$emit('changePage',current)
    },
    // 点击导入按钮
    uploadFile() {
        this.$refs.imFile.click();
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
        let url = '/factory/excel_upload'
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
    },
    selectedRow(rows) {
        this.$emit('selectedRow',rows)
    }
  }
};
</script>

<style lang="less" scoped>
#tableModel {
    height: 100%;
    .table {
        height: 100%;
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
#tableModel {
    display: flex;
    flex-direction: column;
}
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
