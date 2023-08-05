import os
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Dict, Callable

import importlib_metadata

from bio_embeddings.embed.pipeline import run as run_embed
from bio_embeddings.extract.pipeline import run as run_extract
from bio_embeddings.project.pipeline import run as run_project
from bio_embeddings.utilities import get_file_manager, read_fasta, reindex_sequences, write_fasta_file, \
    check_required, MD5ClashException
from bio_embeddings.utilities.config import read_config_file, write_config_file
from bio_embeddings.visualize.pipeline import run as run_visualize

_STAGES = {
    "embed": run_embed,
    "project": run_project,
    "visualize": run_visualize,
    "extract": run_extract
}

_IN_CONFIG_NAME = "input_parameters_file"
_OUT_CONFIG_NAME = "ouput_parameters_file"


def _valid_file(file_path):
    """
    Verify if a file exists and is not empty.
    Parameters
    ----------
    file_path : str
        Path to file to check
    Returns
    -------
    bool
        True if file exists and is non-zero size,
        False otherwise.
    """
    try:
        return os.stat(file_path).st_size > 0
    except (OSError, TypeError):
        # catch TypeError for nonsense paths, e.g. None
        return False


def _process_fasta_file(**kwargs):
    """
    Will assign MD5 hash as ID if no if provided for a sequence.
    """
    result_kwargs = deepcopy(kwargs)
    file_manager = get_file_manager(**kwargs)

    sequences = read_fasta(kwargs['sequences_file'])
    sequences_file_path = file_manager.create_file(kwargs.get('prefix'), None, 'sequences_file',
                                                   extension='.fasta')
    write_fasta_file(sequences, sequences_file_path)

    result_kwargs['sequences_file'] = sequences_file_path

    # Remap using sequence position rather than md5 hash -- not encouraged!
    result_kwargs['simple_remapping'] = result_kwargs.get('simple_remapping', False)

    mapping = reindex_sequences(sequences, simple=result_kwargs['simple_remapping'])

    # Check if there's the same MD5 index twice. This most likely indicates 100% sequence identity.
    # Throw an error for MD5 hash clashes!
    if mapping.index.has_duplicates:
        raise MD5ClashException("There is at least one MD5 hash clash.\n"
                                "This most likely indicates there are multiple identical sequences in your FASTA file.\n"
                                "MD5 hashes are used to remap sequence identifiers from the input FASTA.\n"
                                "This error exists to prevent wasting resources (computing the same embedding twice).\n"
                                "There's a (very) low probability of this indicating a real MD5 clash.\n\n"
                                "If you are sure there are no identical sequences in your set, please open an issue at "
                                "https://github.com/sacdallago/bio_embeddings/issues . "
                                "Otherwise, use cd-hit to reduce your input FASTA to exclude identical sequences!")

    mapping_file_path = file_manager.create_file(kwargs.get('prefix'), None, 'mapping_file', extension='.csv')
    remapped_sequence_file_path = file_manager.create_file(kwargs.get('prefix'), None, 'remapped_sequences_file',
                                                           extension='.fasta')

    write_fasta_file(sequences, remapped_sequence_file_path)
    mapping.to_csv(mapping_file_path)

    result_kwargs['mapping_file'] = mapping_file_path
    result_kwargs['remapped_sequences_file'] = remapped_sequence_file_path

    return result_kwargs


def _null_function(config: Dict) -> None:
    pass


def execute_pipeline_from_config(config: Dict,
                                 post_stage: Callable[[Dict], None] = _null_function,
                                 **kwargs) -> Dict:

    original_config = deepcopy(config)

    check_required(
        config,
        ["global"]
    )

    # !! pop = remove from config!
    global_parameters = config.pop('global')

    check_required(
        global_parameters,
        ["prefix", "sequences_file"]
    )

    file_manager = get_file_manager(**global_parameters)

    # Make sure prefix exists
    prefix = global_parameters['prefix']

    # If prefix already exists
    if file_manager.exists(prefix):
        if not kwargs.get('overwrite'):
            raise FileExistsError("The prefix already exists & no overwrite option has been set.\n"
                                  "Either set --overwrite, or move data from the prefix.\n"
                                  "Prefix: {}".format(prefix))
    else:
        # create the prefix
        file_manager.create_prefix(prefix)

    Path(prefix).joinpath("bio_embeddings_version.txt").write_text(importlib_metadata.version("bio_embeddings"))

    # Copy original config to prefix
    global_in = file_manager.create_file(prefix, None, _IN_CONFIG_NAME, extension='.yml')
    write_config_file(global_in, original_config)

    global_parameters = _process_fasta_file(**global_parameters)

    for stage_name in config:
        stage_parameters = config[stage_name]

        check_required(
            stage_parameters,
            ["protocol", "type"]
        )

        stage_type = stage_parameters['type']
        stage_runnable = _STAGES.get(stage_type)

        if not stage_runnable:
            raise Exception("No type defined, or invalid stage type defined: {}".format(stage_type))

        # Prepare to run stage
        stage_parameters['stage_name'] = stage_name
        file_manager.create_stage(prefix, stage_name)

        stage_dependency = stage_parameters.get('depends_on')

        if stage_dependency:
            if stage_dependency not in config:
                raise Exception("Stage {} depends on {}, but dependency not found in config.".format(stage_name,
                                                                                                     stage_dependency))

            stage_dependency_parameters = config.get(stage_dependency)
            stage_parameters = {**global_parameters, **stage_dependency_parameters, **stage_parameters}
        else:
            stage_parameters = {**global_parameters, **stage_parameters}

        # Register start time
        start_time = datetime.now().astimezone()
        stage_parameters['start_time'] = str(start_time)

        stage_in = file_manager.create_file(prefix, stage_name, _IN_CONFIG_NAME, extension='.yml')
        write_config_file(stage_in, stage_parameters)

        stage_output_parameters = stage_runnable(**stage_parameters)

        # Register end time
        end_time = datetime.now().astimezone()
        stage_output_parameters['end_time'] = str(end_time)

        # Register elapsed time
        stage_output_parameters['elapsed_time'] = str(end_time - start_time)

        stage_out = file_manager.create_file(prefix, stage_name, _OUT_CONFIG_NAME, extension='.yml')
        write_config_file(stage_out, stage_output_parameters)

        # Store in global_out config for later retrieval (e.g. depends_on)
        config[stage_name] = stage_output_parameters

        # Execute post-stage function, if provided
        post_stage(stage_output_parameters)

    config['global'] = global_parameters
    global_out = file_manager.create_file(prefix, None, _OUT_CONFIG_NAME, extension='.yml')
    write_config_file(global_out, config)

    return config


def parse_config_file_and_execute_run(config_file_path: str, **kwargs):

    if not _valid_file(config_file_path):
        raise Exception("No config or invalid config was passed.")

    # read configuration and execute
    config = read_config_file(config_file_path)

    execute_pipeline_from_config(config, **kwargs)