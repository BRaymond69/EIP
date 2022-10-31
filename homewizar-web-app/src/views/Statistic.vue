<script setup lang="ts">
    import { ref } from 'vue'
    import { Chart, registerables, DoughnutController, ArcElement, Tooltip, ChartData, ChartOptions } from 'chart.js';
    import { DoughnutChart, BarChart, PieChart} from 'vue-chart-3';
    import Modal from '../components/Modal.vue'
    import { useI18n } from 'vue3-i18n'
    import axios from '../assets/ts/axios'

    Chart.register(...registerables, DoughnutController, ArcElement, Tooltip);
    
    // import CustomButtonVue from '../components/CustomButtonVue.vue'

    // import { defineComponent } from 'vue';

    const emit = defineEmits(['open-toast'])
    const { t } = useI18n();
    let modal_totalfurniture = ref(false)
    let modal_furnitureprocess = ref(false)
    let modal_typeoffurniture = ref(false)
    let modal_bestseller = ref(false)
    let data_tag = ref()
    let display_total = ref(false)
    let display_typeof = ref(false)
    let no_data = ref(false)
    let month = ref(9)

    const options = ref<ChartOptions<'bar'>>({
        responsive: true,
        plugins: {
            legend: {
                display: false,
            }
        },
    });

    let labels = ref({
        label_totalfurniture: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        label_furnitureprocess: ['Not Modelize', 'IA Progess', '3D Progress', 'Modelize', 'Downloadable Model'],
        label_typeoffurniture: [],
        label_bestseller: []
    })

    let sort_furniture = ref(labels.value.label_typeoffurniture)
    let selected = ref({})
    let furniture_sort = ref({
        chair: false,
        sofa: false,
        bookcase: false,
        cupboard: false,
        fridge: false,
        desk: false,
        table: false,
        })

    let datasets = ref({
        dataset_totalfurniture: ([{
            data: [], 
            backgroundColor: ['#0079AF']
        }]),
        dataset_furnitureprocess: ([{
            data: [30, 40, 60, 70, 5],
            backgroundColor: ['#77CEFF', '#0079AF', '#123E6B', '#97B0C4', '#A5C8ED'],
        }]),
        dataset_typeoffurniture: ([{
            data: [],
            backgroundColor: ['#77CEFF', '#0079AF', '#123E6B', '#97B0C4', '#A5C8ED', "#5794FF", "#1765EE", "#3B62A7"],
        }]),
        dataset_bestseller: ([{
            data: [2, 1, 6, 6, 7, 4, 3],
            backgroundColor: ['#77CEFF', '#0079AF', '#123E6B', '#97B0C4', '#A5C8ED', "#5794FF", "#1765EE", "#3B62A7"],
        }])
    })

    let datasets_totalfurniture = ref({
        labels: labels.value.label_totalfurniture,
        datasets: datasets.value.dataset_totalfurniture
    })
    let datasets_furnitureprocess = ref({
        labels: labels.value.label_furnitureprocess,
        datasets: datasets.value.dataset_furnitureprocess
    })
    let datasets_typeoffurniture = ref({
        labels: labels.value.label_typeoffurniture,
        datasets: datasets.value.dataset_typeoffurniture
    })
    let datasets_bestseller= ref({
        labels: labels.value.label_bestseller,
        datasets: datasets.value.dataset_bestseller
    })

    async function sortData() {
        datasets.value.dataset_typeoffurniture[0].data = []
        datasets_typeoffurniture.value.labels = []
        getStatsTypeof()
        closeModal()
    }

    async function all_Selected() {
        furniture_sort.value.chair = true
        furniture_sort.value.sofa = true
        furniture_sort.value.bookcase = true
        furniture_sort.value.cupboard = true
        furniture_sort.value.fridge = true
        furniture_sort.value.desk = true
        furniture_sort.value.table = true
        selected.value = labels.value.label_typeoffurniture
    }

    interface  ParamsInterface { 
        params: { 
            month?: number, 
            year?: number,
        } 
    }

    function getStatsTypeof() {
        var save_data: any = []
        var list_id: any = []
        var data_res_id: any = []

        let params: ParamsInterface = { params: { month: month.value, year: 2022 } }
        axios.get('/api/stats/', params)
            .then(res => {
                if (params.params.month === month.value) {
                    var data: any[] = []
                    var arr: any[] = res.data
                    for(var item in arr){
                        data.push(arr[item].tag)
                    }
                    data_res_id = removeduplicate(data)
                    Object.keys(data_res_id).forEach(key => {
                        list_id.push(data_res_id[key])
                        for(var y in data_tag.value){
                            if (parseInt(key) === data_tag.value[y].id) {
                                save_data.push(data_tag.value[y].name)
                            }
                        }
                        datasets.value.dataset_typeoffurniture[0].data = list_id
                    });
                    datasets_typeoffurniture.value.labels = save_data
                    display_typeof.value = true
                }
            if (datasets.value.dataset_typeoffurniture[0].data.length === 0 || datasets_typeoffurniture.value.labels.length === 0) {
                no_data.value = true
            }
            
            }).catch( error => {
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Error during tag retrieval.'
                })
            } )
    }

    function getStats() {
        var number_total: any = []
        var save_data: any = []
        var list_id: any = []
        var data_res_id: any = []

        for (var i = 1 ; i <= 12 ; i++) {
            let params: ParamsInterface = { params: { month: i, year: 2022 } }
            axios.get('/api/stats/', params)
                .then(res => {
                    number_total.push(res.data.length)
                    if (number_total.length === 12) {
                        display_total.value = true
                        datasets.value.dataset_totalfurniture[0].data = number_total
                    }
                    if (params.params.month === month.value) {
                        var data: any[] = []
                        var arr: any[] = res.data
                        for(var item in arr){
                            data.push(arr[item].tag)
                        }
                        data_res_id = removeduplicate(data)
                        Object.keys(data_res_id).forEach(key => {
                            list_id.push(data_res_id[key])
                            for(var y in data_tag.value){
                                if (parseInt(key) === data_tag.value[y].id) {
                                    save_data.push(data_tag.value[y].name)
                                }
                            }
                            datasets.value.dataset_typeoffurniture[0].data = list_id
                        });
                        datasets_typeoffurniture.value.labels = save_data
                        display_typeof.value = true
                    }
                }).catch( error => {
                    emit('open-toast', {
                        'type': 'fail',
                        'text': 'Error during tag retrieval.'
                    })
                } )
        }
    }
    async function getTag() {
        return await axios.get('/api/tags/')
            .then(res => {
                data_tag.value = res.data
            }).catch( error => {
                emit('open-toast', {
                    'type': 'fail',
                    'text': 'Error during tag retrieval.'
                })
            } )
    }
    
    function removeduplicate(array: any){
        const counts: any = {};
        for (var i = 0; i < array.length; i++) {
            counts[array[i]] = 1 + (counts[array[i]] || 0);
        };
        return counts;
    }

    function closeModal() {
        modal_totalfurniture.value = false
        modal_furnitureprocess.value = false
        modal_typeoffurniture.value = false
        modal_bestseller.value = false
    }

        /* Mounted */
    async function mount() {
        await getTag()
    }

    mount()
    getStats()
