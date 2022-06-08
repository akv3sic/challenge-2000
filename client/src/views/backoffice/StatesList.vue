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
            class="pa-1 my-2"
            outlined
        >
            <v-row>
            <v-col cols="3" md="4">

                <span v-if="editedDrzava.id != state.id">{{ state.naziv}}</span> 

                <v-text-field
                    v-else
                    v-model="state.naziv"
                    class="pa-0"
                >
                </v-text-field>
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
                <div  v-if="editedDrzava.id != state.id">
                    <v-icon @click="deleteState(state.id, state.naziv)">mdi-delete</v-icon>
                    <v-icon class="ml-1" @click="activateEdit(state.id)">mdi-pencil</v-icon>
                </div>

                <div v-else>
                    <v-icon class="ml-1" @click="updateState" color="green">mdi-check</v-icon>
                    <v-icon class="ml-1" @click="activateEdit(null)" color="red">mdi-close</v-icon>
                </div>
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
           naziv: "",
       },
       editedDrzava: {
           naziv: "",
           id: ""
       },
       addNewActivated: false,
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
                    .dispatch('crudUniversalHelper/deleteItem', {id: stateId, url: 'drzave'}, {root: true})
                setTimeout(() => {
                    this.fetchStates()
                    console.log("ma uslo u timeout haha")
                }, 400)
                
                }
            })
        /*********************************/
        },
        activateAddNew() {
            console.log("add new activated")
            this.addNewActivated = true
        },
        activateEdit(id) {
            console.log("uredi drzavu id " + id)
            this.editedDrzava.id = id
        },
        addNewState() {
            this.$store
                .dispatch('states/addNewState', this.novaDrzava, { root: true })
                .catch( err => {
                    console.log(err)
                })
            this.addNewActivated = false
            setTimeout(()=>{this.fetchStates()}, 700)
            
        },
        updateState(){
            this.editedDrzava.naziv = this.states.find(x => x.id === this.editedDrzava.id).naziv;
            console.log(JSON.stringify(this.editedDrzava) + "idemo")

            this.$store
                .dispatch('crudUniversalHelper/updateItem',
                        {payload: {'naziv': this.editedDrzava.naziv}, url: 'drzave/' + this.editedDrzava.id},
                        {root: true})
                .catch( err => {
                    console.log(err)
                })

            this.editedDrzava.id = null
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