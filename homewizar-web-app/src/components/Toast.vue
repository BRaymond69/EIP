<script setup lang="ts">
    import { ref, toRefs } from 'vue'

    const emit = defineEmits(['close-toast'])

    const props = defineProps({
        toast: {type: Object, default:{'display': false,'type': 'success', 'text':''}}
    })

    const { toast } = toRefs(props)

    function closeToast() {
        emit('close-toast')
    }

</script>

<template>

    <transition enter-active-class="duration-500 ease-out"
        enter-from-class="transform opacity-0 translate-y-3"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="duration-500 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="transform opacity-0 translate-y-3">
        <div v-if="toast.display" class="fixed bottom-2 right-2 z-50 flex items-center w-full max-w-xs p-4 mb-4 text-gray-500 bg-white rounded shadow dark:text-gray-400" role="alert">
            <div v-if="toast.type == 'success'" class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-500 bg-green-100 rounded">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
            </div>
            <div v-else class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </div>
            <div class="ml-3 text-sm font-normal">{{ toast.text }}</div>
            <button @click="closeToast()" type="button" class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded focus:ring-2 transition-all duration-500 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8" data-dismiss-target="#toast-success" aria-label="Close">
                <span class="sr-only">Close</span>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
            </button>
        </div>
    </transition>

</template>