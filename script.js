$(document).ready(function() {
    $('#myTable').DataTable({
      processing: true,
      serverSide: true,
      ajax: {
        url: 'http://localhost:8000/data', // URL of your FastAPI endpoint
        type: 'POST',
        contentType: 'application/json',
        data: function(params) {
          return JSON.stringify({
            draw: params.draw,
            start: params.start,
            length: params.length,
            search: {
              value: params.search.value
            },
            order: [{
              column: params.order[0].column,
              dir: params.order[0].dir
            }],
            columns: params.columns
          });
        },
        dataSrc: function(response) {
          return response.data;
        }
      },
      columns: [
        { data: 'id' },
        { data: 'email' },
        { data: 'first_name' },
        { data: 'last_name' },
        { data: 'avatar' }
      ]
    });
  });
  