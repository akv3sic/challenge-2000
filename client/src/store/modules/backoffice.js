import httpClient from "./../../common/httpClient";

// initial state
const state = () => ({
    drawer: null,
    selectedDatabase: 0,
    baseUrl: process.env.VUE_APP_BASE_URL
 })
 
 // getters
 const getters = {
    drawer(state) {
        return state.drawer
    },
    selectedDatabase(state) {
        return state.selectedDatabase
    }
 }
 
 // actions
 const actions = {
    setDrawer( {commit}, payload) {
        commit('SET_DRAWER', payload)
    },
    setSelectedDatabase( {commit}, payload) {
        commit('SET_SELECTED_DATABASE', payload)
    },
 }
 
 // mutations
 const mutations = {
    SET_DRAWER (state, payload) {
        state.drawer = payload
    },
    SET_SELECTED_DATABASE (state, payload) {
        state.selectedContract = payload
        if(payload == 0) {
            console.log("postgres")
            console.log(httpClient)
            httpClient.defaults.baseURL = "http://127.0.0.1:9595/postgres/"
        } 

        else {
            console.log("mongo db")
            httpClient.defaults.baseURL = "http://127.0.0.1:9595/mongo/"
        }
          

            
    },
 }
 
 export default {
     namespaced: true,
     state,
     getters,
     actions,
     mutations
 }