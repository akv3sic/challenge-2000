<template>
    <v-container>
        <v-row>
            <v-col>
                <span class="text-h5">Dodaj novog korisnika</span>
                <div class="ml-2 d-inline">
                    <v-btn text small class="red--text" to="korisnici">Odustani</v-btn>   
                </div>
            </v-col>
        </v-row>

        <v-form ref="addNewUserForm" lazy-validation v-model="valid" class="add-new-form"> 
            <v-row>
                <!--Data -->
                <v-col cols="6" class="mx-auto">
                    <v-text-field v-model="ime" :rules="[rules.required]" label="Ime" maxlength="20" required></v-text-field>
                </v-col>
                <v-col cols="6" class="mx-auto">
                    <v-text-field v-model="prezime" :rules="[rules.required]" label="Prezime" maxlength="20" required></v-text-field>
                </v-col>
                <v-col cols="12" class="mb-2 mx-auto">
                    <v-select
                    v-model="selectedRole"
                    :items="uloge"
                    label="Uloga korisnika"
                    ></v-select>
                </v-col>
                <v-col cols="12" class="mx-auto">
                    <v-text-field v-model="email" :rules="emailRules" label="E-mail" required></v-text-field>
                </v-col>
                <v-col cols="12" class="mb-2 mx-auto">
                    <v-text-field v-model="password" :append-icon="showPassword?'mdi-eye':'mdi-eye-off'" :rules="[rules.required]" :type="showPassword ? 'text' : 'password'" name="input-10-1" label="Lozinka" counter @click:append="showPassword = !showPassword"></v-text-field>
                </v-col>
                
                <!--add new btn -->
                <v-col cols="12" class="mx-auto">
                    <v-btn class="primary" :disabled="!valid" @click="addNewStaff">Dodaj korisnika</v-btn>
                </v-col> 
            </v-row>
        </v-form>
    </v-container>
</template>

<script>
export default {
    name: "addNewuser",
    data: () => ({
        valid: false,
        ime: "",
        prezime: "",
        password: "",
        email: "",
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
    methods: {
        addNewStaff() {
        if (this.$refs.addNewUserForm.validate()) {
            const USER = {
                email: this.email,
                ime: this.ime,
                prezime: this.prezime,
                password: this.password,
                rola: this.selectedRole
            }
            console.log(USER)
            this.$store
                .dispatch('users/addNewUser', USER, { root: true })
                .catch( err => {
                    console.log("Greška pri dodavanju novog korisnika: " + err)
                })
            }
            setTimeout(()=>{this.$router.push({path: 'korisnici'})}, 500)
        },
    }
}
</script>

<style>
@media screen and (min-width: 1200px){
   .add-new-form {
    max-width: 50vw;
    } 
}
</style>