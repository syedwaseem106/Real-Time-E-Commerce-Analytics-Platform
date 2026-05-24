import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from src.utils.config import get_postgres_uri
from src.utils.logger import get_logger

logger = get_logger("analytics-exporter")

class AnalyticsExporter:
    """
    Dumps analytical summaries from PostgreSQL warehouse views into flat CSV files.
    Enables zero-friction integration with Excel, Power BI Desktop, or Tableau.
    """
    def __init__(self, postgres_uri=None, export_dir="data/exports"):
        self.uri = postgres_uri if postgres_uri else get_postgres_uri()
        self.engine = create_engine(self.uri)
        self.export_dir = export_dir
        
        # Ensure directories exist
        os.makedirs(self.export_dir, exist_ok=True)

    def export_view_to_csv(self, view_name, filename):
        """Pulls a single reporting view and exports it to CSV."""
        try:
            logger.info(f"Extracting {view_name} to {filename}...")
            
            # Use pandas to query Postgres
            query = f"SELECT * FROM {view_name}"
            df = pd.read_sql_query(query, self.engine)
            
            # Define output path
            output_path = os.path.join(self.export_dir, filename)
            
            # Export to CSV
            df.to_csv(output_path, index=False, encoding='utf-8')
            logger.info(f"Successfully exported {len(df)} records to: {output_path}")
            return len(df)
        except Exception as e:
            logger.error(f"Failed exporting view {view_name}: {e}")
            return 0

    def export_all(self):
        """Exports all analytical dashboard views to CSV reports."""
        start_time = datetime.now()
        logger.info("Starting batch CSV export process...")
        
        exports = {
            "analytics.v_executive_summary": "executive_summary_report.csv",
            "analytics.v_daily_sales_summary": "daily_sales_report.csv",
            "analytics.v_product_performance": "product_performance_report.csv",
            "analytics.v_category_revenue": "category_revenue_report.csv",
            "analytics.v_user_segments": "user_segments_report.csv",
            "analytics.v_conversion_funnel": "conversion_funnel_report.csv",
            "analytics.v_hourly_traffic": "hourly_traffic_report.csv"
        }
        
        counts = {}
        for view, file in exports.items():
            counts[file] = self.export_view_to_csv(view, file)
            
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Analytics export completed in {duration:.2f} seconds. Files: {len(counts)}")
        return counts

def main():
    # Allow target directory override from args
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "data/exports"
    exporter = AnalyticsExporter(export_dir=target_dir)
    exporter.export_all()

if __name__ == '__main__':
    main()
