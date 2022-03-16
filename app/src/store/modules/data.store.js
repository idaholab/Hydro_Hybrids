const state = {
        csv: {
            battery_degredation_annual: null,
            battery_degredation_daily: null,
            financial_performance_annual: null,
            financial_performance_daily: null
        },
        plots: {
            payback_plot: null,
            roi_plot: null,
            revenue_plot: null
        }
    }


const getters = {
    data: (state) => state
}

const mutations = {
    battery_degredation_annual(state, data) {
        state.csv.battery_degredation_annual = data;
    },
    battery_degredation_daily(state, data) {
        state.csv.battery_degredation_daily = data;
    },
    financial_performance_annual(state, data) {
        state.csv.financial_performance_annual = data;
    },
    financial_performance_daily(state, data) {
        state.csv.financial_performance_daily = data;
    },
    payback_plot(state, data) {
        state.plots.payback_plot = data;
    },
    roi_plot(state, data) {
        state.plots.roi_plot = data;
    },
    revenue_plot(state, data) {
        state.plots.revenue_plot = data;
    }
}

const actions = {
    clear(context) {
        context.commit('battery_degredation_annual', null);
        context.commit('battery_degredation_daily', null);
        context.commit('financial_performance_annual', null);
        context.commit('financial_performance_daily', null);
        context.commit('payback_plot', null);
        context.commit('roi_plot', null);
        context.commit('revenue_plot', null);
    }
}


export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}