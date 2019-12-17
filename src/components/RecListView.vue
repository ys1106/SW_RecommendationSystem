<template>
    <div class="reclistview_outer">
        <hooper :itemsToShow="7" :centerMode="true" :initialSlide="3">
            <slide v-for="(movie, index) in recMovieLists" :key="movie.id" style="z-index:2; width:14.286%"
                   aria-hidden="true" :index="index">
                <div class="item-wrapper" @mouseover="movie.upRating=true" @mouseleave="movie.upRating=false">
                    <div class="recRating-div" v-show="movie.upRating">
                        <p class="recRating-p" style="padding:10%">추천된 영화를<br> 평가해주세요.</p>
                        <star-rating :increment="0.5"
                                     :star-size="30"
                                     :max-rating="5"
                                     :padding="8"
                                     v-model="movie.score"
                                     class="starRatingPart"></star-rating>
                        <button class="ratingButton" @click="sendRating()">저장</button>
                    </div>
                    <div class="user-list-img">
                        <img :src="'http://13.125.139.101/static/media/'+movie.id+'.jpg'" @error="replaceByDefault"/>
                    </div>
                    <div class="user-list-p">
                        <p><span class="moviePredictP">{{movie.predict}}</span>{{movie.title}}</p>
                    </div>
                </div>
            </slide>
            <hooper-navigation slot="hooper-addons"></hooper-navigation>
        </hooper>
    </div>
</template>

<script>
    import img from '@/assets/imgerror.png'
    import 'hooper/dist/hooper.css';
    import axios from "axios";
    import StarRating from 'vue-star-rating'

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
            StarRating,

        },
        data: () => ({
            recMovieLists: [],
        }),
        created() {
            this.RecMovieList();
        },
        methods: {
            // img 존재하지 않을 때 대체하기 위한 이벤트 함수
            replaceByDefault(e) {
                e.target.src = img
            },
            // 추천된 영화에 대해 사용자가 평가시 그것을 서버로 전송하는 함수
            sendRating: function() {
                let objs = []
                for (let movie of this.recMovieLists) {
                    if (movie.score > 0) {
                        objs.push({
                            id: movie.id,
                            score: movie.score
                        });
                    }
                }
                // eslint-disable-next-line no-console
                console.log(objs)
                objs = {addmovies: objs}

                // eslint-disable-next-line no-console
                console.log(objs)
                axios.post('/users/sendrating', objs)
                // eslint-disable-next-line no-console
                    .then(response => {
                        // eslint-disable-next-line no-console
                        console.log(response.data + 'success')

                        this.$router.go()
                    }).catch(error => {
                    // eslint-disable-next-line no-console
                    console.log(error)
                })
            },
            //  MyPage 띄울 때 추천리스트 뜨게하기위함
            RecMovieList: function () {
                axios.get('/users/recommovies',).then(res => {
                    // eslint-disable-next-line no-console
                    console.log(res.data)
                    const recMovies = res.data.split("}")
                    // eslint-disable-next-line no-console
                    console.log(recMovies)
                    // recMovies = JSON.parse(recMovies.replace(/'/g,'"'))
                    for (var i = 0; i < recMovies.length; i++) {
                        recMovies[i] = recMovies[i] + "}";
                        // eslint-disable-next-line no-console
                        console.log(JSON.parse(recMovies[i].replace(/'/g, '"')));
                        recMovies[i] = JSON.parse(recMovies[i].replace(/'/g, '"'));
                        recMovies[i]['score'] = 0;
                        recMovies[i]['upRating'] = false;
                        this.recMovieLists.push(recMovies[i])
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
        width: 268.65px;
        height: 381.5px;
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

    .user-list-p p {
        font-size: 10px;
        color: white;
        width: 100%;
        padding: 0px;
        font-size: 15px;
        margin: 10px 0px;

    }

    .user-list-p {
        font-weight: 700;
        width: 100%;
    }

    img {
        width: 94.645%;
        height: 99.69%;
        padding-top: 4.33%;
        padding-bottom: 0;
    }

    .user-list-img {
        height: 340px;
    }

    .recRating-div {
        opacity: 0.6;
        background-color: black;
        position: absolute;
        left: 2%;
        bottom: 10%;
        height: 50%;
        width: 95.5%;
    }

    .item-wrapper {
        position: relative;
        z-index: -1;
    }

    .recRating-p {
        font-weight: 700;
        font-size: 15px;
    }

    .reclistview_outer {
        height: 450px;
    }

    .starRatingPart {
        padding: 0 4% 7% 3%;
    }
    .ratingButton{
        cursor: pointer;
        background-color: black;
        color: white;
    }
    .moviePredictP{
        font-weight: 900;
        font-size: 15px;
        z-index: 2;
        position: relative;
        margin: 0 3% 0 0;
        padding: 0.2% 0.4%;
        left:1%;
        background-color: #EA5A69;
        border-radius: 100px;
        border-color: #EA5A69;
        width: 130%;
    }

</style>
