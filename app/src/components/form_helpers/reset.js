function reset(vue) {
    // reset the form
    vue.$store.dispatch("reset");

    // reset the validation
    vue.$refs.site.reset();
    vue.$refs.profiles.reset();
    vue.$refs.financial.reset();
    vue.$refs.battery.reset();

    // toggle the validation error
    vue.valid = true;
}

export default reset;