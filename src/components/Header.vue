<template>
    <div id="test">
        <div class="banner">
            <img alt="film logo" src="@/assets/film.png" style="height: 30px"/>
            <p class="banner_word" style="text-align: left">
                "본인의 취향에 맞는 영화에 평점을 매겨 취향에 맞는 영화를 추천받으세요."
            </p>
        </div>


        <nav class="navigation_bar">
            <div class="homepage-Logo">
                <img alt="Vue logo" src="@/assets/MainLogo.png" style="height: 60px"/>
            </div>
            <ul class="banner_rightNav">
                <li class="banner_rightNav_li">
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
    export default {
        name: "header",
        //
        // data() {
        //     return {
        //         imgUrl: null,
        //     }
        // },
        // methods: {
        //     onLogoImage(e) {
        //         const file = e.target.files[0];
        //         print(e.target.files);
        //         this.imgUrl = ".\src\assets".createObjectURL(file);
        //     }
        // }
    }
</script>

<style scoped>

    a, div, img, ul, span {
        font-size: 100%;
        margin: 0;
        padding: 0;
        border: 0;
        vertical-align: baseline;
        word-break: break-all;
    }

    div {
        display: block;
    }

    div[class^="sect-"] {
        clear: both;
        zoom: 1;
    }

    div[class^="sect-"]:after {
        content: '';
        clear: both;
        display: block;
    }

    .banner_word {
        -webkit-flex: 1;
        -ms-flex: 1;
        flex: 1;
        color: white;
        font-size: 14px;
        font-weight: 700;
        -webkit-letter-spacing: -0.4px;
        -moz-letter-spacing: -0.4px;
        -ms-letter-spacing: -0.4px;
        letter-spacing: -0.4px;
        line-height: 25px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-left: 1em;
    }

    .banner p img {
        display: inline-block;
        vertical-align: top;
        width: 25px;
        height: 25px;
        font-size: 30px;
        margin: 3px 9px 0 0;
        color: white;
    }

    .banner_rightNav {
        display: -webkit-box;
        display: -webkit-flex;
        display: -ms-flexbox;
        display: flex;
        position: relative;
        right: 150px;
        bottom: 10px;
        float: right;
        list-style: none;
    }

    .banner_rightNav_li {
        line-height: 72px;
        font-size: 20px;
    }

    nav {
        display: block;
    }

    .navigation_bar {
        position: fixed;
        top: 56px;
        z-index: 500;
        font-size: 14px;
        -webkit-letter-spacing: -0.4px;
        -moz-letter-spacing: -0.4px;
        -ms-letter-spacing: -0.4px;
        letter-spacing: -0.4px;
        width: 100%;
        height: 72px;
        padding: 0 4%;
        background-color: white;
        /* #030708; */
        /* left: 0px;
          padding-left: 50px; */
    }

    a {
        color: inherit;
        text-decoration: none;
    }

    input, select, img {
        vertical-align: middle;
    }

    ol, ul {
        list-style: none;
    }

    ul {
        display: block;
        list-style-type: disc;
        margin-block-start: 1em;
        margin-block-end: 1em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        padding-inline-start: 40px;
    }

    .banner {
        display: -webkit-box;
        display: -webkit-flex;
        display: -ms-flexbox;
        display: flex;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 500;
        -webkit-align-items: center;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        background: #EA5A69;
        width: 100%;
        height: 56px;
        padding: 0 50px;
    }

    /*#preview {*/
    /*    display: flex;*/
    /*    justify-content: center;*/
    /*    align-items: center;*/
    /*}*/

    #preview img {
        max-width: 100%;
        max-height: 500px;
    }

    .homepage-Logo {
        float: left;
        /* 0 24px no-repeat; */
        background-size: 173px 26px;
        width: 173px;
        /*height: 72px;*/
    }



</style>