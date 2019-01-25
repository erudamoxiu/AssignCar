<template>
    <div id="car">
        测试{{message}}
        <button @click="changMessage">改变message</button>
    </div>
</template>

<script>

import request from '@/common/js/request.js'
let getAllFactoryApi = '/factory/getAllFactory?id='


export default {
    data(){
        return {
            message: '1111'
        }
    },
    methods: {
        // changMessage() {
        //     this.message = '2222'
        // }
        getData(id) {

            let _this = this
            let getAllFactoryApi = getAllFactoryApi + id
            request.get(getAllFactoryApi).then(function(result){
                console.log(result)
            })

            let sendData = {
                pageIndex: 1,
                pageSize: 50
            }
            request.post(getAllFactoryApi,sendData).then((result)=> {

            })
        }
    }
}
</script>


<style lang="">
    
</style>