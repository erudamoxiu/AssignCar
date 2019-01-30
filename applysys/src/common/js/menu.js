

// const nativeMenu = [
//     {
//         id: 15,
//         parentId: 0,
//         name: 'approval',
//         icon: '',
//         alias: '派车管理',
//     },{
//         id: 1,
//         parentId: 15,
//         name: 'apply',       
//         icon: '',
//         alias: '用车申请',
//         components: 'components/apply'
//     },{
//         id: 2,
//         parentId: 15,
//         name: 'approvalApply',
//         icon: '',
//         alias: '用车审批',
//         components: 'components/approvalApply'
//     },{
//         id: 12,
//         parentId: 15,
//         name: 'assignCar',
//         alias: '分派车辆',
//         components: 'components/AssignCar'
//     },{
//         id:13,
//         parentId: 15,
//         name: 'vehiclereturninfo',
//         alias: '车辆记录表',
//         components: 'components/vehiclereturninfo'
//     },{
//         id: 14,
//         parentId: 15,
//         name: 'assignCarApproval',
//         alias: '车辆回程审批',
//         components: 'components/basics/assignCarApproval'
//     },{
//         id: 3,
//         parentId: 0,
//         name: 'basics',
//         icon: '',
//         alias: '基础资料',
//     },{
//         id: 10,
//         parentId: 3,
//         name: 'factory',
//         alias: '厂别',
//         components: 'components/basics/factory'
//     },{
//         id: 11,
//         parentId: 3,
//         name: 'carModel',
//         alias: '车型',
//         components: 'components/basics/carModel'
//     },{
//         id: 4,
//         parentId: 3,
//         name: 'driver',
//         alias: '司机',
//         components: 'components/basics/driver'
//     },{
//         id: 6,
//         parentId: 3,
//         name: 'cars',
//         alias: '车辆',
//         components: 'components/basics/cars'
//     },{
//         id: 7,
//         parentId: 3,
//         name: 'place',
//         alias: '出发地',
//         components: 'components/basics/place'
//     },{
//         id: 5,
//         parentId: 3,
//         name: 'cost',
//         alias: '目的地与费用关系表',
//         components: 'components/basics/cost'
//     },{
//         id:16,
//         parentId:0,
//         name:'',
//         icon:'',
//         alias:'报表'
//     },{
//         id: 8,
//         parentId: 0,
//         name: 'setting',
//         icon: '',
//         alias: '设置',
//     },{
//         id: 9,
//         parentId: 8,
//         name: 'user',
//         alias: '用户管理',
//         components: 'components/setting/user'
//     },
// ]

function getMenu(persona) {
    let nativeMenu;
    switch (persona) {
        case 0:                                                 // 用户
            nativeMenu = [
                {
                    id: 15,
                    parentId: 0,
                    name: 'approval',
                    icon: '',
                    alias: '派车管理',
                },{
                    id: 1,
                    parentId: 15,
                    name: 'apply',       
                    icon: '',
                    alias: '用车申请',
                    components: 'components/apply'
                },
            ]
            break;
        case 1:                                                 // 管理员
            nativeMenu = [
                {
                    id: 15,
                    parentId: 0,
                    name: 'approval',
                    icon: '',
                    alias: '派车管理',
                },{
                    id: 1,
                    parentId: 15,
                    name: 'apply',       
                    icon: '',
                    alias: '用车申请',
                    components: 'components/apply'
                },{
                    id: 2,
                    parentId: 15,
                    name: 'approvalApply',
                    icon: '',
                    alias: '用车审批',
                    components: 'components/approvalApply'
                },{
                    id: 12,
                    parentId: 15,
                    name: 'assignCar',
                    alias: '分派车辆',
                    components: 'components/AssignCar'
                },{
                    id:13,
                    parentId: 15,
                    name: 'vehiclereturninfo',
                    alias: '车辆记录表',
                    components: 'components/vehiclereturninfo'
                },{
                    id: 14,
                    parentId: 15,
                    name: 'assignCarApproval',
                    alias: '车辆回程审批',
                    components: 'components/basics/assignCarApproval'
                },{
                    id: 3,
                    parentId: 0,
                    name: 'basics',
                    icon: '',
                    alias: '基础资料',
                },{
                    id: 10,
                    parentId: 3,
                    name: 'factory',
                    alias: '厂别',
                    components: 'components/basics/factory'
                },{
                    id: 11,
                    parentId: 3,
                    name: 'carModel',
                    alias: '车型',
                    components: 'components/basics/carModel'
                },{
                    id: 4,
                    parentId: 3,
                    name: 'driver',
                    alias: '司机',
                    components: 'components/basics/driver'
                },{
                    id: 6,
                    parentId: 3,
                    name: 'cars',
                    alias: '车辆',
                    components: 'components/basics/cars'
                },{
                    id: 7,
                    parentId: 3,
                    name: 'place',
                    alias: '出发地',
                    components: 'components/basics/place'
                },{
                    id: 5,
                    parentId: 3,
                    name: 'cost',
                    alias: '目的地与费用关系表',
                    components: 'components/basics/cost'
                },{
                    id:16,
                    parentId:0,
                    name:'',
                    icon:'',
                    alias:'报表'
                },{
                    id: 8,
                    parentId: 0,
                    name: 'setting',
                    icon: '',
                    alias: '设置',
                },{
                    id: 9,
                    parentId: 8,
                    name: 'user',
                    alias: '用户管理',
                    components: 'components/setting/user'
                },
            ]
            break;
        case 2:                                                 // 审核员
            nativeMenu = [
                {
                    id: 15,
                    parentId: 0,
                    name: 'approval',
                    icon: '',
                    alias: '派车管理',
                },
                {
                    id: 2,
                    parentId: 15,
                    name: 'approvalApply',
                    icon: '',
                    alias: '用车审批',
                    components: 'components/approvalApply'
                },{
                    id: 14,
                    parentId: 15,
                    name: 'assignCarApproval',
                    alias: '车辆回程审批',
                    components: 'components/basics/assignCarApproval'
                }
            ]
            break;
        case 3:                                                 // 分派员
            nativeMenu = [
                {
                    id: 15,
                    parentId: 0,
                    name: 'approval',
                    icon: '',
                    alias: '派车管理',
                },{
                    id: 12,
                    parentId: 15,
                    name: 'assignCar',
                    alias: '分派车辆',
                    components: 'components/AssignCar'
                }
            ]
            break;
        case 4:                                                 // 司机
            nativeMenu = [
                {
                    id: 15,
                    parentId: 0,
                    name: 'approval',
                    icon: '',
                    alias: '派车管理',
                },{
                    id:13,
                    parentId: 15,
                    name: 'vehiclereturninfo',
                    alias: '车辆记录表',
                    components: 'components/vehiclereturninfo'
                }
            ]
            break;
        default:
            break;
    }
    let menus = changeMenu(nativeMenu)
    return {
        nativeMenu,
        menus
    }
}




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

// const menus = changeMenu(nativeMenu)

export { getMenu }