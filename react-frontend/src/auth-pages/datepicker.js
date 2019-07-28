const datepickerTrigger = () => {
    window.$('#calendar').datepicker({
        autoclose: true,
        todayHighlight: true,
        clearBtn: true
    });
};

const datepickerRemove = () => {
    window.$('.datepicker').remove();
};

export { datepickerTrigger, datepickerRemove };
