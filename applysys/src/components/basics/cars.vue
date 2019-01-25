<template>
    <div id="cars" style="height: 100%">
        <tableModel :columns='columns' @changePage="changePage" :tableData="tableData" :tableTitle="tableTitle" :pageOption="pageOption">
             <Button slot="addBtn" @click="add">
                <Icon type="ios-add" /> 新增
            </Button>
        </tableModel>
        
        <Modal v-model="showForm" :title="fromTitle" @on-ok="save" >
            <Form :model="formData" :label-width="100">
                <FormItem label="厂别">
                    <Select v-model="formData.factoryId" placeholder="请选择厂别">
                        <Option v-for="item in factoryData" :value="item.id">{{item.factoryName}}</Option>
                    </Select>
                </FormItem>
                <FormItem label="车型">
                    <Select v-model="formData.carModelId" placeholder="请选择车型">
                        <Option v-for="item in carModelData" :value="item.id">{{item.carModel}}</Option>
                    </Select>
                </FormItem>
                <FormItem label="车牌号码">
                    <Input v-model="formData.licensePlate" placeholder="请输入车牌号码"></Input>
                </FormItem>
                <FormItem label="固定司机">
                    <Select v-model="formData.driverId" placeholder="请选择固定司机">
                        <Option v-for="item in driverData" :value="item.id">{{item.name}}</Option>
                    </Select>
                </FormItem>
                <FormItem label="核载人数">
                    <Input v-model="formData.number" placeholder="请输入核载人数"></Input>
                </FormItem>
                <FormItem label="车辆百公里油耗">
                    <Input v-model="formData.carFuel" placeholder="请输入车辆百公里油耗"></Input>
                </FormItem>
                <FormItem label="车辆超公里数">
                    <Input v-model="formData.extraKm" placeholder="请输入车辆超公里数"></Input>
                </FormItem>
                <FormItem label="超公里单价">
                    <Input v-model="formData.extraKmPrice" placeholder="请输入超公里单价"></Input>
                </FormItem>
                <FormItem label="其他说明">
                    <Input v-model="formData.remark" placeholder="请输入其他说明"></Input>
                </FormItem>
            </Form>
        </Modal>
    </div>
</template>

<script>

let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))

let getAllCarApi = '/carinfo/getAllCarInfo'
let getCarByIdApi = '/carinfo/getCarInfo?id='
let addCarApi = '/carinfo/createdateCarInfo'
let updateCarApi = '/carinfo/updateCarInfo'
let deleteCarApi = '/carinfo/deleteCarInfo?id='

let getAllFactoryApi = '/factory/getAllFactory'
let getAllCarModelApi = '/carmodel/getAllCarModel'
let getAllDriverApi = '/driver/getAllDriver'

