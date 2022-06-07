<template>
    <v-container>
        <v-row>
            <v-col>
                <span class="text-h6">Dodaj novo postignuće</span>
                <div class="ml-2 d-inline">
                    <v-btn text small class="red--text" @click="setAddNewActivated(!addNewActivated)">Odustani</v-btn>   
                </div>
            </v-col>
        </v-row>

        <v-form ref="addNewAchievementForm" lazy-validation v-model="valid" class="add-new-form"> 
            <v-row>
                <!--Data -->
                <v-col cols="12" class="mx-auto">
                    <v-text-field v-model="newAchievement.naslov" :rules="[rules.required]" label="Naslov" maxlength="20" required></v-text-field>
                </v-col>
                <v-col cols="12" class="mx-auto">
                    <v-textarea v-model="newAchievement.opis" :rules="[rules.required]" label="Opis" maxlength="120" counter="" required></v-textarea>
                </v-col>
                <v-col cols="12" class="mx-auto">
                    <v-text-field v-model="newAchievement.link_gpx_traga" :rules="[rules.required]" label="GPX trag" maxlength="20" required></v-text-field>
                </v-col>
                
                <!--add new btn -->
                <v-col cols="12" class="mx-auto">
                    <v-btn class="primary" :disabled="!valid" @click="addNewAchievement">Dodaj postignuće</v-btn>
                </v-col> 
            </v-row>
        </v-form>
    </v-container>
</template>

<script>
import { mapGetters } from "vuex"
import { mapActions } from "vuex"

export default {
    name: "addNewuser",
    data: () => ({
        newAchievement: {
            korisnik_id:3,
            naslov:"",
            opis:"",
            link_gpx_traga:""
        },
        rules: {
            required: value => !!value || "Obavezno polje.",
        },
        valid: false
    }),
    computed: {
        ...mapGetters('users', ['addNewActivated'])
    },
    methods: {
        ...mapActions('users', ['setAddNewActivated']),

        addNewAchievement() {
        if (this.$refs.addNewAchievementForm.validate()) {
            this.newAchievement.korisnik_id = this.$route.params.id
            console.log(this.newAchievement)
            this.$store
                .dispatch('crudUniversalHelper/createItem', { payload: this.newAchievement, url: '/postignuca' }, { root: true })
                .catch( err => {
                    console.log("Greška pri dodavanju novog postignuća: " + err)
                })
            }
            setTimeout(()=>{this.$store.dispatch('users/fetchUser', this.$route.params.id, {root: true})}, 500)
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