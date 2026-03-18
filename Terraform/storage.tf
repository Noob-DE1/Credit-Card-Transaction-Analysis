resource "google_storage_bucket" "source_ccta" {

  name     = "${var.project_id}-ccta-customers"
  location = var.region

  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "ccta_scripts" {

  name     = "${var.project_id}-ccta-scripts"
  location = var.region

  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "ccta_transactions" {

  name     = "${var.project_id}-ccta-transactions"
  location = var.region

  uniform_bucket_level_access = true
}