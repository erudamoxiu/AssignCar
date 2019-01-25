<template>
    <div id="cost" style="height: 100%">
        <tableModel  @changePage='changePage' :columns='columns' :tableData="tableData" :tableTitle="tableTitle" :pageOption="pageOption">
            <div slot="search">
            </div>
             <Button slot="addBtn" @click="add">
                <Icon type="ios-add" /> 新增
            </Button>
        </tableModel>

        <Modal v-model="showForm" :title="fromTitle" @on-ok="save">
            <Form :model="formData" :label-width="80">
                <FormItem label="出发地">
                    <Select v-model="formData.departureInfoId" placeholder="请选择出发地">
                        <Option v-for="item in departureData" :value="item.id">{{item.departure}}</Option>
                    </Select>
                </FormItem>
                <FormItem label="目的地">
                    <!-- <Input v-model="formData.dest" placeholder="请输入目的地"></Input> -->
                    <Input v-model="formData.dest" placeholder="请输入目的地"></Input>
                </FormItem>
                <FormItem label="内部费用">
                    <Input v-model="formData.internalFee" placeholder="请输入内部费用"></Input>
                </FormItem>
                <FormItem label="市场价格">
                    <Input v-model="formData.marketFee" placeholder="请输入市场价格"></Input>
                </FormItem>
                <FormItem label="车型">
                    <Select v-model="formData.carModelId" placeholder="请选择车型">
                        <Option v-for="item in carModelData" :value="item.id">{{item.carModel}}</Option>
                    </Select>
                </FormItem>
                <FormItem label="途径地">
                    <Input v-model="formData.channel" placeholder="请输入途径地"></Input>
                </FormItem>
                <FormItem label="其他说明">
                    <Input v-model="formData.otherNote" placeholder="请输入其他说明"></Input>
                </FormItem>
            </Form>
        </Modal>
    </div>
</template>

<script>

let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))

let getAllDestFeeApi = '/destfee/getAllDestFee'
let getDetailApi = '/destfee/getDestFee?id='
let addApi = '/destfee/createdateDestFee'
let updateApi = '/destfee/updateDestFee'
let deleteApi = '/destfee/deleteDestFee?id='

let getAllDepartureApi = '/departureinfo/getAllDeparture'
let getAllCarModelApi = '/carmodel/getAllCarModel'

import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
import { setTimeout } from 'timers';
    export default {
        name: 'cost',
        components: {
            tableModel
        },
        data() {
            return {
                showForm: false,
                fromTitle: '目的地与费用', 
                pageOption: {
                    pageIndex: 1,
                    total: 0,
                    pageSize: 20
                },
                type: 'add',
                tableTitle: '目的费用关系数据表',
                columns: [
                    {
                        type: 'index',
                        title: '序号',
                        width: 80,
                        align: 'center'
                    },
                    {
                        title: '出发地',
                        key: 'deparTureName',
                        align: 'center',
                    },{
                        title: '车型',
                        key: 'carModel',
                        align: 'center',
                    },{
                        title: '目的地',
                        key: 'dest',
                        align: 'center'
                    },{
                        title: '内部费用',
                        key: 'internalFee',
                        align: 'right'
                    },{
                        title: '市场价格',
                        key: 'marketFee',
                        align: 'right'
                    },{
                        title: '途径地',
                        key: 'channel',
                        align: 'center'
                    },{
                        title: '其他说明',
                        key: 'otherNote',
                        align: 'center'
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
                                            console.log('modify')
                                            this.showForm = true
                                            let url = getDetailApi + params.row.id
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
                                            this.$Modal.confirm({
                                                title: '提示',
                                                content: '你确定要删除吗？',
                                                onOk: () => {
                                                    let url = deleteApi + params.row.id
                                                    request.get(url).then(res => {
                                                        // console.log(res)
                                                        if (res === true) {
                                                            this.$Message.success('删除成功')
                                                            this.getAllData()
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
                tableData: [],
                formData: {
                    departureInfoId: '',    // 出发地id
                    dest: '',               // 目的地
                    internalFee: '',        // 内部费用
                    marketFee: '',          // 市场价格
                    carModelId: '',         // 车型id
                    channel: '',            // 途径地
                    otherNote: '',          // 其他说明
                    createUser: '',
                    updateUser: ''
                },
                departureData: [],
                destData: [],
                carModelData: []
            }
        },
        mounted() {
            this.userInfo = localStorage.getItem('userInfo')
            // this.getAllData();
            let _this = this
            setTimeout(() => {
                _this.getAllDeparture()
                // _this.getAlldest()
                _this.getAllCarModel()
            },600)
            this.getAllData()
        },
        methods: {
            // 获取所有数据
            getAllData() {
                request.post(getAllDestFeeApi,this.pageOption).then( res => {
                    console.log(res)
                    this.tableData = res.data
                    this.pageOption.total = res.total
                })
            },
            // 更换页码
            changePage(current) {
                this.pageOption.pageIndex = current
                this.getAllData()
            },
            add() {
                this.type = 'add'
                this.showForm = true
            },
            save() {
                // 新增
                if (this.type === 'add') {
                    let sendData = Object.assign(this.formData,{
                        createUser: userInfo.userId
                    })
                    request.post(addApi,sendData).then(res => {
                        console.log(res)
                        if(res === true ) {
                            this.$Message.success('新增成功')
                            this.getAllData()
                        }
                    })
                // 修改
                }else if (this.type === 'modify') {
                    let sendData = Object.assign(this.formData,{
                        updateUser: userInfo.userId
                    })
                    request.post(updateApi,sendData).then(res => {
                        console.log(res)
                        if(res === true ) {
                            this.$Message.success('修改成功')
                            this.getAllData()
                        }
                    })
                }
            },
            // 获取所有出发地
            getAllDeparture() {
                // let queryData = {page: 1}
                let queryData = {
                    pageIndex: 1,
                    pageSize: 100
                }
                request.post(getAllDepartureApi,queryData).then(res => {
                    console.log('departureData',res)
                    this.departureData = res.data
                })
            },

            // 获取所有车型
            getAllCarModel() {
                // let queryData = {page: 1}
                let queryData = {
                    pageIndex: 1,
                    pageSize: 100
                }
                request.post(getAllCarModelApi,queryData).then(res => {
                    console.log('carModelData',res)
                    this.carModelData = res.data
                })
            }
        },
        watch: {
            showForm(val) {
                if (val == false) {
                    this.formData = {
                        departureInfoId: '',    // 出发地id
                        dest: '',               // 目的地
                        internalFee: '',        // 内部费用
                        marketFee: '',          // 市场价格
                        carModelId: '',         // 车型id
                        channel: '',            // 途径地
                        otherNote: ''           // 其他说明
                    }
                }
            }
        }
    }
</script>