<template>
  <v-container>
    <v-row>
      <v-col>
        <v-img
          height="350px"
          contain
          src="../assets/hydro-illustration-1.png"
        ></v-img>
      </v-col>
    </v-row>
    <Form @submit="submit" @reset="reset" />
    <v-row justify="center" style="padding: 1rem">
      <v-btn
        v-if="$store.getters.working"
        small
        color="error"
        v-on:click="cancel"
        >Cancel</v-btn
      >
    </v-row>

    <v-row justify="center">
      <template v-if="this.celery.state === 'SUCCESS'">
        <v-btn to="/plots">Preview</v-btn>
      </template>
      <template v-if="$store.getters.plots === true">
        <v-btn to="/plots">Preview</v-btn>
      </template>
    </v-row>

    <v-row justify="center">
      <p v-if="$store.getters.working">
        The machine learning module is making predictions. This could take
        several minutes.
      </p>

      <p style="color: #cf1e4c" v-if="$store.getters.error">
        {{ $store.getters.error }}
      </p>
    </v-row>
  </v-container>
</template>

<script>
import { v4 as uuid } from "uuid";
import axios from "axios";
import Form from "./Form";

export default {
  name: "Home",
  components: {
    Form,
  },
  data: () => ({
    plots: false,
    celery: {},
    celery_link: null,
    task_id: null,
  }),
  watch: {
    celery_link: function() {
      this.status();
    },
  },
  methods: {
    async status() {
      if (this.celery_link) {
        setTimeout(async () => {
          await axios
            .get(`${this.celery_link}`)
            .then((response) => {
              this.celery = response.data;

              console.log(this.celery);

              if (this.celery.state === "PENDING") {
                this.status();
              } else if (this.celery.state === "REVOKED") {
                this.$store.commit("working", false);
              } else if (this.celery.state === "SUCCESS") {
                this.$store.commit("working", false);
              } else {
                this.$store.commit("working", false);
                this.$store.commit("error", this.celery.exception);
              }
              return;
            })
            .catch((error) => {
              console.log(error);
              this.status();
            });
        }, 10000);
      }
      return;
    },
    async submit() {
      this.$store.commit("error", null);
      this.$store.commit("working", true);
      this.$store.commit("uuid", uuid());

      let form = new FormData();

      const data = {
        site: this.$store.getters["site/data"],
        financial: this.$store.getters["financial/data"],
        battery: this.$store.getters["battery/data"],
        uuid: this.$store.getters.uuid,
      };

      form.append("data", JSON.stringify(data));
      for (let [profile, file] of Object.entries(
        this.$store.getters["profiles/data"]
      )) {
        if (file != null) {
          form.append(`${profile}`, file);
        }
      }

      await axios
        .post(`http://localhost:5000/predict`, form, {
          headers: {
            "content-type": "multipart/form-data",
          },
        })
        .then((response) => {
          if (response.status === 202) {
            // Celery
            this.task_id = response.headers["task_id"];
            this.celery_link = `api/tasks/status/${this.task_id}`;
          } else if (response.status === 200) {
            // HTTP
            let data = response.data;

            this.$store.commit(
              "data/battery_degredation_annual",
              data.csv["Battery_Degradation_Annual"]
            );
            this.$store.commit(
              "data/battery_degredation_daily",
              data.csv["Battery_Degradation_Daily"]
            );
            this.$store.commit(
              "data/financial_performance_annual",
              data.csv["Financial_Performance_Annual"]
            );
            this.$store.commit(
              "data/financial_performance_daily",
              data.csv["Financial_Performance_Daily"]
            );

            this.$store.commit("data/payback_plot", data.plots["Payback_Plot"]);
            this.$store.commit("data/roi_plot", data.plots["ROI_Plot"]);
            this.$store.commit("data/revenue_plot", data.plots["Revenue_Plot"]);

            this.$store.commit("working", false);
            this.$store.commit("plots", true);
          }
        })
        .catch((error) => {
          console.log(error);
          this.$store.commit("working", false);
          this.$store.commit("error", error.response.data.message);
        });
    },
    async cancel() {
      this.$store.commit("working", false);
      await axios
        .get(`api/tasks/kill`, {
          params: {
            task_id: this.task_id,
          },
        })
        .then((response) => {
          if (response.status === 200) {
            this.$store.commit(
              "error",
              "Successfully canceled the machine learning task."
            );
            setTimeout(() => {
              this.$store.commit("error", null);
            }, 3500);
          } else {
            this.$store.commit("error", response.data);
          }
        })
        .catch((error) => {
          console.log(error);
          this.$store.commit("error", error.data.message);
        });
    },
    reset() {
      this.plots = false;
      this.error = null;
      this.celery = {};
    },
  },
};
</script>

<style></style>
