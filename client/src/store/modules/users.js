import httpClient from '@/common/httpClient'
import Swal from 'sweetalert2'

// initial state
const state = () => ({
   users: [],
   isLoading: true,
   // ui control
   addNewActivated: false
})

// getters
const getters = {
    users(state) {
        return state.users;
      },
    isLoading(state) {
        return state.isLoading;
      },
    addNewActivated(state) {
        return state.addNewActivated
    },
}

// actions
const actions = {
    fetchUsers( {commit}) {
        commit('FETCH_START')
        let url = '/korisnici'
         
        httpClient.get(url)
        .then((response) => {
            console.log(response.data);
            commit('FETCH_END', response.data.korisnici)
          })
        .catch(err => {
           console.log(err)
        })
    },
    fetchUser( {commit}, korisnikId) {
      const url = '/korisnici/' + korisnikId
      // console.log('Request to' + url)
      httpClient.get(url)
          .then((response) => {
              console.log(response.data)
              commit('FETCH_END', response.data.korisnici)
          })
          .catch(err => {
              console.log(err)
           })
      
  },
    addNewUser({commit}, user) {
      return new Promise((resolve, reject) => {
          commit('REQUEST')
          httpClient.post("/korisnici", user)
          .then(response => {
              console.log(response.data)
              // check response status
              if(response.status === 201) { // resource created 
                  console.log(JSON.stringify(response.data))
                  // call mutation
                  commit('REQUEST_SUCCESS')
                  commit('CREATE_SUCCESS')
                  resolve(response)
              }   
          })
          .catch(err => {
              console.log(err)
              reject(err)
              commit('CREATE_FAIL')
          })
      })
  },
  setAddNewActivated( {commit}, payload) {
    commit('SET_ADD_NEW_ACTIVATED', payload)
},
}

// mutations
const mutations = {
    FETCH_START(state) {
      state.isLoading = true
    },
    FETCH_END(state, payload) {
      state.users = payload
      state.isLoading = false
    },
    REQUEST (state){
      state.isLoading = true
    },
    REQUEST_SUCCESS (state){
        state.isLoading = false
    },
    SET_ADD_NEW_ACTIVATED (state, payload) {
      state.addNewActivated = payload
    },
    CREATE_SUCCESS() {
      /* success alert */
    Swal.fire({
        width: 400,
        position: 'top-end',
        icon: 'success',
        title: 'Uspješno dodano.',
        showConfirmButton: false,
        timer: 1500
    })
    /*********************************/
  },
  CREATE_FAIL() {
      /* FAIL alert */
    Swal.fire({
        width: 400,
        position: 'top-end',
        icon: 'error',
        title: 'Izgleda da je došlo do greške.',
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