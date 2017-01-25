function manage_domain(domain_name) {

}

function start_challenge()
{
    var names = document.getElementsByName('username');
    console.log(names);
    var selected_rows = [];
    var challenge_table = document.getElementById("domain-list")

    for (var i = 0; i < names.length; i++) {
        if (names[i].value == "--")
        {
            continue;
        }
        var row_idx = names[i].parentElement.parentElement.rowIndex;

        var domain_name = challenge_table.rows[row_idx].cells[0].innerText;
        var snapshot_name = challenge_table.rows[row_idx].cells[1].innerText;

        selected_rows.push({
            "domain_name" : domain_name,
            "snapshot_name" : snapshot_name,
            "username" : names[i].value
        });
    }

      // construct an HTTP request
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/startvm", true);
      xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

      // send the collected data as JSON
      xhr.send(JSON.stringify(selected_rows));

      xhr.onloadend = function () {
        alert("Sent. I can't program web pages")
      };

    console.log(selected_rows);
}
