
# THU 2021 应用密码学 期末作业


## 主要代码

* 密码学文件： ``./crypto`` 中包含sm3, sm4代码。
* 密钥协商：``./GM/key_exchange_methods.py``
* 其他代码部分见PPT。

## 运行方式

添加 ``./crypo`` 包，内含自我实现所需密码学函数。
运行前先 ``cd ./crypto`` 并执行 ``make``, 生成所需编译文件和某个辅助文件夹。
后按之前运行方式运行即可。

后在``./pymodbus/`` 文件夹下执行 ``python ./GM_examples/keyex_server_handle.py`` 启动server程序，另起终端执行``python ./GM_examples/keyex_client_connect.py`` 启动client程序。