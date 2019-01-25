import Store from '../store'

Store.registerModule('menu', {
    namespaced: true,
    state: {
        activeItem: '',
        menus: [],
        nativeMenu: [],
        tabs: [],
        tabsName: []
    },
    mutations: {
        initMenu(state, menus) {
            state.menus = menus
        },
        initTabs(state, tabs) {
            state.tabs = tabs
        },
        initNativeMenu(state, nativeMenu) {
            state.nativeMenu = nativeMenu
        },
        addTab(state, tab) {
            let areadyHas = state.tabs.filter( item => {
                return item.alias == tab.alias
            })
            if (areadyHas && areadyHas.length < 1) {
                state.tabs.push(tab)
            }
        },
        switchTab(state, nowIndex) {
            state.activeItem = nowIndex
        }
    },
    actions: {
        getMenus({commit}, menuData) {
            commit('initMenu',menuData)
        },
        getNativeMenu({commit}, nativeMenu) {
            commit('initNativeMenu', nativeMenu)
        },
        menuClick({commit}, name) {
            let menus = this.state.menu.nativeMenu
            let addTab = menus.filter( item => {
                return item.name == name
            })
            commit('addTab',addTab[0])
            commit('switchTab', name)
        },
        menuClose({commit}, name) {
            let tabs = this.state.menu.tabs
            let indexNum = tabs.findIndex( f => f.name == name)
            let newTabs = tabs.filter( item => {
                return item.name != name
            })  
            commit('initTabs', newTabs)
            let alias = newTabs[indexNum - 1] ? newTabs[indexNum - 1].name : (newTabs[indexNum+1] ? newTabs[indexNum].name : '')
            commit('switchTab', alias)
        }
    }
})