const state = {
    analysis: null,
    discountrate10: null,
    discountrate20: null,
    capital: null,
    oandm: null,
    insurance: null,
    property: null,
    income: null,
}

const getters = {
    data: (state) => state
}

const mutations = {
    analysis(state, value) {
        state.analysis = value;
    },
    discountrate10(state, value) {
        state.discountrate10 = value;
    },
    discountrate20(state, value) {
        state.discountrate20 = value;
    },
    capital(state, value) {
        state.capital = value;
    },
    oandm(state, value) {
        state.oandm = value;
    },
    insurance(state, value) {
        state.insurance = value;
    },
    property(state, value) {
        state.property = value;
    },
    income(state, value) {
        state.income = value;
    }

}

const actions = {
    default(context) {
        Object.keys(state).forEach(key => {
            context.commit(`${key}`, defaults[`${key}`]);
        })
    },
    clear(context) {
        Object.keys(state).forEach(key => {
            context.commit(`${key}`, null);
        })
    }
}

const defaults = {
    analysis: 10,
    discountrate10: 1.79,
    discountrate20: 2.06,
    capital: 7.6,
    oandm: 2.5,
    insurance: 0.5,
    property: 0.6,
    income: 24.9,
}


export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
    defaults,
}