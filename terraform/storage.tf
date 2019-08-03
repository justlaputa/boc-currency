
resource "google_storage_bucket" "main" {
  name     = "${var.bucket_name}"
  storage_class = "${var.storage_class}"
  location = "${var.location}"

  versioning {
      enabled = true
  }
}

resource "google_storage_bucket_object" "chart-html" {
  name   = "index.html"
  source = "./chart.html"
  bucket = "${google_storage_bucket.main.name}"

  content_type = "text/html;charset=utf-8"
}

resource "google_storage_object_acl" "html-acl" {
  bucket = "${google_storage_bucket.main.name}"
  object = "${google_storage_bucket_object.chart-html.output_name}"

  predefined_acl = "publicRead"
}