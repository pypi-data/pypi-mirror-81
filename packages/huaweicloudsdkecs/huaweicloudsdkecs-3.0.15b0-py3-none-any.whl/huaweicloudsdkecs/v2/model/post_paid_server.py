# coding: utf-8

import pprint
import re

import six





class PostPaidServer:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'admin_pass': 'str',
        'availability_zone': 'str',
        'count': 'int',
        'data_volumes': 'list[PostPaidServerDataVolume]',
        'extendparam': 'PostPaidServerExtendParam',
        'flavor_ref': 'str',
        'image_ref': 'str',
        'is_auto_rename': 'bool',
        'key_name': 'str',
        'metadata': 'dict(str, str)',
        'name': 'str',
        'nics': 'list[PostPaidServerNic]',
        'osscheduler_hints': 'PostPaidServerSchedulerHints',
        'publicip': 'PostPaidServerPublicip',
        'root_volume': 'PostPaidServerRootVolume',
        'security_groups': 'list[PostPaidServerSecurityGroup]',
        'server_tags': 'list[PostPaidServerTag]',
        'tags': 'list[str]',
        'user_data': 'str',
        'vpcid': 'str',
        'description': 'str'
    }

    attribute_map = {
        'admin_pass': 'adminPass',
        'availability_zone': 'availability_zone',
        'count': 'count',
        'data_volumes': 'data_volumes',
        'extendparam': 'extendparam',
        'flavor_ref': 'flavorRef',
        'image_ref': 'imageRef',
        'is_auto_rename': 'isAutoRename',
        'key_name': 'key_name',
        'metadata': 'metadata',
        'name': 'name',
        'nics': 'nics',
        'osscheduler_hints': 'os:scheduler_hints',
        'publicip': 'publicip',
        'root_volume': 'root_volume',
        'security_groups': 'security_groups',
        'server_tags': 'server_tags',
        'tags': 'tags',
        'user_data': 'user_data',
        'vpcid': 'vpcid',
        'description': 'description'
    }

    def __init__(self, admin_pass=None, availability_zone=None, count=1, data_volumes=None, extendparam=None, flavor_ref=None, image_ref=None, is_auto_rename=True, key_name=None, metadata=None, name=None, nics=None, osscheduler_hints=None, publicip=None, root_volume=None, security_groups=None, server_tags=None, tags=None, user_data=None, vpcid=None, description=None):
        """PostPaidServer - a model defined in huaweicloud sdk"""
        
        

        self._admin_pass = None
        self._availability_zone = None
        self._count = None
        self._data_volumes = None
        self._extendparam = None
        self._flavor_ref = None
        self._image_ref = None
        self._is_auto_rename = None
        self._key_name = None
        self._metadata = None
        self._name = None
        self._nics = None
        self._osscheduler_hints = None
        self._publicip = None
        self._root_volume = None
        self._security_groups = None
        self._server_tags = None
        self._tags = None
        self._user_data = None
        self._vpcid = None
        self._description = None
        self.discriminator = None

        if admin_pass is not None:
            self.admin_pass = admin_pass
        self.availability_zone = availability_zone
        if count is not None:
            self.count = count
        if data_volumes is not None:
            self.data_volumes = data_volumes
        if extendparam is not None:
            self.extendparam = extendparam
        self.flavor_ref = flavor_ref
        self.image_ref = image_ref
        if is_auto_rename is not None:
            self.is_auto_rename = is_auto_rename
        if key_name is not None:
            self.key_name = key_name
        if metadata is not None:
            self.metadata = metadata
        self.name = name
        self.nics = nics
        if osscheduler_hints is not None:
            self.osscheduler_hints = osscheduler_hints
        if publicip is not None:
            self.publicip = publicip
        self.root_volume = root_volume
        if security_groups is not None:
            self.security_groups = security_groups
        if server_tags is not None:
            self.server_tags = server_tags
        if tags is not None:
            self.tags = tags
        if user_data is not None:
            self.user_data = user_data
        self.vpcid = vpcid
        if description is not None:
            self.description = description

    @property
    def admin_pass(self):
        """Gets the admin_pass of this PostPaidServer.

        如果需要使用密码方式登录云服务器，可使用adminPass字段指定云服务器管理员帐户初始登录密码。其中，Linux管理员帐户为root，Windows管理员帐户为Administrator。具体使用方法请参见接口描述信息（设置登录鉴权方式）。  密码复杂度要求：   - 长度为8-26位。  - 密码至少必须包含大写字母、小写字母、数字和特殊字符（!@$%^-_=+[{}]:,./?）中的三种。 - 密码不能包含用户名或用户名的逆序。  - Windows系统密码不能包含用户名或用户名的逆序，不能包含用户名中超过两个连续字符的部分。

        :return: The admin_pass of this PostPaidServer.
        :rtype: str
        """
        return self._admin_pass

    @admin_pass.setter
    def admin_pass(self, admin_pass):
        """Sets the admin_pass of this PostPaidServer.

        如果需要使用密码方式登录云服务器，可使用adminPass字段指定云服务器管理员帐户初始登录密码。其中，Linux管理员帐户为root，Windows管理员帐户为Administrator。具体使用方法请参见接口描述信息（设置登录鉴权方式）。  密码复杂度要求：   - 长度为8-26位。  - 密码至少必须包含大写字母、小写字母、数字和特殊字符（!@$%^-_=+[{}]:,./?）中的三种。 - 密码不能包含用户名或用户名的逆序。  - Windows系统密码不能包含用户名或用户名的逆序，不能包含用户名中超过两个连续字符的部分。

        :param admin_pass: The admin_pass of this PostPaidServer.
        :type: str
        """
        self._admin_pass = admin_pass

    @property
    def availability_zone(self):
        """Gets the availability_zone of this PostPaidServer.

        待创建云服务器所在的可用分区，需要指定可用分区（AZ）的名称。  请参考[地区和终端节点](https://developer.huaweicloud.com/endpoint)获取。

        :return: The availability_zone of this PostPaidServer.
        :rtype: str
        """
        return self._availability_zone

    @availability_zone.setter
    def availability_zone(self, availability_zone):
        """Sets the availability_zone of this PostPaidServer.

        待创建云服务器所在的可用分区，需要指定可用分区（AZ）的名称。  请参考[地区和终端节点](https://developer.huaweicloud.com/endpoint)获取。

        :param availability_zone: The availability_zone of this PostPaidServer.
        :type: str
        """
        self._availability_zone = availability_zone

    @property
    def count(self):
        """Gets the count of this PostPaidServer.

        创建云服务器数量。  约束：  - 不传该字段时默认取值为1。 - 租户的配额足够时，最大值为500。

        :return: The count of this PostPaidServer.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this PostPaidServer.

        创建云服务器数量。  约束：  - 不传该字段时默认取值为1。 - 租户的配额足够时，最大值为500。

        :param count: The count of this PostPaidServer.
        :type: int
        """
        self._count = count

    @property
    def data_volumes(self):
        """Gets the data_volumes of this PostPaidServer.

        云服务器对应数据盘相关配置。每一个数据结构代表一块待创建的数据盘。 约束：目前新创建的弹性云服务器最多可挂载23块数据盘。

        :return: The data_volumes of this PostPaidServer.
        :rtype: list[PostPaidServerDataVolume]
        """
        return self._data_volumes

    @data_volumes.setter
    def data_volumes(self, data_volumes):
        """Sets the data_volumes of this PostPaidServer.

        云服务器对应数据盘相关配置。每一个数据结构代表一块待创建的数据盘。 约束：目前新创建的弹性云服务器最多可挂载23块数据盘。

        :param data_volumes: The data_volumes of this PostPaidServer.
        :type: list[PostPaidServerDataVolume]
        """
        self._data_volumes = data_volumes

    @property
    def extendparam(self):
        """Gets the extendparam of this PostPaidServer.


        :return: The extendparam of this PostPaidServer.
        :rtype: PostPaidServerExtendParam
        """
        return self._extendparam

    @extendparam.setter
    def extendparam(self, extendparam):
        """Sets the extendparam of this PostPaidServer.


        :param extendparam: The extendparam of this PostPaidServer.
        :type: PostPaidServerExtendParam
        """
        self._extendparam = extendparam

    @property
    def flavor_ref(self):
        """Gets the flavor_ref of this PostPaidServer.

        待创建云服务器的系统规格的ID。  已上线的规格请参见《[弹性云服务器产品介绍](https://support.huaweicloud.com/ecs/index.html)》的“实例类型与规格”章节。

        :return: The flavor_ref of this PostPaidServer.
        :rtype: str
        """
        return self._flavor_ref

    @flavor_ref.setter
    def flavor_ref(self, flavor_ref):
        """Sets the flavor_ref of this PostPaidServer.

        待创建云服务器的系统规格的ID。  已上线的规格请参见《[弹性云服务器产品介绍](https://support.huaweicloud.com/ecs/index.html)》的“实例类型与规格”章节。

        :param flavor_ref: The flavor_ref of this PostPaidServer.
        :type: str
        """
        self._flavor_ref = flavor_ref

    @property
    def image_ref(self):
        """Gets the image_ref of this PostPaidServer.

        待创建云服务器的系统镜像，需要指定已创建镜像的ID，ID格式为通用唯一识别码（Universally Unique Identifier，简称UUID）。

        :return: The image_ref of this PostPaidServer.
        :rtype: str
        """
        return self._image_ref

    @image_ref.setter
    def image_ref(self, image_ref):
        """Sets the image_ref of this PostPaidServer.

        待创建云服务器的系统镜像，需要指定已创建镜像的ID，ID格式为通用唯一识别码（Universally Unique Identifier，简称UUID）。

        :param image_ref: The image_ref of this PostPaidServer.
        :type: str
        """
        self._image_ref = image_ref

    @property
    def is_auto_rename(self):
        """Gets the is_auto_rename of this PostPaidServer.

        当批量创建弹性云服务器时，云服务器名称是否允许重名，当count大于1的时候该参数生效。默认为True。  - True，表示允许重名。 - False，表示不允许重名。

        :return: The is_auto_rename of this PostPaidServer.
        :rtype: bool
        """
        return self._is_auto_rename

    @is_auto_rename.setter
    def is_auto_rename(self, is_auto_rename):
        """Sets the is_auto_rename of this PostPaidServer.

        当批量创建弹性云服务器时，云服务器名称是否允许重名，当count大于1的时候该参数生效。默认为True。  - True，表示允许重名。 - False，表示不允许重名。

        :param is_auto_rename: The is_auto_rename of this PostPaidServer.
        :type: bool
        """
        self._is_auto_rename = is_auto_rename

    @property
    def key_name(self):
        """Gets the key_name of this PostPaidServer.

        如果需要使用SSH密钥方式登录云服务器，请指定已创建密钥的名称。  密钥可以通过密钥创建接口进行创建 [创建和导入SSH密钥](https://support.huaweicloud.com/api-ecs/zh-cn_topic_0020212678.html)（请参见），或使用SSH密钥查询接口查询已有的密钥（请参见[查询SSH密钥列表](https://support.huaweicloud.com/api-ecs/zh-cn_topic_0020212676.html) ）。

        :return: The key_name of this PostPaidServer.
        :rtype: str
        """
        return self._key_name

    @key_name.setter
    def key_name(self, key_name):
        """Sets the key_name of this PostPaidServer.

        如果需要使用SSH密钥方式登录云服务器，请指定已创建密钥的名称。  密钥可以通过密钥创建接口进行创建 [创建和导入SSH密钥](https://support.huaweicloud.com/api-ecs/zh-cn_topic_0020212678.html)（请参见），或使用SSH密钥查询接口查询已有的密钥（请参见[查询SSH密钥列表](https://support.huaweicloud.com/api-ecs/zh-cn_topic_0020212676.html) ）。

        :param key_name: The key_name of this PostPaidServer.
        :type: str
        """
        self._key_name = key_name

    @property
    def metadata(self):
        """Gets the metadata of this PostPaidServer.

        用户自定义字段键值对。  > 说明： >  > - 最多可注入10对键值（Key/Value）。 > - 主键（Key）只能由大写字母（A-Z）、小写字母（a-z）、数字（0-9）、中划线（-）、下划线（_）、冒号（:）和小数点（.）组成，长度为[1-255]个字符。 > - 值（value）最大长度为255个字符。  系统预留字段  1. op_svc_userid : 用户ID       2. agency_name  :  委托的名称   委托是由租户管理员在统一身份认证服务（Identity and Access Management，IAM）上创建的，可以为弹性云服务器提供访问云服务的临时凭证。  > 说明： >  > 委托获取、更新请参考如下步骤： >  > 1. 使用IAM服务提供的[查询委托列表](https://support.huaweicloud.com/api-iam/zh-cn_topic_0079467614.html)接口，获取有效可用的委托名称。 > 2. 使用[更新云服务器元数](https://support.huaweicloud.com/api-ecs/zh-cn_topic_0025560298.html)据接口，更新metadata中agency_name字段为新的委托名称。  3. __support_agent_list: 云服务器是否支持企业主机安全、主机监控。 - \"hss\"：企业主机安全 - \"ces\"：主机监控  取值样例： __support_agent_list: \"hss,ces\"  可以通过查询[镜像详情](https://support.huaweicloud.com/api-ims/ims_03_0702.html)判断创建云服务器使用的镜像是否支持企业主机安全或主机监控。

        :return: The metadata of this PostPaidServer.
        :rtype: dict(str, str)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this PostPaidServer.

        用户自定义字段键值对。  > 说明： >  > - 最多可注入10对键值（Key/Value）。 > - 主键（Key）只能由大写字母（A-Z）、小写字母（a-z）、数字（0-9）、中划线（-）、下划线（_）、冒号（:）和小数点（.）组成，长度为[1-255]个字符。 > - 值（value）最大长度为255个字符。  系统预留字段  1. op_svc_userid : 用户ID       2. agency_name  :  委托的名称   委托是由租户管理员在统一身份认证服务（Identity and Access Management，IAM）上创建的，可以为弹性云服务器提供访问云服务的临时凭证。  > 说明： >  > 委托获取、更新请参考如下步骤： >  > 1. 使用IAM服务提供的[查询委托列表](https://support.huaweicloud.com/api-iam/zh-cn_topic_0079467614.html)接口，获取有效可用的委托名称。 > 2. 使用[更新云服务器元数](https://support.huaweicloud.com/api-ecs/zh-cn_topic_0025560298.html)据接口，更新metadata中agency_name字段为新的委托名称。  3. __support_agent_list: 云服务器是否支持企业主机安全、主机监控。 - \"hss\"：企业主机安全 - \"ces\"：主机监控  取值样例： __support_agent_list: \"hss,ces\"  可以通过查询[镜像详情](https://support.huaweicloud.com/api-ims/ims_03_0702.html)判断创建云服务器使用的镜像是否支持企业主机安全或主机监控。

        :param metadata: The metadata of this PostPaidServer.
        :type: dict(str, str)
        """
        self._metadata = metadata

    @property
    def name(self):
        """Gets the name of this PostPaidServer.

        云服务器名称。  取值范围：  - 只能由中文字符、英文字母、数字及“_”、“-”、“.”组成，且长度为[1-64]个字符。 - 创建的云服务器器数量（count字段对应的值）大于1时，为区分不同云服务器，创建过程中系统会自动在名称后加“-0000”的类似标记。故此时名称的长度为[1-59]个字符。  > 说明： >  > 云服务器虚拟机内部(hostname)命名规则遵循 RFC 952和RFC 1123命名规范，建议使用a-zA-z或0-9以及中划线\"-\"组成的名称命名，\"_\"将在弹性云服务器内部默认转化为\"-\"。

        :return: The name of this PostPaidServer.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PostPaidServer.

        云服务器名称。  取值范围：  - 只能由中文字符、英文字母、数字及“_”、“-”、“.”组成，且长度为[1-64]个字符。 - 创建的云服务器器数量（count字段对应的值）大于1时，为区分不同云服务器，创建过程中系统会自动在名称后加“-0000”的类似标记。故此时名称的长度为[1-59]个字符。  > 说明： >  > 云服务器虚拟机内部(hostname)命名规则遵循 RFC 952和RFC 1123命名规范，建议使用a-zA-z或0-9以及中划线\"-\"组成的名称命名，\"_\"将在弹性云服务器内部默认转化为\"-\"。

        :param name: The name of this PostPaidServer.
        :type: str
        """
        self._name = name

    @property
    def nics(self):
        """Gets the nics of this PostPaidServer.

        待创建云服务器的网卡信息。  约束：  - 网卡对应的子网（subnet）必须属于vpcid对应的VPC。 - 当前单个云服务器支持最多挂载12张网卡。

        :return: The nics of this PostPaidServer.
        :rtype: list[PostPaidServerNic]
        """
        return self._nics

    @nics.setter
    def nics(self, nics):
        """Sets the nics of this PostPaidServer.

        待创建云服务器的网卡信息。  约束：  - 网卡对应的子网（subnet）必须属于vpcid对应的VPC。 - 当前单个云服务器支持最多挂载12张网卡。

        :param nics: The nics of this PostPaidServer.
        :type: list[PostPaidServerNic]
        """
        self._nics = nics

    @property
    def osscheduler_hints(self):
        """Gets the osscheduler_hints of this PostPaidServer.


        :return: The osscheduler_hints of this PostPaidServer.
        :rtype: PostPaidServerSchedulerHints
        """
        return self._osscheduler_hints

    @osscheduler_hints.setter
    def osscheduler_hints(self, osscheduler_hints):
        """Sets the osscheduler_hints of this PostPaidServer.


        :param osscheduler_hints: The osscheduler_hints of this PostPaidServer.
        :type: PostPaidServerSchedulerHints
        """
        self._osscheduler_hints = osscheduler_hints

    @property
    def publicip(self):
        """Gets the publicip of this PostPaidServer.


        :return: The publicip of this PostPaidServer.
        :rtype: PostPaidServerPublicip
        """
        return self._publicip

    @publicip.setter
    def publicip(self, publicip):
        """Sets the publicip of this PostPaidServer.


        :param publicip: The publicip of this PostPaidServer.
        :type: PostPaidServerPublicip
        """
        self._publicip = publicip

    @property
    def root_volume(self):
        """Gets the root_volume of this PostPaidServer.


        :return: The root_volume of this PostPaidServer.
        :rtype: PostPaidServerRootVolume
        """
        return self._root_volume

    @root_volume.setter
    def root_volume(self, root_volume):
        """Sets the root_volume of this PostPaidServer.


        :param root_volume: The root_volume of this PostPaidServer.
        :type: PostPaidServerRootVolume
        """
        self._root_volume = root_volume

    @property
    def security_groups(self):
        """Gets the security_groups of this PostPaidServer.

        云服务器对应安全组信息。  约束：当该值指定为空时，默认给云服务器绑定default安全组。

        :return: The security_groups of this PostPaidServer.
        :rtype: list[PostPaidServerSecurityGroup]
        """
        return self._security_groups

    @security_groups.setter
    def security_groups(self, security_groups):
        """Sets the security_groups of this PostPaidServer.

        云服务器对应安全组信息。  约束：当该值指定为空时，默认给云服务器绑定default安全组。

        :param security_groups: The security_groups of this PostPaidServer.
        :type: list[PostPaidServerSecurityGroup]
        """
        self._security_groups = security_groups

    @property
    def server_tags(self):
        """Gets the server_tags of this PostPaidServer.

        弹性云服务器的标签。  > 说明： >  > 创建弹性云服务器时，一台弹性云服务器最多可以添加10个标签。 > 公有云新增server_tags字段，该字段与tags字段功能相同，支持的key、value取值范围更广，建议使用server_tags字段。

        :return: The server_tags of this PostPaidServer.
        :rtype: list[PostPaidServerTag]
        """
        return self._server_tags

    @server_tags.setter
    def server_tags(self, server_tags):
        """Sets the server_tags of this PostPaidServer.

        弹性云服务器的标签。  > 说明： >  > 创建弹性云服务器时，一台弹性云服务器最多可以添加10个标签。 > 公有云新增server_tags字段，该字段与tags字段功能相同，支持的key、value取值范围更广，建议使用server_tags字段。

        :param server_tags: The server_tags of this PostPaidServer.
        :type: list[PostPaidServerTag]
        """
        self._server_tags = server_tags

    @property
    def tags(self):
        """Gets the tags of this PostPaidServer.

        弹性云服务器的标签。  标签的格式为“key.value”。其中，key的长度不超过36个字符，value的长度不超过43个字符。  标签命名时，需满足如下要求：  - 标签的key值只能包含大写字母（A~Z）、小写字母（a~z）、数字（0-9）、下划线（_）、中划线（-）以及中文字符。 - 标签的value值只能包含大写字母（A~Z）、小写字母（a~z）、数字（0-9）、下划线（_）、中划线（-）、小数点（.）以及中文字符。  > 说明： >  > 创建弹性云服务器时，一台弹性云服务器最多可以添加10个标签。 > 公有云新增server_tags字段，该字段与tags字段功能相同，支持的key、value取值范围更广，建议使用server_tags字段。

        :return: The tags of this PostPaidServer.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this PostPaidServer.

        弹性云服务器的标签。  标签的格式为“key.value”。其中，key的长度不超过36个字符，value的长度不超过43个字符。  标签命名时，需满足如下要求：  - 标签的key值只能包含大写字母（A~Z）、小写字母（a~z）、数字（0-9）、下划线（_）、中划线（-）以及中文字符。 - 标签的value值只能包含大写字母（A~Z）、小写字母（a~z）、数字（0-9）、下划线（_）、中划线（-）、小数点（.）以及中文字符。  > 说明： >  > 创建弹性云服务器时，一台弹性云服务器最多可以添加10个标签。 > 公有云新增server_tags字段，该字段与tags字段功能相同，支持的key、value取值范围更广，建议使用server_tags字段。

        :param tags: The tags of this PostPaidServer.
        :type: list[str]
        """
        self._tags = tags

    @property
    def user_data(self):
        """Gets the user_data of this PostPaidServer.

        创建云服务器过程中待注入用户数据。支持注入文本、文本文件或gzip文件。  更多关于待注入用户数据的信息，请参见《弹性云服务器用户指南 》的“用户数据注入”章节。  约束：  - 注入内容，需要进行base64格式编码。注入内容（编码之前的内容）最大长度32KB。 - 创建密码方式鉴权的Linux弹性云服务器时，该字段可为root用户注入自定义初始化密码，具体注入密码的使用方法请参见接口描述（设置登录鉴权方式）。 示例（base64编码前）：  - Linux弹性云服务器  ``` #! /bin/bash echo user_test >> /home/user.txt  ```  - Windows弹性云服务器  ``` rem cmd echo 111 > c:\\aaa.tx ```

        :return: The user_data of this PostPaidServer.
        :rtype: str
        """
        return self._user_data

    @user_data.setter
    def user_data(self, user_data):
        """Sets the user_data of this PostPaidServer.

        创建云服务器过程中待注入用户数据。支持注入文本、文本文件或gzip文件。  更多关于待注入用户数据的信息，请参见《弹性云服务器用户指南 》的“用户数据注入”章节。  约束：  - 注入内容，需要进行base64格式编码。注入内容（编码之前的内容）最大长度32KB。 - 创建密码方式鉴权的Linux弹性云服务器时，该字段可为root用户注入自定义初始化密码，具体注入密码的使用方法请参见接口描述（设置登录鉴权方式）。 示例（base64编码前）：  - Linux弹性云服务器  ``` #! /bin/bash echo user_test >> /home/user.txt  ```  - Windows弹性云服务器  ``` rem cmd echo 111 > c:\\aaa.tx ```

        :param user_data: The user_data of this PostPaidServer.
        :type: str
        """
        self._user_data = user_data

    @property
    def vpcid(self):
        """Gets the vpcid of this PostPaidServer.

        待创建云服务器所属虚拟私有云（简称VPC），需要指定已创建VPC的ID，UUID格式。

        :return: The vpcid of this PostPaidServer.
        :rtype: str
        """
        return self._vpcid

    @vpcid.setter
    def vpcid(self, vpcid):
        """Sets the vpcid of this PostPaidServer.

        待创建云服务器所属虚拟私有云（简称VPC），需要指定已创建VPC的ID，UUID格式。

        :param vpcid: The vpcid of this PostPaidServer.
        :type: str
        """
        self._vpcid = vpcid

    @property
    def description(self):
        """Gets the description of this PostPaidServer.

        云服务器描述信息，默认为空字符串。  - 长度最多允许85个字符。 - 不能包含“<” 和 “>”。

        :return: The description of this PostPaidServer.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PostPaidServer.

        云服务器描述信息，默认为空字符串。  - 长度最多允许85个字符。 - 不能包含“<” 和 “>”。

        :param description: The description of this PostPaidServer.
        :type: str
        """
        self._description = description

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PostPaidServer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
