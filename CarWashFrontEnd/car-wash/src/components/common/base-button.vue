<script setup>
import { computed } from "vue";

const props = defineProps({
  variant: {
    type: String,
    default: "confirm",
    validator(value) {
      return ["confirm", "cancel", "link"].includes(value);
    },
  },
  size: {
    type: String,
    default: "medium",
    validator(value) {
      return ["x-large", "large", "medium", "small", "normal"].includes(value);
    },
  },
});

const buttonClasses = computed(() => {
  const classes = { "base-button": true };

  classes[`base-button_variant_${props.variant}`] = true;
  classes[`base-button_size_${props.size}`] = true;

  return classes;
});
</script>

<template>
  <button :class="buttonClasses">
    <slot />
  </button>
</template>

<style scoped lang="scss">
.base-button {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 20px;
  padding: 20px;

  &_size_x-large {
    width: 100%;
    font-size: large;
    font-weight: bold;
    height: 50px;
  }
  &_size_large {
    width: 40%;
    font-size: medium;
    font-weight: normal;
    height: 60px;
  }
  &_size_medium {
    width: 50%;
    font-size: medium;
    font-weight: normal;
    height: 60px;
  }

  &_size_small {
    width: 27%;
    font-size: small;
    font-weight: normal;
    height: 30px;
  }
  &_size_normal {
    font-size: small;
    font-weight: normal;
    height: 45px;
  }

  &_variant_confirm {
    background: #43a2aa;
    color: white;

    &:hover {
      background-color: rgb(35, 160, 154);
    }

    &:disabled {
      opacity: 0.56;
      background-color: rgb(173, 173, 173);
    }
  }

  &_variant_link {
    background: white;
    border: 1px solid #6b96b7;
    padding: 10px;

    &:hover {
      background-color: rgb(242, 243, 249);
    }

    &:disabled {
      opacity: 0.56;
      background-color: rgb(173, 173, 173);
    }
  }

  &_variant_cancel {
    background-color: rgb(255, 98, 98);
    border: 1px solid rgb(255, 98, 98);
    color: white;
    &:hover {
      background-color: red;
      border: 1px solid red;
    }

    &:disabled {
      opacity: 0.56;
      background-color: rgb(173, 173, 173);
    }
  }
}
</style>
