import Vue from "vue";
import Vuex from "vuex";

// Modules
import site from './modules/site.store';
import profiles from './modules/profiles.store';
import financial from './modules/financial.store';
import battery from './modules/battery.store';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    site,
    profiles,
    financial,
    battery
  },
  state: {
    uuid: null,
    error: null,
    working: false,
    task_id: null,
    plots: null
  },
  getters: {
    uuid: (state) => state.uuid,
    error: (state) => state.error,
    working: (state) => state.working,
    task_id: (state) => state.task_id,
    plots: (state) => state.plots
  },
  mutations: {
    uuid(state, uuid) {
      state.uuid = uuid;
    },
    error(state, error) {
      state.error = error;
    },
    working(state, progress) {
      state.working = progress;
    },
    task_id(state, id) {
      state.task_id = id;
    },
    plots(state, plots) {
      state.plots = plots;
    }
  },
  actions: {
    reset(context) {
      context.dispatch('site/clear');
      context.dispatch('profiles/clear');
      context.dispatch('financial/clear');
      context.dispatch('battery/clear');
      
      context.commit('uuid', null);
      context.commit('error', null);
      context.commit('working', false);
      context.commit('plots', false);
    }
  }
});
