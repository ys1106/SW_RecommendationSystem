<template>
    <div>
        <div class="main_header">
            <div class="main_header_progress">
                <p class="main_header_progressCount">{{count}}</p>
                <p class="main_header_progressMessage">많은 영화를 평가할수록 취향에 맞는 영화가 추천됩니다.</p>
            </div>
            <v-btn class="completeButton" @click="sendPreference(), doLoading()">추가 완료! 추천 받기</v-btn>
            <loading :active.sync="isLoading"
                     :can-cancel="false"
                     :is-full-page="fullPage"
                     :loader="bars"></loading>
        </div>

        <div v-infinite-scroll="loadMore"
             infinite-scroll-disabled="bottom"
             infinite-scroll-distance="10" class="scroll-div">
            <section class="movieSection">
                <div v-for="movie in movies" :key=movie.id class="movie_div">
                    <img :src="'/static/media/'+movie.id+'.jpg'" @error="replaceByDefault"/>
                    <p>{{movie.title}}</p>
                    <input type="range" class="scores_range" name="scores" score="0" min="0" max="10"
                           step="1" v-model="movie.score" @change="counting">
                    <span v-text="movie.score"></span>
                </div>
            </section>
        </div>
    </div>
</template>

<script>
    import Loading from 'vue-loading-overlay'
    import 'vue-loading-overlay/dist/vue-loading.css';
    import img from '@/assets/imgerror.png'
    import infiniteScroll from 'vue-infinite-scroll'
    import axios from "axios";


    export default {
        name: "Preference",
        components: {
            Loading
        },
        data: () => ({
            movies: [],
            loading: true,
            bottom: false,
            limit: 20,
            count: 0,
            isLoading: false,
            fullPage: true,
            ratedMovies: [],

            // 다음 영화 목록 가져오기 위해 next 오브젝트 사용
            next: {
                exist: true,
                id: null,
                title: null
            }
        }),
        computed: { // 페이지 뜨자마자 가장 먼저 실행되어야 할 것...
        },
        directives: {
            infiniteScroll
        },
        methods: {
            // loading 표시 뜨도록 하는 함수
            doLoading() {
                this.isLoading = true;
                // setTimeout(() => {
                //     this.isLoading = false
                // },3000)
            },
            // Img 없는 경우 이 img로 대체하기 위한 이벤트 함수
            replaceByDefault(e) {
                e.target.src = img
            },
            counting: function () {
                for (let movie of this.movies) {
                    if (movie.score > 0 && !this.ratedMovies.includes(movie.id)) {
                        this.ratedMovies.push(movie.id);
                        this.count++;
                    } else if (this.ratedMovies.includes(movie.id) && movie.score == 0) {
                        let num = this.ratedMovies.indexOf(movie.id);
                        this.ratedMovies.splice(num, 1);
                        this.count--;
                    }
                }
            },
            // bottom 활성화시키고 movie들 가져오기
            loadMore: function () {
                if (!this.bottom) {
                    this.bottom = true
                    this.getMovies()
                }
            },
            // 새로운 영화리스트들 추가해주기 위한 함수
            getMovies: function () {
                axios.get('/users/randommovies',).then(res => {
                    // eslint-disable-next-line no-console
                    console.log(res.data)
                    const rndmovie = res.data.split("}")
                    // eslint-disable-next-line no-console
                    console.log(res.data)
                    for (var i = 0; i < rndmovie.length; i++) {
                        rndmovie[i] = rndmovie[i] + "}";
                        // eslint-disable-next-line no-console
                        console.log(typeof rndmovie[i]);
                        rndmovie[i] = JSON.parse(rndmovie[i].replace(/'/g, '"'));
                        // eslint-disable-next-line no-console
                        console.log(rndmovie[i]);
                        rndmovie[i]['score'] = 0;
                        this.movies.push(rndmovie[i]);
                    }
                    this.next.exist = (rndmovie.length > 10)
                    if (this.next.exist) {
                        this.bottom = false;
                    }
                }).catch((Error) => {
                    // eslint-disable-next-line no-console
                    console.log(Error)
                    this.bottom = false;
                })
            },
            // 서버에 user가 평점 매긴 영화와 평점 보내주기 위한 함수
            sendPreference: function () {
                let objs = []
                for (let movie of this.movies) {
                    // eslint-disable-next-line no-console
                    console.log(movie)
                    // eslint-disable-next-line no-console
                    console.log(movie.score)

                    if (movie.score > 0) {
                        objs.push({
                            id: movie.id,
                            score: movie.score
                        });
                    }
                }
                if(objs.length == 0){
                    // eslint-disable-next-line no-console
                    // JSON.stringify(objs)
                    // eslint-disable-next-line no-console
                    axios.get('/users/recommend_movies',)
                    // eslint-disable-next-line no-console
                        .then(response => {
                            // eslint-disable-next-line no-console
                            console.log(response.data + 'success')
                            this.isLoading = false
                            this.$router.push({name: 'mypage'})
                        }).catch(error => {
                        // eslint-disable-next-line no-console
                        console.log(error)
                    })
                }
                else {
                    // eslint-disable-next-line no-console
                    console.log(objs)
                    objs = {addmovies: objs}
                    // JSON.stringify(objs)
                    // eslint-disable-next-line no-console
                    console.log(objs)
                    axios.post('/users/addmymovies', objs)
                    // eslint-disable-next-line no-console
                        .then(response => {
                            // eslint-disable-next-line no-console
                            console.log(response.data + 'success')
                            this.isLoading = false
                            this.$router.push({name: 'mypage'})
                        }).catch(error => {
                        // eslint-disable-next-line no-console
                        console.log(error)
                    })
                }

            },
        },

        created() {
            //this.loadMore();
            // eslint-disable-next-line no-console
            console.log('Preference.vue created => type:', this.type)
        },
        deactivated() {
            this.bottom = true
        },
        activated() {
            this.bottom = false
        }
    }
</script>

<style scoped>
    .movie_div > p {
        font-weight: 700;
        font-size: 17px;
    }

    .movieSection {
        display: flex;
        flex-wrap: wrap;
        margin: 0px -1.5%;
        overflow: hidden;
    }

    .movie_div {
        position: relative;
        width: 17%;
        margin: 1.5%;
        height: 460px;
    }

    .movie_poster {
        display: block;
        width: 100%;
    }

    img {
        border-style: none;
    }

    .movie_div > img {
        width: 247px;
        height: 358.8px;
    }

    input[type=range] {
        height: 34px;
        -webkit-appearance: none;
        margin: 10px 0;
        width: 100%;
        background-color: #F1E1CA;
    }

    input[type=range]:focus {
        outline: none;
    }

    input[type=range]::-webkit-slider-runnable-track {
        width: 100%;
        height: 18px;
        cursor: pointer;
        animate: 0.2s;
        box-shadow: 0px 0px 1px #FCC16D;
        background: #FCC16D;
        border-radius: 14px;
        border: 0px solid #000000;
    }

    input[type=range]::-webkit-slider-thumb {
        box-shadow: 0px 0px 3px #6E6E6E;
        border: 3px solid #FFFFFF;
        height: 25px;
        width: 48px;
        border-radius: 16px;
        background: #FCA119;
        cursor: pointer;
        -webkit-appearance: none;
        margin-top: -5px;
    }

    input[type=range]:focus::-webkit-slider-runnable-track {
        background: #FCC16D;
    }

    input[type=range]::-moz-range-track {
        width: 100%;
        height: 18px;
        cursor: pointer;
        animate: 0.2s;
        box-shadow: 0px 0px 1px #FCC16D;
        background: #FCC16D;
        border-radius: 14px;
        border: 0px solid #000000;
    }

    input[type=range]::-moz-range-thumb {
        box-shadow: 0px 0px 3px #6E6E6E;
        border: 3px solid #FFFFFF;
        height: 25px;
        width: 48px;
        border-radius: 16px;
        background: #FCA119;
        cursor: pointer;
    }

    input[type=range]::-ms-track {
        width: 100%;
        height: 18px;
        cursor: pointer;
        animate: 0.2s;
        background: transparent;
        border-color: transparent;
        color: transparent;
    }

    input[type=range]::-ms-fill-lower {
        background: #FCC16D;
        border: 0px solid #000000;
        border-radius: 28px;
        box-shadow: 0px 0px 1px #FCC16D;
    }

    input[type=range]::-ms-fill-upper {
        background: #FCC16D;
        border: 0px solid #000000;
        border-radius: 28px;
        box-shadow: 0px 0px 1px #FCC16D;
    }

    input[type=range]::-ms-thumb {
        margin-top: 1px;
        box-shadow: 0px 0px 3px #6E6E6E;
        border: 3px solid #FFFFFF;
        height: 25px;
        width: 48px;
        border-radius: 16px;
        background: #FCA119;
        cursor: pointer;
    }

    input[type=range]:focus::-ms-fill-lower {
        background: #FCC16D;
    }

    input[type=range]:focus::-ms-fill-upper {
        background: #FCC16D;
    }

    .scroll-div {
        /*position: fixed;*/
        margin-top: 192px;
        right: 0px;
        left: 0px;
        background-color: #F1E1CA;
    }

    .main_header {
        position: fixed;
        top: 56px;
        right: 0px;
        left: 0px;
        z-index: 400;
        text-align: center;
        width: 100%;
        height: 192px;
        background: linear-gradient(180deg, white 70%, #F1E1CA);
    }

    .main_header_progress {
        text-align: center;
        width: 40.2%;
        max-width: 580px;
        margin: 89px auto 0px;
    }

    .main_header_progressCount {
        font-family: Roboto;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 1px;
        color: black;
    }

    .main_header_progressMessage {
        color: black;
        /* rgba(255, 255, 255, 0.7); */
        font-size: 14px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 1px;
    }

    /*.progressBar_div {*/
    /*    display: flex;*/
    /*    -webkit-box-pack: start;*/
    /*    justify-content: flex-start;*/
    /*    background-color: transparent;*/
    /*    width: 100%;*/
    /*    height: 8px;*/
    /*    margin-top: 11px;*/
    /*    border-width: 1px;*/
    /*    border-style: solid;*/
    /*    border-color: #fcc16d;*/
    /*    border-image: initial;*/
    /*    border-radius: 40px;*/
    /*}*/

    /*.progresssBar {*/
    /*    height: 100%;*/
    /*    background-color: #fcc16d;*/
    /*    transition: width 0.5s linear 0s;*/
    /*}*/

    .completeButton {
        display: inline-block;
        font-size: 13px;
        line-height: 32px;
        height: 32px;
        text-align: center;
        position: absolute;
        top: 106px;
        right: 4%;
        background-color: #fcc16d;
        color: white;
        font-weight: 700;
        letter-spacing: -0.2px;
        cursor: pointer;
        padding: 0px 18px;
        border-radius: 40px;
    }

    body {
        margin: 0px;
    }

    .scores_range {
        width: 300px;
    }

    .movie_div > span {
        font-weight: 700;
    }

    .loading_icon {
        color: rgb(128, 128, 128);
        background-color: white;
    }
</style>
