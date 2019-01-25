<template>
    <div id="approvalApply">
        <tableModel height="100%" @changePage="changePage" :columns='columns' :tableData="approvalDate" :tableTitle="tableTitle" :pageOption="pageOption">
        </tableModel>

        <Modal id="car" v-model="showForm" width="80%" :title="fromTitle">
            <Card class="card">
                      
                <Form :model="formData" :label-width="80">
                    <Row>
                        <Col span="10">
                            <FormItem label="用车单号">
                                <Input v-model="formData.order_no" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="厂别">
                                <Input v-model="formData.factory_name" readonly></Input>
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
                                <!--<Button>选择申请人</Button> -->
                                <Input v-model="formData.applyUser" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="申请部门" offset="4">
                                <!--<Button>选择申请部门</Button> -->
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
                            <FormItem label="人员数量">
                                <Input v-model="formData.number" readonly></Input>
                            </FormItem>
                        </Col>
                        
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="使用日期">
                                <Input v-model="formData.useDate" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="使用时间">
                                <Input v-model="formData.useTime" readonly></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="10">
                            <FormItem label="车辆数量">
                                <Input v-model="formData.carNumber" readonly></Input>
                            </FormItem>
                        </Col>
                        <Col span="10" offset="4">
                            <FormItem label="车型">
                                <Input v-model="formData.carModel" readonly></Input>
                                
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <FormItem label="目的地">
                            <Input v-model="formData.dest" readonly></Input>
                        </FormItem>
                    </Row>
                    <Row>
                        <FormItem label="申请事由">
                            <Input v-model="formData.applyCause" readonly></Input>
                        </FormItem>
                    </Row>
                    <Row>
                        <FormItem label="审核意见">
                            <Input v-model="formData.approvalOpinion" placeholder="请输入审核意见" ></Input>
                        </FormItem>
                    </Row>

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

let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))

let getAllApprovalApi = '/apply/approval_apply_all'
let updateApplyApi = '/apply/approval_apply'
let getApplyApi = '/apply/getApply?id='


import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
import { setTimeout } from 'timers';
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
                order_no: '',
                factory_name: '',
                departure: '',
                applyUser: '',
                applyDepart: '',
                phone: '',
                number: '',
                useDate: '',
                useTime: '',
                carNumber: '',
                carModel: '',
                dest: '',
                applyCause: '',
                approvalOpinion: '',
                updateUser: '',

            },
            type: 'add',
            tableTitle: '用车审核单',
            columns: [
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
        // 获取所有未审核用车单
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
            this.formData.updateUser = userInfo.name
            request.post(updateApplyApi,this.formData).then(res => {
                console.log(res)
                if (res === true) {
                    this.$Message.success('审核成功')
                    this.getAllApproval()
                    this.showForm = false
                }
            })
        },
        refusal() {
            this.formData.status='2'
            this.formData.updateUser = userInfo.name
            request.post(updateApplyApi,this.formData).then(res => {
                console.log(res)
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
                    // factoryId: '',                  // 厂别id
                    // applyDepart: '',                // 申请部门
                    // name: '',                  // 申请人
                    // departureInfoId: '',            // 出发地id
                    // number: '',                      // 人员数量
                    // useDate: '',          // 使用日期
                    // useTime: '',                    // 使用时间
                    // phone: '',                      // 电话号码
                    // carNumber: '',                  // 车辆数量
                    // carModelId: '',                 // 车型id
                    // destId: '',                     // 目的地id
                    // applyCause: '',
                    // destname: ''
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




