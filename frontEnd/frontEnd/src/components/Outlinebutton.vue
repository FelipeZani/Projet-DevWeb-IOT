<template>
    <button class="custom-button mx-1 rounded-1 ">{{title}}</button>
</template>
<script setup>
    const props=defineProps({
        buttonColor:String,
        title:String,
        size:String
    })
    const classDescription = "custom-button mx-1 rounded-1 p-1";

</script>



<style setup>
    .custom-button{
        border-color: v-bind('buttonColor');
        color:v-bind('buttonColor');
        background-color: transparent;
        border-style: outset;
        border: solid 1.5px;
       padding: v-bind('size');
    }
    .custom-button:hover{
        background-color: v-bind('buttonColor');
        border-color: v-bind('buttonColor');
        color: whitesmoke;
        transition: .4s;
    }
</style>