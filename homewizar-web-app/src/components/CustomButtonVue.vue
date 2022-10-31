<script setup lang="ts">
import { ref, toRefs } from 'vue'

const props = defineProps({
    title: { type: String, default: 'Validate' },
    color: { type: String, default: 'bg-blue-600 hover:bg-blue-700' },
    colorText: { type: String, default: 'text-white' },
    loading: { type: Boolean, default: 'false' },
})

const {title, color, loading} = toRefs(props)

const emit = defineEmits(['clickEvent'])

let clickHandler = () => {
    emit('clickEvent')
}

</script>

<template>
        <div @click="(!loading) ? clickHandler() : ''" class="relative" :class="(loading) ? '' : 'cursor-pointer'">
            <span :class="color + ' ' + colorText" class="group relative w-full flex justify-center py-2 px-4 border border-transparent transition-all duration-500 text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <slot name="icon"></slot>
                {{ title }}
            </span>
            <div v-show="loading" class="absolute top-0 flex justify-center items-center w-full h-full bg-white z-50">
                <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-900"></div>
            </div>
        </div>
</template>

<style scoped>
</style>