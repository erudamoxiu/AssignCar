<template>
    <div id="factory">
        <tableModel height="100%" @changePage="changePage" :columns='columns' :tableData="tableData" :tableTitle="tableTitle" :pageOption="pageOption">
            <Button slot="addBtn" @click="add">
                <Icon type="ios-add" /> 新增
            </Button>
        </tableModel>

        <Modal v-model="showForm" :title="fromTitle" @on-ok="save">

            <Form :model="formData" :label-width="80">
                <FormItem label="厂别">
                    <Input type="text" v-model="formData.factoryName" placehoIder="请输入厂别"></Input>
                </FormItem>
            </Form>
        </Modal>
    </div>
</template>

<script>

let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))

let getAllFactoryApi = '/factory/getAllFactory'
let addFactoryApi = '/factory/createdateFactory'
let getFactoryApi = '/factory/getFactory?id='
let updateFactoryApi = '/factory/updateFactory'
let deleteFactoryApi = '/factory/deleteFactory?id='
let excel_uploadApi = '/factory/excel_upload'

import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
import { map } from 'async';

    export default {
        name: 'factory',
        data(){
            return {
                showForm : false,
                fromTitle: '厂别',
                pageOption: {
                    pageIndex: 1,
                    pageSize: 20,   
                    total: 0,
                },
                
                tableData: [],
                formData: {
                    factoryName: '',
                    createUser: '',
                    updateUser: ''
                },
                type: 'add',
                tableTitle: '厂别基础资料',
                columns: [
                    {
                        type: 'index',
                        title: '序号',
                        width: 80,
                        align: 'center'
                    },
                    {
                        title: '厂别',
                        key: 'factoryName',
                        align: 'center',
                    },
                    {
                        title: '操作',
                        key: 'action',
                        align: 'center',
                        width: '150',
                        render: (h,params) =>{
                            return h('div',[
                                h('Button',{
                                    props: {
                                        type: 'info',
                                        size: 'small',
                                    },
                                    on: {
                                        click: () => {
                                            this.type = 'modify'
                                            this.showForm = true
                                            let url = getFactoryApi + params.row.id
                                            request.get(url).then( res => {
                                                console.log('res',res)
                                                this.formData = res
                                            })
                                        }
                                    }
                                },'修改'),
                                h('Button',{
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    style: {
                                        maginLeft: '10px'
                                    },
                                    on: {
                                        click: () => {
                                            console.log('delete')
                                            this.$Modal.confirm({
                                                title: '提示',
                                                content: '确定是否删除?',
                                                onOk: () => {
                                                    let url = deleteFactoryApi + params.row.id
                                                    request.get(url).then(res =>{
                                                        console.log(res)
                                                        if (res === true) {
                                                            this.$Message.success('删除成功')
                                                            this.getFactoryData()
                                                        }
                                                    })
                                                }
                                            })
                                        }
                                    }
                                }, '删除')
                            ])
                        },
                    }
                ]
            }
        },
        components: {
            tableModel
        },
        methods: {
            // 新增
            add() {
                console.log('1111')
                this.type = 'add'
                this.showForm = true
            },
            save() {
                if (this.type === 'add') {
                    let sendData = Object.assign(this.formData,{
                        createUser: userInfo.userId
                    })
                    request.post(addFactoryApi,sendData).then(res =>{
                        if (res === true) {
                            this.$Message.success('新增成功')
                            this.getFactoryData()
                        }
                    })
                }else if (this.type === 'modify') {
                    // let params = {
                    //     id: this.formData.id,
                    // }
                    let sendData = Object.assign(this.formData,{
                        updateUser: userInfo.userId
                    })
                    request.post(updateFactoryApi,sendData).then(res => {
                        if (res === true) {
                            this.$Message.success('修改成功')
                            this.getFactoryData()
                        }
                    })
                }
            },
            // 获取厂别数据
            getFactoryData() {
                // let queryData = {
                //     pageIndex: 1,
                //     pageSize: 50
                // }
                request.post(getAllFactoryApi,this.pageOption).then( res => {
                    this.tableData = res.data
                    this.pageOption.total = res.total
                })
            },
            // 更换页码
            changePage(current) {
                this.pageOption.pageIndex = current
                this.getFactoryData()
            }
        },
        mounted() {
            this.getFactoryData()
        },
        watch: {
            showForm(value) {
                if (value === false) {
                    this.formData = {
                        factory: ''
                    }
                }
            }
        }
    }
</script>
<style>
#factory {
    height: 100%;
}
</style>