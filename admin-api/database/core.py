# -*- coding: utf-8 -*-
"""
@Author ：mengying
@Date   ：2024/5/30 15:39
@Email  : 652044581@qq.com
@Desc   : 功能描述
"""
from django.db import models


class CoreModel(models.Model):
    """
    核心标准抽象模型
    """
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")
    remark = models.CharField(max_length=64, blank=True, verbose_name="备注信息", help_text="备注信息")
    createBy = models.CharField(max_length=64, blank=True, verbose_name="创建者", help_text="创建者")
    objects = models.Manager()

    class Meta:
        abstract = True
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name
