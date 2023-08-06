
字节跳动小程序第三方sdk
=======================

快速开始
--------

安装
^^^^

.. code-block:: sh

   pip install bytedance

引入和初始化
^^^^^^^^^^^^

.. code-block:: py

   from bytedance import ByteDance

   tt_app = ByteDance(
       # 核心配置
       app_id='app_id',
       app_secret='app_secret',
       # 支付相关配置，可以不配置
       mch_id='mch_id',
       mch_secret='mch_secret',
       mch_app_id='mch_app_id',
       access_token_type='auto', # 保存access_token的方法
       redis={'host':'127.0.0.1','port':6379}, # redis 的配置
       ac_path='path' # 如果指定access_token_type = file的时候，指定路径用，不指定就是根目录
       )

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 默认值
     - 说明
   * - app_id
     - str
     - -
     - 小程序的appid
   * - app_secret
     - str
     - -
     - 小程序的secret
   * - mch_id
     - str
     - -
     - 商户id
   * - mch_secret
     - str
     - -
     - 商户密钥
   * - mch_app_id
     - str
     - -
     - 商户appid
   * - access_token_type
     - str
     - auto
     - 保存access_token的方法，可选项有auto、redis、file；auto会检查是否有redis，有就启用redis存access_token；file就会把access_token存到根目录
   * - redis
     - dict
     - {"host":"redis","port":6379,"decode_responses":True}
     - 当access_token_type配置为auto或者redis的时候，可以配置redis连接参数，参考\ ``https://pypi.org/project/redis/``\ 文档
   * - ac_path
     - str
     - -
     - access_token 保存文件路径，当access_token_type配置为file或者auto下没有安装redis库的时候启用，默认是根目录


API使用
^^^^^^^

登录code换取session和openid
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: py

   data = tt_app.code2Session(code='code')

   print(data)

   print(data.openid)

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 默认值
     - 说明
   * - code
     - str
     - -
     - 从前端小程序获取到的code
   * - anonymous_code
     - str
     - -
     - 从前端小程序获取到的anonymous_code，头条系app可能是在匿名下使用，这个时候就只能拿到anonymous_code


..

   code和anonymous_code均可登录

   返回值可以使用data.openid这种方式访问属性

   官方文档：\ ``https://microapp.bytedance.com/docs/zh-CN/mini-app/develop/server/log-in/code-2-session``


set_user_storage 存用户数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: py

   data = tt_app.set_user_storage(openid, session_key, kv_list, sig_method="hmac_sha256")
   print(data)

..

   更多信息查看官方文档

   ``https://microapp.bytedance.com/docs/zh-CN/mini-app/develop/server/data-caching/set-user-storage``


remove_user_storage 删除用户数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: py

   data = tt_app.remove_user_storage(openid, session_key, key_list, sig_method="hmac_sha256")
   print(data)

..

   更多信息查看官方文档

   ``https://microapp.bytedance.com/docs/zh-CN/mini-app/develop/server/data-caching/remove-user-storage``


create_qrcode 获取小程序/小游戏的二维码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: py

   data = tt_app.create_qrcode(appname=None, path=None, width=None, line_color=None, background=None, set_icon=None)

..

   请注意，这个api如果正确将返回完整的response而不是json，因为内容是包含了一个二维码图片

   错误的话依然是json数据

   更多信息查看官方文档

   ``https://microapp.bytedance.com/docs/zh-CN/mini-app/develop/server/qr-code/create-qr-code``


template_send 发送模板消息
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: py

   data = tt_app.template_send(touser, template_id, form_id, data, page=None)

..

   更多信息查看官方文档

   ``https://microapp.bytedance.com/docs/zh-CN/mini-app/develop/server/model-news/send``


text_antidirt 文本内容检测
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: py

   resp = tt_app.images_antidirt(tasks=[{"content": "要检测的文本"}])
   print(data, '>>images_antidirt')

..

   更多信息查看官方文档

   ``https://microapp.bytedance.com/docs/zh-CN/mini-app/develop/server/content-security/content-security-detect``


images_antidirt 图片检测
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: py

   data = tt_app.images_antidirt([
           {
           "image": "http://pic.jj20.com/up/allimg/mn02/062QZ1021Z62P10251-0.jpg"
           }
       ])
   print(data, '>>images_antidirt')

..

   更多信息查看官方文档

   ``https://microapp.bytedance.com/docs/zh-CN/mini-app/develop/server/content-security/picture-detect``


subscribe_send 订阅消息推送
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: py

   data = tt_app.subscribe_send(tpl_id, open_id, data, page=None)

..

   更多信息查看官方文档

   ``https://microapp.bytedance.com/docs/zh-CN/mini-app/develop/server/subscribe-notification/notify``


官方文档
^^^^^^^^

https://microapp.bytedance.com/docs/zh-CN/mini-app/develop/server/interface-request-credential/get-access-token
