import axios from 'axios'
import jwt_decode from 'jwt-decode';

interface DateInterface {
    exp: number
}

function parseJwt(token: string): boolean {
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
        window.location.href = "/login"
        return false
    })
}

const instance = axios.create({
    baseURL: import.meta.env.VITE_APP_URL,
    headers: {
        "Content-Type": "application/json",
    },
})

instance.interceptors.request.use(
    async (config) => {
        const token = localStorage.getItem('token')
        let access = false
        let refresh = false

        if (token) {
            access = parseJwt(JSON.parse(token).access)
            refresh = parseJwt(JSON.parse(token).refresh)
        }
        if (access && token && config.headers)
            config.headers['Authorization'] = 'Bearer ' + JSON.parse(token).access
        else if (refresh && token) {
            (await refreshToken(token) && config.headers) ? config.headers['Authorization'] = 'Bearer ' + JSON.parse(token).access : null
        } else
            window.location.href = "/login"

        return config
    },
    (error) => {
        window.location.href = "/login"
        return Promise.reject(error)
    }
)

export default instance