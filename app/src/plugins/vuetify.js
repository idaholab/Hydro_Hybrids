import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: false,
    themes: {
      light: {
        primary: "#07519E",
        secondary: "#07519E",
        accent: "#07519E",
        error: "#CF1E4C",
      },
    },
  },
});
