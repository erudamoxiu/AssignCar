# Generated by Django 2.1.4 on 2019-01-24 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderDate', models.DateField(verbose_name='用车单日期')),
                ('applyDepart', models.CharField(max_length=20, verbose_name='申请部门')),
                ('applyCause', models.CharField(max_length=100, verbose_name='申请事由')),
                ('applyDate', models.DateField(null=True, verbose_name='申请时间')),
                ('number', models.IntegerField(verbose_name='人员数量')),
                ('phone', models.CharField(max_length=20, verbose_name='申请人电话')),
                ('carNumber', models.IntegerField(verbose_name='车辆数量')),
                ('useDate', models.DateField(null=True, verbose_name='使用日期')),
                ('useTime', models.TimeField(null=True, verbose_name='使用时间')),
                ('approvalUserId', models.CharField(max_length=20, verbose_name='审核人员')),
                ('approvalDate', models.DateField(null=True, verbose_name='审核时间')),
                ('approvalOpinion', models.CharField(blank=True, max_length=100, null=True, verbose_name='部门领导审核意见')),
                ('approvalStatus', models.SmallIntegerField(choices=[(0, '未审批'), (1, '同意'), (2, '拒绝'), (3, '已派车')], default=0, verbose_name='审核状态')),
                ('createDate', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('createUser', models.CharField(blank=True, max_length=20, null=True, verbose_name='创建用户')),
                ('updateDate', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('updateUser', models.CharField(blank=True, max_length=20, null=True, verbose_name='更新用户')),
            ],
            options={
                'db_table': 'apply',
            },
        ),
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internalFeeTotal', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='内部费用总和')),
                ('marketFeeTotal', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='市场价格费用总和')),
                ('departureDate', models.DateField(blank=True, null=True, verbose_name='出发日期')),
                ('departureTime', models.TimeField(blank=True, null=True, verbose_name='出发时间')),
                ('createDate', models.DateField(auto_now_add=True)),
                ('createUser', models.CharField(blank=True, max_length=20, null=True)),
                ('updateDate', models.DateField(auto_now=True)),
                ('updateUser', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'assign',
            },
        ),
        migrations.CreateModel(
            name='AssignDetail1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Apply')),
                ('assignId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Assign')),
            ],
            options={
                'db_table': 'assignDetail1',
            },
        ),
        migrations.CreateModel(
            name='AssignDetail2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(0, '未提交回程'), (1, '已提交回程')], default=0, verbose_name='回程数据状态')),
                ('assignId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Assign')),
            ],
            options={
                'db_table': 'assignDetail2',
            },
        ),
        migrations.CreateModel(
            name='CarInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licensePlate', models.CharField(max_length=20)),
                ('number', models.IntegerField()),
                ('carFuel', models.DecimalField(decimal_places=2, max_digits=10)),
                ('extraKm', models.DecimalField(decimal_places=2, max_digits=10)),
                ('extraKmPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remark', models.CharField(blank=True, max_length=100, null=True)),
                ('createDate', models.DateField(auto_now_add=True)),
                ('createUser', models.CharField(max_length=20, null=True)),
                ('updateDate', models.DateField(auto_now=True)),
                ('updateUser', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'carInfo',
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carModel', models.CharField(max_length=20)),
                ('createDate', models.DateField(auto_now_add=True)),
                ('createUser', models.CharField(max_length=20, null=True)),
                ('updateDate', models.DateField(auto_now=True)),
                ('updateUser', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'carModel',
            },
        ),
        migrations.CreateModel(
            name='DepartureInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure', models.CharField(max_length=50)),
                ('createDate', models.DateField(auto_now_add=True)),
                ('createUser', models.CharField(max_length=20, null=True)),
                ('updateDate', models.DateField(auto_now=True)),
                ('updateUser', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'departureInfo',
            },
        ),
        migrations.CreateModel(
            name='DestFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dest', models.CharField(max_length=50, verbose_name='目的地')),
                ('internalFee', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='内部费用')),
                ('marketFee', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('channel', models.CharField(max_length=50, null=True)),
                ('otherNote', models.CharField(blank=True, max_length=50, null=True)),
                ('createDate', models.DateField(auto_now_add=True)),
                ('createUser', models.CharField(max_length=20, null=True)),
                ('updateDate', models.DateField(auto_now=True)),
                ('updateUser', models.CharField(max_length=20, null=True)),
                ('carModelId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.CarModel')),
                ('departureInfoId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.DepartureInfo')),
            ],
            options={
                'db_table': 'destFee',
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('createDate', models.DateField(auto_now_add=True)),
                ('createUser', models.CharField(max_length=20, null=True)),
                ('updateDate', models.DateField(auto_now=True)),
                ('updateUser', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'driver',
            },
        ),
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factoryName', models.CharField(max_length=50)),
                ('createDate', models.DateField(auto_now_add=True)),
                ('createUser', models.CharField(max_length=20, null=True)),
                ('updateDate', models.DateField(auto_now=True)),
                ('updateUser', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'factory',
            },
        ),
        migrations.CreateModel(
            name='OrderNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderNo', models.CharField(max_length=20)),
                ('createDate', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'orderNumber',
            },
        ),
        migrations.CreateModel(
            name='ReturnOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carStartDate', models.DateField(null=True, verbose_name='出车日期')),
                ('carStartTime', models.CharField(max_length=20, null=True, verbose_name='出车时间')),
                ('carReturnDate', models.DateField(null=True, verbose_name='返程日期')),
                ('carReturnTime', models.CharField(max_length=20, null=True, verbose_name='返程时间')),
                ('startMileage', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='出发里程')),
                ('returnMileage', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='返程里程')),
                ('oilVolume', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='油升数')),
                ('toll', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='过路费')),
                ('parkingFee', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='停车费')),
                ('expresswayFee', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='高速路费')),
                ('overtime', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='加班费')),
                ('mealFee', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='餐费')),
                ('otherFee', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='其它费用')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('approvalDate', models.DateField(auto_now=True, null=True, verbose_name='审核时间')),
                ('approvalStatus', models.SmallIntegerField(choices=[(0, '未审批'), (1, '同意'), (2, '拒绝')], default=0, verbose_name='审核状态')),
                ('approvalExplanation', models.CharField(max_length=50, null=True)),
                ('createDate', models.DateField(auto_now_add=True)),
                ('createUser', models.CharField(max_length=20, null=True)),
                ('updateDate', models.DateField(auto_now=True)),
                ('updateUser', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'returnOrder',
            },
        ),
        migrations.CreateModel(
            name='UEOrderNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderNo', models.CharField(max_length=20)),
                ('createDate', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'ueOrderNumber',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(max_length=50, unique=True)),
                ('openId', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=20)),
                ('persona', models.SmallIntegerField(choices=[(0, '普通用户'), (1, '管理员'), (2, '审核员'), (3, '派车员')], default=0)),
                ('position', models.CharField(blank=True, max_length=150, null=True)),
                ('avatar', models.CharField(blank=True, max_length=200)),
                ('jobNumber', models.CharField(blank=True, max_length=15, null=True)),
                ('createUser', models.CharField(max_length=20, null=True)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateUser', models.CharField(max_length=20, null=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'userInfo',
            },
        ),
        migrations.AddField(
            model_name='returnorder',
            name='approvalUserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo', to_field='userId', verbose_name='审核人员'),
        ),
        migrations.AddField(
            model_name='returnorder',
            name='assignDetail2Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.AssignDetail2', verbose_name='明细2'),
        ),
        migrations.AddField(
            model_name='driver',
            name='driverUserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo', to_field='userId'),
        ),
        migrations.AddField(
            model_name='driver',
            name='factoryId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factory', to='user.Factory'),
        ),
        migrations.AddField(
            model_name='carinfo',
            name='carModelId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.CarModel'),
        ),
        migrations.AddField(
            model_name='carinfo',
            name='driverId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Driver'),
        ),
        migrations.AddField(
            model_name='carinfo',
            name='factoryId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Factory'),
        ),
        migrations.AddField(
            model_name='assigndetail2',
            name='carInfoId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.CarInfo'),
        ),
        migrations.AddField(
            model_name='assigndetail2',
            name='driverId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Driver'),
        ),
        migrations.AddField(
            model_name='assign',
            name='destFeeId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.DestFee'),
        ),
        migrations.AddField(
            model_name='assign',
            name='orderNo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UEOrderNumber'),
        ),
        migrations.AddField(
            model_name='apply',
            name='carModelId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.CarModel', verbose_name='车型id'),
        ),
        migrations.AddField(
            model_name='apply',
            name='departureInfoId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.DepartureInfo', verbose_name='出发地id'),
        ),
        migrations.AddField(
            model_name='apply',
            name='destId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.DestFee', verbose_name='目的地id'),
        ),
        migrations.AddField(
            model_name='apply',
            name='factoryId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Factory', verbose_name='厂别id'),
        ),
        migrations.AddField(
            model_name='apply',
            name='orderNo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.OrderNumber', verbose_name='用车单号'),
        ),
        migrations.AddField(
            model_name='apply',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo', to_field='userId', verbose_name='申请人'),
        ),
    ]
