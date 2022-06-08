<template>
    <v-container>
        <v-row>
            <v-col>
                <span class="text-h5">Uredi korisnika</span>
                <div class="ml-2 d-inline">
                    <v-btn text small class="red--text" to="korisnici">Odustani</v-btn>   
                </div>
            </v-col>
        </v-row>

        <v-form ref="addNewUserForm" lazy-validation v-model="valid" class="add-new-form"> 
            <v-row>
                <!--Data -->
                <v-col cols="6" class="mx-auto">
                    <v-text-field v-model="users.ime" :rules="[rules.required]" label="Ime" maxlength="20" required></v-text-field>
                </v-col>
                <v-col cols="6" class="mx-auto">
                    <v-text-field v-model="users.prezime" :rules="[rules.required]" label="Prezime" maxlength="20" required></v-text-field>
                </v-col>
                <v-col cols="12" class="mb-2 mx-auto">
                    <v-select
                    v-model="users.rola"
                    :items="uloge"
                    label="Uloga korisnika"
                    ></v-select>
                </v-col>
                <v-col cols="12" class="mx-auto">
                    <v-text-field v-model="users.email" :rules="emailRules" label="E-mail" required></v-text-field>
                </v-col>

                
                <!--add new btn -->
                <v-col cols="12" class="mx-auto">
                    <v-btn class="primary" :disabled="!valid" @click="editUser">Uredi korisnika</v-btn>
                </v-col> 
            </v-row>
        </v-form>
    </v-container>
</template>

<script>
import { mapGetters } from "vuex"
import store from "@/store";


export default {
    name: "addNewuser",
    data: () => ({
        valid: false,
        emailRules: [
        v => !!v || "Obavezno polje.",
        v => /.+@.+\..+/.test(v) || "Unesite ispravnu e-mail adresu."
        ],
        rules: {
        required: value => !!value || "Obavezno polje.",
        },
        showPassword: false,
        uloge: [
            'Admin', 'Korisnik'
        ],
        selectedRole: null
    }),
    beforeRouteEnter(to, from, next) {
      store.dispatch('users/fetchUser', to.params.id, {root: true})
      next()

    },
    mounted() {
        this.ime = this.users.ime
    },
    methods: {
        editUser() {
        if (this.$refs.addNewUserForm.validate()) {
            const USER = {
                email: this.users.email,
                ime: this.users.ime,
                prezime: this.users.prezime,
                rola: this.selectedRole
            }
            console.log(USER)
            this.$store
                .dispatch('crudUniversalHelper/updateItem', {payload: USER, url: 'korisnici/' + this.$route.params.id}, {root: true})
                .catch( err => {
                    console.log("Greška pri ažuriranju korisnika: " + err)
                })
            }
            setTimeout(()=>{this.$store.dispatch('users/fetchUser', this.$route.params.id, {root: true})}, 500)
        },
    },
    computed: {
        ...mapGetters('users', ['users', 'isLoading'])
    },
}
</script>

<style>
@media screen and (min-width: 1200px){
   .add-new-form {
    max-width: 50vw;
    } 
}
</style>