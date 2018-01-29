function manage_domain(domain_name) {

}

function start_challenge() {
	selected_doms = [];
	player0 = document.getElementById("player0").value;
	player1 = document.getElementById("player1").value;
	os = document.getElementById("os").value;
	type = document.getElementById("type").value;
	lvl = document.getElementById("lvl").value;

	//Resolve player0
	doms.forEach(function(dom) {
		if(dom["snapshot_name"].includes(type) && dom["snapshot_name"].includes(lvl)) {
			if(dom["domain_name"].includes(os)) {
				if(dom["domain_name"].split('-')[2] == "player0") {
					username = player0;
				}
				else {
					username = player1;
				}
			}
			if(!dom["domain_name"].includes("player")) {
					username = "--";
			}
			selected_doms.push({
			    "domain_name" : dom["domain_name"],
			    "snapshot_name" : dom["snapshot_name"],
			    "username" : username
			});
		}
	});
      // construct an HTTP request
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/startvm", true);
      xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

      // send the collected data as JSON
      xhr.send(JSON.stringify(selected_doms));

      xhr.onloadend = function () {
        alert("Sent. I can't program web pages")
      };

    console.log(selected_doms);
}

function start_challenge_old()
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

function stop_challenge()
{
    console.log("STOPPING CHALLENGES");
      // construct an HTTP request
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/stopvm", true);
      xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

      // send the collected data as JSON
      xhr.send(JSON.stringify("kill"));

      xhr.onloadend = function () {
        alert("The deed has been done.")
      };
}
