import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        dark: false,
        themes: {
          light: {
            primary: '#07519E',
            secondary: '#8DC340',
            accent: '#2BA8E0',
            error: '#CF1E4C'
          }
        }
      }
});
