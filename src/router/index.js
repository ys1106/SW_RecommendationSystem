import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
    {path: '/', component: 'MainPage', name: 'main', meta:{title:'SNACK'} },
    {path: '/mypage', component: 'MyPage', name: 'mypage', meta:{title:'SNACK'} },
    {path: '/preference', component: 'Preference', name: 'preference', meta:{title:'SNACK'} },
    {path: '*', redirect:'/', meta:{title:'SNACK'} }
]

const routes = routerOptions.map(route => {
    return {
        ...route,
        component: () => import(`@/components/${route.component}.vue`)
    }
})

Vue.use(Router)

export default new Router({
    routes,
    mode: 'history'
})