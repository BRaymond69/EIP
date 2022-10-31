<script setup lang="ts">
    import axios from 'axios'

    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    import CustomButtonVue from '../components/CustomButtonVue.vue'
    import { useI18n } from 'vue3-i18n'

    const router = useRouter()
    const { t } = useI18n();
    let code = ref('')
    let error = ref('')

    let loading = ref(false)
    let loadingResend = ref(false)

    async function send() {
        const email = localStorage.getItem('email')

        if (code.value.length != 4) {
        error.value = "Need to add a code of 4 number."
        return
        }
        loading.value = true

        return await axios.get(import.meta.env.VITE_APP_URL + "/api/user/email_verification/", {
            params: {
            code: code.value,
            email: email
            }
        }).then(res => {
            loading.value = false
            error.value = ""
            router.push('/login')
        }).catch(error => {
            loading.value = false
            error.value = "Bad code try another one or send new code."
        })
    }

    async function resend() {
        const email = localStorage.getItem('email')
        loadingResend.value = true

        return await axios.get(import.meta.env.VITE_APP_URL + "/api/user/send_code/", {
            params: {
            email: email
            }
        }).then(res => {
            loadingResend.value = false
            error.value = ""
        }).catch(error => {
            loadingResend.value = false
            error.value = "Error during resend code, try later."
        })
    }

    </script>

<template>
    <section class="relative flex flex-col justify-center items-center h-screen w-screen bg-gray-100">
        <img class="absolute top-4 left-4 w-8 h-8" src="/img/logo_miniature_transparent.png" alt="logo homewizar" />
        <div class="flex flex-col justify-center items-center gap-2 w-3/12">
        <p class="text-xl font-extrabold text-gray-600">{{t('message.verifemail.chckemail')}}</p>
        <p class="text-xs text-gray-400 mb-4">{{t('message.verifemail.againsend')}}</p>
        <input v-model="code" type="password" :placeholder="t('message.register.code')"
            class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
        <span class="w-full text-red-500 px-3 text-xs italic">{{ error }}</span>

        <div class="w-full">
            <CustomButtonVue @clickEvent="send()"
            :title="t('message.home.send')"
            :loading="loading">
            </CustomButtonVue>
        </div>

        <div class="w-full">
            <CustomButtonVue @clickEvent="resend()"
            :title="t('message.login.resend')"
            :color="'bg-gray-300 hover:bg-gray-400'"
            :colorText="'text-gray-500'"
            :loading="loadingResend">
            </CustomButtonVue>
        </div>
        </div>

    </section>
</template>