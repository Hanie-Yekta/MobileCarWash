<template>
    <div class="container">
        <div class="auth-container">
            <div class="auth-container__form">
                <router-view/>
            </div>
            <img class="auth-container__image" src="@/assets/images/authentication.png">
        </div>
    </div>
</template>
<style scoped lang="scss">

.container{
height: 100vh;
max-width:100vw;
background-color: rgb(246, 248, 249);
display: flex;
align-items: center;

}
.auth-container{
    background-color: rgb(255, 255, 255);
    border-radius:50px;
    width:65%;
    height: 95%;
    margin: auto;
    display: flex;
    flex-direction:row;

    &__form{
        width:55%;
    }


    &__image{
        border-radius:50px;
        width:45%;
    }
}

</style>