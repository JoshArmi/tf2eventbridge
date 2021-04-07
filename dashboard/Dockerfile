FROM grafana/grafana:7.2.2

ENV GF_INSTALL_PLUGINS="grafana-timestream-datasource"

COPY timestream.yml /etc/grafana/provisioning/datasources/timestream.yml
COPY dashboards.yml /etc/grafana/provisioning/dashboards/dashboards.yml
COPY slo_dashboard.json /etc/grafana/provisioning/dashboards/slo_dashboard.json
