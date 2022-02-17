const state = {
    electricity: null,
    price: null
}

const getters = {
    data: (state) => state
}

const mutations = {
    electricity(state, file) {
        state.electricity = file;
    },
    price(state, file) {
        state.price = file;
    }
}

const actions = {
    electricity(context, file) {
        context.commit(this.electricity(file))
    },
    price(context, file) {
        context.commit(this.price(file))
    },
    clear(context) {
        Object.keys(state).forEach(key => {
            context.commit(`${key}`, null);
        })
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}