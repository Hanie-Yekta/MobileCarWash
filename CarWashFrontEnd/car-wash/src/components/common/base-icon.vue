<template>
  <component :is="icon" />
</template>

<script setup>
import { defineAsyncComponent, computed } from "vue";

const props = defineProps({
  iconName: {
    type: String,
    required: true,
  },
});

const icon = computed(() => {
  const iconName = props.iconName;
  return defineAsyncComponent({
    loader: async () => {
      let module;
      try {
        module = await import(`../../assets/icons/${iconName}.vue`);
      } catch (error) {
        console.log(error);
      }
      return module;
    },
  });
});
</script>
