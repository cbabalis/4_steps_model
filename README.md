# Prerequisites

[ ] Run osrm backend:

`sudo docker run -t -i -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --algorithm mld --max-table-size 1000000 /data/greece-latest.osrm`

[ ] Run osrm frontend (not mandatory)
`sudo docker run -p 9966:9966 osrm/osrm-frontend`

[ ] Run the program.