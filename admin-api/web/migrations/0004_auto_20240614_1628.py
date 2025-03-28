# Generated by Django 3.2.25 on 2024-06-14 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20240531_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemmenu',
            name='isCache',
            field=models.CharField(default='0', help_text='是否缓存（0缓存 1不缓存）', max_length=4, verbose_name='是否缓存（0缓存 1不缓存）'),
        ),
        migrations.AlterField(
            model_name='systemmenu',
            name='isFrame',
            field=models.CharField(default='1', help_text='是否为外链（0是 1否）', max_length=4, verbose_name='是否为外链（0是 1否）'),
        ),
        migrations.AlterField(
            model_name='systemmenu',
            name='status',
            field=models.CharField(default='0', help_text='菜单状态（0正常 1停用）', max_length=4, verbose_name='菜单状态（0正常 1停用）'),
        ),
        migrations.AlterField(
            model_name='systemmenu',
            name='visible',
            field=models.CharField(default='0', help_text='菜单状态（0显示 1隐藏）', max_length=4, verbose_name='菜单状态（0显示 1隐藏）'),
        ),
        migrations.AlterField(
            model_name='systemuser',
            name='userType',
            field=models.CharField(default='00', help_text='用户类型（00系统用户）', max_length=4, verbose_name='用户类型（00系统用户）'),
        ),
        migrations.AddIndex(
            model_name='systemdept',
            index=models.Index(fields=['deptId'], name='SystemDept_deptId'),
        ),
        migrations.AddIndex(
            model_name='systemmenu',
            index=models.Index(fields=['menuId'], name='SystemMenu_menuId'),
        ),
        migrations.AddIndex(
            model_name='systemrole',
            index=models.Index(fields=['roleId'], name='SystemRole_roleId'),
        ),
        migrations.AddIndex(
            model_name='systemrolemenu',
            index=models.Index(fields=['roleId'], name='SystemRoleMenu_roleId'),
        ),
        migrations.AddIndex(
            model_name='systemuser',
            index=models.Index(fields=['userId'], name='SystemUser_userId'),
        ),
    ]
