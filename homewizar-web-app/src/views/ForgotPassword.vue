<script setup lang="ts">
    import axios from 'axios'

    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    import CustomButtonVue from '../components/CustomButtonVue.vue'
    import Modal from '../components/Modal.vue'
    import { useI18n } from 'vue3-i18n'


    const router = useRouter()
    const { t } = useI18n();
    let modal_btn = t('message.home.send')
    let password = ref('')
    let password2 = ref('')
    let error = ref('')

    let loading = ref(false)

    async function send() {
        if (password.value.length == 0 && password2.value.length == 0) {
            error.value = "Besoin de remplir les 2 champs."
            return
        }

        if (password.value != password2.value) {
            error.value = "Les deux mots de passe doivent être identique."
            return
        }
        loading.value = true

        let params = new URLSearchParams(window.location.search)
        let token = params.get('token')
        let id = params.get('id')

        return await axios.post(import.meta.env.VITE_APP_URL + "/api/user/reset_password/?token=" + token, {
                id: id,
                password: password2.value
            }).then(res => {
                loading.value = false
                error.value = ""
                router.push('/login')
            }).catch(error => {
                loading.value = false
                error.value = "Erreur durant le changement de mots de passe, réessayer plus tard."
            })
    }

</script>

<template>
  <section class="relative flex flex-col justify-center items-center h-screen w-screen bg-gray-100">
    <img class="absolute top-4 left-4 w-8 h-8"
      src="/img/logo_miniature_transparent.png" alt="logo homewizar" />

    <div class="flex flex-col justify-center items-center gap-2 w-5/12">
        <p class="w-full text-xl font-extrabold text-gray-600">{{t('message.forget.reset')}}</p>
        <p class="w-full text-xs text-gray-400 mb-4">{{t('message.forget.confirm')}}</p>
        <div class="w-full">
            <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                {{t('message.forget.enterpwd')}}
            </label>
            <input v-model="password" type="password" :placeholder="t('message.login.password') + '...'"
                class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
        </div>
        <div class="w-full">
            <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                {{t('message.forget.enterpwd2')}}
            </label>
            <input @keyup.enter="send()"
                v-model="password2" type="password" :placeholder="t('message.login.password') + '...'"
                class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
        </div>
        <span class="w-full text-red-500 px-3 text-xs italic">{{ error }}</span>

        <div class="w-full">
            <CustomButtonVue @clickEvent="send()"
            :title="modal_btn"
            :loading="loading">
            </CustomButtonVue>
        </div>

    </div>

  </section>
</template>