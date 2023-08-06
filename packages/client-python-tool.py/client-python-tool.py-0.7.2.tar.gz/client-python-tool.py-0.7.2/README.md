



# client-python-tool

[![Join the chat at https://gitter.im/ethereum/web3.py](https://badges.gitter.im/ethereum/web3.py.svg)](https://github.com/PlatONnetwork/client-sdk-python)

[![Build Status](https://circleci.com/gh/ethereum/web3.py.svg?style=shield)](https://github.com/PlatONnetwork/client-sdk-python)

## 说明

client-python-tool 是一个服务于Platon python sdk 的转换工具，功能如下：

1. 版本声明改为middle版本对应的最高支持版本

2. TOKEN单位，由LAT/LAX替换为ATP/ATX

3. 地址格式，将lat/lax或0x前缀的地址转换为atp/atx前缀的地址

## 快速入门

### 一、安装

#### **1** Python环境要求

​     支持Python 3.6+版本

#### **2** 可使用pip直接安装：

​    $ pip install client-python-tool

​    或下载代码，在python编辑器中使用。git bash 拉取源代码，如下操作

​    $ git clone git@github.com:jiuen1115/client-python-tool.git

#### **3** 安装python sdk 依赖项

​    建议使用pycharm编辑器，按照编辑器提示，安装setup中的第三方依赖包。若因网络问题安装失败，可使用清华镜像安装   

```python
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 第三方包名称
```

### 二、使用

  在testfile.py文件中 ，第4行，将需要转化的脚本文档所在的目录地址写入 open后的括号中，如下所示：

```python
file = open("D:/clinet-python tool/test/testaddress1.py","r+",encoding = 'utf-8')
```

​       其中"D:/clinet-python tool/test/testaddress1.py" 就是所要修改脚本/文档的地址目录。

然后运行testfile.py ，运行完毕后，自动转换成功。

# client-python-tool
