<template>
    
    
    <section class=" p-4 container-fluid overlay-div home" style="background-color: #020230;">
        <nav class="navbar navbar-expand-lg position-sticky top-0" style="background-color: transparent;">
            <a class="navbar-brand text-white" href="">Navbar</a>
            
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav"> <!-- standard bootstrap nav bar ref documentation to more info -->
                <ul class="navbar-nav ms-auto " >
                    <li class="nav-item active ">
                        <a class="nav-link text-white" href="#home">Home </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white" href="#products">Products</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white" href="#info">Discover the area</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link disabled text-white" href="#">Disabled</a>
                    </li>
                    <Outlinebutton buttonColor="#2661c2" title="Signup" size="5px 15px"/> <!-- This is a piece of UI which can be reused, ref to its structure to more info-->
                    <Outlinebutton buttonColor="#d87c1f" title="Login" size="5px 20px"/>
                </ul>
            </div>
        
        </nav>
        <div class="row align-items-center my-5 ">
            <div class="col-md-4  align-self-center" >
                <h1 class="display-5 fw-bold text-white">Name of the app</h1>
                <p class="col-md-8 lead text-white"><span>Take full control</span> of your smart <span>home</span> effortlessly, managing everything from <span>lighting to security</span>—all from <span>the palm of your hand.</span></p>
                <button class="btn btn-dark btn-lg">Contact US</button>
               

            </div>
            <img src="./assets/houseImg.webp" class="img-fluid col img-stuff " alt="Smart house with all provided services" style="width: 200px; height:500px;">
        </div>
    </section>
    <section class="products">
        <h1 class="text-center">Choose your plan</h1>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus impedit autem et labore ducimus ipsam sequi inventore a repellat laboriosam quam quis, fugit ex, suscipit sint! Voluptates quo quasi nesciunt!
        Harum quos voluptatem totam inventore assumenda sed ipsam laboriosam, sint tempora saepe repellendus quis magnam eos id nostrum, eligendi quo veniam itaque numquam soluta molestias libero, deserunt cupiditate velit? Hic.
        Reiciendis voluptate quaerat in adipisci temporibus suscipit nulla voluptates iste autem? Nesciunt voluptatem exercitationem quo nihil nobis expedita atque delectus, minus, asperiores, repellat totam quae amet saepe aliquam modi blanditiis.
        Voluptates, explicabo incidunt fugiat quis harum quisquam blanditiis ducimus beatae? Nihil numquam nam quas unde cum eligendi ipsa maxime suscipit qui hic! Quia deserunt neque officia reiciendis nam sapiente delectus!
        Nesciunt deleniti impedit molestiae laboriosam, iste tenetur earum temporibus repellendus commodi, ipsum mollitia reprehenderit. Pariatur reprehenderit praesentium, obcaecati in doloribus sit. Dolorum possimus deserunt deleniti odio illo amet unde ex?
        Voluptas dolore deleniti quaerat consequuntur cupiditate facere. Iusto qui nemo nesciunt facere sint, veniam pariatur quis sequi at aliquam dolores velit? Praesentium exercitationem quae error minima, autem blanditiis ipsum dignissimos?
        Sequi reprehenderit qui nihil. Ducimus fugit veritatis molestias! Explicabo sint eum beatae mollitia dicta sit aliquam quibusdam dolore natus, impedit atque odit inventore rerum molestiae, iure quo quae aliquid doloremque.
        Quasi corrupti minus officia quos deleniti temporibus fugiat error similique voluptatibus provident, porro sequi quidem aliquam hic magnam odio delectus tenetur iste voluptatem pariatur accusantium quas minima beatae? Aspernatur, unde?
        Voluptatem corporis libero magni mollitia minus voluptate, saepe laudantium rerum molestias iusto fugit asperiores sunt inventore corrupti eum, hic accusantium. Assumenda eum magnam nisi odio animi iusto deserunt illo corrupti.
        Vero ipsam aperiam harum eius, maxime repellat quae ducimus architecto laudantium sapiente dolor perferendis a exercitationem ipsa, eaque mollitia, aliquid illum iusto. Odit eum, magni animi omnis ex suscipit aliquam.</p>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus impedit autem et labore ducimus ipsam sequi inventore a repellat laboriosam quam quis, fugit ex, suscipit sint! Voluptates quo quasi nesciunt!
        Harum quos voluptatem totam inventore assumenda sed ipsam laboriosam, sint tempora saepe repellendus quis magnam eos id nostrum, eligendi quo veniam itaque numquam soluta molestias libero, deserunt cupiditate velit? Hic.
        Reiciendis voluptate quaerat in adipisci temporibus suscipit nulla voluptates iste autem? Nesciunt voluptatem exercitationem quo nihil nobis expedita atque delectus, minus, asperiores, repellat totam quae amet saepe aliquam modi blanditiis.
        Voluptates, explicabo incidunt fugiat quis harum quisquam blanditiis ducimus beatae? Nihil numquam nam quas unde cum eligendi ipsa maxime suscipit qui hic! Quia deserunt neque officia reiciendis nam sapiente delectus!
        Nesciunt deleniti impedit molestiae laboriosam, iste tenetur earum temporibus repellendus commodi, ipsum mollitia reprehenderit. Pariatur reprehenderit praesentium, obcaecati in doloribus sit. Dolorum possimus deserunt deleniti odio illo amet unde ex?
        Voluptas dolore deleniti quaerat consequuntur cupiditate facere. Iusto qui nemo nesciunt facere sint, veniam pariatur quis sequi at aliquam dolores velit? Praesentium exercitationem quae error minima, autem blanditiis ipsum dignissimos?
        Sequi reprehenderit qui nihil. Ducimus fugit veritatis molestias! Explicabo sint eum beatae mollitia dicta sit aliquam quibusdam dolore natus, impedit atque odit inventore rerum molestiae, iure quo quae aliquid doloremque.
        Quasi corrupti minus officia quos deleniti temporibus fugiat error similique voluptatibus provident, porro sequi quidem aliquam hic magnam odio delectus tenetur iste voluptatem pariatur accusantium quas minima beatae? Aspernatur, unde?
        Voluptatem corporis libero magni mollitia minus voluptate, saepe laudantium rerum molestias iusto fugit asperiores sunt inventore corrupti eum, hic accusantium. Assumenda eum magnam nisi odio animi iusto deserunt illo corrupti.
        Vero ipsam aperiam harum eius, maxime repellat quae ducimus architecto laudantium sapiente dolor perferendis a exercitationem ipsa, eaque mollitia, aliquid illum iusto. Odit eum, magni animi omnis ex suscipit aliquam.</p>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus impedit autem et labore ducimus ipsam sequi inventore a repellat laboriosam quam quis, fugit ex, suscipit sint! Voluptates quo quasi nesciunt!
        Harum quos voluptatem totam inventore assumenda sed ipsam laboriosam, sint tempora saepe repellendus quis magnam eos id nostrum, eligendi quo veniam itaque numquam soluta molestias libero, deserunt cupiditate velit? Hic.
        Reiciendis voluptate quaerat in adipisci temporibus suscipit nulla voluptates iste autem? Nesciunt voluptatem exercitationem quo nihil nobis expedita atque delectus, minus, asperiores, repellat totam quae amet saepe aliquam modi blanditiis.
        Voluptates, explicabo incidunt fugiat quis harum quisquam blanditiis ducimus beatae? Nihil numquam nam quas unde cum eligendi ipsa maxime suscipit qui hic! Quia deserunt neque officia reiciendis nam sapiente delectus!
        Nesciunt deleniti impedit molestiae laboriosam, iste tenetur earum temporibus repellendus commodi, ipsum mollitia reprehenderit. Pariatur reprehenderit praesentium, obcaecati in doloribus sit. Dolorum possimus deserunt deleniti odio illo amet unde ex?
        Voluptas dolore deleniti quaerat consequuntur cupiditate facere. Iusto qui nemo nesciunt facere sint, veniam pariatur quis sequi at aliquam dolores velit? Praesentium exercitationem quae error minima, autem blanditiis ipsum dignissimos?
        Sequi reprehenderit qui nihil. Ducimus fugit veritatis molestias! Explicabo sint eum beatae mollitia dicta sit aliquam quibusdam dolore natus, impedit atque odit inventore rerum molestiae, iure quo quae aliquid doloremque.
        Quasi corrupti minus officia quos deleniti temporibus fugiat error similique voluptatibus provident, porro sequi quidem aliquam hic magnam odio delectus tenetur iste voluptatem pariatur accusantium quas minima beatae? Aspernatur, unde?
        Voluptatem corporis libero magni mollitia minus voluptate, saepe laudantium rerum molestias iusto fugit asperiores sunt inventore corrupti eum, hic accusantium. Assumenda eum magnam nisi odio animi iusto deserunt illo corrupti.
        Vero ipsam aperiam harum eius, maxime repellat quae ducimus architecto laudantium sapiente dolor perferendis a exercitationem ipsa, eaque mollitia, aliquid illum iusto. Odit eum, magni animi omnis ex suscipit aliquam.</p>
    </section>
    
    <section class="info">
        <h1 class="text-center">Discover the neighborhood</h1>

    
        <div class="row ">
            <div class="col d-flex justify-content-end"><LMap/></div>
            <div class="col">
                <div class="row row-cols-1">
                    <div class="col"><OutlinedIcon color="red" text="Health care" icon="bi bi-bandaid"></OutlinedIcon></div>
                    <div class="col"><OutlinedIcon color="#0092da" text="Transportation" icon="bi bi-bus-front"></OutlinedIcon></div>
                    <div class="col"><OutlinedIcon color="#ac39ac" text="Groceries" icon="bi bi-basket2"></OutlinedIcon></div>
                    <div class="col"><OutlinedIcon color="#c77400" text="Food services" icon="bi bi-cookie"></OutlinedIcon></div>
                </div>

            </div>
                
        </div>

        <div class="d-flex justify-content-center"><p>testing</p></div>
            
            
    </section>


</template>


<script setup> 
    //Components used in the Homepage
    import Outlinebutton from './components/Outlinebutton.vue';
    import LMap from './components/LMap.vue';
    import OutlinedIcon from './components/OutlinedIcon.vue';
</script>

<style>
    .home{
        height: 1000px;
    }
    span{
        color: #d87c1f;
        font-weight: bold;
    }

    .info{
        height: 3000px;
    }

</style>
