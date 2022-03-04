<template>
  <v-app>
    <v-app-bar app absolute color="primary" class="toolbar">
      <v-img max-width="250px" src="./assets/inl-banner.png"></v-img>

      <v-spacer></v-spacer>
    </v-app-bar>

    <v-navigation-drawer app min-width="30%">
      <v-container fill-height>
        <v-row align="center" justify="center">
          <v-col class="introduction">
            <h1>
              Hydro + Storage <br />
              Sizing Tool
            </h1>
            <hr />
            <br />
            <p>
              The Hydro + Storage Sizing Tool is designed to help hydropower
              asset owners who participate in competitive electricity markets do
              a preliminary assessment of the value of integrating batteries
              with their facility. The basic requirements for using the tool are
              hydropower generation, electricity prices, and financial
              performance metrics of interest. The tool is based upon research
              conducted by Idaho National Laboratory and Argonne National
              Laboratory. It is a research product and may not be accurate for
              every set of conditions provided. Users should not interpret the
              output as financial advice. The output is meant to guide asset
              owners and developers down the initial steps of considering
              hydropower hybridization.
            </p>
            <v-spacer></v-spacer>
            <v-img height="40px" contain src="./assets/inl-logo.png"></v-img>
            <br />
            <v-img height="40px" contain src="./assets/anl-logo.png"></v-img>
            <br />
            <v-img height="40px" contain src="./assets/nrel-logo.png"></v-img
          ></v-col>
        </v-row>
      </v-container>
    </v-navigation-drawer>

    <v-main>
      <v-container>
        <keep-alive>
          <router-view />
        </keep-alive>
      </v-container>
    </v-main>

    <v-footer align="center">
      <template v-if="$store.getters.working">
        <v-progress-linear indeterminate></v-progress-linear>
      </template>
    </v-footer>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  components: {},
  data: () => ({
    //
  }),
  mounted: async function () {
    await axios
      .get(`api/healthcheck`)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>

<style scoped>
/deep/ .v-toolbar__content {
  border-bottom: 5px #8dc340 solid !important;
}

.introduction {
  padding: 1rem;
}

.introduction > p {
  font-size: 11px;
}

.v-footer {
  background-color: white !important;
}
</style>
