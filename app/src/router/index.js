import Vue from 'vue';
import Router from 'vue-router';
import Home from '../components/Home';
import Plots from '../components/Plots';

Vue.use(Router);

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    }, 
    {
        path: '/plots',
        name: 'Plots',
        component: Plots
    }
]

export default new Router({routes});