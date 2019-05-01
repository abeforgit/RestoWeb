<template>
    <div>
        <li>

        </li>
    </div>
</template>

<script>
    import axios from 'axios';
    const URL = 'https://groep22.webdev.ilabt.imec.be';

    export default {
        name: 'RestoList',
        data() {
            return {
                info: null,
                restos: [
                    
                ]
            }
        },
        mounted() {
            axios
                .get(URL + '/restos')
                .then(response => (this.info = response))
        }
    }
</script>

<style scoped>

</style>