from django.db import models

# Create your models here.


#  用户详情表
class UserInfo(models.Model):
    user_type = (
        (0, '普通用户'),
        (1, '管理员'),
        (2, '审核员'),
        (3, '派车员'),
        (4, '司机')
    )
    userId = models.CharField(max_length=50, unique=True)    # 不可重复
    openId = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=20)
    department = models.CharField(max_length=20, null=True, blank=True)                      # 部门
    persona = models.SmallIntegerField(choices=user_type, default=0)  # 角色
    position = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True)
    jobNumber = models.CharField(max_length=15, blank=True, null=True)
    createUser = models.CharField(max_length=20, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateUser = models.CharField(max_length=20, null=True)
    updateDate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'userInfo'


# 厂别 OK
class Factory(models.Model):
    factoryName = models.CharField(max_length=50, null=False)
    createDate = models.DateField(auto_now_add=True)
    createUser = models.CharField(max_length=20, null=True)
    updateDate = models.DateField(auto_now=True)
    updateUser = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'factory'

    # def __str__(self):
    #     return self.factoryName


# 车型 OK
class CarModel(models.Model):
    carModel = models.CharField(max_length=20, null=False)
    createDate = models.DateField(auto_now_add=True)
    createUser = models.CharField(max_length=20, null=True)
    updateDate = models.DateField(auto_now=True)
    updateUser = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'carModel'

    # def __str__(self):
    #     return self.carModel


# 司机 OK
class Driver(models.Model):
    driverName = models.ForeignKey(UserInfo, to_field='userId', on_delete=models.CASCADE)  # 司机姓名
    phone = models.CharField(max_length=20, null=False)
    factoryId = models.ForeignKey(Factory, on_delete=models.CASCADE, null=False, related_name='factory')
    createDate = models.DateField(auto_now_add=True)
    createUser = models.CharField(max_length=20, null=True)
    updateDate = models.DateField(auto_now=True)
    updateUser = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'driver'

    # def __str__(self):
    #     return self.driverName


# 车辆资料 OK
class CarInfo(models.Model):
    factoryId = models.ForeignKey(Factory, on_delete=models.CASCADE)
    licensePlate = models.CharField(max_length=20, null=False)
    carModelId = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    number = models.IntegerField(null=False)
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE)
    carFuel = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    extraKm = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    extraKmPrice = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    remark = models.CharField(max_length=100, null=True, blank=True)
    createDate = models.DateField(auto_now_add=True)
    createUser = models.CharField(max_length=20, null=True)
    updateDate = models.DateField(auto_now=True)
    updateUser = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'carInfo'

    # def __str__(self):
    #     return self.factoryId.factoryName


# 出发地资料 OK
class DepartureInfo(models.Model):
    departure = models.CharField(max_length=50, null=False)
    createDate = models.DateField(auto_now_add=True)
    createUser = models.CharField(max_length=20, null=True)
    updateDate = models.DateField(auto_now=True)
    updateUser = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'departureInfo'


# 目的地与费用 OK
class DestFee(models.Model):
    departureInfoId = models.ForeignKey(DepartureInfo, on_delete=models.CASCADE, null=True)
    carModelId = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True)
    dest = models.CharField(max_length=50, verbose_name='目的地')
    internalFee = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='内部费用')
    marketFee = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    channel = models.CharField(max_length=50, null=True)
    otherNote = models.CharField(max_length=50, null=True, blank=True)
    createDate = models.DateField(auto_now_add=True)
    createUser = models.CharField(max_length=20, null=True)
    updateDate = models.DateField(auto_now=True)
    updateUser = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'destFee'


# 用车单号
class OrderNumber(models.Model):
    orderNo = models.CharField(max_length=20, null=False, unique=False)
    createDate = models.DateField(auto_now=True)

    class Meta:
        db_table = 'orderNumber'


