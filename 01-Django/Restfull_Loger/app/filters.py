import django_filters

from rest_framework import filters

from app.models import Student

"""
    自定义过滤
"""
class StudentFilter(filters.FilterSet):
    # 定义字段  代表模糊搜索   查找时的字段名字
    s_name_contain = django_filters.CharFilter('s_name', lookup_expr='contains')
    s_shuxue_max = django_filters.CharFilter('s_shuxue', lookup_expr='gte')
    s_shuxue_min = django_filters.CharFilter('s_shuxue', lookup_expr='lte')
    s_yuwen_max = django_filters.CharFilter('s_yuwen', lookup_expr='gte')
    s_yuwen_min = django_filters.CharFilter('s_yuwen', lookup_expr='lte')

    class Meta:
        model = Student
        fields = ('s_name', 's_shuxue', 's_yuwen')