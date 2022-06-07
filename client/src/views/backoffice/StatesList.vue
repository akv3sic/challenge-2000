<template>
    <v-container>
        <v-row>
            <v-col>
                <span class="text-h5">Države</span>
                <span class="text-h5 grey--text" v-if="!isLoading"> ({{ states.length }})</span>
                <div class="ml-2 d-inline" v-if="!addNewActivated">
                    <v-btn text small class="primary--text" @click="activateAddNew">Dodaj novu</v-btn>   
                </div>

                <v-row v-if="addNewActivated">
                    <v-col >
                        <v-text-field
                            label="Naziv države"
                            v-model="novaDrzava.naziv"
                        ></v-text-field>  
                    </v-col>
                    <v-col>
                        <v-btn text small class="primary--text mt-2" @click="addNewState">Potvrdi</v-btn>  
                    </v-col>
                </v-row>
            </v-col>
        </v-row>

        <!-- **** ZAGLAVLJE liste **** -->
        <v-row class="hidden-sm-and-down mt-1">
            <v-col class="text-left" cols="4">
                Naziv
            </v-col>
            <v-col class="text-left" cols="3">
                Kreirano
            </v-col>
            <v-col class="text-left" cols="3">
                Broj planina
            </v-col>
        </v-row>
        <!-- ************************** -->

        <!-- AKO se element liste učitavaju -->
        <v-skeleton-loader v-if="isLoading" type="table-tbody@3" width="100%"></v-skeleton-loader>
        <!-- ************************** -->
        
        <!-- **** STAVKE liste **** -->
        <v-card
            v-for="state in states"
            :key="state.id"
            class="pa-1 my-2 list-item"
            outlined
        >
            <v-row>
            <v-col cols="3" md="4">
                {{ state.naziv}}
            </v-col>
            <v-col cols="5" md="3">
                <v-row class="hidden-md-and-up"> 
                    <v-col class="text-caption">Kreirano</v-col>
                </v-row>
                {{ state.created_at}}
            </v-col><v-col cols="3" md="3">
                <v-row class="hidden-md-and-up"> 
                    <v-col class="text-caption">Broj planina</v-col>
                </v-row>
                {{ state.broj_planina}}
            </v-col>

            <v-col md="1">
                <v-icon @click="deleteState(state.id, state.ime, state.url_slike)">mdi-delete</v-icon>
                <router-link class="rm-underline" :to="'/admin/uredi-planinu/' + state.id + '/' + state.slug">
                    <v-icon class="ml-1">mdi-pencil</v-icon>
                </router-link>
            </v-col>
            </v-row>
        </v-card>
        <!-- ************************** -->
    </v-container>
</template>

<script>
import { mapGetters } from "vuex"
import Swal from 'sweetalert2'

export default {
    name: 'statesList',
    data: () => ({
       novaDrzava: {
           naziv: ""
       },
       addNewActivated: false
    }),
    mounted() {
        this.fetchStates();
    },
    methods: {
        fetchStates() {
            this.$store
                .dispatch('states/fetchStates', {root: true})
        },
        deleteState(stateId, stateName, stateImageUrl) {
            /* confirmation dialog */
            Swal.fire({
                title: 'Sigurno želite izbrisati ovu planinu?',
                text: stateName,
                imageUrl: stateImageUrl,
                imageHeight: 135,
                showDenyButton: true,
                confirmButtonText: `Da, izbriši`,
                confirmButtonColor: '#052949',
                denyButtonText: 'Ne',
                denyButtonColor: '#c52033',
                customClass: {
                confirmButton: 'order-2',
                denyButton: 'order-3',
                }
            }).then((result) => {
                if (result.isConfirmed) {
                this.$store
                .dispatch('states/deleteState', stateId, {root: true})
                this.fetchstates()
                }
            })
        /*********************************/
        },
        activateAddNew() {
            console.log("add new activated")
            this.addNewActivated = true
        },
        addNewState() {
            this.$store
                .dispatch('states/addNewState', this.novaDrzava, { root: true })
                .catch( err => {
                    console.log(err)
                })
            this.addNewActivated = false
            setTimeout(()=>{this.fetchStates()}, 700)
            
        }
    },
    computed: {
        ...mapGetters('states', ['states', 'isLoading'])
    },
}
</script>

<style scoped>
.rm-underline{
    text-decoration: none;
}
</style>