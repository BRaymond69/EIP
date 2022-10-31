<script setup lang="ts">
import { list } from 'postcss';
import { ref, onMounted, toRefs } from 'vue'
import { useI18n } from 'vue3-i18n'

const { t } = useI18n();
let checkFirst = ref(false)

const props = defineProps({
    show: Boolean,
    title: String,
    width: {type: String, default: '40'},
    widthUnit: {type: String, default: 'vw'},
    lockScroll: {type: Boolean, default: false},
    closeOnClick: {type: Boolean, default: false},
    showClose: {type: Boolean, default: true},
    customFooter: {type: Boolean, default: false},
    hasFooter: {type: Boolean, default: true},
    nameValidButton: {type: String, default: 'Validate'},
})

const { show, title,
        width, widthUnit,
        lockScroll, closeOnClick,
        showClose, customFooter,
        hasFooter, nameValidButton, } = toRefs(props)

const emit = defineEmits(['validate', 'close'])

let close = () => {
    emit('close')
}

let save = () => {
    emit('validate')
}

let clickHandler = () => {
    if (closeOnClick.value)
        close()
}

</script>

<template>
    <transition
        enter-active-class="transition-all transform duration-500 ease-out"
        leave-active-class="transition-all transform duration-500 ease-in-out"
        enter-class="opacity-0"
        enter-to-class="opacity-100"
        leave-class="opacity-100"
        leave-to-class="opacity-0">
        <div v-if="show" class="fixed z-50 inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
            <transition
                enter-active-class="transition-all transform duration-500 ease-out"
                leave-active-class="transition-all transform duration-500 ease-in-out"
                enter-class="opacity-0 -translate-y-8"
                enter-to-class="opacity-100"
                leave-class="opacity-100"
                leave-to-class="opacity-0 -translate-y-8"
                appear>
                <div class="relative flex flex-col rounded py-6 px-6 bg-white opacity-100 shadow-xl overflow-x-hidden z-40"
                    :style="'max-width:90vw; max-height: 90vh; width:'+ width + widthUnit + ';'"
                    v-click-away="clickHandler">
                    <div class="relative w-full h-16">
                        <div class="absolute top-2 left-2">
                            <span class="text-lg leading-6 font-medium">{{ title }}</span>
                        </div>
                        <span v-if="showClose" @click="close" class="absolute right-0 flex flex-row items-center justify-center h-8 w-8  transition-colors duration-500 rounded hover:bg-red-100 hover:text-red-500 text-gray-400 cursor-pointer">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                            </svg>
                        </span>
                    </div>
                    <div class="w-full overflow-x-hidden"
                        :class="(hasFooter ? 'h-4/5 ' : 'h-full ') + ((lockScroll) ? 'overflow-y-hidden' : 'overflow-y-auto')">
                        <slot name="content"></slot>
                    </div>
                    <div v-if="hasFooter" class="w-full h-auto pt-2">
                        <slot v-if="customFooter" name="footer"></slot>
                        <div v-else class="flex space-x-3 justify-end">
                            <button @click="close" class="px-6 py-2 focus:outline-none rounded border hover:bg-gray-50 bg-white border-gray-300 transition-colors duration-500">{{t('message.home.cancel')}}</button>
                            <button @click="save" class="px-6 py-2 bg-blue-700 border border-blue-700 text-sm rounded text-white focus:outline-none hover:border-blue-600 hover:bg-blue-600 transition-colors duration-500">{{ nameValidButton }}</button>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
    </transition>
</template>