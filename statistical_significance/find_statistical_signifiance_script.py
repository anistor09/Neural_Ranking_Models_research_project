import pyterrier as pt
from pathlib import Path
import os
from ranx import compare, Run, Qrels

datasets_names = ['passage']

models = ["tct_colbert_msmarco",
          "gte-base-en-v1.5",
          "bge-base-en-v1.5",
          "snowflake-arctic-embed-m",
          "e5-base-v2",
          "e5-base-unsupervised",
          "nomic-embed-text-v1",
          "bge-small-en-v1.5",
          "snowflake-arctic-embed-xs",
          "e5-small-v2"]


def main():
    """
        Create statistical significance reports based on the TREC files of each dataset.
    """
    # Initialize PyTerrier
    if not pt.started():
        pt.init(tqdm="notebook")

    for dataset_name in datasets_names:

        try:
            # Construct path for TREC result files and load runs for each model.
            path = os.path.abspath(os.getcwd()) + "/results/trec_runs/" + dataset_name + "/"

            runs = []
            for model_name in models:
                run_files = Run.from_file(Path(path + model_name + ".trec").resolve().as_posix())

                runs.append(run_files)

            if "passage" not in dataset_name:
                qrels = pt.get_dataset(f'irds:beir/{dataset_name}/test').get_qrels()
            else:
                qrels = pt.get_dataset('irds:msmarco-passage/trec-dl-2019').get_qrels()
                qrels.loc[qrels['label'] < 2, 'label'] = 0 # Minimum relavance is 2 in Trec Dl Eval set


            qrels = Qrels.from_df(qrels, q_id_col='qid', doc_id_col='docno', score_col='label')

            # Compare runs using the specified metrics and significance testing.
            report = compare(qrels, runs, metrics=["mrr@10", "ndcg@10"], max_p=0.05,
                             stat_test='student', make_comparable=True)
            print(report)

            output_path = path + "/../../significance_reports/" + dataset_name

            # Save reports to text and JSON files.
            with open(output_path + '.txt', 'w') as file:
                file.write(str(report))

            report.save(output_path + ".json")

            print(dataset_name + " DONE")
        except Exception as e:
            # Handles any other exceptions
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
