# Generated by Django 3.1.7 on 2022-08-01 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='标题')),
                ('category', models.IntegerField(choices=[(0, '新闻资讯'), (1, '员工风采'), (2, 'banner发布')], db_index=True, default=0, verbose_name='新闻信息类别')),
                ('figure', models.URLField(null=True, verbose_name='封面图')),
                ('news_time', models.DateTimeField(db_index=True, null=True, verbose_name='新闻时间')),
                ('news_text', models.TextField(null=True, verbose_name='新闻正文')),
                ('release_time', models.DateTimeField(null=True, verbose_name='发布时间')),
                ('views_number', models.IntegerField(default=0, null=True, verbose_name='浏览次数')),
                ('explain', models.CharField(max_length=256, null=True, verbose_name='说明/摘要/备注')),
                ('jump_link', models.URLField(null=True, verbose_name='跳转链接')),
                ('news_state', models.IntegerField(choices=[(-1, '删除'), (0, '已发布'), (1, '未发布'), (2, '审核中')], db_index=True, default=0, verbose_name='新闻发布状态')),
                ('examine', models.IntegerField(choices=[(0, '是'), (1, '否')], db_index=True, default=0, null=True, verbose_name='审核需求')),
                ('topping', models.IntegerField(choices=[(1, '首页第一位'), (2, '首页第二位'), (0, '否')], db_index=True, default=2, null=True, verbose_name='置顶状态')),
                ('banner_format', models.IntegerField(choices=[(0, '图片'), (1, '视频')], db_index=True, default=0, null=True, verbose_name='banner格式')),
                ('banner_order', models.IntegerField(choices=[(0, '下架'), (1, '轮播图第一位'), (2, '轮播图第一位'), (3, '轮播图第三位'), (4, '轮播图第四位')], db_index=True, default=0, null=True, verbose_name='banner轮播顺序')),
                ('release_location', models.IntegerField(choices=[(1, '关于我们-新闻资讯'), (2, '专项行动-学习文件'), (3, '专项行动-相关资讯')], db_index=True, default=1, null=True, verbose_name='发布模块')),
                ('examine_result', models.IntegerField(choices=[(0, '审核失败'), (1, '审核成功')], db_index=True, default=0, verbose_name='审核结果')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.user', verbose_name='人员')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Attachments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_file', models.CharField(max_length=128, verbose_name='附件文章')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='attachments', to='news.news', verbose_name='文章')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
    ]
