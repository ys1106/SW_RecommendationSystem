<template>
    <div class="outer">
        <button @click="openInfoModal" class="infoModal"><img src="@/assets/info.png" class="modalImg">
        <span class="infoSpan">Info</span>
        </button>
        <Mymodal @close="closeInfoModal" v-if="infomodal">
            <p class="infoP">이용 방법</p>
            <div><span>페이지를 밑으로 스크롤하여, 당신의 취향인 영화를 추가해보세요.</span></div>
            <template slot="footer">
                <button @click="closeInfoModal" class="closeModalbtn">확인</button>
            </template>
        </Mymodal>
        <a href="/users/logout">
            <img alt="logout logo" src="@/assets/logout.png" class="logout_icon"/>
            <span class="logoutSpan">Logout</span>
        </a>
        <p class="user-list-title">당신이 평가한 영화 리스트</p>
        <UserListView></UserListView>

        <p class="user-list-title">추천받은 영화 리스트</p>
        <RecListView @do-change="getChildMessage"></RecListView>

        <router-link :to="{name: 'preference'}">
            <button class="insert-btn">추가하기</button>
        </router-link>

<!--        페이지 평가 모달-->
        <button @click="openEstModal" class="estModal">페이지 평가</button>
        <EstimationModal @close="closeEstModal" v-if="estmodal">
            <p class="infoP estP">페이지 평가</p>
            <div class="estDiv"><span>더 좋은 추천이 이루어질 수 있도록 페이지가 만족스러운지 평가해주세요.</span></div>
            <RadioToggleButtons
                    :values='values'
                    selectedTextColor='pink'
                    color='black'
                    background-color='white'
                    textColor='black'
                    v-model="value"
                    class="radiotogglebtn"
            />
            <template slot="footer">
                <button @click="doSend" class="closeEstbtn">제출</button>
            </template>
        </EstimationModal>
    </div>
</template>

<script>
    import UserListView from "@/components/UserListView";
    import RecListView from "@/components/RecListView";
    import Mymodal from "@/components/Mymodal";
    import EstimationModal from "@/components/EstimationModal";
    import axios from "axios";
    export default {
        name: "MyPage",
        components: {
            UserListView,
            RecListView,
            Mymodal,
            EstimationModal,
        },
        data: () => ({

            infomodal: false,
            estmodal: false,
            value:'',
            values: [
                { label: '매우 불만', value: '1'},
                { label: '불만', value: '2'},
                { label: '보통', value: '3'},
                { label: '만족', value: '4'},
                { label: '매우 만족', value: '5'},
            ],
            currentValue: '',
        }),
        methods:{

            openInfoModal() {
                this.infomodal = true
            },
            closeInfoModal() {
                this.infomodal = false
            },
            openEstModal() {
                this.estmodal = true
            },
            closeEstModal() {
                this.estmodal = false
            },

            // 페이지 평가한 것 서버로 전송
            doSend: function() {
                // eslint-disable-next-line no-console
                let obj = []
                // eslint-disable-next-line no-console
                console.log(this.values.value)
                obj = {evaluate: this.value}

                // eslint-disable-next-line no-console
                console.log(obj)
                axios.post('/users/evaluatepage', obj)
                // eslint-disable-next-line no-console
                    .then(response => {
                        // eslint-disable-next-line no-console
                        console.log(response.data + 'success')
                        alert('감사합니다!')
                        this.closeEstModal()
                    }).catch(error => {
                    // eslint-disable-next-line no-console
                    console.log(error)
                    alert('감사합니다!')
                    this.closeEstModal()
                })
            },

        }
    }
</script>

<style scoped>
    .user-list-title {
        text-align: left;
        position: relative;
        top: 70px;
        font-size: 25px;
        color: white;
        font-weight: bold;
        margin-left: 1em;
        margin-bottom: 1em;
    }
    .insert-btn, .recommand-btn{
        color: white;
        background-color: #EA5A69;
        border-radius: 10px;
        position: relative;
        top: 80px;
        font-size: 14px;
        font-weight: 600;
        width: 110px;
        height: 40px;
        bottom: 100px;
    }
    .insert-btn{
        margin-right: 60px;
        margin-bottom: 120px;
    }

    .logout_icon {
        display: -webkit-box;
        display: -webkit-flex;
        display: -ms-flexbox;
        display: flex;
        position: relative;
        right: 20px;
        bottom: 10px;
        float: right;
        list-style: none;
    }

    .logout_icon {
        line-height: 72px;
        font-size: 20px;
        height: 40px;
        top: 20px;
    }
    .outer{
        height: 100%;
        top: 40px;
        position: relative;
    }
    .logoutSpan{
        width: 42px;
        height: 20px;
        color: white;
        float: right;
        display: flex;
        position: relative;
        right: 0;
        top: 55px;
        left: 18px;
    }
    .infoSpan{
        width: 55px;
        height: 30px;
        color: white;
        float: right;
        display: flex;
        position: relative;
        right: 0;
        top: 40px;
        left:-33px;
        font-size: 15px;
    }
    .infoModal{
        width: 55px;
        height: 60px;
        float: right;
        display: flex;
        position: relative;
        right: 140px;
        top: 10px;
        cursor: pointer;
        background-color: black;
        border: 0px;
    }
    .modalImg{
        width: 42px;
    }
    .infoP{
        font-size: 22px;
        font-weight: 700;
    }
    .closeModalbtn{
        margin-right: 45%;
        margin-left: 45%;
    }
    .estModal{
        float: right;
        position: absolute;
        bottom: 1%;
        right: 1%;
        background-color: black;
        border:0;
        color:white;
        font-size: 12px;
    }
    .closeEstbtn{
        width: 20%;
        margin-right: 40%;
        margin-left: 40%;
    }
    .radiotogglebtn{
        background-color: white;
        border-color: white;
    }
    .estDiv{
        margin-bottom: 6%;
        padding-top: 9%;
    }
    .estP{
        margin-bottom: 1%;
    }
    RadioToggleButtons > .radio-toggle-button{
        background-color: white;
        border-color: white;
        padding: 3%;
    }
    RadioToggleButtons >.is-selected{
        background-color: white;
        border-color: white;
        padding: 3%;
    }
    .is-hovered{
        background-color: white;
    }
</style>
