import httpClient from '@/common/httpClient'

// initial state
const state = () => ({
   mountains: [],
   isLoading: true,
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
            console.log(response.data);
            commit('FETCH_END', response.data.planine)
          })
        .catch(err => {
           console.log(err)
        })
    },
    fetchMountain( {commit}, mountainId) {
      const url = '/planine/' + mountainId
      // console.log('Request to' + url)
      httpClient.get(url)
          .then((response) => {
              console.log(response.data)
              commit('FETCH_END', response.data.planine)
          })
          .catch(err => {
              console.log(err)
           })
      
  },
  addNewMountain( {commit}, payload) {
    return new Promise((resolve, reject) => {
        httpClient.post("/planine", payload)
        .then(response => {
            // check response status
            if(response.status === 200) { // OK
                // assign response data
                const msg = response.data.message
                console.log(msg)
                // call mutation
                //commit('PUBLISH_SUCCESS')
                resolve(response)
            }
        })
        .catch(err => {
            console.log(err)
            reject(err)
        })
    })
},
}

// mutations
const mutations = {
    FETCH_START(state) {
      state.isLoading = true
    },
    FETCH_END(state, payload) {
      state.mountains = payload
      state.isLoading = false
    },
    SET_MOUNTAIN(state, payload) {
      state.mountain = payload
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