const state = {
        range_power: [null, null],
        range_energy: [null, null],
        plotting_interval: null,
        range_charge: [null, null],
        efficiency: null,
        cycles: null,
        lifespan: null,
    }

const getters = {
    data: (state) => state
}

const mutations = {
    range_power(state, range) {
        state.range_power = range;
    },
    range_energy(state, range) {
        state.range_energy = range;
    },
    plotting_interval(state, interval) {
        state.plotting_interval = interval;
    },
    range_charge(state, range) {
        state.range_charge = range;
    },
    efficiency(state, efficiency) {
        state.efficiency = efficiency;
    },
    cycles(state, cycles) {
        state.cycles = cycles;
    },
    lifespan(state, lifespan) {
        state.lifespan = lifespan;
    }
}

const actions = {
    default(context) {
        Object.keys(state).forEach(key => {
            context.commit(`${key}`, defaults[`${key}`]);
        })
    },
    clear(context) {
        context.commit('range_power', [null, null]);
        context.commit('range_energy', [null, null]);
        context.commit('plotting_interval', null);
        context.commit('range_charge', [null, null]);
        context.commit('efficiency', null);
        context.commit('cycles', null);
        context.commit('lifespan', null);
    }
}

const defaults = {
    range_power: [0.125, 60],
    range_energy: [0.25, 8],
    plotting_interval: 10,
    range_charge: [20, 100],
    efficiency: 86,
    cycles: 3500,
    lifespan: 10,
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}