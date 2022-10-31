<script setup lang="ts">
    import { ref } from 'vue'

    import axios from '../assets/ts/axios'

    import DataTable from '../components/DataTable.vue'
    import Dropdown from '../components/Dropdown.vue'
    import Modal from '../components/Modal.vue'
    import CustomButtonVue from '../components/CustomButtonVue.vue'
    import { useI18n } from 'vue3-i18n'


    const emit = defineEmits(['open-toast'])
    const { t } = useI18n();

    let users = ref([])
    let closeDropdown = ref(false)
    let idCompany = ref(0)

    let modalAddUser = ref(false)
    let inputEmail = ref('')
    let errorEmail = ref('')
    let dataModel = ref([{
        name: "",
    }])

    let get_user = ref([])
    let modal_title = t('message.company.addstaff')

    async function getListUser() {
        return await axios.get('/api/company/get_staff/')
            .then(res => {
                users.value = res.data
            }).catch(error => {
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Error during getting staff user list.'
                })
            })
    }

    async function getUserInfo() {
        return await axios.get('/api/users/retrieve_user/')
            .then(res => {
                idCompany.value = res.data.company
            }).catch(error => {
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Error during getting information profil.'
                })
            })
    }

    interface  ParamsInterface { 
        params: { 
            user_id?: number, 
            username?: string 
        } 
    }

    async function getLogsUser() {
        let id: number = 0
        let user_id: number = 0
        let username: string = ""

        return await axios.get('/api/company/logs')
            .then(res => {
                dataModel.value = res.data.reverse()
                dataModel.value.forEach((el: any )=> {
                    get_user.value.forEach((element: any) => {
                        if (element.id === el.user_id) {
                            el['name'] = element.username
                        }
                    })
                })
            }).catch(error => {
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Error during getting information profil.'
                })
            })
    }

    async function getallUserInfo() {
        return await axios.get('/api/users')
            .then(res => {
                get_user.value = res.data
            }).catch(error => {
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Error during getting information profil.'
                })
            })
    }

    /* Action */

    function deleteUser(id: number) {
        return axios.delete('/api/company/' + id + '/remove_user/')
            .then(res => {
                getListUser()
                emit('open-toast', {
                    'type': 'success',
                    'text': 'Users delete from the company.'
                })
            }).catch(error => {
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Fail during user deletion: try again later or contact the support team.'
                })
            })
    }

    /* Modal */

    async function addUser() {
        if (inputEmail.value.length == 0) {
            errorEmail.value = "Need to enter a valid email."
            return
        }

        return await axios.post('/api/company/' + idCompany.value + '/add_user/', {
                'email': inputEmail.value
            }).then(res => {
                closeModal()
                getListUser()
                emit('open-toast', {
                    'type': 'success',
                    'text': 'User add to the company.'
                })
            }).catch(error => {
                closeModal()
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Error during adding user to the staff company.'
                })
            })
    }

    function gettypes(mytypes: any) {
        if (mytypes === 'create_product') {
            return t('message.topbar.created')
        }
        if (mytypes === 'update_product') {
            return t('message.topbar.updated')
        }
        if (mytypes === 'product_delete') {
            return t('message.topbar.deleted')
        }
        if (mytypes === 'generate_model	') {
            return t('message.topbar.generate')
        }
    }

    function getjsontodate(date: any) {
        if (date){
            date = date.split('T')
            return (date[0] + ' ' + date[1].substring(0,8))
        }
    }

    function closeModal() {
        modalAddUser.value = false
        inputEmail.value = ""
        errorEmail.value = ""
    }

    /* Mounted */
    async function mount() {
        await getListUser()
        await getallUserInfo()
        await getLogsUser()
        await getUserInfo()
    }

    mount()

</script>

