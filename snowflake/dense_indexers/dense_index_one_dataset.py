import torch
from fast_forward import Mode
from general_dense_indexers.dense_index_one_dataset import index_collection
from encoders.snowflake_arctic_embed_m import SnowFlakeDocumentEncoder, SnowFlakeQueryEncoder
from func_timeout import func_timeout


def index_snowflake_collection(dataset_name, max_id_length, directory, model_name, dim=768):
    """
       Indexes a dataset using the SnowFlake encoders for both queries and documents with specified parameters.

       Args:
       dataset_name (str): The name of the dataset to index.
       max_id_length (int): Maximum length of the IDs in the dataset.
       directory (str): Directory to store the indexed files.
       model_name (str): Name of the model used for encoding.
       dim (int, optional): Dimension of the embeddings generated by the encoder. Defaults to 768.

       This function configures and utilizes document and query encoders from the SnowFlake series, applying them to the
       specified dataset with consideration for device availability (GPU acceleration).
    """
    q_encoder = SnowFlakeQueryEncoder("Snowflake/" + model_name)
    d_encoder = SnowFlakeDocumentEncoder(
        "Snowflake/" + model_name,
        device="cuda:0" if torch.cuda.is_available() else "cpu",
    )
    index_collection(dataset_name, model_name, q_encoder, d_encoder, max_id_length, directory, batch_size=8, dim=dim,
                     mode=Mode.MAXP)


def index_snowflake_m_collection(dataset_name, max_id_length, directory):
    """
      Indexes a dataset using the 'snowflake-arctic-embed-m' model configuration.

      Args:
      dataset_name (str): The name of the dataset to index.
      max_id_length (int): Maximum length of the IDs in the dataset.
      directory (str): Directory to store the indexed files.
    """
    model_name = "snowflake-arctic-embed-m"
    index_snowflake_collection(dataset_name, max_id_length, directory, model_name)


def index_snowflake_xs_collection(dataset_name, max_id_length, directory):
    """
     Indexes a dataset using the 'snowflake-arctic-embed-xs' model with a smaller dimension size.

     Args:
     dataset_name (str): The name of the dataset to index.
     max_id_length (int): Maximum length of the IDs in the dataset.
     directory (str): Directory to store the indexed files.
     """
    model_name = "snowflake-arctic-embed-xs"
    index_snowflake_collection(dataset_name, max_id_length, directory, model_name, dim=384)


def main():
    """
      Main function to initiate indexing of the 'irds:msmarco-passage' dataset using the 'snowflake-arctic-embed-xs' model.
      It sets a timeout for the entire indexing process for easier debugging on the SuperComputer.
    """
    dataset_name = "irds:msmarco-passage"
    max_id_length = 7
    directory = "snowflake"

    try:
        func_timeout(9 * 3600 - 120, index_snowflake_xs_collection, args=(dataset_name, max_id_length, directory))
    except Exception as e:
        # Handles any other exceptions
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
