import sys
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, concat, when, count, sum,lit,spark_round
from google.cloud import bigquery

def proccess_data(cardholders_df, transactions_df,time_format)-> "DataFrame":

    """Enriches the transactions data by joining it with the cardholders data and performing necessary transformations."""

    # 1. Validate and clean transactions data
    df = transactions_df.filter(
        (col("transaction_amount") > 0) &
        (col("transaction_status").isin("SUCCESS", "FAILED","PENDING")) &
        (col("cardholder_id").isNotNull()) &
        (col("merchant_id").isNotNull()) 
    )

    #2.Catogery, timestamp,high_risk,merchant_info

    df = df.withColumn("transaction_category", 
                       when(col("transaction_amount") <=100 , lit("Low"))
                       .when((col("transaction_amount") > 100) & (col("transaction_amount") <= 500), lit("Medium"))
                       .otherwise(lit("High"))
                       )\
                       .withColumn("transaction_timestamp", col("transaction_timestamp").cast("timestamp"))\
                       .withColumn("is_high_risk", (col("fraud_flag") == True) | (col("transaction_amount") > 1000) | (col("transaction_category") == "High_risk"))\
                       .withColumn("merchant_info", concat(col("marchant_name"), lit(" - "), col("merchant_location")))
    
    #3.Join with cardholders data
    df = df.join(cardholders_df, on="cardholder_id", how="left")

    #4.update reward points
    df = df.withColumn(
        "updated_reward_points",
        col("reward_points") + spark_round(col("transaction_amount") / 10)
        
    )

    #5.Fraud detection
    df = df.withColumn(
        "fraud_risk_level",
        when(col("high_risk"), lit("High"))\
        .when((col("risk_score")>0.3) | col("fraud_flag"), lit("High"))\
        .otherwise(lit("Low"))
    )

    return df


if __name__ == "__main__":

    # Initialize Spark session
    spark = SparkSession.builder.appName("CreditCardTransactionAnalysis").getOrCreate()

    BQ_PROJECT = "project-a48dc085-0e8c-4a6e-9ca"
    BQ_DATASET = "CCTA"
    BQ_CARDHOLDERS_TABLE = f"{BQ_PROJECT}.{BQ_DATASET}.Customers-tb"
    BQ_TRANSACTIONS_TABLE = f"{BQ_PROJECT}.{BQ_DATASET}.Transactions-tb"    

    transaction_files_path = sys.argv[1]  if len(sys.argv) > 1 else "gs://project-a48dc085-0e8c-4a6e-9ca-ccta-transactions/transactions/transactions_*.json"

    # Load data from BigQuery and GCS
    cardholders_df = spark.read.format("bigquery").option("table", BQ_CARDHOLDERS_TABLE).load()
    transactions_df = spark.read.format("json").option("multiline", "true").load(transaction_files_path)

    #process data
    enriched_df = proccess_data(cardholders_df, transactions_df)

    #sink data back to BigQuery
    enriched_df.write.format("bigquery")\
        .option("table", BQ_TRANSACTIONS_TABLE)\
        .option("temporaryGcsBucket", "project-a48dc085-0e8c-4a6e-9ca-ccta-transactions/temp")\
        .option("createDisposition", "CREATE_IF_NEEDED")\
        .option("writeDisposition", "WRITE_APPEND")\
        .save()
    
    # Log success message
    print("Data successfully written to BigQuery")

    # Stop the Spark session
    spark.stop()






