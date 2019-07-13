resource "google_bigquery_dataset" "default" {
  dataset_id                 = "exchange_rate"
  friendly_name              = "currency-exchange-rate"
  description                = "exhange rate scraped from bank web site"
  location                   = "US"
  delete_contents_on_destroy = false
}

resource "google_bigquery_table" "default" {
  dataset_id = "${google_bigquery_dataset.default.dataset_id}"
  table_id   = "boc"

  time_partitioning {
    type = "DAY"
  }

  schema = "${file("schema.json")}"
}
