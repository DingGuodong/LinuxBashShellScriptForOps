# 

基础不牢，地动天摇。稳定的基础才能构建出稳定的上层建筑。

## Exception 
尽可能定义并使用具体某个Exception，而不是直接使用Exception类
```python
class CustomizedException(Exception):
    pass

raise CustomizedException
```

## 返回两种结果及其以上的函数
返回值建议返回错误代码和运行结果，0 为成功，1及以上为失败
```python
def get_resource():
    pass


def customized_function():
    res = get_resource()
    if res:
        return 0, res
    else:
        return 1, "error message"
```

