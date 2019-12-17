<template>
    <div id="app">
        <Header></Header>
        <br>
        <br>
        <br>
        <router-view></router-view>
    </div>
</template>

<script>

    import Header from "@/components/Header";

    export default {
        name: 'app',
        components: {
            Header,
        },
        watch: {
            '$route': {
                handler: (to) => {
                    document.title = to.meta.title || 'SNACK'
                }
            },
            immediate: true
        }
    }
</script>

<style>
    #app, body {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin: 0;
        left: 0;
        top: 0;
        background-color: black;
        /*margin-top: 60px;*/
    }

</style>