# 用车单
class Apply (models.Model):
    status = (
        (0, '未审批'),
        (1, '同意'),
        (2, '拒绝'),
        (3, '已派车')
    )
    orderNo = models.ForeignKey(OrderNumber, on_delete=models.CASCADE, null=False, verbose_name='用车单号')
    orderDate = models.DateField(null=False, verbose_name='用车单日期')
    userId = models.ForeignKey(UserInfo, to_field='userId', on_delete=models.CASCADE, verbose_name='申请人')
    applyDepart = models.CharField(max_length=20, null=False, verbose_name='申请部门')
    applyCause = models.CharField(max_length=100, null=False, verbose_name='申请事由')
    applyDate = models.DateField(null=True, verbose_name='申请时间')
    number = models.IntegerField(null=False, verbose_name='人员数量')
    phone = models.CharField(max_length=20, null=False, verbose_name='申请人电话')
    departureInfoId = models.ForeignKey(DepartureInfo, on_delete=models.CASCADE, null=False, verbose_name='出发地id')
    destId = models.ForeignKey(DestFee, on_delete=models.CASCADE, null=False, verbose_name='目的地id')
    carNumber = models.IntegerField(null=False, verbose_name='车辆数量')
    carModelId = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=False, verbose_name='车型id')
    factoryId = models.ForeignKey(Factory, on_delete=models.CASCADE, null=False, verbose_name='厂别id')
    useDate = models.DateField(null=True, verbose_name='使用日期')
    useTime = models.CharField(max_length=20, null=True, blank=True, verbose_name='使用时间')
    approvalUserId = models.CharField(max_length=20, verbose_name='审核人员', null=True)
    approvalDate = models.DateField(null=True, verbose_name='审核时间')
    approvalOpinion = models.CharField(max_length=100, null=True, blank=True, verbose_name='部门领导审核意见')
    approvalStatus = models.SmallIntegerField(choices=status, default=0, verbose_name='审核状态')
    createDate = models.DateField(auto_now_add=True, verbose_name='创建时间')
    createUser = models.CharField(max_length=20, null=True, blank=True, verbose_name='创建用户')
    updateDate = models.DateField(auto_now=True, verbose_name='更新时间')
    updateUser = models.CharField(max_length=20, null=True, blank=True, verbose_name='更新用户')

    class Meta:
        db_table = 'apply'


# 派车单号
class UEOrderNumber(models.Model):
    orderNo = models.CharField(max_length=20, null=False, unique=False)
    createDate = models.DateField(auto_now=True)

    class Meta:
        db_table = 'ueOrderNumber'


# 派车单 OK
class Assign (models.Model):
    orderNo = models.ForeignKey(UEOrderNumber, on_delete=models.CASCADE, null=False)
    destFeeId = models.ForeignKey(DestFee, on_delete=models.CASCADE, null=False)
    internalFeeTotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='内部费用总和', null=True)
    marketFeeTotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='市场价格费用总和', null=True)
    departureDate = models.DateField(null=True, blank=True, verbose_name='出发日期')
    departureTime = models.TimeField(null=True, blank=True, verbose_name='出发时间')
    createDate = models.DateField(auto_now_add=True)
    createUser = models.CharField(max_length=20, null=True, blank=True)
    updateDate = models.DateField(auto_now=True)
    updateUser = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'assign'


# 明细1
class AssignDetail1 (models.Model):
    assignId = models.ForeignKey(Assign, on_delete=models.CASCADE, null=False)
    applyId = models.ForeignKey(Apply, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'assignDetail1'


# 明细2
class AssignDetail2 (models.Model):
    status = (
        (0, '未提交回程'),
        (1, '已提交回程')
    )
    assignId = models.ForeignKey(Assign, on_delete=models.CASCADE, null=False)
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE, null=False)
    carInfoId = models.ForeignKey(CarInfo, on_delete=models.CASCADE, null=False)
    type = models.SmallIntegerField(choices=status, default=0, verbose_name='回程数据状态')

    class Meta:
        db_table = 'assignDetail2'


# 车辆回程数据表
class ReturnOrder(models.Model):
    status = (
        (0, '未审批'),
        (1, '同意'),
        (2, '拒绝')
    )
    assignDetail2Id = models.ForeignKey(AssignDetail2, on_delete=models.CASCADE, null=False, verbose_name='明细2')
    carStartDate = models.DateField(null=True, verbose_name='出车日期')
    carStartTime = models.CharField(max_length=20, null=True, verbose_name='出车时间')
    carReturnDate = models.DateField(null=True, verbose_name='返程日期')
    carReturnTime = models.CharField(max_length=20, null=True, verbose_name='返程时间')
    startMileage = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='出发里程')
    returnMileage = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='返程里程')
    oilVolume = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='油升数')
    toll = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='过路费')
    parkingFee = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='停车费')
    expresswayFee = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='高速路费')
    overtime = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='加班费')
    mealFee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='餐费', null=True)
    otherFee = models.CharField(max_length=255, null=True, verbose_name='其它费用附件')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name='备注')
    approvalUserId = models.ForeignKey(UserInfo, to_field='userId', on_delete=models.CASCADE, null=True, verbose_name='审核人员')
    approvalDate = models.DateField(auto_now=True, null=True, verbose_name='审核时间')
    approvalStatus = models.SmallIntegerField(choices=status, default=0, verbose_name='审核状态')
    approvalExplanation = models.CharField(max_length=50, null=True)  # 审核理由
    createDate = models.DateField(auto_now_add=True)
    createUser = models.CharField(max_length=20, null=True)
    updateDate = models.DateField(auto_now=True)
    updateUser = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'returnOrder'
