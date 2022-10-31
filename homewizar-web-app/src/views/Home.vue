<script setup lang="ts">
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    import axios from '../assets/ts/axios'

    import TopBar from '../components/TopBar.vue'
    import RightBar from '../components/RightBar.vue'
    import Toast from '../components/Toast.vue'
    import Dropdown from '../components/Dropdown.vue'
    import Modal from '../components/Modal.vue'
    import CustomButtonVue from '../components/CustomButtonVue.vue'

    import Modelization from './Modelization.vue'
    import Company from './Company.vue'
    import Statistic from './Statistic.vue'
    import { useI18n } from 'vue3-i18n'

    interface ToastInterface {
        display: boolean,
        type: string,
        text: string
    }

    const { t } = useI18n();
    let page = ref("Home")
    let toastModal = ref({'display': false, 'type': 'success', 'text': ''})

    let modalContact = ref(false)
    let modalfiles = ref(false)
    let errorContact = ref('')
    let fileName = ref('')
    let inputUpdate = ref<{ tag: string, file: FileList | null}>({
        'tag': "Select",
        'file': null
    })
    let inputContact = ref({
        'body': "",
        'objet': "",
    })
    let modalSend_title = t('message.home.contact')
    let modalSend_btn = t('message.home.send')

    function changePageAction(tab: string) {
        page.value = tab
    }

    /* Toast */

    function openToast(toast: ToastInterface) {
        toastModal.value.display = true
        toastModal.value.type = toast.type
        toastModal.value.text = toast.text
        setTimeout(() => {
            toastModal.value.display = false
            toastModal.value.text = ''
        }, 3000);
    }

    function closeToast() {
        toastModal.value.display = false
        toastModal.value.text = ''
        inputContact.value = {
            'body': "",
            'objet': ""
        }
        errorContact.value = ""
    }

    /* Modal */
    function closeModalAdd () {
        modalfiles.value = false
    }

    function closeModal() {
        modalContact.value = false
        errorContact.value = ""
        inputContact.value = {
            'body': "",
            'objet': "",
        }
    }

    function changeUploadFile() {
        let files = (<HTMLInputElement>document.getElementById("fileInput"))

        if (!files)
            return
        let file = files.files

        if (file && file[0].name != null) {
            fileName.value = file[0].name
            inputUpdate.value.file = file
        } else {
            fileName.value = ''
            inputUpdate.value.file = null
        }
    }

    async function sendMessage() {
        if (inputContact.value.objet.length == 0 || inputContact.value.body.length == 0) {
            errorContact.value = "Need to add an object and body."
            return
        }

        return await axios.post('/api/send_email_contact/', inputContact.value)
            .then(res => {
                closeModal()
                openToast({
                    'display': true,
                    'type': 'success',
                    'text': 'Message send.'
                })
            }).catch(error => {
                closeModal()
                openToast({
                    'display': true,
                    'type': 'fail',
                    'text': 'Error during mail send.'
                })
            })
    }

