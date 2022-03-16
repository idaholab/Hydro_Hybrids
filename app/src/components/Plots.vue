<template>
  <v-container fill-height height="100vh">
    <v-row align="center" justify="center" width="100vw">
      <v-col>
        <v-btn icon to="/">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <h2 class="d-inline">{{ site }} Machine Learning Plots</h2>
      </v-col>
    </v-row>
    <v-row justify="center" height="80vh">
      <v-row align="center" justify="center" width="100vw">
        <v-col cols="4" align="center">
          This 3D plot shows total hydropower and energy storage revenue (blue
          dots) as a function of battery power (MW) and Energy (MWh). The green
          surface indicates the estimated revenue from the hydropower plant only
          (i.e., without a battery and assumed to only participate in the energy
          market)
        </v-col>
        <v-col cols="4">
          <v-img
            :src="
              'data:image/jpeg;base64,' +
                this.store.getters['data/revenue_plot']
            "
            height="100%"
            width="100%"
          ></v-img>
        </v-col>
      </v-row>
      <v-row align="center" justify="center" width="100vw">
        <v-col cols="4" align="center">
          This 3D plot shows return on investment (ROI) (red dots) associated
          with adding a new battery to an existing hydropower plant (i.e., it is
          the ROI on the battery component). The horizontal axis indicates the
          battery size search space. The ROI is calculated based on the
          estimated increase in revenue possible from adding the battery system
          relative to the corresponding estimated battery capital and
          operational costs. The green text displays the battery system with the
          highest estimated return on investment out of the sizes assessed.
        </v-col>
        <v-col cols="4">
          <v-img
            :src="
              'data:image/jpeg;base64,' + this.store.getters['data/roi_plot']
            "
            height="100%"
            width="100%"
          ></v-img>
        </v-col>
      </v-row>
      <v-row align="center" justify="center" width="100vw">
        <v-col cols="4" align="center">
          This 3D plot shows payback period (red dots) associated with adding a
          new battery to an existing hydropower plant (i.e., it is the payback
          period on the battery component. The horizontal axis indicates the
          battery size search space. The payback period is calculated as the
          number of years required for the additional revenue to equal the total
          costs (both capital and operating). The green text displays the
          battery system with the lowest estimated payback period out of the
          sizes assessed.
        </v-col>
        <v-col cols="4">
          <v-img
            :src="
              'data:image/jpeg;base64,' +
                this.store.getters['data/payback_plot']
            "
          ></v-img>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-btn large color="primary" v-on:click="download">Download</v-btn>
      </v-row>
    </v-row>
  </v-container>
</template>

<script>
import JSZip from "jszip";
import { saveAs } from "file-saver";

export default {
  name: "Plots",
  data: () => ({
    dialog: false,
    site: null,
    uuid: null,
  }),
  mounted: function() {
    this.site = this.$store.getters["site/data"].project_name;
    this.uuid = this.$store.getters.uuid;
    console.log(this.uuid);
    console.log(this.$store.getters["data"]);
  },
  computed: {
    //
  },
  methods: {
    flask_host: function() {
      return `api`;
    },
    csv(filename) {
      return `api/static/${this.uuid}/csv/${filename}_${this.site}.csv`;
    },
    async download() {
      this.$store.commit("working", true);

      let revenue_plot = this.$store.getters["data/revenue_plot"];

      let return_plot = this.$store.getters["data/roi_plot"];

      let payback_plot = this.$store.getters["data/payback_plot"];

      // Get the .csv
      let daily_revenue_csv = this.$store.getters[
        "data/financial_performance_daily"
      ];

      let annual_revenue_csv = this.$store.getters[
        "data/financial_performance_annual"
      ];

      let daily_battery_csv = this.$store.getters[
        "data/battery_degredation_daily"
      ];

      let annual_battery_csv = this.$store.getters[
        "data/battery_degredation_annual"
      ];

      // Load them into a .zip
      let zip = new JSZip();

      zip.folder("plots").file(`RevenuePlot_0_${this.site}.png`, revenue_plot, {
        binary: true,
      });
      zip.folder("plots").file(`ROIPlot_0_${this.site}.png`, return_plot, {
        binary: true,
      });
      zip
        .folder("plots")
        .file(`PaybackPeriodPlot_0_${this.site}.png`, payback_plot, {
          binary: true,
        });

      zip
        .folder("csv")
        .file(`PredictedDailyRevenueData_${this.site}.csv`, daily_revenue_csv, {
          binary: true,
        });
      zip
        .folder("csv")
        .file(
          `PredictedAnnualFinancialPerformance_${this.site}.csv`,
          annual_revenue_csv,
          {
            binary: true,
          }
        );
      zip
        .folder("csv")
        .file(
          `PredictedDailyBatteryDegredation_${this.site}.csv`,
          daily_battery_csv,
          { binary: true }
        );
      zip
        .folder("csv")
        .file(
          `PredictedAnnualBatteryDegredation_${this.site}.csv`,
          annual_battery_csv,
          {
            binary: true,
          }
        );

      await zip.generateAsync({ type: "blob" }).then((content) => {
        saveAs(content, `${this.site}.zip`);
      });

      this.$store.commit("working", false);
    },
  },
};
</script>

<style scoped>
.v-card__text {
  padding: 5rem !important;
}
.col-2 {
  padding: 2rem !important;
}
a {
  bottom: 0.2rem !important;
}
</style>
