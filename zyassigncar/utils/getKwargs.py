# 获取动态过滤条件
def getKwargs(data={}):
     kwargs = {}
     kwargs['state'] = True
     for (k, v) in data.items():
        if v is not None and v != '':
            kwargs[k] = v
        return kwargs