</script>

<template>
    <div class="relative inline-grid grid-cols-2 gap-4 w-full h-1/2  rounded transition-shadow duration-500 border border-gray-100 shadow-md hover:shadow-xl">
        <div class="flex flex-col flex-wrap bg-gray-100 border rounded w-11/12 shadow-md hover:shadow-xl h-80 ml-10">
            <div v-if="display_total === true" class="flex flex-row mt-5 ml-2">
                <label class="flex ml-auto mr-auto uppercase underline tracking-wide text-gray-700 text-s font-bold">
                    {{t('message.statistic.totalfurniture')}}
                </label>
            </div>
            <span v-if="display_total === true">
                <BarChart :height="250" :chartData="datasets_totalfurniture" :options="options"/>
            </span>
            <div v-else class="h-full w-full flex justify-center items-center">
                    <svg aria-hidden="true" class="mr-2 w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                </svg>
                <span class="sr-only">Loading...</span>
            </div>
        </div>
        <div class="flex flex-col flex-wrap bg-gray-100 border rounded w-11/12 shadow-md hover:shadow-xl h-80 ml-4">
            <div class="flex flex-row mt-5">
                <label class="flex ml-auto mr-auto uppercase underline tracking-wide text-gray-700 text-s font-bold">
                    {{t('message.statistic.furnitureprocess')}}
                </label>
                <svg @click="modal_furnitureprocess = true" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2 mr-2 transform hover:rotate-45 hover:scale-150 transition duration-100 ease-in-out bg-slate-300 rounded-full inline-flex" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
                </svg>
            </div>
            <div class="flex mt-6 items-center justify-center">
                <DoughnutChart :height="200" :chartData="datasets_furnitureprocess"/>
            </div>
        </div>
        <div class="flex flex-col flex-wrap bg-gray-100 border rounded w-11/12 shadow-md hover:shadow-xl h-80 ml-10 mb-2">
            <div v-if="display_typeof === true" class="flex flex-row mt-5 ml-2">
                <label class="flex ml-auto mr-auto uppercase underline tracking-wide text-gray-700 text-s font-bold">
                    {{t('message.statistic.typeoffurniture')}}
                </label>
                <svg @click="modal_typeoffurniture = true" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2 mr-2 transform hover:rotate-45 hover:scale-150 transition duration-100 ease-in-out bg-slate-300 rounded-full inline-flex" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
                </svg>
            </div>
            <span v-if="display_typeof === true" >
                <PieChart :height="200" :chartData="datasets_typeoffurniture"/>
            </span>
            <div v-else-if="no_data === true" class="h-full w-full flex justify-center items-center">
                <label class="flex ml-auto mr-auto uppercase underline tracking-wide text-gray-700 text-s font-bold">
                    {{t('message.statistic.typeoffurniture')}}
                </label>
            </div>
            <div v-else class="h-full w-full flex justify-center items-center">
                    <svg aria-hidden="true" class="mr-2 w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                </svg>
                <span class="sr-only">Loading...</span>
            </div>
        </div>
        <div class="flex flex-col flex-wrap bg-gray-100 border rounded w-11/12 shadow-md hover:shadow-xl h-11/12 ml-4 my-5">
            <div class="flex flex-row mt-5">
                <label class="flex ml-auto mr-auto uppercase underline tracking-wide text-gray-700 text-s font-bold">
                    {{t('message.statistic.bestseller')}}
                </label>
                <svg @click="modal_bestseller = true" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2 mr-2 transform hover:rotate-45 hover:scale-150 transition duration-100 ease-in-out bg-slate-300 rounded-full inline-flex" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
                </svg>
            </div>
            <div class="flex mt-5 justify-center">
                <BarChart :height="200" :chartData="datasets_bestseller" :options="options"/>
            </div>
        </div>
    </div>

    <!-- Modal Furniture  -->
    <Modal :show="modal_furnitureprocess"
        title="Modal Furniture Process:"
        nameValidButton="Sort"
        width="60"
        :closeOnClick="true"
        @validate="sortData()"
        @close="closeModal()">

        <template #content>
            <div class="w-full px-3">
                <label class="flex ml-auto mr-auto uppercase underline tracking-wide text-gray-700 text-s font-bold">
                    {{t('message.statistic.furnitureprocess')}}
                </label>
                <select name="Months"
                    class="border-0 cursor-pointer rounded-full drop-shadow-md h-8 w-96 duration-300 m-2">
                    <option value="1">{{t('message.statistic.jan')}}</option>
                    <option value="2">{{t('message.statistic.feb')}}</option>
                    <option value="3">{{t('message.statistic.mar')}}</option>
                    <option value="4">{{t('message.statistic.apr')}}</option>
                    <option value="5">{{t('message.statistic.may')}}</option>
                    <option value="6">{{t('message.statistic.jun')}}</option>
                    <option value="7">{{t('message.statistic.jul')}}</option>
                    <option value="8">{{t('message.statistic.aug')}}</option>
                    <option value="9">{{t('message.statistic.sep')}}</option>
                    <option value="10">{{t('message.statistic.oct')}}</option>
                    <option value="11">{{t('message.statistic.nov')}}</option>
                    <option value="12">{{t('message.statistic.dec')}}</option>
                </select>
                 <select name="Year"
                    class="border-0 cursor-pointer rounded-full drop-shadow-md h-8 w-96 duration-300 m-2">
                    <option value="2020" disabled>2020</option>
                    <option value="2021" disabled>2021</option>
                    <option value="2022" selected>2022</option>
                </select>
            </div>
        </template>
    </Modal>
    <!-- Modal Type of Furniture  -->
    <Modal :show="modal_typeoffurniture"
        :title="t('message.statistic.typeoffurniture')"
        :nameValidButton="t('message.modelization.ttlbtnnext')"
        width="60"
        :closeOnClick="true"
        @validate="sortData()"
        @close="closeModal()">

        <template #content>
            <div class="w-full px-3">
                <label class="flex ml-auto mr-auto uppercase underline tracking-wide text-gray-700 text-s font-bold">
                    {{t('message.statistic.typeoffurniture')}}
                </label>
                <select v-model="month" name="Months"
                    class="border-0 cursor-pointer rounded-lg drop-shadow-lg h-8 w-96 duration-300 m-2">
                    <option value="1">{{t('message.statistic.jan')}}</option>
                    <option value="2">{{t('message.statistic.feb')}}</option>
                    <option value="3">{{t('message.statistic.mar')}}</option>
                    <option value="4">{{t('message.statistic.apr')}}</option>
                    <option value="5">{{t('message.statistic.may')}}</option>
                    <option value="6">{{t('message.statistic.jun')}}</option>
                    <option value="7">{{t('message.statistic.jul')}}</option>
                    <option value="8">{{t('message.statistic.aug')}}</option>
                    <option value="9">{{t('message.statistic.sep')}}</option>
                    <option value="10">{{t('message.statistic.oct')}}</option>
                    <option value="11" selected>{{t('message.statistic.nov')}}</option>
                    <option value="12">{{t('message.statistic.dec')}}</option>
                </select>
                <select name="Year"
                    class="border-0 cursor-pointer rounded-lg drop-shadow-lg h-8 w-96 duration-300 m-2">
                    <option value="2020" class="ml-2" disabled>2020</option>
                    <option value="2021" class="ml-2" disabled>2021</option>
                    <option value="2022" class="ml-2" selected>2022</option>
                </select>
            </div>
        </template>
    </Modal>
    <!-- Modal Best Seller  -->
    <Modal :show="modal_bestseller"
        title="Modal Best Seller:"
        nameValidButton="Sort"
        width="60"
        :closeOnClick="true"
        @validate="sortData()"
        @close="closeModal()">

        <template #content>
            <div class="w-full px-3">
                <label class="flex ml-auto mr-auto uppercase underline tracking-wide text-gray-700 text-s font-bold">
                    {{t('message.statistic.bestseller')}}
                </label>
                <select name="Months"
                    class="border-0 cursor-pointer rounded-full drop-shadow-md h-8 w-96 duration-300 m-2">
                    <option value="January">January</option>
                    <option value="February">February</option>
                    <option value="March">March</option>
                    <option value="April">April</option>
                    <option value="May">May</option>
                    <option value="June">June</option>
                    <option value="July">July</option>
                    <option value="August">August</option>
                    <option value="September">September</option>
                    <option value="October">October</option>
                    <option value="November">November</option>
                    <option value="December">December</option>
                </select>
                <select name="Year"
                    class="border-0 cursor-pointer rounded-full drop-shadow-md h-8 w-96 duration-300 m-2">
                    <option value="2020">2020</option>
                    <option value="2021">2021</option>
                    <option value="2022" selected>2022</option>
                </select>
            </div>
        </template>
    </Modal>
</template>