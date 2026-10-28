"""Run the trained optional ML model on synthetic data only."""
import argparse
import json
from pathlib import Path
from src.ingestion.generate import generate_sales
from src.forecasting.ml_benchmark import train_and_evaluate

def main(args=None):
    parser=argparse.ArgumentParser(description="Train/test one synthetic-SKU random forest model")
    parser.add_argument("--sku",default="ELEC-101")
    parser.add_argument("--trees",type=int,default=48)
    parser.add_argument("--out",type=Path,default=Path("data/generated/ml_benchmark.json"))
    options=parser.parse_args(args)
    rows=[r for r in generate_sales() if r["sku"]==options.sku]
    if not rows:
        parser.error("Unrecognized synthetic SKU")
    metrics=train_and_evaluate([r["units"] for r in rows],start_date=rows[0]["date"],n_estimators=options.trees)
    metrics["sku"]=options.sku
    options.out.parent.mkdir(parents=True,exist_ok=True)
    options.out.write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    print(options.sku,metrics["model"],"holdout WAPE=",metrics["holdout"]["wape"],
          "seasonal naive WAPE=",metrics["seasonal_naive_holdout"]["wape"])
    return metrics

if __name__=="__main__":
    main()
