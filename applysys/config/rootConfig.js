
const url = 'http://127.0.0.1:8080';


let ROOT;
//由于封装的axios请求中，会将ROOT打包进去，为了方便之后不再更改，判断了当前环境，而生成的不同的ROOT
if (process.env.NODE_ENV === 'development') {
  //开发环境下的代理地址，解决本地跨域跨域，配置在config目录下的index.js dev.proxyTable中
  ROOT = "/apis"
} else {
  //生产环境下的地址
  ROOT = url;
}

exports.PROXYROOT = url; //代理指向地址
exports.ROOT = ROOT;
