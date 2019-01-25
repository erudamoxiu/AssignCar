<template>
    <div id="approvalApply">
        <tableModel height="100%" @changePage="changePage" :columns='columns' :tableData="approvalDate" :tableTitle="tableTitle" :pageOption="pageOption">
        </tableModel>

        <Modal id="car" v-model="showForm" width="80%" :title="fromTitle">
            <Card class="card">
                      
                <Form :model="formData" :label-width="80">
                    <Row>
                        <Col span="10">
                            <FormItem label="派车单号">
                                <Input v-model="formData.orderNo" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="厂别">
                                <Input v-model="formData.factoryName" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="出发地">
                                <Input v-model="formData.departure" readonly>
                                </Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="申请人">
                                <Input v-model="formData.applyUser" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="申请部门" offset="4">
                                <Input v-model="formData.applyDepart" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="电话号码">
                                <Input v-model="formData.phone" readonly></Input>
                            </FormItem>
                        </Col>   
                        <Col span="10"   offset="4">
                            <FormItem label="申请事由">
                                <Input v-model="formData.applyCause" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="目的地">
                                <Input v-model="formData.dest" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="乘座人数">
                                <Input v-model="formData.number" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="司机">
                                <Input v-model="formData.driverName" readonly></Input>
                            </FormItem>
                        </Col>   
                        <Col span="10"   offset="4">
                            <FormItem label="电话号码">
                                <Input v-model="formData.driverPhone" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="车牌">
                                <Input v-model="formData.licensePlate" readonly></Input>
                            </FormItem>
                        </Col>   
                        <Col span="10"   offset="4">
                            <FormItem label="车型">
                                <Input v-model="formData.carModel" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="出车日期">
                                <Input v-model="formData.carStartDate" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="出车时间">
                                <Input v-model="formData.carStartTime" readonly></Input>
                                
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="回车日期">
                                <Input v-model="formData.carReturnDate" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="回车时间">
                                <Input v-model="formData.carReturnTime" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                 
                    <Row>
                        <span></span>
                    </Row>
                    <Row>
                        <Col span="4">
                            <FormItem label="出发里程">
                                <Input v-model="formData.startMileage" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="返回里程">
                                <Input v-model="formData.returnMileage" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="油升数">
                                <Input v-model="formData.oilVolume" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="过路/过桥费">
                                <Input v-model="formData.toll" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="停车费">
                                <Input v-model="formData.parkingFee" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="4">
                            <FormItem label="餐费">
                                <Input v-model="formData.mealFee" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="高速度路费">
                                <Input v-model="formData.expresswayFee" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="加班费">
                                <Input v-model="formData.overtime" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="其它费用">
                                <Input v-model="formData.otherFee" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="4" offset='1'>
                            <FormItem label="其它说明">
                                <Input v-model="formData.remark" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <FormItem label="审核意见">
                                <Input v-model="formData.approvalExplanation" placeholder="请输入审核意见" ></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <!-- <Row>
                        <Col span="10" offset="4">
                            <FormItem label="审核意见">
                                <Input v-model="formData.approvalOpinion" placeholder="请输入审核意见" ></Input>
                            </FormItem>
                        </Col>
                    </Row> -->

                    <div style="text-align:center"> 
                        <Button style="margin:10px 0" type="primary" size="large" @click="save" v-model="formData.status">同意</Button>
                        <Button style="margin:10px 0" type="primary" size="large" @click="refusal" v-model="formData.status">拒绝</Button>
                    </div>
                    
                </Form>
            </Card>
        </Modal>
    </div>
</template>

<script>


let getAllApprovalApi = '/vehiclereturninfo/getAllVehicleReturn'
let updateReturnApi = '/vehiclereturninfo/in_approval'
let getReturnApi = '/vehiclereturninfo/getVehicleReturn?id='


import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
import { setTimeout } from 'timers';


let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))
export default {
    name: 'approvalApply',
    data() {
        return {
            showForm: false,
            fromTitle: '用车审核单',
            pageOption: {
                pageIndex: 1,
                total: 0,
                pageSize: 20
            },
            approvalDate: [],
            formData: {
                updateUser: userInfo.name,
            },
            type: 'add',
            tableTitle: '车辆回程单',
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
                    title: '车牌号码',
                    key: 'licensePlate',
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
                                        let url = getReturnApi + params.row.id
                                        request.get(url).then(res => {
                                            console.log('res',res)
                                            this.formData = res
                                            
                                        })
                                    }
                                }
                            }, '审核')
                        ])
                    },
                }

            ],
            tableData: []
        }
    },
    components: {
        tableModel
    },
    mounted() {
        this.getAllApproval()
        
 
    },
    methods: {
        // 获取所有未审核派车单
        getAllApproval() {
            request.post(getAllApprovalApi,this.pageOption).then(res =>  {
                console.log(res)
                this.approvalDate = res.data
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
        save() {
            this.formData.status='1'
            this.formData.approvalUser = userInfo.name        
            request.post(updateReturnApi,this.formData).then(res => {
                console.log(this.formData)
                console.log(res)
                if (res === true) {
                    this.$Message.success('审核成功')
                    this.getAllApproval()
                    this.showForm = false
                }else {
                    this.$Message.success('缺少参数')
                }
            })
        },
        refusal() {
            this.formData.status='2'
            this.formData.approvalUser = userInfo.name         // 假数据
            console.log(this.formData)
            request.post(updateReturnApi,this.formData).then(res => {
                console.log(res)
                console.log(this.formData)
                if (res === true) {
                    this.$Message.success('审核成功')
                    this.getAllApproval()
                    this.showForm = false
                }
            })
        },

    },
    watch: {
        showForm(val) {
            if (val == true) {
                this.formData = {

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
        width: 80%;
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
</style>