</script>
<template>
    <section class="absolute right-0 w-11/12 bg-gray-100">
        <TopBar @open-toast="openToast($event)" 
            @changePage="changePageAction($event)" />
        <RightBar @changePage="changePageAction($event)"
            :currentPage="page" />

        <a @click="modalContact = true" class="fixed bottom-8 right-8 z-10 cursor-pointer">
            <span class="flex h-10 w-10 transition-all duration-500 hover:scale-110">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                <span class="relative flex items-center justify-center rounded-full h-10 w-10 bg-blue-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                    </svg>
                </span>
            </span>
        </a>

    </section>
    
    <section class="absolute right-0 w-11/12 bg-gray-100">

        <transition
                enter-active-class="duration-300 ease-out"
                enter-from-class="transform opacity-0 translate-x-32"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="duration-200 ease-in"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="transform opacity-0 translate-x-32">
            
            <div v-if="page == 'Home'" class="w-full flex flex-wrap justify-center gap-4 bg-gray-100" style="min-height:100vh;padding-top:20vh;">
                <img src="/img/logo_transparent.png"
                    class="h-24 md:h-36" alt="logo homewizar"/>
                <div class="w-full h-auto flex flex-row items-center justify-center flex-wrap absolute -bottom-20">
                    <img src="/img/menumobile.jpg"
                        class="min-h-96 md:h-96 shadow shadow-slate-300 hover:animate-bounce" alt="HomeWizar Mobile Menu"/>
                </div>
            </div>
        </transition>

        <transition
                enter-active-class="duration-300 ease-out"
                enter-from-class="transform opacity-0 translate-x-32"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="duration-200 ease-in"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="transform opacity-0 translate-x-32">
            
            <div v-if="page == 'Modelization'" class="w-full p-4 flex flex-row flex-wrap justify-center items-center gap-4 bg-gray-100" style="min-height:100vh;padding-top:20vh;">

                <Modelization @open-toast="openToast($event)" />

            </div>
        </transition>

        <transition
                enter-active-class="duration-300 ease-out"
                enter-from-class="transform opacity-0 translate-x-32"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="duration-200 ease-in"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="transform opacity-0 translate-x-32">
            
            <div v-if="page == 'Company'" class="w-full p-4 flex flex-row flex-wrap justify-center items-center gap-4 bg-gray-100" style="min-height:100vh;padding-top:20vh;">

                <Company @open-toast="openToast($event)" />

            </div>
        </transition>

        <transition
                enter-active-class="duration-300 ease-out"
                enter-from-class="transform opacity-0 translate-x-32"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="duration-200 ease-in"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="transform opacity-0 translate-x-32">
            
            <div v-if="page == 'Statistic'" class="w-full p-4 flex flex-row flex-wrap justify-center items-center gap-4 bg-gray-100" style="min-height:100vh;padding-top:20vh;">

                <Statistic @open-toast="openToast($event)" />

            </div>
        </transition>

    </section>

    <Toast @close-toast="closeToast()" :toast="toastModal" />

    <Modal :show="modalContact"
        :title="modalSend_title"
        :nameValidButton="modalSend_btn"
        width="70"
        :closeOnClick="true"
        @validate="sendMessage()"
        @close="closeModal()">

        <template #content>
            <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                    {{t('message.home.enterobj')}}
                </label>
                <input v-model="inputContact.objet" type="text" :placeholder="t('message.home.obj')"
                    class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
            </div>
            <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                    {{t('message.home.entermsg')}}
                </label>
                <textarea v-model="inputContact.body" type="text" :placeholder="t('message.home.msg')"
                    class="appearance-none block w-full h-48 bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                </textarea>
            </div>
            <!-- <div class="w-full px-3">
                <button @click="modalfiles = true" class="px-6 py-2 bg-blue-700 border border-blue-700 text-sm rounded text-white focus:outline-none hover:border-blue-600 hover:bg-blue-600 transition-colors duration-500">{{t('message.home.addfile')}}</button>
            </div> -->
            <span class="text-red-500 px-3 text-xs italic">{{ errorContact }}</span>

        </template>

    </Modal>
<!-- 
    <Modal :show="modalfiles"
        title="Add new file (img or pdf)"
        nameValidButton="Add new file"
        width="40"
        :closeOnClick="true"
        @close="closeModalAdd()">

        <template #content>
            <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                    {{t('message.modelization.chooseimg')}}
                </label>
                <div class="max-w-md mx-auto rounded-lg overflow-hidden md:max-w-xl">
                    <div class="md:flex">
                        <div class="w-full p-3">
                            <div class="relative h-36 rounded-lg border-dashed border-2 border-blue-700 bg-gray-100 flex justify-center items-center">
                                <div class="absolute">
                                    <div class="flex flex-col items-center"> 
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                        <span class="block text-gray-400 font-normal">
                                            {{t('message.modelization.choosefile')}}(.jpg, .png)
                                        </span>
                                    </div>
                                </div> <input id="fileInput" type="file" class="h-full w-full opacity-0 cursor-pointer" @change="changeUploadFile()" name="">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <span class="text-red-500 px-3 text-xs italic">{{ errorContact }}</span>

        </template>

    </Modal> -->


</template>