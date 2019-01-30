import axios  from 'axios'
import qs from 'qs'
import { Message } from 'iview'


axios.defaults.baseURL = 'http://127.0.0.1:8000'
// axios.defaults.baseURL = 'http://10.10.131.238:8888/'
// axios.defaults.baseURL = 'http://www.sofa-geek.cn:9099/zyassigncar'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

class request {
    constructor() {}

    // GET网络请求
   get(url, data = {}) {
        data = qs.stringify(data)
       return this.requestAll(url,data,'GET')
   }

   // POST网络请求
   post(url, data) {
       data = qs.stringify(data, {arrayFormat: 'indices', allowDots: true})
       return this.requestAll(url,data,'POST')
   }
//    {arrayFormat: 'indices', allowDots: true}
   //PUT网络请求
   put(url, data) {
        data = qs.stringify(data)
       return this.requestAll(url,data,'PUT')
   }

   //DELETE网络请求
   delete(url, data = {}) {
    data = qs.stringify(data)
       return this.requestAll(url,data, 'DELETE')
   }

   requestAll(url, data, method) {
       return new Promise( resolve => {
            axios({
                url,
                data,
                method
           }).then( res => {  
                if(res.data.code === 0) {
                    resolve(res.data.data)
                }else if(res.data.code === 1) {
                    Message.error(res.data.message)
                }
           }).catch( err => {
                Message.error('服务器内部错误')
           })
       })
   }
}

export default new request()