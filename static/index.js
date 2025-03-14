document.addEventListener("DOMContentLoaded", function () {
    $('.select2').select2({
        placeholder: "Select an option...",
        allowClear: true,
        width: '13%'
    });

    function populateSelect2(selectId) {
        $.ajax({
            url: '/airports',
            method: 'GET',
            success: function (data) {
                let select = $(`#${selectId}`);
                select.empty();
                select.append('<option value="" disabled selected></option>');

                data.forEach((airport, index) => {
                    if (index === 0 && (!airport["IATA Code"] || airport["IATA Code"].length !== 3)) {
                        return;
                    }

                    let option = $('<option>', {
                        value: airport["IATA Code"],
                        text: `${airport["Airport Name"]} (${airport["IATA Code"]}) - ${airport["City"]}, ${airport["Country"]}`
                    });
                    select.append(option);
                });

                select.trigger('change');
            }
        });
    }

    populateSelect2('departure');
    populateSelect2('destination');

    document.getElementById('form')
        .addEventListener('submit', function (event) {
        let departure = document.getElementById('departure').value;
        let destination = document.getElementById('destination').value;
        let algorithm = document.getElementById('algorithm').value;
        let aircraft = document.getElementById('aircraft').value;
        if (!departure || !destination) {
            alert('Please select both departure and destination airports.');
            event.preventDefault();
        } else if (departure === destination) {
            alert('Departure and destination airports cannot be the same :(');
            event.preventDefault();
        } else if(!algorithm) {
            alert('Please select an algorithm.');
            event.preventDefault();
        } else if(!aircraft) {
            alert('Please select an aircraft.');
            event.preventDefault();
        }

    });
});



$(document).ready(function() {
  function removeSuccess() {
    $('.button').removeClass('success');
  }

  $('.button').click(function() {
    $(this).addClass('success');
    setTimeout(removeSuccess, 3000); // Reset
  });
});