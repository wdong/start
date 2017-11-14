# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

def modify_fields(**kwargs):
    def wrap(cls):
        for field, prop_dict in kwargs.items():
            for prop, val in prop_dict.items():
                setattr(cls._meta.get_field(field), prop, val)
        return cls
    return wrap

# 基础数据基类
class QrikBaseModel(models.Model):
    qrik_key         = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    qrik_version     = models.IntegerField(verbose_name="版本号", default=1) 
    qrik_code        = models.CharField(max_length=200, default='',verbose_name="编码")
    qrik_name        = models.CharField(max_length=200, default='',verbose_name="名称")
    qrik_value       = models.CharField(max_length=200, default='0',verbose_name="值")   
    qrik_order_no    = models.IntegerField(verbose_name="排序号", default=0)
    qrik_enabled     = models.BooleanField(verbose_name="启用标识", default=True)
    qrik_del_flag    = models.BooleanField(verbose_name="删除标识", default=False) 
    qrik_updater     = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_related_updater', related_query_name="%(app_label)s_%(class)s_relates_updater_query",verbose_name="修改人", default=None, blank=True)
    qrik_creater     = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_related_creater', related_query_name="%(app_label)s_%(class)s_related_creater_query",verbose_name="创建人", default=None, blank=True)
    qrik_stamp       = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    qrik_update_time = models.DateTimeField(auto_now=True,verbose_name="修改时间")
    qrik_summary     = models.TextField(verbose_name="描述",blank=True)
    
    related_name="%(app_label)s_%(class)s_related",
        
    class Meta:
        abstract = True    
        ordering = ['-qrik_order_no']
        get_latest_by = "qrik_update_time"

        
        
class AbstractParentClass(QrikBaseModel):  
    parent     = models.ForeignKey('self', related_name='%(app_label)s_%(class)s_related_parent', related_query_name="%(app_label)s_%(class)s_related_parent_query",verbose_name="所属上级", default=None, blank=True)
    class Meta(QrikBaseModel.Meta):  
        abstract = True  
        
# Register your models here.
class QrikBaseModelAdmin(admin.ModelAdmin):
    fields = ('qrik_creater', 'qrik_updater','qrik_code','qrik_name', 'qrik_value','qrik_order_no','qrik_enabled','qrik_summary')
    list_display = ('qrik_creater', 'qrik_code','qrik_name', 'qrik_value','qrik_stamp')
    list_filter = ('qrik_name',)                
    
    # actions = [upload_image.]
    
    # def upload_image():
        
        
    class Media:
        # 在管理后台的HTML文件中加入css, js文件, 每一个路径都会追加STATIC_URL/
        css = {
            "all": (
                "/static/js/easyui/themes/default/easyui.css",
            )
        }
        
        js = (
            '/static/js/kindeditor/kindeditor-all.js',
            '/static/js/kindeditor/lang/zh-CN.js',
            '/static/js/kindeditor/config.js',
            '/static/js/easyui/jquery.easyui.min.js',
            '/qrik_widgets/easyui_combotree/combotree/id_qrik_value',
        )
