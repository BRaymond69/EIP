<script setup lang="ts">
    import { ref, toRefs, watch } from 'vue'

    let isOpen = ref(false)

    const props = defineProps({
        width: { type: String, default: 'w-56 right-0' },
        position: { type: String, default: 'right-0' },
        closeModal: { type: Boolean, required: false, default: false },
    })
    const { width, position, closeModal } = toRefs(props)

    function closeDropdown() {
        isOpen.value = false
    }

    watch(closeModal, (closeModal, prevCloseModal) => {
        if (closeModal)
            closeDropdown()
    })

</script>

<template>

    <div class="relative inline-block text-left text-gray-800"
        v-click-away="closeDropdown">

        <div @click="isOpen = !isOpen">
            <slot></slot>
        </div>

        <transition enter-active-class="duration-500 ease-out"
            enter-from-class="transform opacity-0 translate-y-3"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="duration-500 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="transform opacity-0 translate-y-3">
            <div v-if="isOpen"
                :class="width"
                class="origin-top-left absolute mt-2 rounded shadow-lg text-sm overflow-hidden border z-20">
                <slot name="content"></slot>
            </div>
        </transition>

    </div>

</template>