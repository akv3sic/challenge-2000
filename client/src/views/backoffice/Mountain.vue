<template>
    <v-container>
        <v-row>
            <v-col>
                <span class="text-h4">{{ mountains.naziv }} - {{ mountains.drzava }}</span>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <span class="text-h6">Vrhovi</span>
                <span class="text-h6 grey--text" v-if="!isLoading"> ({{ mountains.vrhovi.length }})</span>
                <div class="ml-2 d-inline" v-if="!addNewActivated">
                    <v-btn text small class="primary--text"  @click="activateAddNew">Dodaj novi</v-btn>   
                </div>
                <v-row v-else>
                    <v-col >
                        <v-text-field
                            label="Naziv vrha"
                            v-model="noviVrh.naziv"
                        ></v-text-field>  
                    </v-col>
                    <v-col >
                        <v-text-field
                            label="Visina"
                            v-model="noviVrh.nadmorska_visina"
                        ></v-text-field>  
                    </v-col>
                    <v-col>
                        <v-btn text small class="primary--text mt-2" @click="addNewMountain">Potvrdi</v-btn>  
                    </v-col>
                </v-row>
            </v-col>
        </v-row>

                
        <div v-if="!isLoading && mountains.vrhovi.length > 0">
            <!-- **** ZAGLAVLJE liste **** -->
            <v-row class="hidden-sm-and-down mt-1">
                <v-col class="text-left" cols="3">
                    Naziv
                </v-col>
                <v-col class="text-left" cols="6">
                    Visina
                </v-col>
            </v-row>
            <!-- ************************** -->

            <!-- AKO se element liste učitavaju -->
            <v-skeleton-loader v-if="isLoading" type="table-tbody@3" width="100%"></v-skeleton-loader>
            <!-- ************************** -->
            
            <!-- **** STAVKE liste **** -->
            <v-card
                v-else
                v-for="vrh in mountains.vrhovi"
                :key="vrh.id"
                class="pa-1 my-2"
                outlined
            >
                <v-row>
                <v-col cols="3" md="3">
                    <span v-if="editedId != vrh.id">
                        {{ vrh.naziv}}
                    </span>
                    <v-text-field
                        v-else
                        v-model="vrh.naziv"
                        class="pa-0"
                    >
                    </v-text-field>

                    <!-- najvisi vrh ima zastavicu -->
                    <v-icon color="red" v-if="vrh.naziv == mountains.najvisi_vrh">mdi-flag-triangle</v-icon>
                </v-col>
                <v-col cols="3" md="5">
                    <v-row class="hidden-md-and-up"> 
                        <v-col class="text-caption">Visina</v-col>
                    </v-row>
                    <span v-if="editedId != vrh.id">
                        {{ vrh.nadmorska_visina }} m
                    </span>
                    <v-text-field
                        v-else
                        v-model="vrh.nadmorska_visina"
                        class="pa-0"
                    >
                    </v-text-field>
                </v-col>

                <v-col  cols="12" md="1">
                    <div  v-if="editedId != vrh.id">
                        <v-icon @click="deletePeak(vrh.id, vrh.naziv)">mdi-delete</v-icon>
                        <v-icon class="ml-1" @click="activateEdit(vrh.id)">mdi-pencil</v-icon>
                    </div>

                    <div v-else>
                        <v-icon class="ml-1" @click="updatePeak" color="green">mdi-check</v-icon>
                        <v-icon class="ml-1" @click="activateEdit(null)" color="red">mdi-close</v-icon>
                    </div>
                </v-col>
                </v-row>
            </v-card>
            <!-- ************************** -->
        </div>


        
        <div v-else>
            <v-row>
                <v-col>
                    Čini se da ova planina nema unesenih vrhova.
                </v-col>
            </v-row>
        </div>

    </v-container>
</template>

<script>
import { mapGetters } from "vuex"
import Swal from 'sweetalert2'
import store from "@/store";

export default {
    name: 'mountainsList',
    data: () => ({
        noviVrh: {
            naziv: "",
            nadmorska_visina: "",
            planina_id: ""
        },
       addNewActivated: false,
       editedId: null
    }),
    beforeRouteEnter(to, from, next) {
      store.dispatch('mountains/fetchMountain', to.params.id, {root: true})
      next()
    },
    methods: {
        deletePeak(peakId, peakName) {
            /* confirmation dialog */
            Swal.fire({
                title: 'Sigurno želite izbrisati ovaj vrh?',
                text: peakName,
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
                .dispatch('crudUniversalHelper/deleteItem', {id: peakId, url: 'vrhovi'}, {root: true})
                setTimeout(() => {
                    this.$store.dispatch('mountains/fetchMountain', this.$route.params.id, {root: true})
                }, 300)
                }
            })
        /*********************************/
        },
        activateAddNew() {
            console.log("add new activated")
            this.addNewActivated = true
        },
        activateEdit(id) {
            console.log("uredi vrh id " + id)
            this.editedId = id
        },
        updatePeak(){
            this.noviVrh.naziv = this.mountains.vrhovi.find(x => x.id === this.editedId).naziv
            this.noviVrh.nadmorska_visina = this.mountains.vrhovi.find(x => x.id === this.editedId).nadmorska_visina
            this.noviVrh.planina_id = this.$route.params.id
            console.log(JSON.stringify(this.noviVrh) + " idemo")

            this.$store
                .dispatch('crudUniversalHelper/updateItem',
                        {payload: this.noviVrh, url: 'vrhovi/' + this.editedId},
                        {root: true})
                .catch( err => {
                    console.log(err)
                })
    
            this.editedId = null
            setTimeout(()=> {
                this.$store.dispatch('mountains/fetchMountain', this.$route.params.id, {root: true})
            }, 400)
            
        },
        addNewMountain() {
            this.noviVrh.planina_id = this.$route.params.id
            console.log(this.noviVrh)

            store.dispatch('crudUniversalHelper/createItem', { payload: this.noviVrh, url: '/vrhovi' }, {root: true})

            this.addNewActivated = false
            setTimeout(()=>{
                store.dispatch('mountains/fetchMountain', this.noviVrh.planina_id, {root: true})
            }, 700)
        }
    },
    computed: {
        ...mapGetters('mountains', ['mountains', 'isLoading'])
    },
}
</script>

<style scoped>
.rm-underline{
    text-decoration: none;
}
</style>

<style>
.list-item:hover {
    border-color: #301E70;
    border-width: 0.15rem;
}
</style>