

const nativeMenu = [
    {
        id: 1,
        parentId: 0,
        name: 'apply',       
        icon: '',
        alias: '用车申请',
        components: 'components/apply'
    },{
        id: 15,
        parentId: 0,
        name: 'approval',
        icon: '',
        alias: '审核',
    },{
        id: 2,
        parentId: 15,
        name: 'approvalApply',
        icon: '',
        alias: '用车审批',
        components: 'components/approvalApply'
    },{
        id: 3,
        parentId: 0,
        name: 'basics',
        icon: '',
        alias: '基础资料',
    },{
        id: 4,
        parentId: 3,
        name: 'driver',
        alias: '司机基础资料',
        components: 'components/basics/driver'
    },{
        id: 5,
        parentId: 3,
        name: 'cost',
        alias: '目的费用关系数据表',
        components: 'components/basics/cost'
    },{
        id: 6,
        parentId: 3,
        name: 'cars',
        alias: '车辆基础资料',
        components: 'components/basics/cars'
    },{
        id: 7,
        parentId: 3,
        name: 'place',
        alias: '出发地基础资料',
        components: 'components/basics/place'
    },{
        id: 12,
        parentId: 0,
        name: 'assignCar',
        alias: '车型安排',
        components: 'components/AssignCar'
    },{
        id: 10,
        parentId: 3,
        name: 'factory',
        alias: '厂别基础资料',
        components: 'components/basics/factory'
    },{
        id: 11,
        parentId: 3,
        name: 'carModel',
        alias: '车型基础资料',
        components: 'components/basics/carModel'
    },{
        id:13,
        parentId: 0,
        name: 'vehiclereturninfo',
        alias: '车辆回程记录',
        components: 'components/vehiclereturninfo'
    },{
        id: 8,
        parentId: 0,
        name: 'setting',
        icon: '',
        alias: '用户管理',
    },{
        id: 14,
        parentId: 15,
        name: 'assignCarApproval',
        alias: '车辆回程审核',
        components: 'components/basics/assignCarApproval'
    },{
        id: 9,
        parentId: 8,
        name: 'user',
        alias: '管理员',
        components: 'components/setting/user'
    },
]

function changeMenu(nativeMenu){
    // nativeMenu.forEach()
    let newMenu = []
    nativeMenu.forEach(item => {
        let newObj = {
          id: item.id,
          parentId: item.parentId,
          name: item.name,
          alias: item.alias
        };
        if (item.parentId === 0 ) {
          newObj.icon = item.icon;         
          if (!item.components) {
            newObj.children = [];
          }
          newMenu.push(newObj);
        } else if (item.components) {
          newMenu.forEach(val => {
            if (val.id === item.parentId && val.children) {
              newObj.components = item.components;
              val.children.push(newObj);
            }
          });
        }
      });
      return newMenu;
}

const menus = changeMenu(nativeMenu)

export {menus,nativeMenu}