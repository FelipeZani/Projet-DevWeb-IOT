<template>
  <div>
    <button class="custom-button" :class="{active:isActive}" :onclick="activeButton">
      <i :class="`${icon} row justify-content-center`" id="myOutlinedIcon"></i>
      <p id="outlinedParagraph">{{ text }}</p>
    </button>
  </div>

</template>

<script setup>

  import {ref} from 'vue'

  const props = defineProps({
    color: String,
    text: String,
    icon: String,
  });

  const isActive = ref(false)

  function activeButton(){
    isActive.value = !isActive.value
    console.log(isActive.value)
  }


</script>
  
<style>
   .custom-button{
        border-color: v-bind('color');
        color:v-bind(color);
        background-color: white;
        border-style: outset;
        border: 4px solid v-bind('color');
        border-radius: 20px;
        word-wrap: break-word;
        padding: 10px;
        width: 140px;

    }
    .custom-button.active,
    .custom-button:hover
    {
        background-color: v-bind('color');
        border-color: v-bind('color');
        color: whitesmoke;
        transition: .4s;
    }
    #myOutlinedIcon{
      font-size: 30px;
    }
    #outlinedParagraph{
      font-size: medium;
    }
    
</style>
