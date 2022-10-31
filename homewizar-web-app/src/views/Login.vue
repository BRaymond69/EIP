<script setup lang="ts">
    import axios from 'axios'
    import instance from '../assets/ts/axios'
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import CustomButtonVue from '../components/CustomButtonVue.vue'
    import Modal from '../components/Modal.vue'
    import Dropdown from '../components/Dropdown.vue';
    import { useI18n } from 'vue3-i18n'

    const router = useRouter()
    let username = ref("")
    let password = ref("")
    let error = ref("")
    let loading = ref(false)
    let modalForgot = ref(false)
    let inputForgot = ref('')
    let errorForgot = ref('')
    let success = ref('en')
    let newlanguage = ref(localStorage.getItem("lang"))
    let language = ref(false)
    const { t } = useI18n();


    async function getUserInformation() {
        return await instance.get("/api/users/retrieve_user/")
        .then(res => {
            localStorage.setItem('company', (res.data.company) 
                                            ? res.data.company : -1)
            if (res.data.company)
            localStorage.setItem('role', res.data.user_type)
        }).catch(error => {})
    }

    async function requestLogin() {
        if (username.value == "" || password.value == "") {
        error.value = "Need to add a value."
        return
        }
        error.value = ""
        loading.value = true
        return await axios.post(import.meta.env.VITE_APP_URL + "/api/token/", {
            username: username.value,
            password: password.value
        }).then(async (response) => {
            localStorage.setItem('token', JSON.stringify({
            'refresh': response.data.refresh, 
            'access': response.data.access
            }))
            await getUserInformation()
            loading.value = false
            router.push('/')
        }).catch((er) => {
            loading.value = false
            error.value = "The username or password is incorrect."
        })
    }

    function chargeRegisterPage() {
        router.push('/register')
    }
    /* Modal */
    async function sendForgot() {
        errorForgot.value = ""
        success.value = ""
        if (inputForgot.value.length == 0) {
        errorForgot.value = "Need to enter a valid email"
        return
        }
        return await axios.get(import.meta.env.VITE_APP_URL + '/api/user/send_reset_password/', {
        params: {
            email: inputForgot.value
        }
        }).then(res => {
        errorForgot.value = ""
        success.value = "Follow instruction in the email receive in you email box."
        }).catch(error => {
        success.value = ""
        errorForgot.value = "Email not valid, try with another email."
        })
    }

    async function changelanguage() {
        localStorage.setItem('lang', newlanguage.value || "")
        closeModal()
        window.location.reload()
    }

    function closeModal() {
        modalForgot.value = false
        language.value = false
        inputForgot.value = ""
        errorForgot.value = ""
        success.value = ""
    }
    

</script>

<template>
    <section class="flex flex-row flex-nowrap h-screen w-screen bg-gray-100">

        <div class="relative hidden sm:flex pl-24 pt-48 w-1/2">
            <img class="absolute top-4 left-4 w-8 h-8"
                src="/img/logo_miniature_transparent.png" alt="logo homewizar" />
            <div class="w-full flex flex-col gap-4 justify-start">
                <p class="text-4xl">{{t('message.login.sol_ar')}}</p>
                <p class="text-xs text-gray-400 w-10/12">{{t('message.login.aim')}}</p>
            </div>
            <img class="absolute right-10 top-1/3 h-72 w-50 rounded-lg z-20"
                    src="/img/preview_mobile.jpg" alt="preview homewizar mobile"/>
            <img class="absolute inset-x-10 bottom-2 w-11/12 h-auto z-0 "
                src="/img/projectlogin.png" alt="preview homewizar"/>
        </div>

        <div class="bg-white h-full w-full sm:w-1/2 flex flex-col justify-center items-center px-12 sm:px-24">
            <div class="w-full flex flex-col justify-center items-start gap-1 mb-20">
                <Dropdown class="absolute top-0 left-3/4 items-center justify-center">
                    <div class="flex flex-row items-center pl-2 cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                        </svg>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-gray-600" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                        </svg>
                    </div>
                    <template #content>
                        <div class="relative inline-block text-gray-500 w-auto p-2  ">

                            <select v-model="newlanguage"
                                @change="changelanguage()"
                                class="w-auto h-auto py-2 pr-6 pl-2  scroll-px-14 text-base border-gray-300 placeholder-gray-500 border rounded-md appearance-none focus:border-indigo-600 focus:outline-none"
                                aria-label="Select language">
                                <option value="en" selected>English</option>
                                <option value="de">Deutsch</option>
                                <option value="fr">Français</option>
                                <option value="es">Español</option>
                                <option value="ko">한국어</option>
                            </select>
                            <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                                <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
                                    <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path>
                                </svg>
                            </div>
                        </div>
                    </template>
                </Dropdown>            
                <span class="text-2xl">{{t('message.login.login')}}</span>
                <span class="text-xs text-gray-400 font-light tracking-wider">{{t('message.login.access_account')}}</span>
            </div>
            <div class="flex flex-col w-full justify-center items-center gap-2">
                <div class="w-full">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                        {{t('message.login.username')}}
                    </label>
                    <input v-model="username" type="text" :placeholder="t('message.login.username') + '...'"
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                    </div>
                    <div class="relative w-full">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                        {{t('message.login.password')}}
                    </label>
                    <input @keyup.enter="requestLogin()"
                        v-model="password" type="password" :placeholder="t('message.login.password') + '...'"
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                    <a @click="modalForgot = true"
                        class="absolute top-0 right-0 text-blue-500 cursor-pointer text-xs">{{t('message.login.fpassword')}}</a>
                </div>
                <span class="w-full text-red-500 px-3 text-xs italic">{{ error }}</span>

                <div class="w-full mt-2">
                    <CustomButtonVue @clickEvent="requestLogin()"
                        :title="'Sign in'"
                        :loading="loading">
                    </CustomButtonVue>
                    </div>
                <div class="flex justify-start w-full mt-4">
                    <span class="text-xs">{{t('message.login.noaccount')}} <a @click="chargeRegisterPage()" class="text-blue-500 cursor-pointer">{{t('message.login.signup')}}</a></span>
                </div>
            </div>
        </div>
        <Modal :show="modalForgot"
            :title="t('message.login.fpassword')"
            :nameValidButton="t('message.home.send')"
            width="60"
            :closeOnClick="true"
            @validate="sendForgot()"
            @close="closeModal()">
            <template #content>
                <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                    {{t('message.login.inputemail')}}
                </label>
                <input v-model="inputForgot" type="text" :placeholder="t('message.login.inputemail') + '...'"
                    class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                </div>
                <span class="text-green-500 px-3 text-xs italic">{{ success }}</span>
                <span class="text-red-500 px-3 text-xs italic">{{ errorForgot }}</span>
            </template>
        </Modal>    
    </section>
</template>