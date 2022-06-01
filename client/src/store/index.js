import Vue from 'vue';
import Vuex from 'vuex';

import backoffice from './modules/backoffice'
import mountains from './modules/mountains'
import states from './modules/states'

Vue.use(Vuex);


export default new Vuex.Store({
  modules: {
      backoffice, mountains, states
  }
});