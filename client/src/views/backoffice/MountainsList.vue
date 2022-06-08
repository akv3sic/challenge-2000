<template>
    <v-container>
        <v-row>
            <v-col>
                <span class="text-h5">Planine</span>
                <span class="text-h5 grey--text" v-if="!isLoading"> ({{ mountains.length }})</span>
                <div class="ml-2 d-inline" v-if="!addNewActivated">
                    <v-btn text small class="primary--text" @click="activateAddNew">Dodaj novu</v-btn>   
                </div>
                <v-row v-else>
                    <v-col >
                        <v-text-field
                            label="Naziv planine"
                            v-model="novaPlanina.naziv"
                        ></v-text-field>  
                    </v-col>
                    <v-col >
                    <v-select
                    v-model="novaPlanina.drzava_id"
                    :items="states"
                    item-text="naziv"
                    item-value="id"
                    label="Država"
                    ></v-select>
                    </v-col>
                    <v-col>
                        <v-btn text small class="primary--text mt-2" @click="addNewMountain">Potvrdi</v-btn>  
                    </v-col>
                </v-row>
            </v-col>
        </v-row>

        <!-- **** ZAGLAVLJE liste **** -->
        <v-row class="hidden-sm-and-down mt-1">
            <v-col class="text-left" cols="3">
                Naziv
            </v-col>
            <v-col class="text-left" cols="3">
                Država
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
            v-for="mountain in mountains"
            :key="mountain.id"
            class="pa-1 my-2"
            outlined
        >
            <v-row>
            <v-col cols="3" md="3">
                <span v-if="editedId != mountain.id">
                    {{ mountain.naziv}}
                </span>
                <v-text-field
                    v-else
                    v-model="mountain.naziv"
                    class="pa-0"
                >
                </v-text-field>
            </v-col>
            <v-col cols="5" md="3">
                <v-row class="hidden-md-and-up"> 
                    <v-col class="text-caption">Država</v-col>
                </v-row>
                <span v-if="editedId != mountain.id">
                    {{ mountain.drzava}}
                </span>
                <v-select
                    v-else
                    v-model="novaPlanina.drzava_id"
                    :items="states"
                    item-text="naziv"
                    item-value="id"
                    label="Država"
                    class="pa-0"
                ></v-select>
            </v-col>
            <v-col cols="3" md="4">
                <v-row class="hidden-md-and-up"> 
                    <v-col class="text-caption">Visina</v-col>
                </v-row>
                <span v-if="mountain.visina_vrha">{{ mountain.visina_vrha}} m - {{ mountain.najvisi_vrh }}</span>
                <span v-else>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                            <v-icon
                            v-bind="attrs"
                            v-on="on"
                            >
                            mdi-alert
                            </v-icon>
                        </template>
                        <span>Nema dodanih vrhova.</span>
                    </v-tooltip>
                </span>
            </v-col>

            <v-col  cols="12" md="2">
                <div v-if="editedId != mountain.id">
                    <router-link class="rm-underline" :to="'planina/' + mountain.id">
                        <v-icon class="ml-1">mdi-book-open</v-icon>
                    </router-link>
                    <v-icon @click="deleteMountain(mountain.id, mountain.naziv)">mdi-delete</v-icon>
                    <v-icon class="ml-1" @click="activateEdit(mountain.id)">mdi-pencil</v-icon>
                </div>
                <div v-else>
                    <v-icon class="ml-1" @click="updateMountain" color="green">mdi-check</v-icon>
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
    name: 'mountainsList',
    data: () => ({
       novaPlanina: {
           naziv: "",
           drzava_id: ""
       },
       editedId: null,
       addNewActivated: false
    }),
    mounted() {
        this.fetchMountains();
    },
    methods: {
        fetchMountains() {
            this.$store
                .dispatch('mountains/fetchMountains', {categoryId: null}, {root: true})
        },
        fetchStates() {
            this.$store
                .dispatch('states/fetchStates', {root: true})
        },
        deleteMountain(mountainId, mountainName, mountainImageUrl) {
            /* confirmation dialog */
            Swal.fire({
                title: 'Sigurno želite izbrisati ovu planinu?',
                text: mountainName,
                imageUrl: mountainImageUrl,
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
                .dispatch('crudUniversalHelper/deleteItem', {id: mountainId, url: 'planine'}, {root: true})
                this.fetchMountains()
                }
            })
        /*********************************/
        },
        activateAddNew() {
            console.log("add new activated")
            this.addNewActivated = true
            this.fetchStates()
        },
        addNewMountain() {
            console.log(this.novaPlanina)
            this.$store
                .dispatch('mountains/addNewMountain', this.novaPlanina, { root: true })
                .catch( err => {
                    console.log(err)
                })
            this.addNewActivated = false
            setTimeout(()=>{this.fetchMountains()}, 700)
        },
        activateEdit(id) {
            console.log("uredi planinu id " + id)
            this.editedId = id
            this.fetchStates()
        },
        updateMountain(){
            this.novaPlanina.naziv = this.mountains.find(x => x.id === this.editedId).naziv;
            console.log(JSON.stringify(this.novaPlanina) + "idemo")

            this.$store
                .dispatch('crudUniversalHelper/updateItem',
                        {payload: this.novaPlanina, url: 'planine/' + this.editedId},
                        {root: true})
                .catch( err => {
                    console.log(err)
                })
    
            this.editedId = null
            setTimeout(()=> {
                this.fetchMountains()
            }, 400)
            
        }
    },
    computed: {
        ...mapGetters('mountains', ['mountains', 'isLoading']),
        ...mapGetters('states', ['states'])
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