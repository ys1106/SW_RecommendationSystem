import Vue from 'vue'
import App from './App.vue'
import ProgressBar from 'vue-simple-progress'

import router from './router'
import VModal from 'vue-js-modal'
import VueRadioToggleButtons from "vue-radio-toggle-buttons";

Vue.config.productionTip = false
Vue.use(VModal, {dialog: true})
Vue.use(VueRadioToggleButtons);
Vue.component('modal', {
  template: '#modal-template'
})

new Vue({
  router,
  render: h => h(App),
  ProgressBar,
}).$mount('#app')


// 이거 연습임.(전역 컴포넌트 사용하려면 여기다가 vue.componenet 써줘야 됨.

// var data = { counter: 0}
// Vue.component('simple-counter',{
//   template:`<button v-on:click="counter += 1">{{ counter }} </span>
//  data: function() {
//     return {
//        counter: 0
//      }
//    }
//   `
//
// })


// Vue.component('child', {
//   // props 정의
//   props: ['message'],
//   //데이터와 마찬가지로 prop은 템플릿 내부에서 사용 가능
//   // vm의 this.message로 사용 가능
//   template: '<span>{{message}}</span>'
// })
// 그런 다음 template 내에 위치시키고 싶은 곳에
//<child message="안녕하세요!"></child>