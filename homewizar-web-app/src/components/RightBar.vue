<script setup lang="ts">
import { ref, toRefs } from 'vue'
import { useRouter } from 'vue-router'

let router = useRouter()

const props = defineProps({
    currentPage: String
})

const { currentPage } = toRefs(props)

const emit = defineEmits(['changePage'])

let role = ref(localStorage.getItem('role'))

function changePageAction(tab: string) {
    emit('changePage', tab)
}

function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('company')
    localStorage.removeItem('email')
    localStorage.removeItem('role')
    router.push('/login')
}

</script>

<template>

  <section class="fixed left-0 flex flex-col items-center justify-between pt-8 pb-8 h-screen w-1/12 bg-white z-10">

    <div>
      <img class="h-8 w-9 sm:h-11 sm:w-10" 
        :src="'img/logo_miniature.png'"
        alt="miniature logo" 
      />
    </div>

    <div class="flex flex-col justify-between h-1/4">

        <svg @click="changePageAction('Home')" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-300 transition-all duration-300 hover:text-blue-500 cursor-pointer" :class="(currentPage == 'Home') ? 'text-blue-500' : ''" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
        </svg>

        <svg @click="changePageAction('Modelization')" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-300 transition-all duration-300 hover:text-blue-500 cursor-pointer" :class="(currentPage == 'Modelization') ? 'text-blue-500' : ''" viewBox="0 0 20 20" fill="currentColor">
            <path d="M11 17a1 1 0 001.447.894l4-2A1 1 0 0017 15V9.236a1 1 0 00-1.447-.894l-4 2a1 1 0 00-.553.894V17zM15.211 6.276a1 1 0 000-1.788l-4.764-2.382a1 1 0 00-.894 0L4.789 4.488a1 1 0 000 1.788l4.764 2.382a1 1 0 00.894 0l4.764-2.382zM4.447 8.342A1 1 0 003 9.236V15a1 1 0 00.553.894l4 2A1 1 0 009 17v-5.764a1 1 0 00-.553-.894l-4-2z" />
        </svg>
        

        <svg v-if="role == 'Manager'" @click="changePageAction('Company')" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-300 transition-all duration-300 hover:text-blue-500 cursor-pointer" :class="(currentPage == 'Company') ? 'text-blue-500' : ''" viewBox="0 0 20 20" fill="currentColor">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
        </svg>

        <svg v-if="role == 'Manager'" @click="changePageAction('Statistic')" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-300 transition-all duration-300 hover:text-blue-500 cursor-pointer" :class="(currentPage == 'Statistic') ? 'text-blue-500' : ''" viewBox="0 0 20 20" fill="currentColor">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
        </svg>


    </div>

    <div @click="logout()" class="p-1 sm:p-2 border-2 border-gray-50 rounded-full transition-all duration-300 text-gray-300 hover:text-blue-500 hover:border-blue-100 cursor-pointer">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-8 sm:w-8" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd" />
        </svg>
    </div>
  </section>

</template>
