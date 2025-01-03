def update_report(mse_train, mse_test, graphs_dir):
    """Aggiorna il report Markdown"""
    report_path = "reports/report.md"
    with open(report_path, "w") as f:
        f.write(f"# Regressione Simbolica\n")
        f.write(f"## Risultati\n")
        f.write(f"- MSE Training: {mse_train}\n")
        f.write(f"- MSE Test: {mse_test}\n")
        f.write(f"## Grafici\n")
        f.write(f"![Model Structure]({graphs_dir}/model_structure.png)\n")
        f.write(f"![Predicted vs Actual]({graphs_dir}/predicted_vs_actual.png)\n")
