import httpClient from '@/common/httpClient'

// initial state
const state = () => ({
   mountains: [],
   isLoading: true
})

// getters
const getters = {
    mountains(state) {
        return state.mountains;
      },
    isLoading(state) {
        return state.isLoading;
      }
}

// actions
const actions = {
    fetchMountains( {commit}) {
        commit('FETCH_START')
        let url = '/planine'
         
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
      state.mountains = proizvodi
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