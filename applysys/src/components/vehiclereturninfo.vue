<template>
    <div id="apply">
        <tableModel height="100%" @changePage="changePage" :columns='columns' :tableData="assignDate" :tableTitle="tableTitle" :pageOption="pageOption">
        </tableModel>
        <Modal id="car" :model="formData" v-model="showForm" width="80%" :title="fromTitle">
            <Card class="card">
                <!-- <div slot="title" style="font-weight:bold;font-size:16px;color:#000000;">
                    车辆回程数据
                </div>        -->
                <Form id="formInline" :model="tableData" :label-width="80">
                    <Row>
                        <Col>
                            <FormItem label="车牌号码" style="font-size:50px;font-weight:bold;">
                                <span class="carInput" style="width:100px;marginRight:400px;font-weight:bold;font-size:16px;color:#C00000" >{{tableData.licensePlate}}</span>
                                <span style="color:#C00000;font-weight:bold;">请核对车牌和以下信息，确定无误后再填写相类数据！！！</span>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10" >
                            <FormItem label="申请部门">
                                <span>{{tableData.applyDepart}}</span>
                                <!-- <Option v-for="item in factoryData" :value="item.id">{{item.factoryName}}</Option> -->
                            </FormItem>
                        </Col>
                        <Col span="5" offset="4">
                            <FormItem label="人数">
                                <span>{{tableData.number}}</span>
                            </FormItem>
                        </Col>
                        <Col span="5" >
                            <FormItem label="厂别">
                                <span>{{tableData.factoryName}}</span>
                            </FormItem>
                        </Col>
                        
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="申请人">
                                <span>{{tableData.applyUser}}</span>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="电话号码" offset="4">
                                <span>{{tableData.phone}}</span>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="5">
                            <FormItem label="使用日期">
                                <span>{{tableData.useDate}}</span>
                            </FormItem>
                        </Col>
                        <Col span="5">
                            <FormItem label="时间">
                                <span>{{tableData.useTime}}</span>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <FormItem label="目的地">
                                <span>{{tableData.dest}}</span>
                            </FormItem>
                        </Col>   
                    </Row>
                    <Row>
                        <FormItem label="审核意见">
                            <span>{{tableData.approvalOpinion}}</span>
                        </FormItem>
                    </Row>
                    
                    <Row>
                        <Col span="10">
                            <FormItem label="内部费用">
                                <span>{{tableData.internalFeeTotal}}</span>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="市场费用">
                                <span>{{tableData.marketFeeTotal}}</span>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="途径地">
                                <span>{{tableData.channel}}</span>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="司机电话">
                                <span>{{tableData.driverPhone}}</span>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="5">
                            <FormItem label="出发日期">
                                <Date-picker type="date" v-model="formData.carStartDate" placeholder="选择日期"  @on-change="startDate" style="width: 168px"></Date-picker>
                            </FormItem>
                        </Col>
                        <Col span="5" offset="">
                            <FormItem label="时间">
                                <Time-picker v-model="formData.carStartTime" @on-change="startTime" format="HH:mm" placeholder="选择时间" style="width: 150px"></Time-picker>
                            </FormItem>
                        </Col>
                        <Col span="5" offset="4">
                            <FormItem label="回车日期">
                                <Date-picker type="date" v-model="formData.carReturnDate" placeholder="选择日期"  @on-change="returnDate" style="width: 150px"></Date-picker>
                            </FormItem>
                        </Col>
                        <Col span="5" offset="">
                            <FormItem label="时间">
                                <Time-picker  v-model="formData.carReturnTime" @on-change="returnTime" format="HH:mm" placeholder="选择时间" style="width: 150px"></Time-picker>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="4">
                            <FormItem label="出发里程">
                                <Input v-model="formData.startMileage" type="text"></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="返回里程">
                                <Input v-model="formData.returnMileage" type="text"></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="油升数">
                                <Input v-model="formData.oilVolume" type="text"></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="过路/过桥费">
                                <Input v-model="formData.toll" type="text"></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="停车费">
                                <Input v-model="formData.parkingFee" type="text"></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="4">
                            <FormItem label="餐费">
                                <Input v-model="formData.mealFee" type="text"></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="高速度路费">
                                <Input v-model="formData.expresswayFee" type="text"></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="加班费">
                                <Input v-model="formData.overtime" type="text"></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="其它费用">
                                <!-- <Input v-model="formData.otherFee" type="text"></Input> -->
                                <Upload multiple action="//jsonplaceholder.typicode.com/posts/">
                                    <i-button type="ghost" icon="ios-cloud-upload-outline">上传文件</i-button>
                                </Upload>
                            </FormItem>
                            
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="其它说明">
                                <Input v-model="formData.remark" type="text"></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <div style="text-align:center">
                            <Button style="margin:10px 0" type="primary" size="large" @click="save">提交数据</Button>
                        </div>
                    </Row>
                </Form>
            </Card>

        </Modal>
    </div>
</template>

<script>

let getvehiclereturninfoApi = '/vehiclereturninfo/show_assign?id='
let createVehicleReturnApi = '/vehiclereturninfo/createVehicleReturn'
let driver_data_allApi = '/vehiclereturninfo/driver_data_all'

