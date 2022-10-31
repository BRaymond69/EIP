<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps({
    headers: Array,
    data: Array,
    is_action: Boolean,
    slotHeaders: {type: Boolean, default: false}
})

</script>

<template>
        <table class="relative w-full table-auto">

            <thead class="bg-gray-100 text-left select-none">
                <tr v-if="slotHeaders">
                    <slot name="header"></slot>
                </tr>

                <tr v-else>
                    <th v-for="header in headers" class="p-5 text-gray-500 font-medium">{{ header }}</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="(row, index) in data" :key="index" class="cursor-default border-t-2 border-b-2 border-gray-100 hover:text-blue-500">
                    <slot name="row" :index="index" :row="row"></slot>
                </tr>

            </tbody>
        </table>
</template>

<style scoped>
    table {
        border-radius: 0.25rem;
        box-shadow: 0 0 0 1px #f2f4f6;
    }
    table th:first-child {
      border-top-left-radius: 0.25rem;
    }
    table th:last-child {
        border-top-right-radius: 0.25rem;
    }
    table tr:last-child td:first-child {
        border-bottom-left-radius: 0.25rem;
    }
    table tr:last-child td:last-child {
        border-bottom-right-radius: 0.25rem;
    }
    table tr:last-child {
        border-bottom: 0px !important;
    }
</style>