import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
import { setTimeout } from 'timers';
    export default {
        name: 'cars',
        components: {
            tableModel
        },
        data() {
            return {
                fromTitle: '新增车辆',
                showForm: false,
                type: 'add',
                tableTitle: '车辆基础资料',
                pageOption: {
                    pageIndex: 1,
                    total: 0,
                    pageSize: 20
                },
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
                        width: 200
                    },{
                        title: '车牌号',
                        key: 'licensePlate',
                        align: 'center',
                        width: 150
                    },{
                        title: '车型',
                        key: 'carModel',
                        align: 'center',
                        width: 100
                    },{
                        title: '核载人数',
                        key: 'number',
                        align: 'center',
                        width: 100
                    },{
                        title: '固定司机',
                        key: 'driverName',
                        align: 'center',
                        width: 100
                    },{
                        title: '电话号码',
                        key: 'driverPhone',
                        align: 'center',
                        width: 150
                    },{
                        title: '车辆百公里油耗',
                        key: 'carFuel',
                        align: 'center',
                        width: 150
                    },{
                        title: '其他说明',
                        key: 'remark',
                        align: 'center',
                        width: 200
                    },{
                        title: '车辆超公里数',
                        key: 'extraKm',
                        align: 'center',
                        width: 150
                    },{
                        title: '超公里单价',
                        key: 'extraKmPrice',
                        align: 'center',
                        width: 150
                    },{
                        title: '操作',
                        key: 'action',
                        align: 'center',
                        width: 150,
                        fixed: 'right',
                        render: (h,params) => {
                            return h('div',[
                                h('Button',{
                                    props: {
                                        type: 'info',
                                        size: 'small',
                                    },
                                    on: {
                                        click: () => {
                                            console.log('modify')
                                            this.showForm = true
                                            this.type = 'modify'
                                            let url = getCarByIdApi + params.row.id
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
                                                    let url = deleteCarApi + params.row.id
                                                    request.get(url).then(res => {
                                                        // console.log(res)
                                                        if (res === true ) {
                                                            this.$Message.success('删除成功')
                                                            this.getCarData()
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
                    factoryId: '',          // 厂别id
                    licensePlate: '',       // 车牌号码
                    carModelId: '',         // 车型id
                    number: '',             // 核载人数
                    driverId: '',           // 固定司机id
                    carFuel: '',            // 车辆百公里油耗
                    extraKm: '',            // 车辆超公里数
                    extraKmPrice: '',       // 超公里单价
                    remark: '',             // 其它说明
                    createUser: '',         // 创建人
                    updateUser: '',         // 修改人
                },
                factoryData: [],
                carModelData: [],
                driverData: []
            }
        },
        mounted() {
            // this.getCarData()

            // let _this = this
            // setTimeout(() => {
            //     _this.getAllFactory()
            //     _this.getAllCarModel()
            //     _this.getAllDriver()
            // },600)
            this.getCarData()
            this.getAllFactory()
            this.getAllCarModel()
            this.getAllDriver()

            // let url = '/deleteRewardGood?id=18'
            // let url2 = '/getRewardList/'
            // request.delete(url).then(res => {
            //     console.log(res)
            //     request.post(url2,{
            //         pageSize: 1,
            //         pageIndex: 1
            //     }).then(res => {
            //         console.log(res)
            //     })
            // })
        },
        methods: {
            // 获取所有厂别
            getAllFactory() {
                // let queryData = {
                //     page: 1
                // }
                request.post(getAllFactoryApi,this.pageOption).then(res => {
                    console.log(res)
                    this.factoryData = res.data
                })
            },
            // 获取所有车型
            getAllCarModel() {
                // let queryData = {
                //     page: 1
                // }
                request.post(getAllCarModelApi,this.pageOption).then(res => {
                    console.log(res)
                    this.carModelData = res.data
                }) 
            },
            // 获取所有司机
            getAllDriver() {
                // let queryData = {
                //     page: 1
                // }
                request.post(getAllDriverApi,this.pageOption).then( res => {
                    console.log(res)
                    this.driverData = res.data
                })
            },
            // 获取数据
            getCarData() {
                // let queryData = {
                //     page: this.pageOption.current
                // }
                request.post(getAllCarApi,this.pageOption).then(res => {
                    // console.log('data',res)
                    this.tableData = res.data
                    this.pageOption.total = res.total
                })
            },
            // 新增按钮
            add() {
                this.showForm = true
                this.type = 'add'
            },
            save() {
                if (this.type === 'add') {
                    let sendData = Object.assign(this.formData,{
                        createUser: userInfo.userId
                    })
                    request.post(addCarApi,sendData).then( res => {
                        console.log(res)
                        if (res === true ) {
                            this.$Message.success('新增成功')
                            this.getCarData()
                        }
                    })
                }else if (this.type === 'modify') {
                    let sendData = Object.assign(this.formData,{
                        updateUser: userInfo.userId
                    })
                    request.post(updateCarApi,sendData).then( res => {
                        console.log(res)
                        if (res === true ) {
                            this.$Message.success('修改成功')
                            this.getCarData()
                        }
                    })
                }
            },
            // 改变页码
            changePage(current) {
                this.pageOption.pageIndex = current
                this.getCarData()
            }
        },
        watch: {
            showForm(val) {
                if (val == true) {
                    
                    this.formData = {
                        factoryId: '',          // 厂别id
                        licensePlate: '',       // 车牌号码
                        carModelId: '',         // 车型id
                        number: '',             // 核载人数
                        driverId: '',           // 固定司机id
                        carFuel: '',            // 车辆百公里油耗
                        extraKm: '',            // 车辆超公里数
                        extraKmPrice: '',       // 超公里单价
                        remark: ''              // 其它说明
                    }
                }
            }
        }
    }
</script>