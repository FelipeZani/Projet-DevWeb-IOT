<template>
     <div ref = "mapContainer" style="width: 400px; height: 400px;"></div>

</template>
<script setup> 
    import {onMounted,ref} from 'vue'
    import L from 'leaflet'

    const map = ref()
    const mapContainer = ref()
    onMounted(()=>{
        map.value = L.map(mapContainer.value).setView([51.505, -0.09],13);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map.value);
    })
</script>