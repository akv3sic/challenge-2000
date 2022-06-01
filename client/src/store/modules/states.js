import httpClient from '@/common/httpClient'

// initial state
const state = () => ({
   states: [],
   isLoading: true
})

// getters
const getters = {
    states(state) {
        return state.states;
      },
    isLoading(state) {
        return state.isLoading;
      }
}

// actions
const actions = {
    fetchStates( {commit}) {
        commit('FETCH_START')
        let url = '/drzave'
         
        httpClient.get(url)
        .then((response) => {
            // console.log(response.data);
            commit('FETCH_END', response.data)
          })
        .catch(err => {
           console.log(err)
        })
    }
}

// mutations
const mutations = {
    FETCH_START(state) {
      state.isLoading = true
    },
    FETCH_END(state, { proizvodi, brendovi, kategorije }) {
      state.states = proizvodi
      state.isLoading = false
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}