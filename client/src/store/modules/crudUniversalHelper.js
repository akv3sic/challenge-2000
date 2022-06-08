import httpClient from '@/common/httpClient'
import Swal from 'sweetalert2'

// initial state
const state = () => ({
   items: [],
   isLoading: true
})

// getters
const getters = {
    items(state) {
        return state.states;
      },
    isLoading(state) {
        return state.isLoading;
      }
}

// actions
const actions = {
    fetchItems( {commit}) {
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
    createItem( {commit}, {payload, url}) {
      return new Promise((resolve, reject) => {
          httpClient.post(url, payload)
          .then(response => {
              // check response status
              if(response.status === 200 || 201) { // OK
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
              commit('FAIL')
          })
      })
    },
    updateItem( {commit}, {payload, url}) {
      return new Promise((resolve, reject) => {
          httpClient.put(url, payload)
          .then(response => {
              // check response status
              if(response.status === 201 || 204) { // success
                  // assign response data
                  const msg = response.data.message
                  console.log(msg)
                  // call mutation
                  commit('UPDATE_SUCCESS')
                  resolve(response)
              }
          })
          .catch(err => {
              console.log(err)
              reject(err)
          })
      })
    },
    deleteItem( {commit}, {id, url}) {
      return new Promise((resolve, reject) => {
          httpClient.delete(url + '/' + id)
          .then(response => {
              // check response status
              if(response.status === 200) { // OK
                  // assign response data
                  const msg = response.data.message
                  console.log(msg)
                  // call mutation
                  resolve(response)
              }
          })
          .catch(err => {
              console.log(err)
              reject(err)
              commit('FAIL')
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
          title: 'Uspješno dodano.',
          showConfirmButton: false,
          timer: 1500
      })
      /*********************************/
    },
    UPDATE_SUCCESS() {
        /* success alert */
      Swal.fire({
          width: 400,
          position: 'top-end',
          icon: 'success',
          title: 'Promjene spremljene.',
          showConfirmButton: false,
          timer: 1500
      })
      /*********************************/
    },
    FAIL() {
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