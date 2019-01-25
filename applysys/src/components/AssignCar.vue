<template>
    <div id="approvalApply">
        <tableModel height="100%" @changePage="changePage" :columns='columns' @selectedRow="selectedRow" :tableData="approvalDate"  :tableTitle="tableTitle" :pageOption="pageOption">
            <div slot="addBtn" style="float:left;margin-right:5px">
                <Button type="primary" @click="adds">统一分派</Button>
            </div>
        </tableModel>
        <Modal id="car" :model="formData" v-model="showForm" width="80%" :title="fromTitle">
                <Form :drivermodel="DriverData" :cardatamodel="CarData" :label-width="80">
                <Card class="card" v-for="item in rows">
                    <Row>
                        <Col span="7">
                            <FormItem label="用车单号">
                                <Input :value="item.order_no" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="7" offset="1">
                            <FormItem label="厂别">
                                <Input :value="item.factory_name" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="7" offset="1">
                            <FormItem label="出发地">
                                <Input :value="item.departure" readonly>
                                </Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="7">
                            <FormItem label="申请人">
                                <Input :value="item.applyUser" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="7" offset="1">
                            <FormItem label="申请部门" >
                                <Input :value="item.applyDepart" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="7" offset="1">
                            <FormItem label="电话号码">
                                <Input :value="item.phone" readonly></Input>
                            </FormItem>
                        </Col> 
                    </Row>
                    <Row>
                        <Col span="7">
                            <FormItem label="人员数量">
                                <Input :value="item.number" readonly ></Input>
                            </FormItem>
                        </Col>
                        <Col span="7" offset="1">
                            <FormItem label="使用日期">
                                <Input :value="item.useDate" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="7" offset="1">
                            <FormItem label="使用时间">
                                <Input :value="item.useTime" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="7">
                            <FormItem label="车辆数量">
                                <Input :value="item.carNumber" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="7" offset="1">
                            <FormItem label="车型">
                                <Input :value="item.carModel" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="7" offset="1">
                            <FormItem label="目的地">
                                <Input :value="item.dest" readonly></Input>
                            </FormItem> 
                        </Col>
                    </Row>
                    <Row>
                        <FormItem label="申请事由">
                            <Input :value="item.applyCause" readonly></Input>
                        </FormItem>
                    </Row>
                    <Row>
                        <FormItem label="审核意见">
                            <Input :value="item.approvalOpinion" readonly ></Input>
                        </FormItem>
                    </Row>
                 </Card>
                    <Row>
                        <Col span="10">
                            <FormItem label='内部费用'>
                                <Input v-model="formData.internalFeeTotal"></Input>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="车辆途经地">
                                <Input v-model="formData.channel" readonly></Input>
                                
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="市场费用">
                                <Input v-model="formData.marketFeeTotal"></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label='出发日期'>
                                <!-- <Date-picker type="date" :value="formData.departureDate" format="yyyy-MM-DD" placeholder="请选择日期"></Date-picker> -->
                                <Date-picker type="date" v-model="formData.departureDate" placeholder="选择日期"  @on-change="dateTime" style="width: 200px"></Date-picker>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label='出发时间'>
                                <Time-picker v-model="formData.departureTime" @on-change="dateChange" format="HH:mm:ss" placeholder="选择时间" style="width: 168px"></Time-picker>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row :gutter="20">
                        <Col span="5">
                            <FormItem label='车牌号码'>
                                <i-select v-model="CarData.carInfoId" >
                                    <!-- style="width:200px" -->
                                    <Option v-for="item in carInfoData" :value="item.id">{{item.licensePlate}}</Option>
                                </i-select>
                            </FormItem>
                        </Col>
                        <Col span="5" >
                            <FormItem label='司机'>
                                <i-select v-model="DriverData.drivarId">
                                    <Option v-for="item in driverData" :value="item.id">{{item.name}}</Option>
                                </i-select>
                            </FormItem>
                        </Col>
                        <div style="text-align:right;margin-right:50px" >
                            <Button @click="addData">增加数据</Button>
                        </div>

                    </Row>
                        <i-table height="300" :columns="Carcolumns" :data="data1"></i-table>
                    <div style="text-align:center"> 
                        <Button style="margin:10px 0" type="primary" size="large" @click="save" v-model="formData.status">分派</Button>
                    </div>
                    
                </Form>
           
        </Modal>
    </div>
