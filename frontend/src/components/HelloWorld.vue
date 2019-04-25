<template>
  <div class="hello">
      <div>{{serverdata}}</div>
  </div>
</template>

<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator';
import axios from 'axios';
const URL = "https://test-cors.org";

@Component
export default class HelloWorld extends Vue {
  @Prop() private msg!: string;
  public serverdata: string = "";

  created() {
      this.getData().then((result) => this.serverdata = result);

  }

  public async getData() {
      let res = await axios({
          baseURL: URL,
          url: "/",
          method: "get",


          headers: {
              "Access-Control-Allow-Origin": "*"
          }
      });
      return res.data;
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
