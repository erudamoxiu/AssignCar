<template>
    <div id="apply">
        </tableModel>
        <Card class="card">
            <div slot="title">
                用车申请单
            </div>       
            <Form id="formInline" :model="formData" :label-width="60">
                <Row>
                    <Col span="10">
                        <FormItem label="厂别">
                            <Select v-model="formData.factoryId">
                                <Option v-for="item in factoryData" :value="item.id">{{item.factoryName}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="10" offset="4">
                        <FormItem label="出发地">
                            <Select v-model="formData.departureInfoId">
                                <Option v-for="item in departureData" :value="item.id">{{item.departure}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    
                </Row>
                <Row>
                    <Col span="10">
                        <FormItem label="申请人">
                            <!--<Button>选择申请人</Button> -->
                            <Input v-model="formData.name"></Input>
                        </FormItem>
                    </Col>
                    <Col span="10" offset="4">
                        <FormItem label="申请部门" offset="4">
                            <!--<Button>选择申请部门</Button> -->
                            <Input v-model="formData.applyDepart"></Input>
                        </FormItem>
                    </Col>
                </Row>
                <Row>
                    <Col span="10">
                        <FormItem label="电话号码">
                            <Input v-model="formData.phone" placeholder="请输入电话号码"></Input>
                        </FormItem>
                    </Col>   
                    <Col span="10"   offset="4">
                        <FormItem label="人员数量">
                            <InputNumber v-model="formData.number"></InputNumber>
                        </FormItem>
                    </Col>
                    
                </Row>
                <Row>
                    <Col span="10">
                        <FormItem label="使用日期">
                            <Date-picker type="date" v-model="formData.useDate" placeholder="选择日期"  @on-change="changeUseData" style="width: 200px"></Date-picker>
                        </FormItem>
                    </Col>
                    <Col span="10" offset="4">
                        <FormItem label="使用时间">
                            <Time-picker v-model="formData.useTime" @on-change="dateChange" format="HH:mm:ss" placeholder="选择时间" style="width: 168px"></Time-picker>
                        </FormItem>
                    </Col>
                </Row>
                <Row>
                    <Col span="10">
                        <FormItem label="车辆数量">
                            <InputNumber v-model="formData.carNumber"></InputNumber>
                        </FormItem>
                    </Col>
                    <Col span="10" offset="4">
                        <FormItem label="车型">
                            <Select v-model="formData.carModelId">
                                <Option v-for="item in carModeData" :value="item.id">{{item.carModel}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                </Row>
                <Row>
                    <FormItem label="目的地">
                        <Select v-model="formData.destId" filterable not-found-text="新增目的地">
                            <Option v-for="item in destData" :value="item.id">{{item.dest}}</Option>
                        </Select>
                    </FormItem>
                </Row>
                <Row>
                    <FormItem label="">
                        <Input v-model="formData.destname" placeholder="如果上面选择框班里面没有需要的数据，请在这里输入数据" ></Input>
                    </FormItem>
                </Row>
                <Row>
                    <FormItem label="申请事由">
                        <Input v-model="formData.applyCause" placeholder="请输入申请事由" ></Input>
                    </FormItem>
                </Row>

                <Button style="margin:10px 0" type="primary" size="large" @click="save">
               立即申请
                </Button>
            </Form>
        </Card>
    </div>
</template>

<script>

let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))


let addApplyApi = '/apply/createdateApply'
let getAllDepartureApi = '/departureinfo/getAllDeparture'
let getAllCarModelApi = '/carmodel/getAllCarModel'
let getAllFactoryApi = '/factory/getAllFactory'
let getAllDestFeeApi = '/destfee/getAllDestFee'

import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
import { setTimeout } from 'timers';
export default {
    name: 'apply',
    data() {
        return {
            pageOption: {
            pageIndex: 1,
            total: 0,
            pageSize: 20
            },
            factoryData: [],
            carModeData: [],
            departureData: [],
            destData: [],
            

            formData: {
                factoryId: '',                  // 厂别id
                applyDepart: '',                // 申请部门
                name: '',                  // 申请人
                departureInfoId: '',            // 出发地id
                number: 1,                      // 人员数量
                useDate: '',                    // 使用日期
                useTime: '',                    // 使用时间
                phone: '',                      // 电话号码
                carNumber: 1,                  // 车辆数量
                carModelId: '',                 // 车型id
                destId: '',                     // 目的地id
                applyCause: '' ,                 // 申请事由
                destname: '',
                userid: '',
                destname: ''                    // 可选
            },
        }
    },
    mounted() {
        this.getAllFactory()
        this.getAllCarModel()
        this.getAllDestFee()
        this.getAllDeparture()
        // this.addUser()

        this.formData.name = userInfo.name
        this.formData.userid = userInfo.userId
    },
    methods: {
        // 获取所有厂别
        getAllFactory() {
            request.post(getAllFactoryApi,this.pageOption).then(res =>  {
                console.log(res)
                this.factoryData = res.data
            })
        },
        // 获取所有车型
        getAllCarModel() {
            request.post(getAllCarModelApi,this.pageOption).then(res => {
                console.log(res)
                this.carModeData = res.data
            })
        },
        // 获取所有出发地
        getAllDeparture() {
            request.post(getAllDepartureApi,this.pageOption).then(res => {
                console.log(res)
                this.departureData = res.data
            })
        },
        // 获取所有目的地
        getAllDestFee() {
            request.post(getAllDestFeeApi,this.pageOption).then(res => {
                console.log(res)
                this.destData = res.data
            })
        },
        // 申请用车按钮
        add() {
            this.showForm = true
            this.type = 'add'
        },
        save() {
            request.post(addApplyApi,this.formData).then(res => {
                console.log(res)
                if (res === true) {
                    this.$Message.success('申请成功')
                    this.showForm = false
                    this.formData = {
                    factoryId: '',                  // 厂别id
                    applyDepart: '',                // 申请部门
                    name: '',                       // 申请人
                    departureInfoId: '',            // 出发地id
                    number: '',                     // 人员数量
                    useDate: '',                    // 使用日期
                    useTime: '',                    // 使用时间
                    phone: '',                      // 电话号码
                    carNumber: '',                  // 车辆数量
                    carModelId: '',                 // 车型id
                    destId: '',                     // 目的地id
                    applyCause: '',                 // 申请事由
                    destname: '',                   // 目的地名字
                    userid: ''                      
                }
                }
            })
        },
        dateChange(dateTime) {
            console.log(dateTime)
            this.formData.useTime = dateTime
        },
        changeUseData(date) {
            console.log(date)
            this.formData.useDate = date
        },
    },
    watch: {
        showForm(val) {
            if (val == false) {
                this.formData = {
                    factoryId: '',                  // 厂别id
                    applyDepart: '',                // 申请部门
                    name: '',                  // 申请人
                    departureInfoId: '',            // 出发地id
                    number: 1,                      // 人员数量
                    useDate: '',                    // 使用日期
                    useTime: '',                    // 使用时间
                    phone: '',                      // 电话号码
                    carNumber: 1,                  // 车辆数量
                    carModelId: '',                 // 车型id
                    destId: '',                     // 目的地id
                    applyCause: '',
                    destname: ''
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
        width: 80%;
        margin: 0 auto;
    }
}
</style>

<style>
.ivu-form-item-content {
    text-align: left
}
</style>



