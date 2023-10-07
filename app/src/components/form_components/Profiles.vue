<template>
  <v-container>
    <br />
    <v-row class="d-block mx-6">
      <h3>Upload Time-Series Profile Data</h3>
      <p>
        The Hydro + Storage Tool requires energy generation and price profiles.
        These profiles are expected to have a one-year duration at a five minute
        time interval. Refer to the profile samples as a template for formatting
        your data.
      </p>
      <hr />
      <p class="helper-text">
        <v-icon class="pa-2">mdi-lightbulb-on-outline</v-icon>
        Download the sample profiles as a template for building your input
        profiles.<br />
        <v-btn color="secondary" v-on:click="samples"
          >Download Profile Samples</v-btn
        >
      </p>

      <hr />
      <br />
      <h3>1. Gather Generation and Electricity Market Price Time-Series</h3>
      <p>
        Two files are required corresponding to “Energy Generation Profile” and
        “Electricity Market Price Profile.”
        <br /><br />The fields required for each file are:
      </p>
    </v-row>
    <v-row class="mx-6">
      <v-col cols="6">
        <h4>Energy Generation Profile</h4>
        <hr />
        <template v-for="header of csv_headers.energy"
          ><div v-bind:key="header">
            <v-tooltip left max-width="250px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on">
                  <v-icon small> mdi-help-circle-outline </v-icon>
                </v-btn>
              </template>
              <span>{{ csv_helpers.energy[header] }}</span> </v-tooltip
            >{{ header }}<br /></div
        ></template>
      </v-col>
      <v-col>
        <h4>Electricity Market Price Profile</h4>
        <hr />
        <template v-for="header of csv_headers.price"
          ><div v-bind:key="header">
            <v-tooltip left max-width="250px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on">
                  <v-icon small> mdi-help-circle-outline </v-icon>
                </v-btn>
              </template>
              <span>{{ csv_helpers.price[header] }}</span> </v-tooltip
            >{{ header }}<br /></div
        ></template>
      </v-col>
    </v-row>
    <br />

    <br />
    <v-row class="d-block mx-6">
      <h3>2. Ensure column headers follow naming convention</h3>
      <p>
        The <i>column names</i> of the data in your profiles must be compliant
        with the template format. Be sure to name your columns correctly in
        order for the model to recognize your data. The application will let you
        know if you need to make changes to the column names.
      </p>
    </v-row>
    <br /><br />
    <v-row class="d-block mx-6">
      <h3>3. Upload Profiles</h3>
      <p>
        Upload the energy generation and price profile data in their respective
        fields below.
      </p>
      <v-file-input
        :rules="rules.required"
        label="Energy Generation Profile"
        v-model="$store.getters['profiles/data'].electricity"
        accept=".csv"
        hint=".csv"
      ></v-file-input>
      <v-file-input
        :rules="rules.required"
        label="Price Profile"
        v-model="$store.getters['profiles/data'].price"
        accept=".csv"
        hint=".csv"
      ></v-file-input>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import JSZip from "jszip";
import { saveAs } from "file-saver";

export default {
  name: "Profiles",
  data: () => ({
    rules: {
      required: [(v) => !!v || "Required"],
    },
    csv_headers: {
      energy: ["Datetime (m/d/yyyy h:mm)", "Total Hydro Generation (MWh)"],
      price: [
        "Datetime (m/d/yyyy h:mm)",
        "Price: Energy ($/MWh)",
        "Price: RegUp ($/MWh)",
        "Price: RegDn ($/MWh)",
        "Price: Spin ($/MWh)",
        "Price: NonSpin ($/MWh)",
      ],
    },
    csv_helpers: {
      energy: {
        "Datetime (m/d/yyyy h:mm)":
          "Date string with indicated format. Five-minute interval is expected.",
        "Total Hydro Generation (MWh)":
          "Day-ahead electricity market prices. Five-minute interval is expected.",
      },
      price: {
        "Datetime (m/d/yyyy h:mm)":
          "Date string with indicated format. Five-minute interval is expected.",
        "Price: Energy ($/MWh)":
          "Day-ahead electricity market prices. Five-minute interval is expected.",
        "Price: RegUp ($/MWh)":
          "Frequency regulation up ancillary service market product. Five-minute interval is expected.",
        "Price: RegDn ($/MWh)":
          "Frequency regulation down ancillary service market product. Five-minute interval is expected.",
        "Price: Spin ($/MWh)":
          "Spinning reserve ancillary service market product. Five-minute interval is expected.",
        "Price: NonSpin ($/MWh)":
          "Non-spinning reserve ancillary service market product. Five-minute interval is expected.",
      },
    },
  }),
  methods: {
    async samples() {
      // Get the Energy Generation sample
      let energy_sample = await axios
        .get(`api/static/samples/EnergyGenerationProfile.csv`, {
          responseType: "arraybuffer",
        })
        .then((response) => {
          return response.data;
        });

      // Get the Price sample
      let profile_sample = await axios
        .get(`api/static/samples/PriceProfile.csv`, {
          responseType: "arraybuffer",
        })
        .then((response) => {
          return response.data;
        });

      // Load them into a .zip
      let zip = new JSZip();

      zip
        .folder("profile_samples")
        .file("EnergyGenerationProfile.csv", energy_sample, { binary: true });
      zip
        .folder("profile_samples")
        .file("PriceProfile.csv", profile_sample, { binary: true });

      await zip.generateAsync({ type: "blob" }).then((content) => {
        saveAs(content, "profile_samples.zip");
      });
    },
  },
};
</script>

<style>
.helper-text {
  margin: 0 !important;
  padding: 0.5rem 0;
}
</style>
