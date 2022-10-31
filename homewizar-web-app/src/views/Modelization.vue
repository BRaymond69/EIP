<script setup lang="ts">
    import { ref, computed } from 'vue'

    import axios from '../assets/ts/axios'
    import QRious from 'qrious'

    import DataTable from '../components/DataTable.vue'
    import Dropdown from '../components/Dropdown.vue'
    import Modal from '../components/Modal.vue'
    import CustomButtonVue from '../components/CustomButtonVue.vue'
    import { useI18n } from 'vue3-i18n'

    const emit = defineEmits(['open-toast'])
    const { t } = useI18n();

    let closeDropdown = ref(false)
    let modalCreateProduct = ref(false)
    let modalCreateTags = ref(false)
    let modalPreview = ref(false)
    let modalUpdateProduct = ref(false)
    let generateModal = ref(false)
    let modalViewImg= ref(false)
    let img_name = ref('')
    let previewId = ref(0)
    let imageUrl = ref('')
    let page = ref(0)

    
    let modalCreateProduct_title = t('message.modelization.createpdt')
    let modalPreview_title = t('message.modelization.preview')
    let modalViewImg_title = t('message.modelization.preimg')
    let modalCreateTags_title = t('message.modelization.createtag')
    let modalGenerateModal_title = t('message.modelization.generateobj')
    let modalUpdateProduct_title = t('message.modelization.updatepdt')
    let modalCreateProduct_btn = t('message.modelization.ttlbuttoncreate')
    let modalPreview_btn = t('message.modelization.dlqrcode')
    let modalCreateTags_btn = t('message.modelization.createtag')
    let modalGenerateModal_btn = t('message.modelization.ttlbuttongenerate')
    let modalUpdateProduct_btn = t('message.modelization.ttlbuttonupdate')
    let nameplaceholder = t('message.modelization.entername')
    let tagplaceholder = t('message.modelization.tagname')
    let linkpro = t('message.modelization.linkpro')
    let headers = ref(['', 'Name', 'Tags', 'Generate', 'Actions', ''])
    let dataModel = ref({
                        count: 0,
                        results: []
                    })
    let tags = ref([{id: -1, name: ""}])

    let filtreName = ref('')
    let filtreTags = ref('all')

    let inputUpdate = ref<{ tag: string, file: FileList | null}>({
        'tag': "Select",
        'file': null
    })
    let fileName = ref('')
    let errorUpdate = ref('')

    let inputCategory = ref('Chaises')
    let idObjet = ref(-1)

    let inputCreate = ref({
        'name': "",
        'is_public': "1",
        'redirect_link': ""
    })
    let errorCreate = ref('')
    let loadingCreate = ref(false)

    let inputCreateTags = ref('')
    let errorTags = ref('')

    /* Interface */
    interface  ParamsInterface { 
        params: { 
            name?: string, 
            tags?: string 
        } 
    }

    /* Tools */
    function getParseDate(date: string) {
        const utcTime = date.split('T')[0]
        return utcTime
    }

    function truncate(string: string, len: number, concat: string) {
        if (string.length < len)
            return string
        return string.substring(0, len) + concat
    }

    /* Actions */
    function preview(id: number) {
        modalPreview.value = true
        previewId.value = id
    }

    function update(id: number) {
        modalUpdateProduct.value = true
        previewId.value = id
    }

    async function download(id: number) {
        axios({
            url: '/api/objects/' + id + '/download/',
            method: 'GET',
            responseType: 'blob',
        }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const a = document.createElement('a')

            document.body.appendChild(a)
            a.href = url
            a.download = "download.glb"
            a.click()

            setTimeout(() => {
                window.URL.revokeObjectURL(url)
                document.body.removeChild(a)
            }, 0)
            emit('open-toast', {
                'type': 'success',
                'text': 'Download success.'
            })
        }).catch(error => {
            emit('open-toast', {
                'type': 'fail',
                'text': 'Error during download.'
            })
        })
    }

    function openGenerateObject(id: number) {
        generateModal.value = true
        idObjet.value = id
    }

    function openImage(list_id: Array<number>) {
        let id = list_id[0]

        axios({
            url: '/api/images/' + id + '/download/',
            method: 'GET',
            responseType: 'blob',
        }).then((response) => {
            imageUrl.value = window.URL.createObjectURL(new Blob([response.data]))
            modalViewImg.value = true
        }).catch(error => {
            emit('open-toast', {
                'type': 'fail',
                'text': 'Fail to download image preview.'
            })
        })
    }

    async function generateObject() {
        if (idObjet.value == -1) {
            closeCreateModal()
            emit('open-toast', {
                'type': 'fail',
                'text': 'Error during object generation, try to upload an image if you have not already do it.'
            })
        }
        return await axios.get('/api/generate_object/', {
            params: {
                id: idObjet.value,
            }
        })
        .then(res => {
            getModels()
            emit('open-toast', {
                'type': 'success',
                'text': 'Success object is generate.'
            })
        }).catch(error => {
            emit('open-toast', {
                'type': 'fail',
                'text': 'Error during object generation, try to upload an image if you have not already do it.'
            })
        })
    }

    async function deleteModel(id: number) {
        return await axios.delete('/api/product/' + id + '/delete/')
            .then(res => {
                getModels()
                emit('open-toast', {
                    'type': 'success',
                    'text': 'Deletion success.'
                })
            }).catch(error => {
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Error during deletion.'
                })
            })
    }

    /* Table */

    interface  ParamsInterface { 
        params: { 
            name?: string, 
            tags?: string 
        } 
    }

    async function getModels() {
        let params: ParamsInterface = { params: { name: "", tags: "" } }

        if (filtreName.value.length != 0)
            params.params.name = filtreName.value
        else
            delete params.params.name

        if (filtreTags.value.length != 0 && filtreTags.value != "all")
            params.params.tags = filtreTags.value
        else
            delete params.params.tags

        return await axios.get('/api/product/', params)
            .then(res => {
                dataModel.value = res.data
            }).catch( error => {
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Error during product retrieval.'
                })
            } )
    }

    async function getTags() {
        return await axios.get('/api/tags/')
            .then(res => {
                tags.value = res.data
            }).catch( error => {
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Error during tag retrieval.'
                })
            } )
    }

    function getNameTags(id: number) {
        let name: string = ""

        tags.value.forEach(element => {
            if (element.id == id)
                name = element.name            
        })
        return name
    }

    /* Modal */

    function closeCreateModal() {
        modalCreateProduct.value = false
        modalPreview.value = false
        modalUpdateProduct.value = false
        modalCreateTags.value = false
        modalViewImg.value = false
        generateModal.value = false
        
        loadingCreate.value = false
        
        inputCreateTags.value = ""
        inputCreate.value = {
            'name': "",
            'is_public': "",
            'redirect_link': ""
        }
        inputUpdate.value = {
            'tag': "Select",
            'file': null
        }

        idObjet.value = -1
        errorCreate.value = ""
        errorTags.value = ""
        errorUpdate.value = ""
    }

    async function create() {
        if (inputCreate.value.name == '') {
            errorCreate.value = "Need to enter value for name."
            return
        } else if (inputCreate.value.is_public == '') {
            errorCreate.value = "Need to enter value for public or private product."
            return
        }
        loadingCreate.value = true
        return await axios.post("/api/product/", inputCreate.value)
            .then(res => {
                createTags()
                emit('open-toast', {
                    'type': 'success',
                    'text': 'Success during product creation.'
                })

            }).catch(error => {
                closeCreateModal()
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Fail during product creation.'
                })
            })
    }

    async function createTags() {
        errorTags.value = ""
        if (inputCreateTags.value.length == 0) {
            errorTags.value = "Need to enter a valid name tags."
            return
        }

        return await axios.post("/api/tags/", { 'name': inputCreateTags.value })
            .then(res => {
                errorTags.value = ""
                closeCreateModal()
                getTags()
                emit('open-toast', {
                    'type': 'success',
                    'text': 'Success during tags creation.'
                })
            }).catch(error => {
                closeCreateModal()
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Fail during tags creation.'
                })
            })
    }

    function genQrCode(id: number) {
        let qr = new QRious({ 
            background: 'white',
            level: 'H',
            padding: 25,
            size: 300,
            value: previewId.value.toString()
         })

        return qr.toDataURL('image/jpeg')
    }

    function downloadQrcode() {
        modalPreview.value = false
        let qr = new QRious({ 
            background: 'white',
            level: 'H',
            padding: 25,
            size: 300,
            value: previewId.value.toString()
         })
        const url = qr.toDataURL('image/jpeg')
        const a = document.createElement('a')

        document.body.appendChild(a)
        a.href = url
        a.download = "qrcode.jpg"
        a.click()

        setTimeout(() => {
            window.URL.revokeObjectURL(url)
            document.body.removeChild(a)
            emit('open-toast', {
                'type': 'success',
                'text': 'Success download QrCode.'
            })
        }, 0)
    }

    async function updateProduct() {
        let success: boolean = false

        errorUpdate.value = ""

        if (inputUpdate.value.tag.length != 0 && inputUpdate.value.tag != "Select") {

            await axios.post('/api/product/' + previewId.value + '/add_tags/', {
                'tags': [inputUpdate.value.tag]
            }).then(res => {
                success = true
            }).catch(error => {
                success = false
            })
        }

        if (inputUpdate.value.file != null) {
            let file = inputUpdate.value.file[0]
            let data = new FormData()

            data.append('product', previewId.value.toString())
            data.append('file', file)
            await axios.post('/api/images/', data, {
                headers : {
                    'Content-Type' : 'multipart/form-data'
                }
            }).then(res => {
                success = true
                fileName.value = ''
            }).catch(error => {
                success = false
                fileName.value = ''
            })
        }

        if (success) {
            emit('open-toast', {
                'type': 'success',
                'text': 'Success update product.'
            })
            closeCreateModal()
            getModels()
        } else if (inputUpdate.value.file == null 
            && inputUpdate.value.tag == "Select")
            errorUpdate.value = "Need to add an image or to select a tag."
        else {
            emit('open-toast', {
                'type': 'fail',
                'text': 'Fail during update product.'
            })
            closeCreateModal()
            getModels()
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


    function up() {
        page.value = page.value + 1
    }

    function down() {
        page.value = page.value - 1
    }

    /* Mounted */
    async function mount() {
        await getModels()
        await getTags()
    }
    mount()
</script>

<template>
    <div class="relative flex flex-col w-full bg-white p-8 rounded transition-shadow duration-500 border border-gray-100 shadow-lg hover:shadow-xl h-fit">
        <div class="w-full flex flex-col justify-center items-start gap-1 mb-8">
            <span class="font-bold text">{{t('message.modelization.lstprod')}}</span>
            <span class="text-xs text-gray-400 font-light tracking-wider">{{t('message.modelization.widget')}}</span>
            <span class="w-full bg-gray-200" style="height:1px;"></span>
        </div>
        <div class="w-full flex flex-row flex-wrap justify-between items-center gap-2 pb-3">
            <div class="flex flex-row justify-start items-center flex-wrap gap-4">
                <div class="flex flex-row justify-center items-center">
                    <input v-model="filtreName" @change="getModels()" @keyup.enter="getModels()"
                        type="text" :placeholder="t('message.modelization.entername')"
                        class="appearance-none block w-26 bg-white border-gray-100 shadow-lg text-gray-700 border rounded-l py-2 px-2 leading-tight transition-shadow duration-500 focus:outline-none focus:shadow-2xl" />
                    <span @click="getModels()" 
                        class="cursor-pointer transition-all duration-500 p-2 bg-blue-700 hover:bg-blue-600 hover:shadow-2xl rounded-r shadow-md shadow-blue-300">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </span>
                </div>

                <div class="relative inline-block text-gray-500 w-36">
                    <select v-model="filtreTags" @change="getModels()"
                        class="w-full h-10 pl-3 pr-6 text-base border-gray-300 placeholder-gray-500 border rounded-md appearance-none focus:border-indigo-600 focus:outline-none"
                            aria-label="Select tags">
                            <option selected>All</option>
                            <option v-for="tag in tags"
                                :value="tag.id">{{ tag.name }}</option>
                    </select>
                    <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                        <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
                            <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path>
                        </svg>
                    </div>
                </div>
            </div>
            <div>
                <Dropdown
                        width="w-48 sm:right-0"
                        position="origin-top-left"
                        :closeModal="closeDropdown">
                        <div class="flex justify-center items-center p-2 cursor-pointer transition-all duration-500 bg-blue-600 hover:bg-blue-400 text-white rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                            </svg>
                        </div>
                        <template #content>
                            <div class="bg-white p-6 flex flex-col space-y-3">

                                <div>
                                    <span @click="modalCreateProduct = true"
                                        class="text-gray-500 transition hover:text-blue-700 cursor-pointer">
                                        {{t('message.modelization.createproduct')}}
                                    </span>
                                </div>

                                <div>
                                    <span @click="modalCreateTags = true"
                                        class="text-gray-500 transition hover:text-blue-700 cursor-pointer">
                                        {{t('message.modelization.tags')}}
                                    </span>
                                </div>
                            </div>
                        </template>
                    </Dropdown>
            </div>
        </div>
        <DataTable
            :headers="headers"
            :data="dataModel.results"
            :is_action="true"
            :slotHeaders="true">
            
            <template v-slot:header>
                <th class="hidden sm:table-cell p-5 text-gray-500 font-medium"></th>
                <th class="table-cell p-5 text-gray-500 font-medium">{{t('message.modelization.name')}}</th>
                <th class="hidden sm:table-cell p-5 text-gray-500 font-medium">{{t('message.modelization.tags')}}</th>
                <th class="hidden sm:table-cell p-5 text-gray-500 font-medium">{{t('message.modelization.generate')}}</th>
                <th class="table-cell p-5 text-gray-500 font-medium">{{t('message.modelization.actions')}}</th>
                <th class="table-cell p-5 text-gray-500 font-medium">{{t('message.modelization.plus')}}</th>
                <th class="table-cell p-5 text-gray-500 font-medium">{{t('message.modelization.info')}}</th>
            </template>

            <template v-slot:row="{row, index}">
                <td class="hidden sm:table-cell p-3 font-thin text-sm">
                    <span v-if="row.is_public" class="bg-indigo-100 px-3 py-1 text-xs text-indigo-600 font-semibold rounded-2xl select-none">
                        {{t('message.modelization.public')}}
                    </span>
                    <span v-else class="bg-gray-100 px-3 py-1 text-xs text-gray-600 font-semibold rounded-2xl select-none">
                        {{t('message.modelization.private')}}
                    </span>
                </td>
                <td class="p-3 font-thin text-sm select-none">
                    {{ truncate(row.name, 10, "...") }}
                </td>
                <td class="hidden sm:table-cell p-3 font-thin text-sm select-none">
                    <div class="flex flex-row gap-2 w-full items-center justify-start">
                        <span v-for="id in row.tags" class="bg-neutral-100 px-3 py-1 text-xs text-neutral-600 font-semibold rounded-2xl select-none">
                            {{ truncate(getNameTags(id), 3, "...") }}
                        </span>
                    </div>
                </td>
                <td class="hidden sm:table-cell p-3 font-thin text-sm">
                    <span v-if="row.is_generate" class="bg-green-100 px-3 py-1 text-xs text-green-600 font-semibold rounded-2xl select-none">
                        {{t('message.modelization.done')}}
                    </span>
                    <span v-else class="bg-blue-100 px-3 py-1 text-xs text-blue-600 font-semibold rounded-2xl select-none">
                        {{t('message.modelization.ndone')}}
                    </span>
                </td>
                <td class="p-3 font-thin text-sm">
                    <div class="flex flex-row gap-2 items-center justify-center">

                        <a v-if="row.is_generate"
                            @click="preview(row.id)" class="cursor-pointer">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600 transition-colors duration-500 hover:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                            </svg>
                        </a>

                        <a @click="update(row.id)" class="cursor-pointer">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600 transition-colors duration-500 hover:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                            </svg>
                        </a>

                        <a v-if="row.is_generate"
                            @click="download(row.id_model)" class="cursor-pointer">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600 transition-colors duration-500 hover:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        </a>

                    </div>
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

                                <div v-if="row.images.length > 0">
                                    <span @click="openGenerateObject(row.id)"
                                        class="text-gray-500 transition hover:text-blue-700 cursor-pointer">
                                        {{t('message.modelization.genrateobj')}}
                                    </span>
                                </div>

                                <div v-if="row.images.length > 0">
                                    <span @click="openImage(row.images)"
                                        class="text-gray-500 transition hover:text-blue-700 cursor-pointer">
                                        {{t('message.modelization.getimg')}}
                                    </span>
                                </div>

                                <div>
                                    <div @click="deleteModel(row.id)"
                                        class="grid grid-cols-2 text-gray-500 justify-center items-center  transition hover:text-red-700 cursor-pointer">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                                        </svg>
                                        <span class="-ml-10">
                                            {{t('message.modelization.del')}}
                                        </span>
                                    </div>
                                </div>

                            </div>
                        </template>
                    </Dropdown>
                </td>
                <td>
                    <Dropdown
                        width="w-60 right-0"
                        :closeModal="closeDropdown">
                        <div class="flex justify-center items-center ml-4 p-2 cursor-pointer transition-all duration-500 hover:bg-gray-100 hover:text-gray-400 rounded">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
                            </svg>
                        </div>
                        <template #content>
                            <div class="bg-white p-6 flex flex-col space-y-3">
                                <span class="font-semibold italic text-lg">{{t('message.modelization.information')}}</span>
                                <div key="step-1" class="flex flex-row space-x-2">
                                    <svg width="20" height="20" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <circle cx="14" cy="14" r="14" fill="#1D4ED8"/>
                                        <path d="M15.2528 8.36364V20H13.4915V10.125H13.4233L10.6392 11.9432V10.2614L13.5426 8.36364H15.2528Z" fill="#FFFCFC"/>
                                    </svg> 
                                    <span class="w-auto">{{t('message.modelization.explain1')}}</span>
                                </div>
                                <div key="step-2" class="flex flex-row space-x-2">
                                    <svg width="20" height="20" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <circle cx="14" cy="14" r="14" fill="#1D4ED8"/>
                                        <path d="M10.7131 20V18.7273L14.6506 14.6477C15.071 14.2045 15.4176 13.8163 15.6903 13.483C15.9669 13.1458 16.1733 12.8258 16.3097 12.5227C16.446 12.2197 16.5142 11.8977 16.5142 11.5568C16.5142 11.1705 16.4233 10.8371 16.2415 10.5568C16.0597 10.2727 15.8116 10.0549 15.4972 9.90341C15.1828 9.74811 14.8286 9.67045 14.4347 9.67045C14.018 9.67045 13.6544 9.75568 13.3438 9.92614C13.0331 10.0966 12.7945 10.3371 12.6278 10.6477C12.4612 10.9583 12.3778 11.322 12.3778 11.7386H10.7017C10.7017 11.0303 10.8646 10.411 11.1903 9.88068C11.5161 9.35038 11.9631 8.93939 12.5312 8.64773C13.0994 8.35227 13.7453 8.20455 14.4688 8.20455C15.1998 8.20455 15.8438 8.35038 16.4006 8.64205C16.9612 8.92992 17.3987 9.32386 17.7131 9.82386C18.0275 10.3201 18.1847 10.8807 18.1847 11.5057C18.1847 11.9375 18.1032 12.3598 17.9403 12.7727C17.7813 13.1856 17.5028 13.6458 17.1051 14.1534C16.7074 14.6572 16.1544 15.2689 15.446 15.9886L13.1335 18.4091V18.4943H18.3722V20H10.7131Z" fill="#FFFCFC"/>
                                    </svg>
                                    <span class="w-auto">{{t('message.modelization.explain2')}}</span>
                                </div>
                                <div key="step-3" class="flex flex-row space-x-2">
                                    <svg width="20" height="20" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <circle cx="14" cy="14" r="14" fill="#1D4ED8"/>
                                        <path d="M14.5142 20.1591C13.7339 20.1591 13.0369 20.0246 12.4233 19.7557C11.8134 19.4867 11.3305 19.1136 10.9744 18.6364C10.6222 18.1553 10.4328 17.5985 10.4062 16.9659H12.1903C12.2131 17.3106 12.3286 17.6098 12.5369 17.8636C12.7491 18.1136 13.0256 18.3068 13.3665 18.4432C13.7074 18.5795 14.0862 18.6477 14.5028 18.6477C14.9612 18.6477 15.3665 18.5682 15.7188 18.4091C16.0748 18.25 16.3532 18.0284 16.554 17.7443C16.7547 17.4564 16.8551 17.125 16.8551 16.75C16.8551 16.3598 16.7547 16.017 16.554 15.7216C16.357 15.4223 16.0672 15.1875 15.6847 15.017C15.3059 14.8466 14.8475 14.7614 14.3097 14.7614H13.3267V13.3295H14.3097C14.7415 13.3295 15.1203 13.2519 15.446 13.0966C15.7756 12.9413 16.0331 12.7254 16.2188 12.4489C16.4044 12.1686 16.4972 11.8409 16.4972 11.4659C16.4972 11.1061 16.4157 10.7936 16.2528 10.5284C16.0938 10.2595 15.8665 10.0492 15.571 9.89773C15.2794 9.74621 14.9347 9.67045 14.5369 9.67045C14.1581 9.67045 13.804 9.74053 13.4744 9.88068C13.1487 10.017 12.8835 10.214 12.679 10.4716C12.4744 10.7254 12.3646 11.0303 12.3494 11.3864H10.6506C10.6695 10.7576 10.8551 10.2045 11.2074 9.72727C11.5634 9.25 12.0331 8.87689 12.6165 8.60795C13.1998 8.33901 13.8475 8.20455 14.5597 8.20455C15.3059 8.20455 15.9498 8.35038 16.4915 8.64205C17.0369 8.92992 17.4574 9.31439 17.7528 9.79545C18.0521 10.2765 18.1998 10.803 18.196 11.375C18.1998 12.0265 18.018 12.5795 17.6506 13.0341C17.2869 13.4886 16.8021 13.7936 16.196 13.9489V14.0398C16.9688 14.1572 17.5672 14.464 17.9915 14.9602C18.4195 15.4564 18.6316 16.072 18.6278 16.8068C18.6316 17.447 18.4536 18.0208 18.0938 18.5284C17.7377 19.036 17.2509 19.4356 16.6335 19.7273C16.0161 20.0152 15.3097 20.1591 14.5142 20.1591Z" fill="#FFFCFC"/>
                                    </svg>
                                    <span class="w-auto">{{t('message.modelization.explain3')}}</span>
                                </div>
                            </div>
                        </template>
                    </Dropdown>
                </td>
            </template>
        </DataTable>
        <div v-if="dataModel.count == 0"
            class="w-full flex items-center justify-center pt-2">
            <h1 class="text-gray-500 text-sm">{{t('message.modelization.nopdrt')}}</h1>
        </div>
    </div>

    <Modal :show="modalCreateProduct"
        :title="modalCreateProduct_title"
        width="80"
        :customFooter="true"
        @close="closeCreateModal()">

        <template #content class="h-96 bg-red-200">
            <div class="p-5">
                <div class="mx-4 p-4">
                    <div class="flex items-center">
                        <div class="flex items-center relative">
                            <div class="rounded-full transition duration-500 ease-in-out h-8 w-8 items-center justify-center ml-4">
                                <svg class="w-full h-full" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="10" cy="10" r="10" fill="#3b82f6"/>
                                    <path d="M11.5337 4.81818V15H9.99254V6.35938H9.93288L7.4968 7.95028V6.47869L10.0373 4.81818H11.5337Z" fill="#FFFCFC"/>
                                </svg>
                            </div>
                            <div class="absolute top-0 -ml-8 text-center mt-12 w-32 text-xs font-medium uppercase text-blue-500">{{t('message.modelization.givename')}}</div>
                        </div>
                        <div v-if="page >= 1" class="flex-auto border-t-2 transition duration-500 ease-in-out border-blue-500"></div>
                        <div v-else-if="page < 1" class="flex-auto border-t-2 transition duration-500 ease-in-out border-gray-300"></div>
                        <div v-if="page >= 1" class="flex items-center text-white relative">
                            <div class="rounded-full transition duration-500 ease-in-out h-8 w-8 items-center justify-center bg-blue-500">
                                <svg class="w-full h-full" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="10" cy="10" r="10"/>
                                    <path d="M6.68643 15V13.8864L10.1317 10.3168C10.4996 9.92898 10.8029 9.58925 11.0415 9.29759C11.2835 9.0026 11.4641 8.72254 11.5835 8.45739C11.7028 8.19223 11.7624 7.91051 11.7624 7.61222C11.7624 7.27415 11.6829 6.98248 11.5238 6.73722C11.3647 6.48864 11.1476 6.29806 10.8725 6.16548C10.5974 6.02959 10.2875 5.96165 9.94283 5.96165C9.57824 5.96165 9.26006 6.03622 8.98828 6.18537C8.7165 6.33452 8.50769 6.54498 8.36186 6.81676C8.21603 7.08854 8.14311 7.40672 8.14311 7.77131H6.67649C6.67649 7.15151 6.81901 6.60961 7.10405 6.1456C7.38909 5.68158 7.78018 5.32197 8.27734 5.06676C8.7745 4.80824 9.33961 4.67898 9.97266 4.67898C10.6123 4.67898 11.1758 4.80658 11.663 5.06179C12.1535 5.31368 12.5363 5.65838 12.8114 6.09588C13.0865 6.53007 13.2241 7.0206 13.2241 7.56747C13.2241 7.94531 13.1528 8.31487 13.0103 8.67614C12.8711 9.0374 12.6275 9.4401 12.2795 9.88423C11.9315 10.325 11.4476 10.8603 10.8278 11.4901L8.80433 13.608V13.6825H13.3881V15H6.68643Z" fill="#FFFCFC"/>
                                </svg>
                            </div>
                            <div class="absolute top-0 -ml-12 text-center mt-12 w-32 text-xs font-medium uppercase text-blue-500">{{t('message.modelization.linkstate')}}</div>
                        </div>
                        <div v-else-if="page < 1" class="flex items-center text-white relative">
                            <div class="rounded-full transition duration-500 ease-in-out h-8 w-8 items-center justify-center bg-gray-400">
                                <svg class="w-full h-full" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="10" cy="10" r="10"/>
                                    <path d="M6.68643 15V13.8864L10.1317 10.3168C10.4996 9.92898 10.8029 9.58925 11.0415 9.29759C11.2835 9.0026 11.4641 8.72254 11.5835 8.45739C11.7028 8.19223 11.7624 7.91051 11.7624 7.61222C11.7624 7.27415 11.6829 6.98248 11.5238 6.73722C11.3647 6.48864 11.1476 6.29806 10.8725 6.16548C10.5974 6.02959 10.2875 5.96165 9.94283 5.96165C9.57824 5.96165 9.26006 6.03622 8.98828 6.18537C8.7165 6.33452 8.50769 6.54498 8.36186 6.81676C8.21603 7.08854 8.14311 7.40672 8.14311 7.77131H6.67649C6.67649 7.15151 6.81901 6.60961 7.10405 6.1456C7.38909 5.68158 7.78018 5.32197 8.27734 5.06676C8.7745 4.80824 9.33961 4.67898 9.97266 4.67898C10.6123 4.67898 11.1758 4.80658 11.663 5.06179C12.1535 5.31368 12.5363 5.65838 12.8114 6.09588C13.0865 6.53007 13.2241 7.0206 13.2241 7.56747C13.2241 7.94531 13.1528 8.31487 13.0103 8.67614C12.8711 9.0374 12.6275 9.4401 12.2795 9.88423C11.9315 10.325 11.4476 10.8603 10.8278 11.4901L8.80433 13.608V13.6825H13.3881V15H6.68643Z" fill="#FFFCFC"/>
                                </svg>
                            </div>
                            <div class="absolute top-0 -ml-12 text-center mt-12 w-32 text-xs font-medium uppercase text-gray-500">{{t('message.modelization.linkstate')}}</div>
                        </div>
                        <div v-if="page >= 2" class="flex-auto border-t-2 transition duration-500 ease-in-out border-blue-500"></div>
                        <div v-else-if="page < 2" class="flex-auto border-t-2 transition duration-500 ease-in-out border-gray-300"></div>                        
                        <div v-if="page >= 2" class="flex items-center text-white relative">
                            <div class="rounded-full transition duration-500 ease-in-out h-8 w-8 items-center justify-center bg-blue-500">
                                <svg class="w-full h-full" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="10" cy="10" r="10"/>
                                    <path d="M10.0124 15.1392C9.32966 15.1392 8.71982 15.0215 8.18288 14.7862C7.64927 14.5509 7.22668 14.2244 6.91513 13.8068C6.60689 13.3859 6.44117 12.8987 6.41797 12.3452H7.97905C7.99893 12.6468 8.10002 12.9086 8.28232 13.1307C8.46792 13.3494 8.70987 13.5185 9.00817 13.6378C9.30646 13.7571 9.6379 13.8168 10.0025 13.8168C10.4035 13.8168 10.7582 13.7472 11.0664 13.608C11.378 13.4687 11.6216 13.2749 11.7972 13.0263C11.9729 12.7744 12.0607 12.4844 12.0607 12.1562C12.0607 11.8149 11.9729 11.5149 11.7972 11.2564C11.6249 10.9946 11.3713 10.7891 11.0366 10.6399C10.7051 10.4908 10.3041 10.4162 9.83345 10.4162H8.97337V9.16335H9.83345C10.2113 9.16335 10.5427 9.09541 10.8278 8.95952C11.1161 8.82363 11.3415 8.63471 11.5039 8.39276C11.6663 8.14749 11.7475 7.8608 11.7475 7.53267C11.7475 7.2178 11.6763 6.94437 11.5337 6.71236C11.3945 6.47704 11.1957 6.29309 10.9371 6.16051C10.6819 6.02794 10.3803 5.96165 10.0323 5.96165C9.70088 5.96165 9.39098 6.02296 9.10263 6.1456C8.81759 6.26491 8.58558 6.43726 8.40661 6.66264C8.22763 6.88471 8.13151 7.15151 8.11825 7.46307H6.63175C6.64832 6.91288 6.81072 6.42898 7.11896 6.01136C7.43052 5.59375 7.8415 5.26728 8.35192 5.03196C8.86233 4.79664 9.4291 4.67898 10.0522 4.67898C10.7051 4.67898 11.2686 4.80658 11.7425 5.06179C12.2198 5.31368 12.5877 5.65009 12.8462 6.07102C13.1081 6.49195 13.2373 6.95265 13.234 7.45312C13.2373 8.0232 13.0782 8.5071 12.7567 8.90483C12.4386 9.30256 12.0143 9.56937 11.484 9.70526V9.7848C12.1602 9.88755 12.6838 10.156 13.055 10.5902C13.4296 11.0244 13.6152 11.563 13.6119 12.206C13.6152 12.7661 13.4594 13.2682 13.1445 13.7124C12.833 14.1565 12.4071 14.5062 11.8668 14.7614C11.3266 15.0133 10.7085 15.1392 10.0124 15.1392Z" fill="#FFFCFC"/>
                                </svg>
                            </div>
                            <div class="absolute top-0 -ml-12 text-center mt-12 w-32 text-xs font-medium uppercase text-blue-500">{{t('message.modelization.uploadimg')}}</div>
                        </div>
                        <div v-else-if="page < 2" class="flex items-center text-white relative">
                            <div class="rounded-full transition duration-500 ease-in-out h-8 w-8 items-center justify-center bg-gray-400">
                                <svg class="w-full h-full" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="10" cy="10" r="10"/>
                                    <path d="M10.0124 15.1392C9.32966 15.1392 8.71982 15.0215 8.18288 14.7862C7.64927 14.5509 7.22668 14.2244 6.91513 13.8068C6.60689 13.3859 6.44117 12.8987 6.41797 12.3452H7.97905C7.99893 12.6468 8.10002 12.9086 8.28232 13.1307C8.46792 13.3494 8.70987 13.5185 9.00817 13.6378C9.30646 13.7571 9.6379 13.8168 10.0025 13.8168C10.4035 13.8168 10.7582 13.7472 11.0664 13.608C11.378 13.4687 11.6216 13.2749 11.7972 13.0263C11.9729 12.7744 12.0607 12.4844 12.0607 12.1562C12.0607 11.8149 11.9729 11.5149 11.7972 11.2564C11.6249 10.9946 11.3713 10.7891 11.0366 10.6399C10.7051 10.4908 10.3041 10.4162 9.83345 10.4162H8.97337V9.16335H9.83345C10.2113 9.16335 10.5427 9.09541 10.8278 8.95952C11.1161 8.82363 11.3415 8.63471 11.5039 8.39276C11.6663 8.14749 11.7475 7.8608 11.7475 7.53267C11.7475 7.2178 11.6763 6.94437 11.5337 6.71236C11.3945 6.47704 11.1957 6.29309 10.9371 6.16051C10.6819 6.02794 10.3803 5.96165 10.0323 5.96165C9.70088 5.96165 9.39098 6.02296 9.10263 6.1456C8.81759 6.26491 8.58558 6.43726 8.40661 6.66264C8.22763 6.88471 8.13151 7.15151 8.11825 7.46307H6.63175C6.64832 6.91288 6.81072 6.42898 7.11896 6.01136C7.43052 5.59375 7.8415 5.26728 8.35192 5.03196C8.86233 4.79664 9.4291 4.67898 10.0522 4.67898C10.7051 4.67898 11.2686 4.80658 11.7425 5.06179C12.2198 5.31368 12.5877 5.65009 12.8462 6.07102C13.1081 6.49195 13.2373 6.95265 13.234 7.45312C13.2373 8.0232 13.0782 8.5071 12.7567 8.90483C12.4386 9.30256 12.0143 9.56937 11.484 9.70526V9.7848C12.1602 9.88755 12.6838 10.156 13.055 10.5902C13.4296 11.0244 13.6152 11.563 13.6119 12.206C13.6152 12.7661 13.4594 13.2682 13.1445 13.7124C12.833 14.1565 12.4071 14.5062 11.8668 14.7614C11.3266 15.0133 10.7085 15.1392 10.0124 15.1392Z" fill="#FFFCFC"/>
                                </svg>
                            </div>
                            <div class="absolute top-0 -ml-12 text-center mt-12 w-32 text-xs font-medium uppercase text-gray-500">{{t('message.modelization.uploadimg')}}</div>
                        </div>
                        <div v-if="page >= 3" class="flex-auto border-t-2 transition duration-500 ease-in-out border-blue-500"></div>
                        <div v-else-if="page < 3" class="flex-auto border-t-2 transition duration-500 ease-in-out border-gray-300"></div>
                        <div v-if="page >= 3" class="flex items-center text-white relative">
                            <div class="rounded-full transition duration-500 ease-in-out h-8 w-8 items-center justify-center bg-blue-500">
                                <svg class="w-full h-full" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="10" cy="10" r="10"/>
                                    <path d="M6.18555 13.0114V11.7685L10.5854 4.81818H11.5648V6.64773H10.9434L7.79634 11.6293V11.7088H13.8269V13.0114H6.18555ZM11.013 15V12.6335L11.0229 12.0668V4.81818H12.4796V15H11.013Z" fill="#FFFCFC"/>
                                </svg>
                            </div>
                            <div class="absolute top-0 -ml-12 text-center mt-12 w-32 text-xs font-medium uppercase text-blue-500">{{t('message.modelization.addtag')}}</div>
                        </div>
                        <div v-else-if="page < 3" class="flex items-center text-white relative">
                            <div class="rounded-full transition duration-500 ease-in-out h-8 w-8 items-center justify-center bg-gray-400">
                                <svg class="w-full h-full" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="10" cy="10" r="10"/>
                                    <path d="M6.18555 13.0114V11.7685L10.5854 4.81818H11.5648V6.64773H10.9434L7.79634 11.6293V11.7088H13.8269V13.0114H6.18555ZM11.013 15V12.6335L11.0229 12.0668V4.81818H12.4796V15H11.013Z" fill="#FFFCFC"/>
                                </svg>
                            </div>
                            <div class="absolute top-0 -ml-12 text-center mt-12 w-32 text-xs font-medium uppercase text-gray-500">{{t('message.modelization.addtag')}}</div>
                        </div>
                        <div v-if="page >= 4" class="flex-auto border-t-2 transition duration-500 ease-in-out border-blue-500"></div>
                        <div v-else-if="page < 4" class="flex-auto border-t-2 transition duration-500 ease-in-out border-gray-300"></div>                        
                        <div v-if="page >= 4" class="flex items-center text-white relative">
                            <div class="rounded-full transition duration-500 ease-in-out h-8 w-8 items-center justify-center bg-blue-500">
                                <svg class="w-full h-full" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="10" cy="10" r="10"/>
                                    <path d="M9.99938 15.1392C9.37627 15.1392 8.81614 15.0199 8.31898 14.7812C7.82514 14.5393 7.43072 14.2079 7.13574 13.7869C6.84076 13.366 6.68333 12.8854 6.66344 12.3452H8.15492C8.19138 12.7827 8.38527 13.1423 8.73659 13.424C9.08792 13.7057 9.50885 13.8466 9.99938 13.8466C10.3905 13.8466 10.7368 13.7571 11.0384 13.5781C11.3434 13.3958 11.582 13.1456 11.7544 12.8274C11.93 12.5092 12.0178 12.1463 12.0178 11.7386C12.0178 11.3243 11.9284 10.9548 11.7494 10.63C11.5704 10.3052 11.3235 10.05 11.0086 9.86435C10.6971 9.67874 10.3391 9.58428 9.93475 9.58097C9.62651 9.58097 9.31661 9.634 9.00506 9.74006C8.69351 9.84612 8.44161 9.98532 8.24938 10.1577L6.84242 9.94886L7.41415 4.81818H13.0122V6.13565H8.69185L8.3687 8.98438H8.42836C8.62722 8.79214 8.89071 8.63139 9.21884 8.50213C9.55028 8.37287 9.90492 8.30824 10.2828 8.30824C10.9026 8.30824 11.4544 8.45573 11.9383 8.75071C12.4255 9.04569 12.8083 9.44839 13.0867 9.95881C13.3685 10.4659 13.5077 11.0492 13.5044 11.7088C13.5077 12.3684 13.3585 12.9567 13.0569 13.4737C12.7586 13.9908 12.3443 14.3984 11.814 14.6967C11.287 14.9917 10.6821 15.1392 9.99938 15.1392Z" fill="#FFFCFC"/>
                                </svg>
                            </div>
                            <div class="absolute top-0 -ml-12 text-center mt-12 w-32 text-xs font-medium uppercase text-blue-500">{{t('message.modelization.review')}}</div>
                        </div>
                        <div v-else-if="page < 4" class="flex items-center text-white relative">
                            <div class="rounded-full transition duration-500 ease-in-out h-8 w-8 items-center justify-center bg-gray-400">
                                <svg class="w-full h-full" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="10" cy="10" r="10"/>
                                    <path d="M9.99938 15.1392C9.37627 15.1392 8.81614 15.0199 8.31898 14.7812C7.82514 14.5393 7.43072 14.2079 7.13574 13.7869C6.84076 13.366 6.68333 12.8854 6.66344 12.3452H8.15492C8.19138 12.7827 8.38527 13.1423 8.73659 13.424C9.08792 13.7057 9.50885 13.8466 9.99938 13.8466C10.3905 13.8466 10.7368 13.7571 11.0384 13.5781C11.3434 13.3958 11.582 13.1456 11.7544 12.8274C11.93 12.5092 12.0178 12.1463 12.0178 11.7386C12.0178 11.3243 11.9284 10.9548 11.7494 10.63C11.5704 10.3052 11.3235 10.05 11.0086 9.86435C10.6971 9.67874 10.3391 9.58428 9.93475 9.58097C9.62651 9.58097 9.31661 9.634 9.00506 9.74006C8.69351 9.84612 8.44161 9.98532 8.24938 10.1577L6.84242 9.94886L7.41415 4.81818H13.0122V6.13565H8.69185L8.3687 8.98438H8.42836C8.62722 8.79214 8.89071 8.63139 9.21884 8.50213C9.55028 8.37287 9.90492 8.30824 10.2828 8.30824C10.9026 8.30824 11.4544 8.45573 11.9383 8.75071C12.4255 9.04569 12.8083 9.44839 13.0867 9.95881C13.3685 10.4659 13.5077 11.0492 13.5044 11.7088C13.5077 12.3684 13.3585 12.9567 13.0569 13.4737C12.7586 13.9908 12.3443 14.3984 11.814 14.6967C11.287 14.9917 10.6821 15.1392 9.99938 15.1392Z" fill="#FFFCFC"/>
                                </svg>
                            </div>
                            <div class="absolute top-0 -ml-12 text-center mt-12 w-32 text-xs font-medium uppercase text-gray-500">{{t('message.modelization.review')}}</div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="page == 0" class="w-full h-auto px-3 py-8">
                <div class="mt-4 ml-10">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                        {{t('message.modelization.enternamepdt')}}
                    </label>
                    <input v-model="inputCreate.name" type="text" :placeholder="t('message.modelization.entername')"
                        class="appearance-none block w-11/12 bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                </div>
                
            </div>
            <div v-if="page == 1" class="w-full h-auto px-3 py-8">
                <div>
                    <label class="block ml-10 uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                        {{t('message.modelization.enterlinkpdt')}}
                    </label>
                    <input v-model="inputCreate.redirect_link" type="text" :placeholder="t('message.modelization.linkpro')"
                        class="appearance-none block ml-10 w-11/12 bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                </div>
                <div class="w-11/12 px-3 ml-7">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                        {{t('message.modelization.choose')}}
                    </label>
                </div>
                <div class="relative inline-block text-gray-500 w-11/12 ml-10 mb-2">
                    <select v-model="inputCreate.is_public"
                        class="w-full h-10 pl-3 pr-6 text-base border-gray-300 placeholder-gray-500 border rounded-md appearance-none focus:border-indigo-600 focus:outline-none"
                            aria-label="Select private or public">
                            <option value="1">{{t('message.modelization.public')}}</option>
                            <option value="0">{{t('message.modelization.private')}}</option>
                    </select>
                    <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                        <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
                            <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path>
                        </svg>
                    </div>
                </div>
            </div>
            <div v-if="page == 2" class="w-full h-auto px-3 py-8">
                <div class="w-full px-3">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2 ml-10" for="grid-first-name">
                        {{t('message.modelization.chooseimg')}}
                    </label>
                    <div class="max-w-md mx-auto rounded-lg overflow-hidden md:max-w-xl">
                        <div class="md:flex">
                            <div class="w-full p-3">
                                <div class="relative h-36 rounded-lg border-dashed border-2 border-blue-700 bg-gray-100 flex justify-center items-center">
                                    <div class="absolute">
                                        <div v-if="fileName == ''" class="flex flex-col items-center"> 
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-20 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                            </svg>
                                            <span class="block text-gray-400 font-normal">
                                                {{t('message.modelization.choosefile')}}(.jpg, .png)
                                            </span>
                                        </div>
                                        <div v-else class="flex flex-col items-center"> 
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-20 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                            </svg>
                                            <span class="block text-gray-400 font-normal">
                                                {{ fileName }}
                                            </span>
                                        </div>
                                    </div> <input id="fileInput" type="file" class="h-full w-full opacity-0 cursor-pointer" @change="changeUploadFile()" name="">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="page == 3" class="w-full h-auto px-3 py-8">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mt-4 ml-10 px-3 mb-2" for="grid-first-name">
                        {{t('message.modelization.entertags')}}
                </label>
                <div class="mt-4 ml-10 px-3 w-36">
                    <select
                        class="w-full h-10 pl-3 pr-6 text-base border-gray-300 placeholder-gray-500 border rounded-md appearance-none focus:border-indigo-600 focus:outline-none"
                            aria-label="Select tags">
                            <option selected>All</option>
                            <option v-for="tag in tags" v-bind:value="tag.id">{{ tag.name }}</option>
                    </select>
                    <span class="absolute -ml-5 mt-3 items-center pointer-events-none">
                        <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
                            <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path>
                        </svg>
                    </span>
                </div>
                <div class="w-11/12 mt-4 ml-10 px-3">
                    <input v-model="inputCreateTags" type="text" :placeholder="t('message.modelization.tagname')"
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
                </div>
                <span class="text-red-500 px-3 text-xs italic">{{ errorTags }}</span>
            </div>
            <div v-if="page == 4" class="w-full h-auto px-3 py-8">
                <div class="w-11/12 h-40 mt-4 ml-10 pl-10 border border-gray-400 grid-cols-2 grid gap-2">
                    <div class="mt-5">
                        <span class="block text-black font-normal">
                            {{t('message.modelization.namepdt')}} {{inputCreate.name}}
                        </span>
                    </div>
                    <div class="mt-5">
                        <span class="block text-black font-normal">
                            {{t('message.modelization.state')}} <span v-if="inputCreate.is_public == 0"> {{t('message.modelization.private')}}</span><span v-else>{{t('message.modelization.public')}}</span>
                        </span>
                    </div>
                    <div class="">
                        <span class="block text-black font-normal">
                            {{t('message.modelization.linkadd')}} {{inputCreate.redirect_link}}
                        </span>
                    </div>
                    <div class="">
                        <span class="block text-black font-normal">
                            {{t('message.modelization.tag')}} {{inputCreateTags}}
                        </span>
                    </div>
                    <div class="">
                        <span class="block text-black font-normal">
                            {{t('message.modelization.img')}} {{inputUpdate.file[0].name}}
                        </span>
                    </div>
                </div>
            </div>
            <span class="text-red-500 px-3 text-xs italic">{{ errorCreate }}</span>
        </template>

        <template #footer>
            <div class="flex-auto flex flex-row-reverse">
                <button v-if="page < 4" class="text-base text-white ml-2 
                        hover:scale-110 focus:outline-none flex justify-center px-4 py-2 rounded font-bold cursor-pointer 
                        hover:bg-blue-600  
                        bg-blue-600
                        border duration-200 ease-in-out 
                        border-blue-600 transition"
                        @click="up()"
                    >
                    {{t('message.modelization.ttlbtnnext')}}
                </button>
                <button v-else-if="page == 4" class="text-base text-white ml-2 
                        hover:scale-110 focus:outline-none flex justify-center px-4 py-2 rounded font-bold cursor-pointer 
                        hover:bg-blue-600  
                        bg-blue-600
                        border duration-200 ease-in-out 
                        border-blue-600 transition"
                        @click="create()"
                    >
                    {{t('message.modelization.ttlbuttoncreate')}}
                </button>
                <button v-if="page > 0" class="text-base text-white ml-2 
                        hover:scale-110 focus:outline-none flex justify-center px-4 py-2 rounded font-bold cursor-pointer 
                        hover:bg-gray-400  
                        bg-gray-400
                        border duration-200 ease-in-out 
                        border-gray-400 transition"
                        @click="down()"
                    >
                    {{t('message.modelization.ttlbtnprevious')}}
                </button>
        </div>
        </template>

    </Modal>

    <Modal :show="modalPreview"
        :title="modalPreview_title"
        :nameValidButton="modalPreview_btn"
        width="40"
        :closeOnClick="true"
        @validate="downloadQrcode()"
        @close="closeCreateModal()">

        <template #content>
            <div class="flex justify-center items-center">
                <img :src="genQrCode(previewId)" alt="QRCode" />
            </div>
        </template>

    </Modal>

    <Modal :show="modalViewImg"
        :title="modalViewImg_title"
        width="40"
        :closeOnClick="true"
        :has-footer="false"
        @close="closeCreateModal()">

        <template #content>
            <div class="flex justify-center items-center" style="height:40vh;">
                <img :src="imageUrl" alt="img preview" />
            </div>
        </template>

    </Modal>


    <Modal :show="modalCreateTags"
        :title="modalCreateTags_title"
        :nameValidButton="modalCreateTags_btn"
        width="60"
        :closeOnClick="true"
        @validate="createTags()"
        @close="closeCreateModal()">

        <template #content>
            <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                    {{t('message.modelization.entertags')}}
                </label>
                <input v-model="inputCreateTags" type="text" :placeholder="t('message.modelization.tagname')"
                    class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight transition-colors duration-500 focus:outline-none focus:bg-white">
            </div>
            <span class="text-red-500 px-3 text-xs italic">{{ errorTags }}</span>

        </template>

    </Modal>

    <Modal :show="generateModal"
        :title="modalGenerateModal_title"
        :nameValidButton="modalGenerateModal_btn"
        width="40"
        :closeOnClick="true"
        @validate="generateObject()"
        @close="closeCreateModal()">
    
        <template #content>
                <div class="relative inline-block text-gray-500 w-full mb-2">
                    <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                        <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
                            <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path>
                        </svg>
                    </div>
                </div>
        </template>

    </Modal>

    <Modal :show="modalUpdateProduct"
        :title="modalUpdateProduct_title"
        :nameValidButton="modalUpdateProduct_btn"
        width="40"
        :closeOnClick="true"
        @validate="updateProduct()"
        @close="closeCreateModal()">

        <template #content>
            <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                    {{t('message.modelization.choosetags')}}
                </label>
                <div class="relative inline-block text-gray-500 w-full mb-2">
                    <select v-model="inputUpdate.tag"
                        class="w-full h-10 pl-3 pr-6 text-base border-gray-300 placeholder-gray-500 border rounded-md appearance-none focus:border-indigo-600 focus:outline-none"
                            aria-label="Select tag">
                            <option v-for="tag in tags" :value="tag.name">{{ tag.name }}</option>
                    </select>
                    <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                        <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
                            <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path>
                        </svg>
                    </div>
                </div>
            </div>

            <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                    {{t('message.modelization.chooseimg')}}
                </label>
                <div class="max-w-md mx-auto rounded-lg overflow-hidden md:max-w-xl">
                    <div class="md:flex">
                        <div class="w-full p-3">
                            <div class="relative h-36 rounded-lg border-dashed border-2 border-blue-700 bg-gray-100 flex justify-center items-center">
                                <div class="absolute">
                                    <div v-if="fileName == ''" class="flex flex-col items-center"> 
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                        <span class="block text-gray-400 font-normal">
                                            {{t('message.modelization.choosefile')}}(.jpg, .png)
                                        </span>
                                    </div>
                                    <div v-else class="flex flex-col items-center"> 
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                        <span class="block text-gray-400 font-normal">
                                            {{ fileName }}
                                        </span>
                                    </div>
                                </div> <input id="fileInput" type="file" class="h-full w-full opacity-0 cursor-pointer" @change="changeUploadFile()" name="">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <span class="text-red-500 px-3 text-xs italic">{{ errorUpdate }}</span>

        </template>

    </Modal>
</template>