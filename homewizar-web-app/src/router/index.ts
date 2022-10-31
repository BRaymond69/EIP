import axios from 'axios'
import jwt_decode from 'jwt-decode';

import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import VerifEmail from '../views/VerifEmail.vue'
import CreateCompany from '../views/CreateCompany.vue'
import ForgotPassword from '../views/ForgotPassword.vue'

interface DateInterface {
    exp: number
}

function parseJwt(token: string): Boolean {
    const now = Math.floor(Date.now() / 1000)
    var decoded: DateInterface = jwt_decode(token)

    return decoded.exp > now
}

async function refreshToken(token: string) {
    let parseToken = JSON.parse(token)

    return await axios.post(import.meta.env.VITE_APP_URL + '/api/token/refresh/', {
        refresh: parseToken.refresh
    }).then(res => {
        parseToken.access = res.data.access
        localStorage.setItem('token', JSON.stringify(parseToken))
        return true
    }).catch(err => {
        return false
    })
}

const routes = [
    { path: '/', name: "Dashboard", component: Home },
    { path: '/login', name: "Login", component: Login },
    { path: '/register', name: "Register", component: Register },
    { path: '/verif_email', name: "VerifEmail", component: VerifEmail },
    { path: '/create_company', name: "CreateCompany", component: CreateCompany },
    { path: '/forgot_password/', name: "ForgotPassword", component: ForgotPassword },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(async (to, from, next) => {
    const publicUrl = ['/login', '/register', '/verif_email', '/forgot_password/']
    const auth_req = !publicUrl.includes(to.path)
    const token = localStorage.getItem('token')
    const company = localStorage.getItem('company')

    if (!auth_req)
        next()

    if (auth_req) {
        if (!token || token.length == 0)
            next('/login')
        else {
            let access: Boolean = parseJwt(JSON.parse(token).access)
            let refresh: Boolean = parseJwt(JSON.parse(token).refresh)

            if (access) {
                if (to.path == '/create_company')
                    next()
                else
                    (company != "-1") ? next() : next('/create_company')
            } else if (refresh) {
                if (to.path == '/create_company')
                    next()
                else
                    (await refreshToken(token)) 
                        ? (company != "-1")
                            ? next() : next('/create_company')
                        : next('/login')
            } else
                next('/login')
        }
    }
})

export default router