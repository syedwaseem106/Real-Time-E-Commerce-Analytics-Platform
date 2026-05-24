from pyspark.sql import functions as F
from pyspark.sql.types import StringType

def add_time_dimensions(df):
    """
    Enriches DataFrame with time dimensions derived from the event timestamp.
    Extremely valuable for time-series and e-commerce cohort analyses.
    """
    return df \
        .withColumn("hour", F.hour(F.col("timestamp"))) \
        .withColumn("day_of_week", F.dayofweek(F.col("timestamp"))) \
        .withColumn("day_name", F.date_format(F.col("timestamp"), "EEEE")) \
        .withColumn("month", F.month(F.col("timestamp"))) \
        .withColumn("month_name", F.date_format(F.col("timestamp"), "MMMM")) \
        .withColumn("year", F.year(F.col("timestamp"))) \
        .withColumn("quarter", F.quarter(F.col("timestamp"))) \
        .withColumn("is_weekend", F.when(F.col("day_of_week").isin(1, 7), True).otherwise(False)) \
        .withColumn("is_business_hours", F.when((F.col("hour") >= 9) & (F.col("hour") <= 18) & (~F.col("is_weekend")), True).otherwise(False))

def classify_user_segment(df):
    """
    Dynamically classifies users into commercial categories based on spending thresholds.
    """
    return df.withColumn(
        "user_segment",
        F.when(F.col("amount") >= 500, "VIP")
         .when((F.col("amount") >= 100) & (F.col("amount") < 500), "Frequent Buyer")
         .when(F.col("amount") > 0, "Bargain Hunter")
         .otherwise("Regular")
    )

def enrich_with_product_info(df, product_catalog_df):
    """Enriches operational streams with static product dimension details via joins."""
    return df.join(
        product_catalog_df, 
        df.product_id == product_catalog_df.product_id, 
        "inner"
    ).drop(product_catalog_df.product_id)

def flag_suspicious_events(df):
    """
    Security/Fraud detection pattern: flags rapid-fire clicks or transaction values 
    exceeding regular purchase ranges.
    """
    return df.withColumn(
        "is_suspicious",
        F.when((F.col("amount") > 2000.0) & (F.col("event_type") == "purchase"), True)
         .when((F.col("quantity") > 5) & (F.col("event_type") == "purchase"), True)
         .otherwise(False)
    )

def calculate_conversion_funnel(df):
    """
    Aggregates e-commerce activity along the conversion funnel stages:
    view -> cart -> checkout -> buy
    """
    # Note: Expects an aggregated session-level DataFrame
    return df.select(
        F.countDistinct("session_id").alias("total_sessions"),
        F.countDistinct(F.when(F.col("event_type") == "page_view", F.col("session_id"))).alias("view_sessions"),
        F.countDistinct(F.when(F.col("event_type") == "add_to_cart", F.col("session_id"))).alias("cart_sessions"),
        F.countDistinct(F.when(F.col("event_type") == "checkout", F.col("session_id"))).alias("checkout_sessions"),
        F.countDistinct(F.when(F.col("event_type") == "purchase", F.col("session_id"))).alias("purchase_sessions")
    )
