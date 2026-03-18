resource "google_bigquery_dataset" "CCTA-Transactions-Data_Set" {
  project    = "project-a48dc085-0e8c-4a6e-9ca"
  dataset_id = "CCTA"
  location   = "US"
}

resource "google_bigquery_table" "Customers-tb" {

  dataset_id = google_bigquery_dataset.CCTA-Transactions-Data_Set.dataset_id
  table_id   = "Customers-tb"

  deletion_protection = false

  schema = jsonencode([
    {
      name = "cardholder_id"
      type = "STRING"
    },
    {
      name = "card_number"
      type = "STRING"
    },
    {
      name = "card_type"
      type = "STRING"
    },
    {
      name = "customer_name"
      type = "STRING"
    },
    {
      name = "email"
      type = "STRING"
    },
    {
      name = "phone_number"
      type = "STRING"
    },
    {
      name = "country"
      type = "STRING"
    },
    {
      name = "preferred_currency"
      type = "STRING"
    },
    {
      name = "reward_points"
      type = "INTEGER"
    },
    {
      name = "risk_score"
      type = "FLOAT"
    }
  ])
}

