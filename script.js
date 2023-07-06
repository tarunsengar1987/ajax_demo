$(document).ready(function() {
    $('#myTable').DataTable({
      ajax: {
        url: 'https://reqres.in/api/users', // URL to your server-side script that provides the JSON data
        dataSrc: 'data' // Leave empty if the JSON response is an array directly
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