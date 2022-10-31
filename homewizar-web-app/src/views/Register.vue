<script setup lang="ts">
    import axios from 'axios'
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import CustomButtonVue from '../components/CustomButtonVue.vue'
    import Modal from '../components/Modal.vue'
    import Dropdown from '../components/Dropdown.vue';
    import { useI18n } from 'vue3-i18n'


    const router = useRouter()
    const { t } = useI18n();
    let username = ref("")
    let email = ref("")
    let password = ref("")
    let password2 = ref("")
    let error = ref("")
    let loading = ref(false)
    let newlanguage = ref(localStorage.getItem("lang"))
    let language = ref(false)

    async function requestRegister() {
        if (username.value == "" || password.value == ""
            || email.value == "" || password2.value == "") {
            error.value = "Need to enter value for each input."
            return
        }
        if (password.value != password2.value) {
            error.value = "The two password need to be the same."
            return
        }
        error.value = ""
        loading.value = true
        return await axios.post(import.meta.env.VITE_APP_URL + "/api/user/register/", {
                username: username.value,
                email: email.value,
                password: password.value,
            }).then((response) => {
                loading.value = false
                localStorage.setItem('email', email.value)
                router.push('/verif_email')
            }).catch((er) => {
                loading.value = false
                error.value = "Email not valid."
            })
    }
    function chargeLoginPage() {
        router.push('/login')
    }

    async function changelanguage() {
        localStorage.setItem('lang', newlanguage.value || "")
        closeModal()
        window.location.reload()
    }

    function closeModal() {
        language.value = false
    }
</script>

<template>
    <section class="flex flex-row flex-nowrap h-screen w-screen bg-gray-100">

        <div class="relative hidden sm:flex pl-24 pt-48 w-1/2">
            <img class="absolute top-4 left-4 w-8 h-8"
                src="/img/logo_miniature_transparent.png" alt="logo homewizar" />
            <div class="w-full flex flex-col gap-4 justify-start">
                <p class="text-4xl">{{t('message.register.sol_ar')}}</p>
                <p class="text-xs text-gray-400 w-10/12">{{t('message.register.aim')}}</p>
            </div>
            <img class="absolute right-10 top-1/3 h-72 w-50 rounded-lg z-20"
                    src="/img/preview_mobile.jpg" alt="preview homewizar mobile"/>
            <img class="absolute inset-x-10 bottom-2 w-11/12 h-auto z-0 "
                src="/img/projectlogin.png" alt="preview homewizar"/>
        </div>

        <div class="bg-white h-full w-full sm:w-1/2 flex flex-col justify-center items-center px-12 sm:px-24">
            <div class="w-full flex flex-col justify-center items-start gap-1 mb-18">
                <Dropdown class="absolute top-0 left-3/4">
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
                                class="w-auto h-auto py-2 pr-6 pl-2 scroll-px-14 text-base border-gray-300 placeholder-gray-500 border rounded-md appearance-none focus:border-indigo-600 focus:outline-none"
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
                <div class="w-full flex flex-col justify-center items-start gap-1 mb-12">
                    <span class="text-2xl">{{t('message.register.register')}}</span>
                    <span class="text-xs text-gray-400 font-light tracking-wider">{{t('message.register.access_account')}}</span>
                </div>
            </div>

            <div class="flex flex-col w-full justify-center items-center">
                <div class="w-full">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                        {{t('message.register.enter_username')}}
                    </label>
                    <input v-model="username" type="text" :placeholder="t('message.register.enter_username')"
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                </div>
                <div class="w-full">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                        {{t('message.register.enter_email')}}
                    </label>
                    <input v-model="email" type="email" :placeholder="t('message.register.enter_email')"
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                </div>
                <div class="w-full">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                        {{t('message.register.enter_password')}}
                    </label>
                    <input v-model="password" type="password" :placeholder="t('message.register.enter_password')"
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                </div>
                <div class="relative w-full">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                        {{t('message.register.enter_password2')}}
                    </label>
                    <input @keyup.enter="requestRegister()"
                        v-model="password2" type="password" :placeholder="t('message.register.enter_password2')"
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                </div>
                <span class="w-full text-red-500 px-3 text-xs italic">{{ error }}</span>

                <div class="w-full mt-6">
                    <CustomButtonVue @clickEvent="requestRegister()"
                        :title="'Sign up'"
                        :loading="loading">
                    </CustomButtonVue>
                </div>

                <div class="flex justify-start w-full mt-4">
                <span class="text-xs">{{t('message.register.already_account')}} <a @click="chargeLoginPage()"
                    class="text-blue-500 cursor-pointer">{{t('message.register.signup')}}</a></span>
                </div>
            </div>
        </div>
    </section>
</template>