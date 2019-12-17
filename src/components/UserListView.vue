<template>
    <div class="userlistview_outer">
        <hooper :itemsToShow="7" :centerMode="true" :initialSlide="3">
            <!--            <div v-if="hasResult"></div>-->
            <slide v-for="(movie, index) in userMovieLists" :key="movie.id" aria-hidden="true" :index="index" style="width:14.286%">
                <div class="user-list-img">
                    <img :src="'http://13.125.139.101/static/media/'+movie.id+'.jpg'" @error="replaceByDefault"/>
                </div>
                <div class="user-list-p">
                 <p>{{movie.title}}</p>
                </div>
            </slide>
            <hooper-navigation slot="hooper-addons"></hooper-navigation>
            <!--            </div>-->
        </hooper>
    </div>
</template>

<script>
    import img from '@/assets/imgerror.png'
    import 'hooper/dist/hooper.css';
    import axios from "axios";
    // import modal from 'vue-js-modal'
    import {
        Hooper,
        Slide,
        Navigation as HooperNavigation
    } from 'hooper';

    export default {
        name: "Main",
        components: {
            Hooper,
            Slide,
            HooperNavigation,
            // modal
        },
        props: ['listTitle'],
        data: () => ({
            userMovieLists: [ ],
        }),
        created() {
            this.userMovieList();
        },
        computed(){
        },
        methods: {

            replaceByDefault(e) {
                e.target.src= img
            },
            // MyPage 띄우면 바로 이 메소드 실행되어서 사용자의 영화 리스트에 사용자가 추가한 영화 띄워지도록
            userMovieList: function () {
                axios.get('/users/mymovies',).then(res => {
                    // eslint-disable-next-line no-console
                    console.log(res.data)
                    const movies = res.data.split("}")
                    for(var i =0; i<movies.length; i++){
                        movies[i] = movies[i]+"}";
                        movies[i] = JSON.parse(movies[i].replace(/'/g,'"'));
                        this.userMovieLists.push(movies[i]);
                    }
                }).catch((Error) => {
                    // eslint-disable-next-line no-console
                    console.log(Error)
                })
            },
        }
    }

</script>

<style scoped>
    .hooper-slide {
        width: 740px;
        padding: 1.054%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        color: white;
        align-items: center;
        /*font-size: 50px;*/
        border-radius: 10px;
        flex-shrink: 0;
        height: 100%;
        margin: .5em;
        list-style: none;
        background-color: rgb(48, 48, 48);
    }

    .hooper, .hooper * {
        box-sizing: border-box;
    }

    li {
        display: list-item;
        text-align: -webkit-match-parent;
        width:268.65px;
        height:381.5px;
    }

    ul {
        list-style-type: disc;
        transform: translate(0px, 0px);
        line-height: 1.7;
    }

    .is-active {
        background-color: rgb(48, 48, 48);
    }

    .hooper-list {
        overflow: hidden;
        width: 100%;
        height: 100%;
    }

    .hooper {
        position: relative;
        top: 50px;
        height: 400px;
        /*width: 100%;*/

    }

    div {
        display: block;
    }

    .hooper-track {
        display: flex;
        box-sizing: border-box;
        width: 100%;
        height: 100%;
        padding: 0;
        margin: 0;
    }

    ul {
        list-style-type: disc;
        margin-block-start: 1em;
        margin-block-end: 1em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        padding-inline-start: 40px;
    }

    p {
        text-align: center;
        padding: 20px;
        font-size: 40px;
    }

    .hooper-next.is-disabled, .hooper-prev.is-disabled {
        opacity: .3;
        cursor: not-allowed;
    }

    .hooper-prev {
        left: 0;
    }

    .hooper-next, .hooper-prev {
        background-color: transparent;
        border: none;
        padding: 1em;
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        cursor: pointer;
    }

    button {
        -webkit-appearance: button;
        -webkit-writing-mode: horizontal-tb !important;
        text-rendering: auto;
        color: buttontext;
        letter-spacing: normal;
        word-spacing: normal;
        text-transform: none;
        text-indent: 0px;
        text-shadow: none;
        display: inline-block;
        text-align: center;
        align-items: flex-start;
        cursor: default;
        background-color: buttonface;
        box-sizing: border-box;
        margin: 0em;
        font: 400 13.3333px Arial;
        padding: 1px 6px;
        border-width: 2px;
        border-style: outset;
        border-color: buttonface;
        border-image: initial;
    }

    svg {
        width: 24px;
        height: 24px;
    }

    svg:not(:root) {
        overflow: hidden;
    }

    .hooper-next.is-disabled, .hooper-prev.is-disabled {
        cursor: not-allowed;
    }

    body {
        /*font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;*/
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        font-size: 16px;
        color: #2c3e50;
    }

    .user-list-p p{
        font-size: 10px;
        color: white;
        width: 100%;
        padding: 0px;
        font-size: 15px;
	margin: 10px 0px;

    }
    .user-list-p{
        font-weight: 700;
        width: 100%;
    }
    img{
	width: 94.645%;
	height: 99.69%;
	padding-top:4.33%;
	padding-bottom:0;
    } 
    .user-list-img{
	height: 340px;
    }
    .userlistview_outer{
        height: 450px;
    }

</style>
