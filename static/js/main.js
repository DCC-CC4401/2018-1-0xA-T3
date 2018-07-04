$("#schedule-demo").jqs({
        mode:"read",
        data: [{
            day: 0,
            periods: [{
                start: "00:00",
                end: "02:00",
                title: "Una reserva"
            },
            {
                start: "20:00",
                end: "00:00",
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
                start: "00:00",
                end: "02:00",
                title: "Una reserva"
            },
            {
                start: "20:00",
                end: "00:00",
                title: "Otra reserva",
                backgroundColor: "rgba(207, 0, 15, 0.5)"
            },
            {
                start: "19:00",
                end: "20:00",
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

