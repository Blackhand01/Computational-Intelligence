

from datetime import datetime
from pathlib import Path

from utils import initialize_experiment, load_data, run_genetic_programming, save_results


def main():
    data_dir = './data/'
    output_file = './src/s333971.py'
    base_output_dir = './output/'

    data_files = sorted(Path(data_dir).glob('*.npz'))

    if not data_files:
        print("No data files found in the directory.")
        return

    for data_file in data_files:
        experiment_successful = True
        start_time = datetime.now()
        reason = "Max generations reached"

        try:
            experiment_config = initialize_experiment(data_file, base_output_dir)
            logger = experiment_config["logger"]

            logger.info(f"Processing Problem {experiment_config['problem_id']}")

            x, y = load_data(data_file)
            best_individual, stats = run_genetic_programming(x, y, logger)

            save_results(
                best_individual=best_individual,
                stats=stats,
                output_file=output_file,
                function_name=f"{experiment_config['problem_id']}",
                plot_dir=experiment_config["plot_dir"],
            )

        except Exception as e:
            experiment_successful = False
            reason = f"Error: {str(e)}"
            logger.info(f"Error processing Problem {experiment_config['problem_id']}: {reason}")
            print(f"Error processing Problem {experiment_config['problem_id']}: {reason}")

        finally:
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            logger.generate_summary(
                stats=stats if 'stats' in locals() else None,
                best_expression=best_individual.tree_to_expression() if 'best_individual' in locals() else "N/A",
                total_time=total_time,
                start_time=start_time,
                end_time=end_time,
                reason=reason,
                success=experiment_successful
            )

    print("All experiments completed.")

if __name__ == "__main__":
    main()
