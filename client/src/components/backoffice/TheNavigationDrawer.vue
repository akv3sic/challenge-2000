<template>
    <div>
        <v-navigation-drawer 
            v-model="drawer"
            app
        >
        <v-list-item>
            <v-list-item-content>
                <v-row>
                    <v-col justify-center>
                    <router-link to="/" class="text-decoration-none  text-uppercase primary--text">
                        <img class="" :src="require('../../assets/img/challenge-2000-logo.png')" height="80"/>
                    </router-link>
                    </v-col>
                </v-row>
            </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

            <v-list
                nav
                dense
            >
                 <v-list-item
                 v-for="item in navigationItems"
                 :key="item.title"
                 :to="item.to"
                 >
                    <v-list-item-icon>
                    <v-icon v-text="item.icon"></v-icon>
                    </v-list-item-icon>

                    <v-list-item-title v-text="item.title"></v-list-item-title>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
    </div>
</template>

<script>

export default {
    name: 'NavigationDrawer',
    data: () => ({
      navigationItems: [
        /*
        {
          icon: 'mdi-account',
          title: 'Moj račun',
          to: "/admin/moj-racun"
        },
        */
        {
          icon: 'mdi-image-filter-hdr',
          title: 'Planine',
          to: "/admin/planine"
        },
        {
          icon: 'mdi-account-multiple',
          title: 'Korisnici',
          to: "/admin/korisnici"
        },
        {
          icon: 'mdi-flag',
          title: 'Države',
          to: "/admin/drzave"
        },
        {
          icon: 'mdi-map-marker-path',
          title: 'GPX tragovi',
          to: "/admin/gpx-tragovi"
        },
        {
          icon: 'mdi-cog',
          title: 'Postavke',
        },
        {
          icon: 'mdi-help',
          title: 'Pomoć',
        },
      ]
    }),
    computed: {
      drawer: {
        get () {
          return this.$store.getters['backoffice/drawer']
        },
        set (val) {
          this.$store.dispatch('backoffice/setDrawer', val)
        },
      },
    },
}
</script>