<template>
    <div class="relative flex flex-col w-full sm:w-1/2 bg-white p-8 rounded transition-shadow duration-500 border border-gray-100 shadow-lg hover:shadow-xl h-fit">
        <div class="w-full flex flex-col justify-center items-start gap-1 mb-8">
            <span class="font-bold text">{{t('message.company.list_staff')}}</span>
            <span class="text-xs text-gray-400 font-light tracking-wider">{{t('message.company.list_staff_company')}}</span>
            <span class="w-full bg-gray-200" style="height:1px;"></span>
        </div>

        <div class="w-full flex flex-row flex-wrap justify-between items-center gap-2 pb-3">
            <CustomButtonVue @clickEvent="modalAddUser = true"
                :title="modal_title"
                :loading="false">
            </CustomButtonVue>
        </div>

        <DataTable
            :data="users"
            :is_action="true"
            :slotHeaders="true">
            
            <template v-slot:header>
                <th class="table-cell p-5 text-gray-500 font-medium">{{t('message.company.type')}}</th>
                <th class="table-cell p-5 text-gray-500 font-medium">{{t('message.company.name')}}</th>
                <th class="table-cell p-5 text-gray-500 font-medium">{{t('message.company.actions')}}</th>
            </template>

            <template v-slot:row="{row, index}">
                <td class="table-cell p-3 font-thin text-sm">
                    <span class="bg-blue-100 px-3 py-1 text-xs text-blue-600 font-semibold rounded-2xl select-none">
                        {{t('message.company.staff')}}
                    </span>
                </td>
                <td class="table-cell p-3 font-thin text-sm">
                    {{ row.user__username }}
                </td>
                <td class="flex flex-row items-center justify-between p-3 font-thin md:w-6/12">
                    <Dropdown
                        width="w-48 right-0"
                        :closeModal="closeDropdown">
                        <div class="flex justify-center items-center p-2 cursor-pointer transition-all duration-500 hover:bg-gray-100 hover:text-gray-400 rounded">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                            </svg>
                        </div>
                        <template #content>
                            <div class="bg-white p-6 flex flex-col space-y-3">

                                <div>
                                    <span @click="deleteUser(row.pk)"
                                        class="text-gray-500 transition hover:text-red-700 cursor-pointer">
                                        {{t('message.company.delete')}}
                                    </span>
                                </div>

                            </div>
                        </template>
                    </Dropdown>
                </td>
            </template>
        </DataTable>


        <div v-if="users.length == 0"
            class="w-full flex items-center justify-center pt-2">
            <h1 class="text-gray-500 text-sm">{{t('message.company.nostaff')}}</h1>
        </div>
    </div>
        <div class="relative flex flex-col w-full sm:w-1/2 bg-white p-8 rounded transition-shadow duration-500 border border-gray-100 shadow-lg hover:shadow-xl h-fit">
        <div class="w-full flex flex-col justify-center items-start gap-1 mb-8">
            <span class="font-bold text">{{t('message.history.message_product')}}</span>
            <span class="text-xs text-gray-400 font-light tracking-wider">{{t('message.history.submsg_product')}}</span>
            <span class="w-full bg-gray-200" style="height:1px;"></span>
        </div>

        <DataTable
            :data="dataModel"
            :is_action="true"
            :slotHeaders="true">
            
            <template v-slot:header>
                <th class="table-cell p-5 text-gray-500 font-medium">{{t('message.history.createby')}}</th>
                <th class="table-cell p-5 text-gray-500 font-medium">{{t('message.history.lastupdate_person')}}</th>
                <th class="table-cell p-5 text-gray-500 font-medium">{{t('message.history.lastupdate_date')}}</th>
            
            </template>

            <template v-slot:row="{row}">
                <td class="hidden sm:table-cell p-3 font-light text-sm">
                    {{row.name}}
                </td>
                <td class="hidden sm:table-cell p-3 font-light text-sm">
                    {{gettypes(row.types)}}
                </td>
                <td class="p-3 font-light text-sm">
                   {{getjsontodate(row.created)}}
                </td>
        
            </template>
        </DataTable>
    </div>

    <Modal :show="modalAddUser"
        :title="modal_title"
        :nameValidButton="modal_title"
        width="60"
        :closeOnClick="true"
        @validate="addUser()"
        @close="closeModal()">

        <template #content>
            <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                    {{t('message.company.emailusr')}}
                </label>
                <input v-model="inputEmail" type="text" :placeholder="t('message.company.emailusr')"
                    class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
            </div>
            <span class="text-red-500 px-3 text-xs italic">{{ errorEmail }}</span>

        </template>

    </Modal>
</template>