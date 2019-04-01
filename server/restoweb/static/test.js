Vue.component('resto-item', {
    props: { resto: Object },
    // language=Vue
    template: `
        <div>[[resto.name]]</div>
    `,
    delimiters: ["[[", "]]"]
});
new Vue({el: '#app'});
