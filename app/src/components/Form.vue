<template>
  <v-container fill-height class="main">
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <h3>Hydro + Storage Tool</h3>
          </v-card-title>

          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-header>
                <p>Plant Information</p>
                <template v-slot:actions v-if="!flags.site">
                  <v-icon color="error"> mdi-alert-circle </v-icon>
                </template>
              </v-expansion-panel-header>
              <v-expansion-panel-content eager>
                <br />
                <!-- PlantData.vue -->
                <v-form ref="site">
                  <Site />
                </v-form>
              </v-expansion-panel-content>
            </v-expansion-panel>

            <v-divider></v-divider>

            <v-expansion-panel>
              <v-expansion-panel-header>
                <p>Hydropower Generation & Electricity Market Prices</p>
                <template v-slot:actions v-if="!flags.profiles">
                  <v-icon color="error"> mdi-alert-circle </v-icon>
                </template>
              </v-expansion-panel-header>
              <v-expansion-panel-content eager>
                <br />
                <!-- Profiles.vue -->
                <v-form ref="profiles">
                  <Profiles />
                </v-form>
              </v-expansion-panel-content>
            </v-expansion-panel>
            <v-divider></v-divider>

            <v-expansion-panel>
              <v-expansion-panel-header>
                <p>Financial Assumptions</p>
                <template v-slot:actions v-if="!flags.financial">
                  <v-icon color="error"> mdi-alert-circle </v-icon>
                </template>
              </v-expansion-panel-header>
              <v-expansion-panel-content eager>
                <br />
                <!-- Financial.vue -->
                <v-form ref="financial">
                  <Financial />
                </v-form>
              </v-expansion-panel-content>
            </v-expansion-panel>
            <v-divider></v-divider>

            <v-expansion-panel>
              <v-expansion-panel-header>
                <p>Battery Search Space and Assumptions</p>
                <template v-slot:actions v-if="!flags.battery">
                  <v-icon color="error"> mdi-alert-circle </v-icon>
                </template>
              </v-expansion-panel-header>
              <v-expansion-panel-content eager>
                <br />
                <!-- Battery.vue -->
                <v-form ref="battery">
                  <Battery />
                </v-form>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card>
        <br />
        <template v-if="!valid">
          <p style="color: #cf1e4c">Please resolve validation errors</p>
        </template>
        <v-btn
          v-if="!$store.getters.working || $store.getters.error"
          color="primary"
          v-on:click="submit"
          >Submit</v-btn
        >
        <v-row id="reset-button" justify="end">
          <v-btn
            small
            v-if="!$store.getters.working && !$store.getters.error"
            color="error"
            v-on:click="reset"
            >Reset</v-btn
          ></v-row
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// Helpers
import validate from "./form_helpers/validate";
import reset from "./form_helpers/reset";

// Components
import Site from "./form_components/Site";
import Profiles from "./form_components/Profiles";
import Financial from "./form_components/Financial";
import Battery from "./form_components/Battery";

export default {
  name: "Home",
  components: {
    Site,
    Profiles,
    Financial,
    Battery,
  },
  methods: {
    async submit() {
      this.valid = validate(this);

      if (this.valid) {
        this.$emit("submit", true);
      }

      return;
    },
    reset() {
      reset(this);
    },
    cancel() {
      this.$emit("cancel");
    },
  },
  data: () => ({
    form_submit: false,
    valid: true,
    flags: {
      site: true,
      profiles: true,
      financial: true,
      battery: true,
    },
  }),
};
</script>

<style scoped>
.custom-placeholder-color input::placeholder {
  color: gray !important;
  opacity: 1;
}
.v-input--is-disabled input::placeholder {
  color: gray !important;
  opacity: 0.6;
}
#reset-button {
  padding: 1rem;
}
.main {
  width: 70%;
}
.v-icon {
  bottom: 0.25rem;
  padding: 0 !important;
}
</style>