let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))

import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
import { setTimeout } from 'timers';
export default {
    name: 'vehiclereturninfo',
    data() {
        return {
            showForm: false,
            fromTitle: '回程数据填写',
            pageOption: {
            pageIndex: 1,
            total: 0,
            pageSize: 20
            },
            driverName:{
                driver_name: userInfo.userId,
            },
            tableData: {

            },
            assignDate: [],
            formData: {
                id: '',
                carStartDate: '',           // 出发日期
                carStartTime: '',           // 出发时间
                carReturnDate: '',          // 回程日期
                carReturnTime: '',          // 回程时间
                startMileage: '',           // 出发里程
                returnMileage: '',          // 返回里程
                oilVolume: '',              // 油升数
                toll: '',                   // 过路/过桥费
                parkingFee: '',             // 停车费
                expresswayFee: '',          // 高速路费
                overtime: '',               // 加班费
                mealFee: '',                // 餐费
                otherFee: '',               // 其他费用
                remark: '',                 // 其他说明
                userid: '',    // 当前获取的司机userid
                createUser: '',
            },
            tableTitle: '司机任务单',
            columns: [
                {
                    type: 'index',
                    title: '序号',
                    width: 80,
                    align: 'center'
                },{
                    title: '派车单号',
                    key: 'orderNo',
                    align: 'center'
                },{
                    title: '司机姓名',
                    key: 'driverName',
                    align: 'center'
                },{
                    title: '司机电话',
                    key: 'driverPhone',
                    align: 'center'
                },{
                    title: '车牌号',
                    key: 'licensePlate',
                    align: 'center'
                },{
                    title: '车型',
                    key: 'carModel',
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
                                        this.showForm = true
                                        let url = getvehiclereturninfoApi + params.row.id
                                        request.get(url).then(res => {
                                            console.log('res',res)
                                            this.rows = [res]
                                            console.log(this.rows)
                                            this.tableData = res
                                            console.log('tableData',this.tableData)
                                        })
                                    }
                                }
                            }, '填写回程数据')
                        ])
                    }
                }
            ],
            returnData: []
        }
    },
    components:{
        tableModel
    },
    mounted() {
        this.driver_data_all()
    },
    methods: {
        // 获取司机派车单
        // vehiclereturninfo() {
        //     request.post(getvehiclereturninfoApi,this.tableData).then(res =>  {
        //         console.log(res)
        //         this.tableData = res
        //     })
        // },
        // 获取司机所有派车任务单
        driver_data_all() {
            let sendData = Object.assign(this.pageOption,{
                tableData: this.driverName.driver_name
            })
            request.post(driver_data_allApi,sendData).then(res => {
                console.log(res)
                this.assignDate = res.data
                this.pageOption.total = res.total
            })
        },
        // 更换页码
        changePage(current) {
            this.pageOption.pageIndex = current
            this.getAllApproval()
        },
        // 创建车辆回程数据单
        save() {
            this.formData.id = this.tableData.id
            this.formData.userid = userInfo.userId
            this.formData.createUser = userInfo.user
            request.post(createVehicleReturnApi,this.formData).then(res => {
                console.log(res)
                if (res === true) {
                    this.$Message.success('申请成功')
                    this.tableData = {

                    },
                    this.formData = {
                        carStartDate: '',           // 出发日期
                        carStartTime: '',           // 出发时间
                        carReturnDate: '',          // 回程日期
                        carReturnTime: '',          // 回程时间
                        startMileage: '',           // 出发里程
                        returnMileage: '',          // 返回里程
                        oilVolume: '',              // 油升数
                        toll: '',                   // 过路/过桥费
                        parkingFee: '',             // 停车费
                        expresswayFee: '',          // 高速路费
                        overtime: '',               // 加班费
                        mealFee: '',                // 餐费
                        otherFee: '',               // 其他费用
                        remark: '',                 // 其他说明
                    },
                    this.showForm = false
                    this.driver_data_all()
                }else {
                    this.$Message.success('缺少数据')
                }
            })
        },
        startDate(date) {
            console.log(date)
            this.formData.carStartDate = date
            
        },
        startTime(start_Time) {
            console.log(start_Time)
            this.formData.carStartTime = start_Time
        },
        returnDate(date) {
            console.log(date)
            this.formData.carReturnDate = date
        },
        returnTime(return_Time) {
            console.log(return_Time)
            this.formData.carReturnTime = return_Time
        },
    },
    watch: {
        showForm(val) {
            if (val == false) {
                this.formData = {

                },
                this.tableData = {

                }
            }
        }
    },
}
</script>

<style lang="less" scoped>
#apply {
    background-color: #fff;
    height: 100%;
    padding-top: 40px;
    
    
    .card {
        width: 50%;
        // height: 60%;
        margin: 0 auto;
        margin-bottom: 10px;
    }
}
</style>

<style>
.ivu-form-item-content {
    text-align: left;
    
}
#apply .carInput .ivu-input{
    border: none;
    margin: 200 auto;
    color: #FF0000;
}
#apply .ivu-form-item {
    margin-bottom: 10px;
}
</style>
