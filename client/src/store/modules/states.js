import httpClient from '@/common/httpClient'
import Swal from 'sweetalert2'

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
            console.log(response.data.drzave);
            commit('FETCH_END', response.data.drzave)
          })
        .catch(err => {
           console.log(err)
        })
    },
    addNewState( {commit}, payload) {
      return new Promise((resolve, reject) => {
          httpClient.post("/drzave", payload)
          .then(response => {
              // check response status
              if(response.status === 201) { // success
                  // assign response data
                  const msg = response.data.message
                  console.log(msg)
                  // call mutation
                  commit('CREATE_SUCCESS')
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
      state.states = payload
      state.isLoading = false
    },
    CREATE_SUCCESS() {
        /* success alert */
      Swal.fire({
          width: 400,
          position: 'top-end',
          icon: 'success',
          title: 'Država uspješno dodana.',
          showConfirmButton: false,
          timer: 1500
      })
      /*********************************/
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}