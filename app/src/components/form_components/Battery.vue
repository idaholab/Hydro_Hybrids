<template>
  <v-container>
    <v-row class="d-block mx-6"
      ><h3>Enter Battery Search Space and Assumptions</h3>
      <p>
        There are some assumptions the machine learning model makes about
        batteries. You should also enter battery parameters, or select the '<i
          >Use Defaults</i
        >' checkbox and make adjustments as necessary.
      </p>
    </v-row>
    <v-row>
      <v-col cols="1"> </v-col>
      <v-col cols="8">
        <hr />
        <v-row justify="start">
          <v-card-subtitle>
            <h3>Fixed assumptions:</h3>
            Range of Charge: 20% - 100%
            <br />
            Total Efficiency: 86%
          </v-card-subtitle>
        </v-row>
        <hr />
        <br />
        <v-row align="center" class="range-inputs">
          <v-card-subtitle style="width: 25%">Capacity</v-card-subtitle>
          <v-col>
            <v-text-field
              :rules="[...rules.required, ...rules.number]"
              min="0.125"
              max="60"
              value="0.125"
              v-model="$store.getters['battery/data'].range_power[0]"
              label="Minimum (MW)"
              type="number"
              step=".125"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              :rules="[...rules.required, ...rules.number]"
              min="0.125"
              max="60"
              value="60"
              v-model="$store.getters['battery/data'].range_power[1]"
              label="Maximum (MW)"
              type="number"
              step="0.125"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col cols="1"
            ><v-tooltip left max-width="250px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on">
                  <v-icon small> mdi-help-circle-outline </v-icon>
                </v-btn>
              </template>
              <span>Number of points plotted on the Capacity-Power axis</span>
            </v-tooltip></v-col
          >
          <v-col cols="11">
            <v-text-field
              :rules="[...rules.required, ...rules.integer]"
              v-model="$store.getters['battery/data'].plotting_interval"
              label="Capacity Interval"
              hint="Integer"
              type="number"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <v-row align="center" class="range-inputs">
          <v-card-subtitle style="width: 25%">Duration</v-card-subtitle>
          <v-col>
            <v-text-field
              :rules="[
                ...rules.required,
                ...rules.number,
                ...rules.range_energy,
              ]"
              min="0.25"
              max="8"
              v-model="$store.getters['battery/data'].range_energy[0]"
              label="Minimum (hours)"
              type="number"
              step="0.25"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              :rules="[
                ...rules.required,
                ...rules.number,
                ...rules.range_energy,
              ]"
              min="0.25"
              max="8"
              v-model="$store.getters['battery/data'].range_energy[1]"
              label="Maximum (hours)"
              type="number"
              step="0.25"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-text-field
            :rules="[...rules.required, ...rules.number]"
            label="Battery Cycle Life at 80% Depth of Discharage"
            hint="Cycles"
            type="number"
            v-model="$store.getters['battery/data'].cycles"
          ></v-text-field>
        </v-row>
        <v-row>
          <v-text-field
            :rules="[...rules.required, ...rules.number]"
            label="Expected Battery Calendar Life"
            hint="Years"
            type="number"
            v-model="$store.getters['battery/data'].lifespan"
          ></v-text-field>
        </v-row>
      </v-col>
      <v-col cols="3">
        <v-checkbox
          color="secondary"
          label="Use Defaults"
          @change="check($event)"
        ></v-checkbox>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Financial",
  methods: {
    check(select) {
      select
        ? this.$store.dispatch("battery/default")
        : this.$store.dispatch("battery/clear");
    },
    state() {
      console.log(this.$store.getters["battery/data"].range_energy);
    },
    clear() {},
  },
  data: () => ({
    rules: {
      required: [(v) => !!v || "Required"],
      number: [
        (v) => !!v || "Required",
        (v) => !Number.isNaN(Number(v)) || "Must be a number",
        (v) => v >= 0 || "Must be a positive number",
      ],
      integer: [
        (v) => !!v || "Required",
        (v) => Number.isInteger(Number(v)) || "Must be an integer",
        (v) => v > 0 || "Must be a non-zero positive integer",
      ],
      range_power: [
        (v) =>
          (v >= 0.125 && v <= 60) ||
          "Battery Capacity must be between 0.125 and 60 MW",
      ],
      range_energy: [
        (v) =>
          (v >= 0.25 && v <= 8) || "Duration must be between 0.25 and 8 hours",
      ],
    },
  }),
};
</script>

<style>
.range-inputs > * {
  padding: 0 0.5rem;
}
</style>