</template>

<script>

let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))

let getAllApprovalApi = '/apply/approval_pass'
let getcreateAssignApi = '/assign/createAssign'
let getApplyApi = '/apply/getApply?id='

let getAllCarInfoApi = '/carinfo/getAllCarInfo'
let getAllDriverApi = '/driver/getAllDriver'

import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
import { setTimeout } from 'timers';
export default {
    name: 'approvalApply',
    data() {
        return {
            showForm: false,
            fromTitle: '分派车辆',
            pageOption: {
                pageIndex: 1,
                total: 0,
                pageSize: 20
            },
            carpageOption: {
                pageIndex: 1,
                total: 0,
                pageSize: 10000
            },
            driverpageOption: {
                pageIndex: 1,
                pageSize: 10000,
                total: 0
            },
            approvalDate: [],
            carInfoData: [],
            driverData: [],
            formData: {
                apply_id: '',  // 用车单id
                destId: '',   // 目的地id
                channel: '',
                driver_id: '',  // 司机id
                carinfo_id: '',  // 车辆id 
                departureDate: '',  // 出发日期
                departureTime: '',  // 出发时间
                createUser: userInfo.name,  // 创建人
                internalFeeTotal: '',  //内部费用总和
                marketFeeTotal: '',  //市场价格费用总和
                // userId: 'manager8217',  // 用户id

            },
            CarData: {
                licensePlate: '',
                carModel: '',
                carInfoId: '',
                remark: ''
            },
            DriverData: {
                name: '',
                phone: '',
                drivarId: ''
            },
            Carcolumns:[
                {
                    type: 'index',
                    title:'序号',
                    width: 80,
                    align: 'center'
                },{
                    title: '车牌号码',
                    key: 'licensePlate',
                    align: 'center'
                },{
                    title: '车型',
                    key: 'carModel',
                    align: 'center'
                },{
                    title: '司机姓名',
                    key: 'name',
                    align: 'center'
                },{
                    title: '电话号码',
                    key: 'phone',
                    align: 'center'
                },{
                    title: '操作',
                    key: 'action',
                    align: 'center',
                    render: (h,params) => {
                        return h('Icon',{
                            props: {
                                "type": "md-trash",
                                "color": '#ed4014',
                                "size" : 15
                            },
                            on: {
                                click: ()=> {
                                    console.log(params)
                                    this.data1.splice(params.index,1)
                                    console.log(params)
                                    // this.remove(params.index)
                                }
                            }
                        })
                    }
                }
            ],
            data1: [],
            type: 'add',
            tableTitle: '分派车单',
            columns: [
                {
                        type: 'selection',
                        width: 60,
                        align: 'center'
                    },
                {
                    type: 'index',
                    title: '序号',
                    width: 80,
                    align: 'center'
                },{
                    title: '用车单号',
                    key: 'order_no',
                    align: 'center'
                },{
                    title: '申请人',
                    key: 'applyUser',
                    align: 'center'
                },{
                    title: '电话号码',
                    key: 'phone',
                    align: 'center'
                },{
                    title: '申请日期',
                    key: 'applyDate',
                    align: 'center'
                },{
                    title: '使用日期',
                    key: 'useDate',
                    align: 'center'
                },{
                    title: '车型',
                    key: 'carModel',
                    align: 'center'
                },{
                    title: '申请事由',
                    key: 'applyCause',
                    align: 'center'
                },{
                    title: '目的地',
                    key: 'dest',
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
                                        let url = getApplyApi + params.row.id
                                        request.get(url).then(res => {
                                            console.log('res',res)
                                            this.rows = [res]
                                            console.log(this.rows)
                                            this.formData = res
                                            console.log('点击分派',this.formData)
                                        })
                                    }
                                }
                            }, '分派车辆')
                        ])
                    },
                }

            ],
            rows: [],
            tableData: [],
            carData: [],
            driverData: []
        }
    },
    components: {
        tableModel
    },
    mounted() {
        this.getAllApproval()
        this.getAllCarInfo()
        this.getAllDriver()
        
 
    },
    methods: {
        // 获取所有已审核通过的用车单
        getAllApproval() {
            request.post(getAllApprovalApi,this.pageOption).then(res =>  {
                console.log(res)
                
                this.approvalDate = res.data
                this.pageOption.total = res.total
            })
        },

        // 获取所有车辆资料
        getAllCarInfo() {
            request.post(getAllCarInfoApi,this.carpageOption).then(res => {
                // console.log(res)
                this.carInfoData = res.data
                this.pageOption.total = res.total
            })
        },
        // 获取所有司机资料
        getAllDriver() {
            request.post(getAllDriverApi,this.driverpageOption).then(res => {
                // console.log(res)
                this.driverData = res.data
                this.pageOption.total = res.total
            })
        },
        // 更换页码
        changePage(current) {
            this.pageOption.pageIndex = current
            this.getAllApproval()
        },

        add() {
            this.showForm = true
            this.type = 'add'
        },
        // 遍历车牌、司机数据加入表格
        addData() {
            let DriverData = {}
            this.driverData.forEach(item => {
                if (item.id === this.DriverData.drivarId) {
                    DriverData = item
                    DriverData.driver_id = item.id
                    
                }
            })
            let CarData = {}
            this.carInfoData.forEach(item => {
                if (item.id === this.CarData.carInfoId) {
                    CarData = {
                        licensePlate: item.licensePlate,
                        carModel: item.carModel,
                        remark: item.remark,
                        carId: item.id
                    }
                }
            })
            this.CarData.carInfoId = ''
            this.DriverData.drivarId = ''
            let newObj = Object.assign(DriverData,CarData)
            this.data1.push(newObj)
            
        },
        save() {
            let ids = [];
            this.rows.forEach(item => {
                ids.push(item.id)
            })
            let datas = {
                id: ids.join(),
                details: JSON.stringify(this.data1),
                internalFeeTotal:this.formData.internalFeeTotal,
                marketFeeTotal: this.formData.marketFeeTotal,
                departureDate: this.formData.departureDate,
                departureTime: this.formData.departureTime,
                createUser: this.formData.createUser,
                // updateUser: this.formData.updateUser,
                destId: this.formData.destId,

            }
            request.post(getcreateAssignApi,datas).then(res => {
                console.log('datas', datas)
                if (res === true) {
                    this.$Message.success('分派成功')
                    this.getAllApproval()
                    this.showForm = false
                    this.data1 = []
                }
            })
        },
        dateChange(dateTime) {
            this.formData.departureTime = dateTime
        },
        dateTime(useDate) {
            console.log(useDate)
            this.formData.departureDate = useDate
        },
        selectedRow(rows) {
            this.selectedRow = rows
        },
        adds() {
            this.showForm = true;
            this.rows = this.selectedRow
            this.formData = this.rows[0]
            console.log(this.formData )
        }

    },
    watch: {
        showForm(val) {
            if (val == false) {
                // this.formData = {
                    
                // },
                this.CarData = {

                },
                this.DriverData = {

                }
            }
        }
    },
}
</script>

<style lang="less" scoped>
#approvalApply {
    background-color: #fff;
    height: 100%;
    // padding-top: 40px;
    .card {
        width: 70%;
        margin: 0 auto;
    }
}
</style>

<style>
.ivu-form-item-content {
    text-align: left
}
#car .ivu-modal-footer {
    display: none;
}
.ivu-form-item {
    margin-bottom: 10px;
}
</style>




