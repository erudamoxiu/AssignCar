<template>
    <div id="place" style="height: 100%">
        <tableModel :columns='columns' :tableData="tableData" @changePage="changePage" :tableTitle="tableTitle" :pageOption="pageOption">
             <Button slot="addBtn" @click="add">
                <Icon type="ios-add" /> 新增
            </Button>
        </tableModel>

        <Modal v-model="showForm" :title="fromTitle" @on-ok="save" >
            <Form :model="formData" :label-width="80">
                <FormItem label="出发地">
                    <Input v-model="formData.departure" placeholder="请输入出发地"></Input>
                </FormItem>
            </Form>
        </Modal>
    </div>
</template>

<script>

let getAllApi = '/departureinfo/getAllDeparture'
let getDetailApi = '/departureinfo/getDeparture?id='
let addApi = '/departureinfo/createdateDeparture'
let updateApi = '/departureinfo/updateDeparture'
let deleteApi = '/departureinfo/deleteDeparture?id='

let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))

import request from '@/common/js/request.js'
import tableModel from '@/components/model/tableModel'
    export default {
        name: 'place',
        components: {
            tableModel
        },
        data() {
            return {
                showForm: false,
                fromTitle: '出发地资料',               
                tableTitle: '出发地基础资料',
                pageOption: {
                    pageIndex: 1,
                    pageSize: 20,   
                    total: 0,
                },
                type: 'add',
                columns: [
                    {
                        type: 'index',
                        title: '序号',
                        width: 80,
                        align: 'center'
                    },
                    {
                        title: '出发地',
                        key: 'departure',
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
                                            this.showForm = true
                                            this.type = 'modify'
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
                                            console.log('delete')
                                            this.$Modal.confirm({
                                                title: '提示',
                                                content: '你确定要删除吗？',
                                                onOk: () => {
                                                    let url = deleteApi + params.row.id
                                                    request.get(url).then(res => {
                                                        if (res === true ) {
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
                    departure: '',    // 出发地
                    createUser: '',
                    updateUser: ''
                }
            }
        },
        mounted() {
            this.getAllData()
        },
        methods: {
            // 获取数据
            getAllData() {
                let queryData = {
                    page: this.pageOption.current
                }
                request.post(getAllApi,this.pageOption).then( res => {
                    console.log(res)
                    this.tableData = res.data
                    this.pageOption.total = res.total
                })
            },
            // 新增按钮
            add() {
                this.type = 'add'
                this.showForm = true
            },
            // 保存
            save() {
                // 新增
                if (this.type === 'add') {
                    let sendData = Object.assign(this.formData,{
                        createUser: userInfo.userId
                    })
                    request.post(addApi,sendData).then( res => {
                        console.log(res)
                        if (res === true ) {
                            this.$Message.success('新增成功')
                            this.getAllData()
                        }
                    })
                // 修改
                }else if(this.type === 'modify') {
                    let sendData = Object.assign(this.formData,{
                        updateUser: userInfo.userId
                    })
                    request.post(updateApi,sendData).then( res => {
                        console.log(res)
                        if (res === true ) {
                            this.$Message.success('修改成功')
                            this.getAllData()
                        }
                    })
                }
            },
            // 改变页码
            changePage(current) {
                this.pageOption.pageIndex = current
                this.getAllData()
            }
        },
        watch: {
            showForm(val) {
                if (val == false) {
                    this.formData = {
                        departure: '',    // 出发地
                    }
                }
            }
        }
    }
</script>