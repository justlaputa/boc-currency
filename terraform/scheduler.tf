resource "google_cloud_scheduler_job" "chart-updater" {
  provider    = "google-beta"
  project     = "${var.scheduler_project}"
  name        = "chart-updater"
  region      = "${var.region}"
  description = "trigger the chart-updater cloud run"
  schedule    = "${var.chart_updater_schedule}"
  time_zone   = "${var.timezone}"

  http_target {
    http_method = "GET"
    uri         = "${var.chart_updater_url}"
  }
}
