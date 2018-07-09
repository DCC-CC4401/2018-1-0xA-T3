$("#schedule-demo").jqs({
        mode:"read",
        data: [{
            day: 0,
            periods: [{
                start: "09:00",
                end: "11:00",
                title: "Una reserva"
            },
            {
                start: "16:00",
                end: "18:00",
                title: "Otra reserva"
            }]
        }, {
                day: 2,
                periods: [
            {
                start: "10:00",
                end: "12:00",
                title: "Una tercera reserva"
            }
        ]
    }
        ]
    });

$("#schedule-espacio-demo").jqs({
        mode:"read",
        data: [{
            day: 0,
            periods: [{
                start: "09:00",
                end: "11:00",
                title: "Una reserva"
            },
            {
                start: "16:00",
                end: "18:00",
                title: "Otra reserva",
                backgroundColor: "rgba(207, 0, 15, 0.5)"
            },
            {
                start: "15:00",
                end: "16:00",
                title: "Otra2 reserva",
                backgroundColor: "rgba(207, 0, 15, 0.5)"
            }]
        }, {
                day: 2,
                periods: [
            {
                start: "10:00",
                end: "12:00",
                title: "Una tercera reserva"
            }
        ]
    }
        ]
});