<template>
<v-container fluid class="mt-16">
    <v-row justify="center" align="center">
        <v-col cols="8" sm="5" md="4" lg="3">
          <v-img class="text-center" src="@/assets/img/challenge-2000-logo.png"></v-img>
          <div class="display-1 text-center mt-5">Stranica nije pronađena</div>
          <div class="subtitle-1 text-center mt-5">Izgleda da ste otišli na stranicu koja je ne postoji ili je premještena na drugu adresu.</div>
        </v-col>
    </v-row>
    <v-row justify="center" align="center">


            <v-btn class="my-5" color="secondary" text @click="$router.back()">Vrati me natrag</v-btn>
            <v-btn class="my-5" color="primary" text @click="$router.push({ path: '/' })">Idi na početnu</v-btn>

    </v-row>
</v-container>
</template>

<script>
export default {
    name: "NotFound",
  data: () => ({
  })
}
</script>