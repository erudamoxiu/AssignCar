<template>
    <div id="carModel">
        <tableModel height="100%" @changePage="changePage" :columns='columns' :tableData="tableData" :tableTitle="tableTitle" :pageOption="pageOption" 
        >
            <Button slot="addBtn" @click="add">
                <Icon type="ios-add" /> 新增
            </Button>
        </tableModel>

        <Modal v-model="showForm" :title="fromTitle" @on-ok="save">
            <Form :model="formData" :label-width="80">
                <FormItem label="车型">
                    <Input type="text" v-model="formData.carModel" placehoIder="请输入车型"></Input>
                    </Select>
                </FormItem>
            </Form>
        </Modal>
    </div>
</template>

<script>

let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))

let getAllCarModelApi = '/carmodel/getAllCarModel'
let addCarModelApi = '/carmodel/createdateCarModel'
let getCarModelApi = '/carmodel/getCarModel?id='
let updateCarModelApi = '/carmodel/updateCarModel'
let deleteCarModelApi = '/carmodel/deleteCarModel?id='
let excel_uploadApi = '/carmodel/excel_upload'

import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
import { map } from 'async';

    export default {
        name: 'carModel',
        data(){
            return {
                showForm : false,
                fromTitle: '车型',
                pageOption: {
                    pageIndex: 1,
                    pageSize: 20,   
                    total: 0,
                },
                type: 'add',
                tableData: [],
                formData: {
                    carModel: '',
                    createUser: '',
                    updateUser: ''
                },
                tableTitle: '车型基础资料',
                columns: [
                    {
                        type: 'index',
                        title: '序号',
                        width: 80,
                        align: 'center'
                    },
                    {
                        title: '车型',
                        key: 'carModel',
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
                                            let url = getCarModelApi + params.row.id
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
                                                    let url = deleteCarModelApi + params.row.id
                                                    request.get(url).then(res =>{
                                                        console.log(res)
                                                        if (res === true) {
                                                            this.$Message.success('删除成功')
                                                            this.getCarModelData()
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
                this.type = 'add'
                this.showForm = true
            },
            save() {
                if (this.type === 'add') {
                    let sendData = Object.assign(this.formData,{
                        createUser: userInfo.userId
                    })
                    request.post(addCarModelApi,sendData).then(res =>{
                        if (res === true) {
                            this.$Message.success('新增成功')
                            this.getCarModelData()
                        }
                    })
                }else if (this.type === 'modify') {
                    let sendData = Object.assign(this.formData,{
                        updateUser: userInfo.userId
                    })
                    request.post(updateCarModelApi,sendData).then(res => {
                        if (res === true) {
                            this.$Message.success('修改成功')
                            this.getCarModelData()
                        }
                    })
                }
            },
            // 获取车型数据
            getCarModelData() {
                // let queryData = {
                //     pageIndex: 1,
                //     pageSize: 50
                // }
                request.post(getAllCarModelApi,this.pageOption).then( res => {
                    this.tableData = res.data
                    this.pageOption.total = res.total
                })
            },
            // 更换页码
            changePage(current) {
                this.pageOption.pageIndex = current
                this.getCarModelData()
            }
        },
        mounted() {
            this.getCarModelData()
        },
        watch: {
            showForm(value) {
                if (value === false) {
                    this.formData = {
                        carModel: ''
                    }
                }
            }
        }
    }
</script>
<style>
#carModel {
    height: 100%;
}
</style>