from json import dumps

from rest_framework import serializers

from app.models import Student, Grade


# 定义序列化, 继承   设置返回的内容
class StudentSerializer(serializers.ModelSerializer):
    s_name = serializers.CharField(max_length=20,
                                   error_messages={}) # 在创建时指定字段, 定制错误信息

    class Meta:
        model = Student
        fields = ('id', 's_name', 's_shuxue', 's_yuwen', 'g') # 'g'

    def to_representation(self, instance):   #instance 获取的对象object
        data = super().to_representation(instance)  # 调用父类序列化,
        data['g_name'] = instance.g.g_name  # 增加
        return data

    """重构数据结构"""
    def update(self, instance, validated_data):
        instance.s_name = validated_data['s_name']
        instance.save()
        data = self.to_representation(instance)
        return {'code': 300, 'msg': 'aaaa', 'data': data}


class GradeSerializer(serializers.ModelSerializer):

    g_name = serializers.CharField(max_length=20, error_messages= {
        'balank': '123'
    })

    class Meta:
        model = Grade
        fields = ('id', 'g_name', 'g_create_time')

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # time_str = data.get('g_cerate_time')
    #     # _str = '%Y-%m-%d %h:%m:%s'% time_str  # 格式化时间失败
    #     # data['g_cerate_time'] =  '%Y-%m-%d %h:%m:%s'% (instance[0]['g_create_time'])
    #     return data

    """重构数据结构"""
    def update(self, instance, validated_data):
        instance.g_name = validated_data['g_name']
        instance.save()
        data = self.to_representation(instance)
        return {'code': 300, 'msg': 'aaaa', 'data': data}
