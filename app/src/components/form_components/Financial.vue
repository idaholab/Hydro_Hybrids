<template>
  <v-container fluid>
    <v-row class="d-block mx-6"
      ><h3>Enter Financial Assumptions</h3>
      <p>
        The Hydro + Storage Tool uses financial assumptions to optimize energy
        storage size based on financial performance of the energy storage
        investment. If you don't know these values you can select the '<i
          >Use Defaults</i
        >' checkbox and make adjustments as necessary.
      </p>
    </v-row>
    <v-row>
      <v-col cols="1"></v-col>
      <v-col cols="8">
        <br />
        <v-row align="center">
          <v-card-subtitle style="width: 25%">
            Discount Rate for NPV
          </v-card-subtitle>
          <v-col>
            <v-text-field
              :rules="rules.required"
              type="number"
              label="10-yr treasury bonds"
              hint="Percent (%)"
              v-model="$store.getters['financial/data'].discountrate10"
              v-on:change="
                (value) => $store.commit('financial/discountrate10', value)
              "
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              :rules="rules.required"
              type="number"
              label="20-yr treasury bonds"
              hint="Percent (%)"
              v-model="$store.getters['financial/data'].discountrate20"
              v-on:change="
                (value) => $store.commit('financial/discountrate20', value)
              "
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-text-field
            :rules="rules.required"
            type="number"
            label="Financial Analysis Period"
            hint="Years"
            v-model="$store.getters['financial/data'].analysis"
            v-on:change="(value) => $store.commit('financial/analysis', value)"
          ></v-text-field>
        </v-row>
        <v-row>
          <v-text-field
            :rules="rules.required"
            type="number"
            label="Weighted Cost of Capital"
            hint="Percent (%)"
            v-model="$store.getters['financial/data'].capital"
            v-on:change="(value) => $store.commit('financial/capital', value)"
          ></v-text-field>
        </v-row>
        <v-row>
          <v-text-field
            :rules="rules.required"
            type="number"
            label="Annual O&M Escalation Rate"
            hint="Percent (%)"
            v-model="$store.getters['financial/data'].oandm"
            v-on:change="(value) => $store.commit('financial/oandm', value)"
          ></v-text-field>
        </v-row>
        <v-row>
          <v-text-field
            :rules="rules.required"
            type="number"
            label="Insurance Rate"
            hint="Percent (%)"
            v-model="$store.getters['financial/data'].insurance"
            v-on:change="(value) => $store.commit('financial/insurance', value)"
          ></v-text-field>
        </v-row>
        <v-row>
          <v-text-field
            :rules="rules.required"
            type="number"
            label="Property Tax Rate"
            hint="Percent (%)"
            v-model="$store.getters['financial/data'].property"
            v-on:change="(value) => $store.commit('financial/property', value)"
          ></v-text-field>
        </v-row>
        <v-row>
          <v-text-field
            :rules="rules.required"
            type="number"
            label="Federal and State Income Tax Rate"
            hint="Percent (%)"
            v-model="$store.getters['financial/data'].income"
            v-on:change="(value) => $store.commit('financial/income', value)"
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
        ? this.$store.dispatch("financial/default")
        : this.$store.dispatch("financial/clear");
    },
  },
  data: () => ({
    rules: {
      required: [(v) => !!v || "Required"],
      number: [
        (v) => !!v || "Required",
        (v) => !Number.isNaN(Number(v)) || "Must be a number",
        (v) => v >= 0 || "Must be a positive number",
      ],
    },
  }),
};
</script>

<style>
/* .v-input {
  padding: 0 0.5rem;
} */
</style>
