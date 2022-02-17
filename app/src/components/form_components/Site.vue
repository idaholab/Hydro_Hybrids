<template>
  <v-container>
    <v-row class="d-block mx-6"
      ><h3>Enter Plant Data</h3>
      <p>
        Get started by entering the utility name and plant capacity.
      </p>
    </v-row>
    <v-row>
      <v-col cols="1"> </v-col>
      <v-col cols="8">
        <v-text-field
          :rules="rules.required"
          label="Project Name"
          v-model="$store.getters['site/data'].project_name"
          hint="Name"
        ></v-text-field>
        <v-text-field
          :rules="rules.number"
          label="Plant Capacity"
          hint="MW"
          v-model="$store.getters['site/data'].capacity"
          :min="0.125"
          type="number"
        ></v-text-field>
      </v-col>
      <v-col cols="3"> </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Site",
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
