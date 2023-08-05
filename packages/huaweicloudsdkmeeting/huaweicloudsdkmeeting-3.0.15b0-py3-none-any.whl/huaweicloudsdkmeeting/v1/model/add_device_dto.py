# coding: utf-8

import pprint
import re

import six





class AddDeviceDTO:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'name': 'str',
        'model': 'str',
        'sn': 'str',
        'prj_code_mode': 'int',
        'dept_code': 'str',
        'phone': 'str',
        'country': 'str',
        'email': 'str',
        'description': 'str',
        'status': 'int',
        'send_notify': 'str'
    }

    attribute_map = {
        'name': 'name',
        'model': 'model',
        'sn': 'sn',
        'prj_code_mode': 'prjCodeMode',
        'dept_code': 'deptCode',
        'phone': 'phone',
        'country': 'country',
        'email': 'email',
        'description': 'description',
        'status': 'status',
        'send_notify': 'sendNotify'
    }

    def __init__(self, name=None, model=None, sn=None, prj_code_mode=None, dept_code=None, phone=None, country=None, email=None, description=None, status=None, send_notify=None):
        """AddDeviceDTO - a model defined in huaweicloud sdk"""
        
        

        self._name = None
        self._model = None
        self._sn = None
        self._prj_code_mode = None
        self._dept_code = None
        self._phone = None
        self._country = None
        self._email = None
        self._description = None
        self._status = None
        self._send_notify = None
        self.discriminator = None

        self.name = name
        self.model = model
        if sn is not None:
            self.sn = sn
        if prj_code_mode is not None:
            self.prj_code_mode = prj_code_mode
        if dept_code is not None:
            self.dept_code = dept_code
        if phone is not None:
            self.phone = phone
        if country is not None:
            self.country = country
        if email is not None:
            self.email = email
        if description is not None:
            self.description = description
        if status is not None:
            self.status = status
        if send_notify is not None:
            self.send_notify = send_notify

    @property
    def name(self):
        """Gets the name of this AddDeviceDTO.

        终端名称，可以自定义，建议为具体位置，方便识别。 maxLength：64 minLength：1

        :return: The name of this AddDeviceDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AddDeviceDTO.

        终端名称，可以自定义，建议为具体位置，方便识别。 maxLength：64 minLength：1

        :param name: The name of this AddDeviceDTO.
        :type: str
        """
        self._name = name

    @property
    def model(self):
        """Gets the model of this AddDeviceDTO.

        终端型号，枚举类型。当前支持TE系列和部分第三方硬件终端，具体的终端类型可以通过获取所有终端类型接口查询。 maxLength：128 minLength：1

        :return: The model of this AddDeviceDTO.
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model):
        """Sets the model of this AddDeviceDTO.

        终端型号，枚举类型。当前支持TE系列和部分第三方硬件终端，具体的终端类型可以通过获取所有终端类型接口查询。 maxLength：128 minLength：1

        :param model: The model of this AddDeviceDTO.
        :type: str
        """
        self._model = model

    @property
    def sn(self):
        """Gets the sn of this AddDeviceDTO.

        终端SN码，仅可包含数字、字母和下划线。 maxLength：30 minLength：1

        :return: The sn of this AddDeviceDTO.
        :rtype: str
        """
        return self._sn

    @sn.setter
    def sn(self, sn):
        """Sets the sn of this AddDeviceDTO.

        终端SN码，仅可包含数字、字母和下划线。 maxLength：30 minLength：1

        :param sn: The sn of this AddDeviceDTO.
        :type: str
        """
        self._sn = sn

    @property
    def prj_code_mode(self):
        """Gets the prj_code_mode of this AddDeviceDTO.

        投影码生成模式，默认为自动 - 0、自动(该模式下根据消息上报的IP地址内部控制复杂度：   私网地址配置成简单模式；公网地址配置成复杂模式) - 1、简单 - 2、复杂

        :return: The prj_code_mode of this AddDeviceDTO.
        :rtype: int
        """
        return self._prj_code_mode

    @prj_code_mode.setter
    def prj_code_mode(self, prj_code_mode):
        """Sets the prj_code_mode of this AddDeviceDTO.

        投影码生成模式，默认为自动 - 0、自动(该模式下根据消息上报的IP地址内部控制复杂度：   私网地址配置成简单模式；公网地址配置成复杂模式) - 1、简单 - 2、复杂

        :param prj_code_mode: The prj_code_mode of this AddDeviceDTO.
        :type: int
        """
        self._prj_code_mode = prj_code_mode

    @property
    def dept_code(self):
        """Gets the dept_code of this AddDeviceDTO.

        部门编号，默认为根部门 默认值：1 maxLength：32 minLength：1

        :return: The dept_code of this AddDeviceDTO.
        :rtype: str
        """
        return self._dept_code

    @dept_code.setter
    def dept_code(self, dept_code):
        """Sets the dept_code of this AddDeviceDTO.

        部门编号，默认为根部门 默认值：1 maxLength：32 minLength：1

        :param dept_code: The dept_code of this AddDeviceDTO.
        :type: str
        """
        self._dept_code = dept_code

    @property
    def phone(self):
        """Gets the phone of this AddDeviceDTO.

        手机号，必须加上国家码，例如中国大陆手机为“+86xxxxxxxxxxx”。当填写手机号时 “country”参数必填。 手机号只允许输入纯数字。 maxLength：32 minLength：0 说明： - 手机号或者邮箱至少填写一个。

        :return: The phone of this AddDeviceDTO.
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this AddDeviceDTO.

        手机号，必须加上国家码，例如中国大陆手机为“+86xxxxxxxxxxx”。当填写手机号时 “country”参数必填。 手机号只允许输入纯数字。 maxLength：32 minLength：0 说明： - 手机号或者邮箱至少填写一个。

        :param phone: The phone of this AddDeviceDTO.
        :type: str
        """
        self._phone = phone

    @property
    def country(self):
        """Gets the country of this AddDeviceDTO.

        手机号所属的国家, 如果国家为中国大陆则country参数取值为chinaPR,国家和国家码的对应关系如下chinaPR: +86(中国大陆); chinaHKG: +852（中国香港）; chinaOMA: +853(中国澳门);  chinaTPE: +886(中国台湾地区); BVl: +1284 (英属维尔京群岛); Bolivia: +591(玻利维亚); CZ: +420(捷克共和国); GB: +245(几内亚比绍); SVGrenadines: +1784(圣文森特和格林纳丁斯); TAT: +1868(特立尼达和多巴哥); UK: +44(英国); afghanistan: +93(阿富汗); albania: +355(阿尔巴尼亚); algeria: +213(阿尔及利亚); andorra: +376(安道尔共和国); angola: +244(安哥拉); argentina: +54(阿根廷); armenia: +374(亚美尼亚); australia: +61(澳大利亚); austria: +43(奥地利); azerbaijan: +994(阿塞拜疆); bahamas: +1242(巴哈马); bahrain: +973(巴林); bangladesh: +880(孟加拉国); belarus: +375(白俄罗斯); belgium: +32(比利时); belize: +501(伯利兹); benin: +229(贝宁); bosniaAndHerzegovina: +387(波斯尼亚和黑塞哥维那); botswana: +267(博茨瓦纳); brazil: +55(巴西); brunei: +673(文莱); bulgaria: +359(保加利亚); burkinaFaso: +226(布基纳法索); burundi: +257(布隆迪); cambodia: +855(柬埔寨); cameroon: +237(喀麦隆); canada: +1(加拿大); capeVerde: +238(佛得角); caymanIslands: +1345(开曼群岛); centralAfrican: +236(中非); chad: +235(乍得); chile: +56(智利);  columbia: +57(哥伦比亚); comoros: +269(科摩罗); congoB: +242(刚果.布); congoJ: +243(刚果.金); costarica: +506(哥斯达黎加); croatia: +385(克罗地亚); curacao: +599(库拉索岛); cyprus: +357(塞浦路斯); denmark: +45(丹麦); djibouti: +253(吉布提); dominica: +1809(多米尼加共和国); ecuador: +593(厄瓜多尔); egypt: +20(埃及); equatorialGuinea: +240(赤道几内亚); estonia: +372(爱沙尼亚); finland: +358(芬兰); france: +33(法国); gabon: +241(加蓬); gambia: +220(冈比亚); georgia: +995(格鲁吉亚); germany: +49(德国); ghana: +233(加纳); greece: +30(希腊); grenada: +1473(格林纳达); guatemala: +502(危地马拉); guinea: +224(几内亚); guyana: +592(圭亚那); honduras: +504(洪都拉斯); hungary: +36(匈牙利); india: +91(印度); indonesia: +62(印度尼西亚); iraq: +964(伊拉克); ireland: +353(爱尔兰); israel: +972( 以色列); italy: +39(意大利); ivoryCoast: +225(科特迪瓦); jamaica: +1876(牙买加); japan: +81(日本); jordan: +962(约旦); kazakhstan: +7(哈萨克斯坦); kenya: +254(肯尼亚); kosovo: +383(科索沃); kuwait: +965(科威特); kyrgyzstan: +996(吉尔吉斯斯坦); laos: +856(老挝); latvia: +371(拉脱维亚); lebanon: +961(黎巴嫩); lesotho: +266(莱索托); liberia: +231(利比里亚); libya: +218(利比亚); lithuania: +370(立陶宛); luxembourg: +352(卢森堡); macedonia: +389(马其顿); madagascar: +261(马达加斯加); malawi: +265(马拉维); malaysia: +60(马来西亚); maldives: +960(马尔代夫); mali: +223(马里); malta: +356(马耳他); mauritania: +222(毛里塔尼亚); mauritius: +230(毛里求斯); mexico: +52(墨西哥); moldova: +373(摩尔多瓦); mongolia: +976(蒙古); montenegro: +382 (黑山共和国); morocco: +212(摩洛哥); mozambique: +258(莫桑比克); myanmar: +95(缅甸); namibia: +264(纳米比亚); nepal: +977(尼泊尔); netherlands: +31(荷兰); newZealand: +64(新西兰); nicaragua: +505(尼加拉瓜); niger: +227(尼日尔); nigeria: +234(尼日利亚); norway: +47(挪威); oman: +968(阿曼); pakistan: +92(巴基斯坦); palestine: +970(巴勒斯坦); panama: +507(巴拿马); papuaNewGuinea: +675(巴布亚新几内亚); peru: +51(秘鲁); philippines: +63(菲律宾); poland: +48(波兰); portugal: +351(葡萄牙); puertoRico: +1787(波多黎各); qatar: +974(卡塔尔); romania: +40(罗马尼亚); russia: +7(俄罗斯); rwanda: +250(卢旺达); saintMartin: +590(圣马丁); salvatore: +503(萨尔瓦多); saudiArabia: +966(沙特阿拉伯); senegal: +221(塞内加尔); serbia: +381(塞尔维亚); seychelles: +248(塞舌尔); sierraLeone: +232(塞拉利昂); singapore: +65(新加坡); slovakia: +421(斯洛伐克); slovenia: +386(斯洛文尼亚); somalia: +252(索马里); southAfrica: +27(南非); southKorea: +82(韩国); spain: +34(西班牙); sriLanka: +94(斯里兰卡); suriname: +597(苏里南); swaziland: +268(斯威士兰); sweden: +46(瑞典); switzerland: +41(瑞士); tajikistan: +992(塔吉克斯坦); tanzania: +255(坦桑尼亚); thailand: +66(泰国); togo: +228(多哥); tunisia: +216(突尼斯); turkey: +90(土耳其); turkmenistan: +993(土库曼斯坦); uae: +971(阿联酋); uganda: +256(乌干达); ukraine: +380(乌克兰); uruguay: +598(乌拉圭); usa: +1(美国); uzbekistan: +998(乌兹别克斯坦); venezuela: +58(委内瑞拉); vietNam: +84(越南); yemen: +967(也门); zambia: +260(赞比亚); zimbabwe: +263(津巴布韦)

        :return: The country of this AddDeviceDTO.
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this AddDeviceDTO.

        手机号所属的国家, 如果国家为中国大陆则country参数取值为chinaPR,国家和国家码的对应关系如下chinaPR: +86(中国大陆); chinaHKG: +852（中国香港）; chinaOMA: +853(中国澳门);  chinaTPE: +886(中国台湾地区); BVl: +1284 (英属维尔京群岛); Bolivia: +591(玻利维亚); CZ: +420(捷克共和国); GB: +245(几内亚比绍); SVGrenadines: +1784(圣文森特和格林纳丁斯); TAT: +1868(特立尼达和多巴哥); UK: +44(英国); afghanistan: +93(阿富汗); albania: +355(阿尔巴尼亚); algeria: +213(阿尔及利亚); andorra: +376(安道尔共和国); angola: +244(安哥拉); argentina: +54(阿根廷); armenia: +374(亚美尼亚); australia: +61(澳大利亚); austria: +43(奥地利); azerbaijan: +994(阿塞拜疆); bahamas: +1242(巴哈马); bahrain: +973(巴林); bangladesh: +880(孟加拉国); belarus: +375(白俄罗斯); belgium: +32(比利时); belize: +501(伯利兹); benin: +229(贝宁); bosniaAndHerzegovina: +387(波斯尼亚和黑塞哥维那); botswana: +267(博茨瓦纳); brazil: +55(巴西); brunei: +673(文莱); bulgaria: +359(保加利亚); burkinaFaso: +226(布基纳法索); burundi: +257(布隆迪); cambodia: +855(柬埔寨); cameroon: +237(喀麦隆); canada: +1(加拿大); capeVerde: +238(佛得角); caymanIslands: +1345(开曼群岛); centralAfrican: +236(中非); chad: +235(乍得); chile: +56(智利);  columbia: +57(哥伦比亚); comoros: +269(科摩罗); congoB: +242(刚果.布); congoJ: +243(刚果.金); costarica: +506(哥斯达黎加); croatia: +385(克罗地亚); curacao: +599(库拉索岛); cyprus: +357(塞浦路斯); denmark: +45(丹麦); djibouti: +253(吉布提); dominica: +1809(多米尼加共和国); ecuador: +593(厄瓜多尔); egypt: +20(埃及); equatorialGuinea: +240(赤道几内亚); estonia: +372(爱沙尼亚); finland: +358(芬兰); france: +33(法国); gabon: +241(加蓬); gambia: +220(冈比亚); georgia: +995(格鲁吉亚); germany: +49(德国); ghana: +233(加纳); greece: +30(希腊); grenada: +1473(格林纳达); guatemala: +502(危地马拉); guinea: +224(几内亚); guyana: +592(圭亚那); honduras: +504(洪都拉斯); hungary: +36(匈牙利); india: +91(印度); indonesia: +62(印度尼西亚); iraq: +964(伊拉克); ireland: +353(爱尔兰); israel: +972( 以色列); italy: +39(意大利); ivoryCoast: +225(科特迪瓦); jamaica: +1876(牙买加); japan: +81(日本); jordan: +962(约旦); kazakhstan: +7(哈萨克斯坦); kenya: +254(肯尼亚); kosovo: +383(科索沃); kuwait: +965(科威特); kyrgyzstan: +996(吉尔吉斯斯坦); laos: +856(老挝); latvia: +371(拉脱维亚); lebanon: +961(黎巴嫩); lesotho: +266(莱索托); liberia: +231(利比里亚); libya: +218(利比亚); lithuania: +370(立陶宛); luxembourg: +352(卢森堡); macedonia: +389(马其顿); madagascar: +261(马达加斯加); malawi: +265(马拉维); malaysia: +60(马来西亚); maldives: +960(马尔代夫); mali: +223(马里); malta: +356(马耳他); mauritania: +222(毛里塔尼亚); mauritius: +230(毛里求斯); mexico: +52(墨西哥); moldova: +373(摩尔多瓦); mongolia: +976(蒙古); montenegro: +382 (黑山共和国); morocco: +212(摩洛哥); mozambique: +258(莫桑比克); myanmar: +95(缅甸); namibia: +264(纳米比亚); nepal: +977(尼泊尔); netherlands: +31(荷兰); newZealand: +64(新西兰); nicaragua: +505(尼加拉瓜); niger: +227(尼日尔); nigeria: +234(尼日利亚); norway: +47(挪威); oman: +968(阿曼); pakistan: +92(巴基斯坦); palestine: +970(巴勒斯坦); panama: +507(巴拿马); papuaNewGuinea: +675(巴布亚新几内亚); peru: +51(秘鲁); philippines: +63(菲律宾); poland: +48(波兰); portugal: +351(葡萄牙); puertoRico: +1787(波多黎各); qatar: +974(卡塔尔); romania: +40(罗马尼亚); russia: +7(俄罗斯); rwanda: +250(卢旺达); saintMartin: +590(圣马丁); salvatore: +503(萨尔瓦多); saudiArabia: +966(沙特阿拉伯); senegal: +221(塞内加尔); serbia: +381(塞尔维亚); seychelles: +248(塞舌尔); sierraLeone: +232(塞拉利昂); singapore: +65(新加坡); slovakia: +421(斯洛伐克); slovenia: +386(斯洛文尼亚); somalia: +252(索马里); southAfrica: +27(南非); southKorea: +82(韩国); spain: +34(西班牙); sriLanka: +94(斯里兰卡); suriname: +597(苏里南); swaziland: +268(斯威士兰); sweden: +46(瑞典); switzerland: +41(瑞士); tajikistan: +992(塔吉克斯坦); tanzania: +255(坦桑尼亚); thailand: +66(泰国); togo: +228(多哥); tunisia: +216(突尼斯); turkey: +90(土耳其); turkmenistan: +993(土库曼斯坦); uae: +971(阿联酋); uganda: +256(乌干达); ukraine: +380(乌克兰); uruguay: +598(乌拉圭); usa: +1(美国); uzbekistan: +998(乌兹别克斯坦); venezuela: +58(委内瑞拉); vietNam: +84(越南); yemen: +967(也门); zambia: +260(赞比亚); zimbabwe: +263(津巴布韦)

        :param country: The country of this AddDeviceDTO.
        :type: str
        """
        self._country = country

    @property
    def email(self):
        """Gets the email of this AddDeviceDTO.

        统一邮箱格式 maxLength：255 minLength：0

        :return: The email of this AddDeviceDTO.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this AddDeviceDTO.

        统一邮箱格式 maxLength：255 minLength：0

        :param email: The email of this AddDeviceDTO.
        :type: str
        """
        self._email = email

    @property
    def description(self):
        """Gets the description of this AddDeviceDTO.

        终端描述 maxLength：128 minLength：0

        :return: The description of this AddDeviceDTO.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AddDeviceDTO.

        终端描述 maxLength：128 minLength：0

        :param description: The description of this AddDeviceDTO.
        :type: str
        """
        self._description = description

    @property
    def status(self):
        """Gets the status of this AddDeviceDTO.

        终端状态 * 0、正常 * 1、冻结\" 默认值：0。 

        :return: The status of this AddDeviceDTO.
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this AddDeviceDTO.

        终端状态 * 0、正常 * 1、冻结\" 默认值：0。 

        :param status: The status of this AddDeviceDTO.
        :type: int
        """
        self._status = status

    @property
    def send_notify(self):
        """Gets the send_notify of this AddDeviceDTO.

        是否发送邮件和短信通知。 * 0：不发送 * 不填或者其他值就发送

        :return: The send_notify of this AddDeviceDTO.
        :rtype: str
        """
        return self._send_notify

    @send_notify.setter
    def send_notify(self, send_notify):
        """Sets the send_notify of this AddDeviceDTO.

        是否发送邮件和短信通知。 * 0：不发送 * 不填或者其他值就发送

        :param send_notify: The send_notify of this AddDeviceDTO.
        :type: str
        """
        self._send_notify = send_notify

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
        if not isinstance(other, AddDeviceDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
