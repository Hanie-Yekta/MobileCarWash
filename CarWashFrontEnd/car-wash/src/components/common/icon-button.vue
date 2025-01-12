<template>
  <button
    class="icon-button"
    :class="{
      'icon-button_variant_text': variant === 'text',
      'icon-button_variant_tonal': variant === 'tonal',
    }"
  >
    <slot>
      <base-icon v-if="iconName" :iconName="iconName"  class="icon-button__icon" />
    </slot>
  </button>
</template>

<script setup>
  import BaseIcon from '@/components/common/base-icon.vue';

  defineProps({
    iconName: {
      type: String,
    },
    variant: {
      type: String,
      default: 'text',
    },
  });
</script>

<style scoped lang="scss">
  .icon-button {
    padding: 8px;
    border-radius: 50%;
    line-height: 0;
    transition: background-color 0.25s ease-out;

    &__icon {
      width:20px;
      height: 20px;
    }

    &:disabled {
      opacity: 0.4;
    }

    &_variant_text {
      background-color: rgb(193, 189, 189);
      box-shadow: 0px 0px 30px 0px rgba(24, 24, 24, 0.1);
      &:hover {
        background-color: gray;
      }
    }

    &_variant_tonal {
      background-color: var(--palette-surface-container);

      &:hover {
        background-color: var(--palette-surface-container-high);
      }
    }
  }
</style>
