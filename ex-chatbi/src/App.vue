<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
// import ChatInterface from './components/ChatInterface.vue';

// export default {
//   components: {
//     HelloWorld,
//     ChatInterface,
//   },
// };
</script>

<template>
  <!-- <header>

    <div id="app">
      <ChatInterface />
    </div>
  </header> -->

  <RouterView />
</template>

<style scoped>
header {
  /*line-height: 0.5;
  max-height: 100vh;*/ 
  height: 100%;
  width: 100%;
}
.app {
  height: 100%;
  width: 100%;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}


</style>
