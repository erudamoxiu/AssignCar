<template>
    <div id="apply">
        </tableModel>
        <Card class="card">
            <div slot="title">
                用车申请单
            </div>       
            <Form id="formInline" :model="formData" :label-width="80" :rules="formRules" ref="forms" >
                <Row>
                    <Col span="10">
                        <FormItem label="厂别" prop="factoryId">
                            <Select v-model="formData.factoryId">
                                <Option v-for="item in factoryData" :value="item.id">{{item.factoryName}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="10" offset="4">
                        <FormItem label="出发地" prop="departureInfoId">
                            <Select v-model="formData.departureInfoId">
                                <Option v-for="item in departureData" :value="item.id">{{item.departure}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    
                </Row>
                <Row>
                    <Col span="10">
                        <FormItem label="申请人" prop="name">
                            <!--<Button>选择申请人</Button> -->
                            <Input v-model="formData.name"></Input>
                        </FormItem>
                    </Col>
                    <Col span="10" offset="4">
                        <FormItem label="申请部门" offset="4" prop="applyDepart">
                            <!--<Button>选择申请部门</Button> -->
                            <Input v-model="formData.applyDepart"></Input>
                        </FormItem>
                    </Col>
                </Row>
                <Row>
                    <Col span="10">
                        <FormItem label="手机号码" prop="phone">
                            <Input v-model="formData.phone" placeholder="请输入手机号码"></Input>
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
                        <FormItem label="使用日期" prop="useDate" required>
                            <Date-picker type="date" v-model="formData.useDate" placeholder="选择日期" format="yyyy-MM-dd"  @on-change="changeUseData" style="width: 200px"></Date-picker>
                        </FormItem>
                    </Col>
                    <Col span="10" offset="4">
                        <FormItem label="使用时间" prop="useTime" required>
                            <Time-picker v-model="formData.useTime" @on-change="dateChange" format="HH:mm" placeholder="选择时间" style="width: 168px"></Time-picker>
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
                        <FormItem label="车型" prop="carModelId">
                            <Select v-model="formData.carModelId">
                                <Option v-for="item in carModeData" :value="item.id">{{item.carModel}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                </Row>
                <Row>
                    <FormItem label="目的地" prop="message">
                        <AutoComplete v-model="message" filterable  @on-change="handleSearch1" @on-select="sekected" not-found-text="新增目的地">
                            <Option v-for="item in data2" :value="item.id">{{item.dest}}</Option>
                        </AutoComplete>
                    </FormItem>
                </Row>
                <Row>
                    <FormItem label="申请事由" prop="applyCause">
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
import { format } from '@/common/js/format.js'
export default {
    name: 'apply',
    data() {
        let validatePass = (rule, value, callback) => {
            if (this.message == '') {
                 callback(new Error('请输入目的地'));
            }else {
                callback();
            }
        }
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
            data2: [],
            message: '',
            formData: {
                factoryId: '',                  // 厂别id
                applyDepart: '',                // 申请部门
                name: '',                       // 申请人
                departureInfoId: '',            // 出发地id
                number: 1,                      // 人员数量
                useDate: new Date(),            // 使用日期
                useTime: '',                    // 使用时间
                phone: '',                      // 电话号码
                carNumber: 1,                   // 车辆数量
                carModelId: '',                 // 车型id
                destId: '',                     // 目的地id
                applyCause: '' ,                // 申请事由
                destname: '',
                userid: '',
                destname: ''                    // 可选
            },
            formRules: {
                factoryId: [
                    { type:'number',required: true, message: '请选择厂别', trigger: 'change' }
                ],
                message: [
                    { required: true, validator: validatePass, trigger: 'blur' }
                ],
                departureInfoId: [
                    { type:'number',required: true, message: '请选择出发地', trigger: 'change' }
                ],
                phone: [
                    { required: true, message: '请输入手机号码', trigger: 'blur' }
                ],
                carModelId: [
                    { type:'number',required: true, message: '请选择车型', trigger: 'change' }
                ],
                applyCause: [
                    { required: true, message: '请输入申请事由', trigger: 'blur' }
                ],
                name: [
                    { required: true, message: '请输入姓名', trigger: 'blur' }
                ],
                applyDepart: [
                    { required: true, message: '请输入部门', trigger: 'blur' }
                ],
                useTime: [
                    { type:'date',required: true, message: '请选择使用时间', trigger: 'change' }
                ],
            }
        }
    },
    mounted() {
        this.getAllFactory()
        this.getAllCarModel()
        this.getAllDestFee()
        this.getAllDeparture()

        this.formData.name = userInfo.name
        this.formData.applyDepart = userInfo.departmentName
        this.formData.userid = userInfo.userId
    },
    methods: {
        // 获取所有厂别
        getAllFactory() {
            request.post(getAllFactoryApi,this.pageOption).then(res =>  {
                this.factoryData = res.data
            })
        },
        // 获取所有车型
        getAllCarModel() {
            request.post(getAllCarModelApi,this.pageOption).then(res => {
                this.carModeData = res.data
            })
        },
        // 获取所有出发地
        getAllDeparture() {
            request.post(getAllDepartureApi,this.pageOption).then(res => {
                this.departureData = res.data
            })
        },
        // 获取所有目的地
        getAllDestFee() {
            request.post(getAllDestFeeApi,this.pageOption).then(res => {
                this.destData = res.data
                this.data2 = res.data
            })
        },
        // 申请用车按钮
        add() {
            this.showForm = true
            this.type = 'add'
        },
        handleSearch1(val) {
            this.data2 = this.destData.filter((item,index) => {
                return item.dest.indexOf(val) != -1
            })
        },
        save() {
            
            this.$refs.forms.validate((valid) => {
                if(!valid) return

                if (this.formData.destId == '') {
                    this.formData.destId = this.message
                }
                // this.destData.forEach(item => {
                //     if (this.message == item.dest) {
                //         this.formData.destId = item.id
                //         return
                //     }else {
                //         this.formData.destId = this.message
                //     }
                // })
                for (let i = 0;i < this.destData.length;i++) {
                    if (this.destData[i].dest == this.message) {
                        this.formData.destId = this.destData[i].id
                        break;
                    }else {
                        this.formData.destId = this.message
                    }
                }
                console.log(this.formData)
                this.formData.useDate = format('yyyy-MM-dd',this.formData.useDate)
                request.post(addApplyApi,this.formData).then(res => {
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
            })
        },
        dateChange(dateTime) {
            this.formData.useTime = dateTime
        },
        changeUseData(date) {
            this.formData.useDate = date
        },
        sekected(val) {
            console.log(val)
            this.formData.destId = val
            // this.message = ''
            this.destData.forEach(item => {
                if(item.id === val) {
                    this.message = item.dest
                }
            })
        }
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



