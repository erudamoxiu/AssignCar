<template>
    <div id="user">
        <!-- user -->
        <div class="list">
            <Input search enter-button placeholder="请输入名称" v-model="keyWord" @on-search="getUserData"/>
            <Tabs value="userType" @on-click="changeType">
                <TabPane label="管理员" name="admin">
                    <ul class="adminList">
                        <li @click="getDetail(item.userId)" v-for="(item,index) in adminList" :key="item.index">
                            <span class="order">{{index+1}}</span>
                            <span class="name">{{item.name}}</span>
                        </li>
                    </ul>
                </TabPane>
                <TabPane label="审核员" name="approval">
                    <ul class="approvalList">
                        <li @click="getDetail(item.userId)" v-for="(item,index) in approvalList" :key="item.index">
                            <span class="order">{{index+1}}</span>
                            <span class="name">{{item.name}}</span>
                        </li>
                    </ul>
                </TabPane>
                <TabPane label="派车员" name="assign">
                    <ul class="assignList">
                        <li @click="getDetail(item.userId)" v-for="(item,index) in assignList" :key="item.index">
                            <span class="order">{{index+1}}</span>
                            <span class="name">{{item.name}}</span>
                        </li>
                    </ul>
                </TabPane>

            </Tabs>
        </div>
        <div class="content">
            <div class="btn">
                <Button @click="addUser" type="primary">添加</Button>
                <Button v-if="showDelBtn" @click="deleteUser" style="margin-left:10px" type="error">删除</Button>
            </div>
            <div class="info">
                <Form :model="formData" :label-width="100">
                    <FormItem label="工号">
                        <Input readonly v-model="formData.jobNumber"></Input>
                    </FormItem>
                    <FormItem label="名称">
                        <Input readonly v-model="formData.name"></Input>
                    </FormItem>
                    <FormItem label="职位">
                        <Input readonly v-model="formData.position"></Input>
                    </FormItem>


                    <Button type="primary" v-if="type == 0" style="margin-top: 50px;float: left;margin-left: 150px;" @click="save">保存</Button>
                </Form>
            </div>
        </div>
    </div>
</template>

<script>
import request from '@/common/js/request.js'

let getApi = '/user/getUser'
let getDetailApi = '/user/getUserDetail?userId='
let addApi = '/user/addUser'
let deleteApi = '/user/deleteUser?userId='
let updateApi = '/user/updateUser'

let CorpId = sessionStorage.getItem('zyCorpId')
let userInfo = JSON.parse(sessionStorage.getItem('zyUserInfo'))
// let userInfo = {
//     userId: 'admin'
// }

export default {
    name: 'user',
    data() {
        return {
            formData: {
                userId: '',
                name: '',
                jobNumber: '',
                position: '',
                isReceive: false
            },
            pageOption: {
                pageIndex: 1,
                pageSize: 20,
                total: 0
            },
            type: 1,        // 1 管理员    2 审核员    3 派车员
            keyWord: '',    // 搜索关键字    可查询用户代号或名称
            userType: 'admin',
            showDelBtn: false,
            adminList: [],
            approvalList: [],
            assignList: []

        }
    },
    mounted() {
        this.getUserData()
        // this.addUser()
    },
    methods: {
        // 获取所有用户
        getUserData() {
            let queryData = Object.assign(this.pageOption,{
                type: parseInt(this.type),
                keyWord: this.keyWord
            })
            request.post(getApi,queryData).then( res => {
                if(this.type == 1) {
                    this.adminList = res.data
                }else if(this.type == 2) {
                    this.approvalList = res.data
                }else if(this.type == 3) {
                    this.assignList = res.data
                }
                this.pageOption.total = res.count
            })
        },
        // 获取单个用户信息
        getDetail(userId) {
            this.showDelBtn = true
            let url = getDetailApi + userId
            request.get(url).then(res => {
                res.position = res.position ? res.position : '暂无'
                res.jobNumber = res.jobNumber ? res.jobNumber : '暂无'
                res.isReceive = res.isReceive ? res.isReceive : false
                this.formData = res
            })
        },
        // 新增用户
        addUser(userId) {
            let newThis = this
            DingTalkPC.biz.contact.choose({
                multiple: true, //是否多选
                corpId: CorpId,
                max: 999,
                onSuccess: (data) => {
                    let ids = []
                    data.forEach((item) => {
                        ids.push(item.emplId)
                    })
                    let sendData = {
                        userIds: ids.join(),
                        userType: this.type,
                        createUser: userInfo.userId
                    }
                    request.post(addApi,sendData).then(res => {
                        if (res === true) {
                            newThis.$Message.success('新增成功')
                            newThis.getUserData()
                            // newThis.getDetail(res.id)
                        }
                    })
                },
                onFail: (err) => {
                }
            })
        },
        // 删除用户
        deleteUser() {
            let url = deleteApi + this.formData.userId
            
            request.get(url).then(res => {
                if(res === true) {
                    this.$Message.success('删除成功')
                    this.getUserData()
                }
            })
        },
        //  修改用户
        save() {
            console.log('this.formData',this.formData)
            request.post(updateApi,this.formData).then(res => {
                if (res.result === true) {
                    this.getDetail(res.id)
                    this.$Message.success('修改成功')
                }
            })
        },
        // 改变用户类型
        changeType(userType) {
            switch (userType) {
                case 'admin':
                    this.type = 1;
                    break;
                case 'approval':
                    this.type = 2;
                    break;
                case 'assign':
                    this.type = 3;
                    break;
                default:
                    this.type = 1;
            }
            this.getUserData()
            this.showDelBtn = false
            this.formData = {
                name: '',
                userId: '',
                position: ''            
            }
        }

    },
    watch: {
        keyWord(val) {
            if (val === '') {
                this.getUserData()
            }
        }
    }
}
</script>

<style lang="less" scoped>
#user {
    display: flex;
    height: 100%;
    .list {
        flex-basis: 250px;
        height: 100%;
        background-color: #fff;
        padding: 15px;

        ul {
            li {
                height: 50px;
                display: flex;
                align-items: center;
                cursor: pointer;
                border-bottom: 1px solid #ccc;
                border-top: 1px solid #eee;

                .order {
                    margin: 0 20px 0 10px;
                }

                &:hover {
                    background-color: #e4e4e4;
                }

                &.active {
                    background-color: #e4e4e4;
                }
            }
        }
    }

    .content {
        flex: 1;
        height: 100%;
        display: flex;
        flex-direction: column;

        margin-left: 5px;
        // padding: 15px;

        .btn {
            flex-basis: 50px;
            background-color: #fff;
            display: flex;
            align-items: center;
            padding-left: 20px;
        }

        .info {
            flex: 1;
            overflow-y: auto;
            margin-top: 5px;
            background-color: #fff;
            padding: 20px 0;
        }
    }
}
</style>


<style>
#user .ivu-tabs .ivu-tabs-bar{
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}
#user .ivu-tabs-tab .ivu-tabs-tab-active .ivu-tabs-tab-focused {
    margin-right: 0;
}
#user .ivu-tabs-tabpane {
    border-radius: 0;
}
#user .ivu-tabs-nav {
    width: 100%;
}
#user .ivu-tabs-nav .ivu-tabs-tab {
    padding: 13px 16px;
}
#user .ivu-tabs-ink-bar.ivu-tabs-ink-bar-animated {
    width: 50% !important;
    margin-left: 10px;
}
#user .content .ivu-input {
    width: 200px;
    float: left;
}
</style>