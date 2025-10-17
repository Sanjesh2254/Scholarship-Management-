frappe.ui.form.on('Checkbox', {
    number_of_seats: function (frm) {
        frm.trigger('render_seat_checkboxes');
    },

    render_seat_checkboxes: function (frm) {
        const numSeats = frm.doc.number_of_seats || 0;
        const cols = 5;
        let html = `
            <style>
                table.seat-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }
                .seat-table td {
                    border: 1px solid #ccc;
                    padding: 10px;
                    text-align: left;
                    vertical-align: middle;
                }
                .seat-table input[type="checkbox"] {
                    margin-right: 6px;
                }
            </style>
            <table class="seat-table">
        `;

        for (let i = 0; i < numSeats; i++) {
            if (i % cols === 0) html += '<tr>';

            html += `
                <td>
                    <input type="checkbox" id="seat_${i + 1}" name="seat_${i + 1}">
                    <label for="seat_${i + 1}">Seat ${i + 1}</label>
                </td>
            `;

            if ((i + 1) % cols === 0) html += '</tr>';
        }

        // Close the last row if it’s not full
        if (numSeats % cols !== 0) {
            let remaining = cols - (numSeats % cols);
            for (let j = 0; j < remaining; j++) {
                html += '<td></td>';
            }
            html += '</tr>';
        }

        html += '</table>';

        frm.fields_dict.seat_checkboxes.$wrapper.html(html);
    },

    refresh: function (frm) {
        frm.trigger('render_seat_checkboxes');
    }
});
