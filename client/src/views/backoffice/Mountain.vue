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
                <div class="ml-2 d-inline">
                    <v-btn text small class="primary--text" to="planine-dodaj-novu">Dodaj novi</v-btn>   
                </div>
            </v-col>
        </v-row>

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
            class="pa-1 my-2 list-item"
            outlined
        >
            <v-row>
            <v-col cols="3" md="3">
                {{ vrh.naziv}}
                <v-icon color="red" v-if="vrh.naziv == mountains.najvisi_vrh">mdi-flag-triangle</v-icon>
            </v-col>
            <v-col cols="3" md="5">
                <v-row class="hidden-md-and-up"> 
                    <v-col class="text-caption">Visina</v-col>
                </v-row>
                {{ vrh.nadmorska_visina }} m
            </v-col>

            <v-col  cols="12" md="1">
                <v-icon @click="deletePeak(vrh.id, vrh.naziv)">mdi-delete</v-icon>
                <router-link class="rm-underline" :to="'/admin/uredi-planinu/' + vrh.id + '/'">
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
import store from "@/store";

export default {
    name: 'mountainsList',
    data: () => ({
       
    }),
    beforeRouteEnter(to, from, next) {
      store.dispatch('mountains/fetchMountain', to.params.id, {root: true})
      next()
    },
    methods: {
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

<style>
.list-item:hover {
    border-color: #301E70;
    border-width: 0.15rem;
}
</style>