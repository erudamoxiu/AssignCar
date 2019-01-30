<template>
    <div id="driver">
        <tableModel height="100%" @changePage="changePage" :columns='columns' :tableData="tableData" :tableTitle="tableTitle" :pageOption="pageOption" :idData="factoryData">
            <Button slot="addBtn" @click="add">
                <Icon type="ios-add" /> 新增
            </Button>
        </tableModel>

        <Modal v-model="showForm" :title="fromTitle" @on-ok="save" >


            <Form :model="formData" :label-width="80">
                <FormItem label="厂别">
                    <Select v-model="formData.factoryId" placeholder="请选择厂别">
                        <Option v-for="item in factoryData" :value="item.id">{{item.factoryName}}</Option>
                    </Select>
                </FormItem>
                <FormItem label="司机">
                    <!-- <Input v-model="formData.driverName" placeholder="请输入司机姓名"></Input> -->
                    <i-button @click="addUser">选择用户</i-button> <span v-if="formData.driverName">{{formData.driverName}}</span>
                </FormItem>
                <FormItem label="电话号码">
                    <Input v-model="formData.phone" placeholder="请输入电话号码"></Input>
                </FormItem>
            </Form>

            
        </Modal>
    </div>
</template>

<script>

let getAllDriverApi = '/driver/getAllDriver'
let getDriverApi = '/driver/getDriver?id='
let addDriverApi = '/driver/createdateDriver'
let getAllFactoryApi = '/factory/getAllFactory'
let updateDriverApi = '/driver/updateDriver'
let deleteDriverApi = '/driver/deleteDriver?id='
let addApi = '/user/addUser'

let CorpId = sessionStorage.getItem('zyCorpId')
let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))

import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
import { map } from 'async';

    export default {
        name: 'driver',
        data() {
            return {
                showForm: false,
                fromTitle: '司机资料',
                pageOption: {
                    pageIndex: 1,
                    total: 0,
                    pageSize: 10000
                },
                factoryData: [],   // 所有厂别
                formData: {
                    factoryId: '',
                    driverName: '',
                    phone: '',
                    createUser: '',
                    driverId: '',
                    updateUser: ''
                },
                type: 'add',
                tableTitle: '司机基础资料',
                columns: [
                    {
                        type: 'index',
                        title: '序号',
                        width: 80,
                        align: 'center'
                    },
                    {
                        title: '厂别',
                        key: 'factory_name',
                        align: 'center',
                    },{
                        title: '司机姓名',
                        key: 'name',
                        align: 'center',
                    },{
                        title: '电话号码',
                        key: 'phone',
                        align: 'center',
                    },{
                        title: '操作',
                        key: 'action',
                        align: 'center',
                        width: 150,
                        render: (h,params) => {
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
                                            let url = getDriverApi + params.row.id
                                            request.get(url).then( res => {
                                                console.log('res',res)
                                                this.formData = res
                                            })
                                        }
                                    }
                                }, '修改'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    style: {
                                        marginLeft: '10px'
                                    },
                                    on: {
                                        click: () => {
                                            console.log('delete')
                                            this.$Modal.confirm({
                                                title: '提示',
                                                content: '你确定要删除吗？',
                                                onOk: () => {
                                                    let url = deleteDriverApi + params.row.id
                                                    request.get(url).then(res => {
                                                        console.log(res)
                                                        if (res===true) {
                                                            this.$Message.success('删除成功')
                                                            this.getDriverData()
                                                        }
                                                    })
                                                }
                                            })
                                        }
                                    }
                                }, '删除')
                            ])
                        }
                    }
                ],
                tableData: []
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
                    request.post(addDriverApi,sendData).then(res => {
                        if (res === true ) {
                            this.$Message.success('新增成功')
                            this.getDriverData()
                        }
                    })
                }else if (this.type === 'modify') {
                    let sendData = Object.assign(this.formData,{
                        updateUser: userInfo.userId
                    })
                    request.post(updateDriverApi,sendData).then(res => {
                        // console.log(res)
                        if (res === true ) {
                            this.$Message.success('修改成功')
                            this.getDriverData()
                        }
                    })
                }
            },
            // 获取司机数据
            getDriverData() {
                request.post(getAllDriverApi,this.pageOption).then( res => {
                    this.tableData = res.data
                    this.pageOption.total = res.total
                })
            },
            // 获取所有厂别数据
            getfactoryAllData() {
                let queryData = {
                    pageIndex: 1,
                    pageSize: 100
                }
                request.post(getAllFactoryApi,queryData).then( res => {
                    console.log(res)
                    this.factoryData = res.data
                })
            },
            // 更换页码
            changePage(current) {
                this.pageOption.pageIndex = current
                this.getDriverData()
            },
            // 新增用户
            addUser(userId) {
                let newThis = this
                DingTalkPC.biz.contact.choose({
                    multiple: false, //是否多选
                    corpId: CorpId,
                    max: 1,
                    onSuccess: (data) => {
                        this.formData.driverName = data[0].name
                        this.formData.driverId = data[0].emplId
                        let ids = []
                        data.forEach((item) => {
                            ids.push(item.emplId)
                        })
                        let sendData = {
                            userIds: ids.join(),
                            userType: 4
                        }
                        request.post(addApi,sendData).then(res => {
                            if (res === true) {
                                // newThis.$Message.success('新增成功')
                                newThis.getUserData()
                                newThis.getDetail(res.id)
                            }
                        })
                    },
                    onFail: (err) => {
                    }
                })
            },
        },
        mounted() {
            this.getDriverData()
            this.getfactoryAllData()
        },
        watch: {
            showForm(value) {
                if (value === false) {
                    this.formData = {
                        factoryId: '',
                        driverName: '',
                        driverId: '',
                        phone: ''
                    }
                }
            }
        }
    }
</script>

<style>
#driver {
    height: 100%;
}
</style>