<script setup>
import {ref} from 'vue';
import BaseIcon from "@/components/common/base-icon.vue";
import { useMediaControls } from '@vueuse/core';
const video = ref()
const showPlay = ref(true);
const showPause = ref(false);
const { playing} = useMediaControls(video)

const showPlayer = ()=>{
  showPause.value = true;
}

const hidePlayer = ()=>{
  showPause.value = false; 
}
</script>

<template>
  <div class="video-container" @mouseover="showPlayer" @mouseleave="hidePlayer">
    <base-icon v-show="!playing" @click="playing=!playing" class="video-container__player" iconName="play"/>
    <base-icon v-show="playing && showPause" @click="playing=!playing"  class="video-container__player" iconName="pause"/>
    <video ref="video" class="video" muted controls poster="../../assets/images/poster-video.png">
      <source src="../../assets/video/quickwash-video.mp4" type="video/mp4" />
    </video>
  </div>
</template>
<style scoped lang="scss">
.video{
    width:700px;
    border-radius: 30px;
}
.video-container{
  position: relative;
  &__player{
    position: absolute;
    top:35%;
    right:44%;
    z-index: 2;
  }
}
</style>