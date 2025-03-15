<!-- MarkdownRenderer.vue -->
<template>
  <div v-html="renderedMarkdown"></div>
</template>

<script>
import { computed } from 'vue';
import MarkdownIt from 'markdown-it';
import axios from "axios";
export default {
  props: {
    content: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const renderedMarkdown = computed(() => {
      const md = new MarkdownIt();
      return md.render(props.content);
    });

    return {
      renderedMarkdown,
    };
  },
};
</script>