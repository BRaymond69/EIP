import { createApp } from 'vue'

import App from './App.vue'
import './index.css'
import i18n from './i18n'
import VueClickAway from "vue3-click-away"

import router from "./router/index"

const app = createApp(App)

app.use(i18n).use(VueClickAway).use(router).mount('#app')