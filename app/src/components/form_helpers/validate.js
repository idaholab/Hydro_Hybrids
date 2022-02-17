function validate(vue) {
    vue.flags["site"] = vue.$refs.site.validate();
    vue.flags["profiles"] = vue.$refs.profiles.validate();
    vue.flags["financial"] = vue.$refs.financial.validate();
    vue.flags["battery"] = vue.$refs.battery.validate();
    
    return !Object.values(vue.flags).includes(false);
}

export default validate;