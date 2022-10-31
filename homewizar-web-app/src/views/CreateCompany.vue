<script setup lang="ts">
    import axios from '../assets/ts/axios'

    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    import CustomButtonVue from '../components/CustomButtonVue.vue'
    import Modal from '../components/Modal.vue'
    import { useI18n } from 'vue3-i18n'


    const router = useRouter()
    const { t } = useI18n();

    let loading = ref(false)
    let entreprise = ref('')
    let siret = ref('')
    let error = ref('')

    async function create() {
        if (entreprise.value.length == 0 || siret.value.length == 0) {
            error.value = "Besoin de rentrer une valuer pour le numéro de siret et pour le nom."
            return
        }

        if (siret.value.length != 14) {
            error.value = "Le numéro de siret doit être composé de 14 chiffres."
            return
        }

        error.value = ""
        loading.value = true

        return await axios.post("/api/company/", {
                name: entreprise.value,
                siret: siret.value,
            }).then(res => {
                loading.value = false
                localStorage.removeItem('token')
                localStorage.removeItem('company')
                router.push('/login')
            }).catch(error => {
                loading.value = false
                error.value = "Le numéro de siret n'est pas valide."
            })
    }

</script>

<template>
    <section class="relative flex flex-col justify-center items-center gap-12 h-screen w-screen bg-gray-100">
        <img class="absolute top-4 left-4 w-8 h-8"
            src="/img/logo_miniature_transparent.png" alt="logo homewizar" />

        <div class="flex flex-col justify-center items-center w-6/12">
            <p class="w-full text-2xl font-extrabold text-gray-600">{{t('message.createCompany.create')}}</p>
            <p class="w-full text-xs text-gray-400 mb-4">{{t('message.createCompany.descript_create')}}</p>
            <div class="w-full">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                    {{t('message.createCompany.name')}}
                </label>
                <input v-model="entreprise" type="text" placeholder="Name..."
                    class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
            </div>
            <div class="w-full">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                    {{t('message.createCompany.nbrsiret')}}
                </label>
                <input v-model="siret" type="text" placeholder="SIRET..."
                    class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
            </div>
            <span class="w-full text-red-500 px-3 text-xs italic">{{ error }}</span>


            <div class="w-full">
                <CustomButtonVue @clickEvent="create()"
                :title="'Create company'"
                :loading="loading">
                </CustomButtonVue>
            </div>
        </div>

        <div class="flex flex-col justify-center items-center gap-12 w-6/12">
            <div class="flex flex-row justify-center items-center gap-1 flex-nowrap w-full">
                <span class="w-1/2 bg-gray-300" style="height:1px;"></span>
                <p class="text-lg text-gray-500">ou</p>
                <span class="w-1/2 bg-gray-300" style="height:1px;"></span>
            </div>
            <p class="text-center text-gray-500 text-sm">{{t('message.createCompany.manager')}}</p>
        </div>

    </section>
</template>