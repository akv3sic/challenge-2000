<template>
    <v-container>
        <v-row>
            <v-col>
                <span class="text-h5">Korisnici</span>
                <span class="text-h5 grey--text" v-if="!isLoading"> ({{ users.length }})</span>
                <div class="ml-2 d-inline">
                    <v-btn text small class="primary--text" to="dodaj-novog-korisnika">Dodaj novog</v-btn>   
                </div>
            </v-col>
        </v-row>

        <!-- **** ZAGLAVLJE liste **** -->
        <v-row class="hidden-sm-and-down mt-1">
            <v-col class="text-left" cols="3">
                Ime i prezime
            </v-col>
            <v-col class="text-left" cols="3">
                E-mail
            </v-col>
            <v-col class="text-left" cols="6">
                Uloga
            </v-col>
        </v-row>
        <!-- ************************** -->

        <!-- AKO se element liste učitavaju -->
        <v-skeleton-loader v-if="isLoading" type="table-tbody@3" width="100%"></v-skeleton-loader>
        <!-- ************************** -->
        
        <!-- **** STAVKE liste **** -->
        <v-card
            v-for="user in users"
            :key="user.id"
            class="pa-1 my-2 list-item"
            outlined
            :to="'korisnik/' + user.id"
        >
            <v-row>
            <v-col cols="3" md="3">
                {{ user.ime}} {{ user.prezime}}
            </v-col>
            <v-col cols="5" md="3">
                <v-row class="hidden-md-and-up"> 
                    <v-col class="text-caption">E-mail</v-col>
                </v-row>
                {{ user.email}}
            </v-col><v-col cols="3" md="5">
                <v-row class="hidden-md-and-up"> 
                    <v-col class="text-caption">Uloga</v-col>
                </v-row>
                {{ user.rola}}
            </v-col>

            <v-col  cols="12" md="1">
                <v-icon @click="deleteUser(user.id, user.ime, user.prezime)">mdi-delete</v-icon>
                <router-link class="rm-underline" :to="'/admin/uredi-planinu/' + user.id + '/'">
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
    name: 'usersList',
    data: () => ({
       
    }),
    mounted() {
        this.fetchUsers();
    },
    methods: {
        fetchUsers() {
            this.$store
                .dispatch('users/fetchUsers', {categoryId: null}, {root: true})
        },
        deleteUser(userId, userName, userSurname) {
            /* confirmation dialog */
            Swal.fire({
                title: 'Sigurno želite izbrisati ovog korisnika?',
                text: userName + userSurname,
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
                .dispatch('user/deleteUser', userId, {root: true})
                this.fetchUsers()
                }
            })
        /*********************************/
        }
    },
    computed: {
        ...mapGetters('users', ['users', 'isLoading'])
    },
}
</script>

<style scoped>
.rm-underline{
    text-decoration: none;
}
</style>