<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <span class="text-h4">{{ users.ime }}  {{ users.prezime }}</span>
                <span class="ml-1 text-caption"> {{ users.rola }} </span>
            </v-col>
            <v-col cols="12">
                E-mail: {{ users.email }}
            </v-col>
            <v-col cols="12" sm="6">
                Kreirano: {{ users.created_at }}
            </v-col>
            <v-col cols="12" sm="6">
                Ažurirano: {{ users.updated_at }}
            </v-col>
        </v-row>

        <!--********************* izlistana postignuća ************************-->
        <v-container v-if="!addNewActivated" class="pa-0">
            <v-row>
                <v-col>
                    <span class="text-h6">Postignuća</span>
                    <span class="text-h6 grey--text" v-if="!isLoading && users"> ({{ users.postignuca.length ? users.postignuca.length : '0' }})</span>
                    <div class="ml-2 d-inline">
                        <v-btn text small class="primary--text" @click="setAddNewActivated(!addNewActivated)">Dodaj novo</v-btn>   
                    </div>
                </v-col>
            </v-row>

            <div v-if=" !isLoading && users.postignuca.length > 0">
                <!-- **** ZAGLAVLJE liste **** -->
                <v-row class="hidden-sm-and-down mt-1">
                    <v-col class="text-center" cols="1">
                        <v-icon class="mb-1">mdi-image</v-icon>
                    </v-col>
                    <v-col class="text-left" cols="2">
                        Naziv
                    </v-col>
                    <v-col class="text-left" cols="5">
                        Opis
                    </v-col>
                    <v-col class="text-center" cols="1">
                        GPX trag
                    </v-col>
                </v-row>
                <!-- ************************** -->

                <!-- AKO se element liste učitavaju -->
                <v-skeleton-loader v-if="isLoading" type="table-tbody@3" width="100%"></v-skeleton-loader>
                <!-- ************************** -->
                
                <!-- **** STAVKE liste **** -->
                <v-card
                    v-else
                    v-for="postignuce in users.postignuca"
                    :key="postignuce.id"
                    class="pa-1 my-2"
                    outlined
                >
                    <v-row>
                    <v-col cols="3" md="1">
                        <v-img :src="postignuce.link_slike" contain height="55px" v-if="postignuce.link_slike"></v-img>
                        <v-img src="../../../src/assets/img/placeholder-image.png" contain height="55px" v-else></v-img>
                    </v-col>
                    <v-col cols="5" md="2">
                        {{ postignuce.naslov}}
                    </v-col>
                    <v-col cols="8" md="5">
                        <v-row class="hidden-md-and-up"> 
                            <v-col class="text-caption">Opis</v-col>
                        </v-row>
                        {{ postignuce.opis }} m
                    </v-col>
                    <v-col cols="3" md="1" class="text-center">
                        <v-row class="hidden-md-and-up"> 
                            <v-col class="text-caption">GPX trag</v-col>
                        </v-row>
                        <v-icon @click="openGpxTrace(postignuce.link_gpx_traga)">mdi-eye-arrow-right</v-icon>  
                    </v-col>
                    <v-col  cols="12" md="1">
                        <router-link class="rm-underline" :to="'postignuce/' + postignuce.id">
                            <v-icon class="ml-1">mdi-book-open</v-icon>
                        </router-link>
                        <v-icon @click="deleteAchievement(postignuce.id, postignuce.naslov)">mdi-delete</v-icon>
                        <router-link class="rm-underline" :to="'/admin/uredi-postignuce/' + postignuce.id + '/'">
                            <v-icon class="ml-1">mdi-pencil</v-icon>
                        </router-link>
                    </v-col>
                    </v-row>
                </v-card>
                <!-- ************************** -->
            </div>
            <div v-else>
                <v-row>
                    <v-col>
                        Čini se da ovaj korisnik još nema postignuća.
                    </v-col>
                </v-row>
            </div> 
        </v-container>
        <!--******************* izlistana postignuća kraj **********************-->

        <!--********************* dodavanje novog postignuća ************************-->

        <AchievementsAddNew  v-if="addNewActivated"/>
        <!--******************* dodavanje novog postignuća kraj*********************-->


    </v-container>
</template>

<script>
import { mapGetters } from "vuex"
import { mapActions } from "vuex"
import Swal from 'sweetalert2'
import store from "@/store";
import AchievementsAddNew from "@/components/backoffice/AchievementsAddNew.vue";

export default {
    name: 'mountainsList',
    components: { AchievementsAddNew },
    data: () => ({

    }),
    beforeRouteEnter(to, from, next) {
      store.dispatch('users/fetchUser', to.params.id, {root: true})
      next()
    },
    methods: {
        ...mapActions('users', ['setAddNewActivated']),

        deleteAchievement(postignuceId, postignuceNaslov) {
            /* confirmation dialog */
            Swal.fire({
                title: 'Sigurno želite izbrisati ovo postignuće?',
                text: postignuceNaslov,
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
                .dispatch('crudUniversalHelper/deleteItem', {id: postignuceId, url: 'postignuca'}, {root: true})
                setTimeout(() => {
                    this.$store.dispatch('users/fetchUser', this.$route.params.id, {root: true})
                }, 400)    
                
                }
            })
        /*********************************/
        },
        openGpxTrace(url) {
            window.open(url, '_blank').focus();
        },
        toggleAddNew() {
            console.log("add new toggled")
            this.addNewActivated = !this.addNewActivated
        },
    },
    computed: {
        ...mapGetters('users', ['users', 'isLoading', 'addNewActivated'])
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