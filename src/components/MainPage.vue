<template>
    <div class="outline">
        <p> 동영상 자리</p>
        <div class="VideoBg">
            <video autoplay="autoplay" loop="loop" muted="muted" class="popcorn">
                <source src="@/assets/popcorn.mp4" type="video/mp4">
            </video>
            <a href="/users/signup">
                <button class="sign-btn main-btn">회원가입</button>
            </a>
            <a href="/users/login">
                <button class="login-btn main-btn">로그인</button>
            </a>
        </div>
    </div>
</template>

<script>


    export default {
        name: "Popcorn",

    }
</script>

<style scoped>
    .popcorn {
        height: 790px;
        width: 100%;
        position: relative;
        top: 0%;
        visibility: visible;
    }

    .sign-btn {
        left: 37%;
        margin-right: 7%;
    }

    .login-btn {
        right: 37%;
        margin-left: 6%;
    }

    .main-btn {
        color: white;
        background-color: #EA5A69;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        top: 70%;
        position: fixed;
        width: 130px;
        height: 40px;
        border-color: #EA5A69;
    }

    .main-btn {
        margin-right: 60px;
    }
    .outline{
        height: 100%;
    }
    .outline > p {
        color: white;
        height: 40px;
    }
    .VideoBg{
        top:0%;
        position: inherit;
        height: 100%;
    }
</style>