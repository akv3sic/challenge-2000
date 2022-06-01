<template>
    <v-container>
        <v-row>
            <v-col>
                <span class="text-h5">Planine</span>
                <span class="text-h5 grey--text"> ({{ mountains.length }})</span>
                <div class="ml-2 d-inline">
                    <v-btn text small class="primary--text" to="planine-dodaj-novu">Dodaj novu</v-btn>   
                </div>
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
            <v-col cols="7" md="3">
                {{ mountain.naziv}}
            </v-col>
            <v-col cols="3" md="3">
                <v-row class="hidden-md-and-up"> 
                    <v-col class="text-caption">Država</v-col>
                </v-row>
                {{ mountain.drzava}}
            </v-col><v-col cols="3" md="6">
                <v-row class="hidden-md-and-up"> 
                    <v-col class="text-caption">Visina</v-col>
                </v-row>
                {{ mountain.visina}}
            </v-col>

            <v-col md="1">
                <v-icon @click="deleteMountain(mountain.id, mountain.ime, mountain.url_slike)">mdi-delete</v-icon>
                <router-link class="rm-underline" :to="'/admin/uredi-planinu/' + mountain.id + '/' + mountain.slug">
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
    name: 'mountainsList',
    data: () => ({
       
    }),
    mounted() {
        this.fetchMountains();
    },
    methods: {
        fetchMountains() {
            this.$store
                .dispatch('mountains/fetchMountains', {categoryId: null}, {root: true})
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
                .dispatch('mountain/deleteMountain', mountainId, {root: true})
                this.fetchMountains()
                }
            })
        /*********************************/
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