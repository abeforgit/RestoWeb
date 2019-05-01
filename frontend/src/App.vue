<template>
    <div class="container">
      <div id="app">
        <Navbar></Navbar>
        <router-view/>
      </div>
    </div>
</template>

<style lang="scss">

</style>

<script>
  import Navbar from "./components/Navbar";
  const URL = 'https://groep22.webdev.ilabt.imec.be';

  export default {
    components: {
      Navbar
    }
  }
</script>