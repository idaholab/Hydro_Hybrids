const state = {
    project_name: null,
    capacity: null
}

const getters = {
    data: (state) => state
}

const mutations = {
    project_name(state, name) {
        state.name = (name) ? name.replace(/ /g,'') : null;
    },
    capacity(state, capacity) {
        state.capacity = capacity;
    }
}

const actions = {
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