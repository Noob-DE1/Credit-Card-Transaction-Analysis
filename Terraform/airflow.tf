resource "google_composer_environment" "airflow_dev" {

  name   = "ccta-airflow-dev"
  region = "us-central1"

  config {

    node_config {
      service_account = "whether-api-data-service@project-a48dc085-0e8c-4a6e-9ca.iam.gserviceaccount.com"
    }

    software_config {
      image_version = "composer-2.16.6-airflow-2.10.5"
    }

    environment_size = "ENVIRONMENT_SIZE_SMALL"
  }
}