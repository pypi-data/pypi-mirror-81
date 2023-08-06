# Copyright (c) 2016. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function, division, absolute_import
import logging
import logging.config
import pkg_resources
import sys

import pandas as pd
from pyensembl.fasta import parse_fasta_dictionary

from .args import make_mhc_arg_parser, mhc_binding_predictor_from_args

logging.config.fileConfig(pkg_resources.resource_filename(__name__, 'logging.conf'))
logger = logging.getLogger(__name__)


arg_parser = make_mhc_arg_parser(
    prog="mhctools",
    description=("Predict MHC ligands from protein sequences."))

def add_input_args(arg_parser):
    input_group = arg_parser.add_argument_group("Inputs")
    input_group.add_argument(
        "--sequence",
        nargs="*",
        help=(
            "Peptide sequences"))
    input_group.add_argument(
        "--extract-subsequences",
        default=False,
        action="store_true",
        help=(
            "Extract subsequences from peptides supplied by --sequence or "
            "--input-peptides-file, lengths specified by "
            "--mhc-peptide-lengths argument."))
    input_group.add_argument(
        "--input-peptides-file",
        help="Path to file with one peptide per line")
    input_group.add_argument(
        "--input-fasta-file",
        help="Path to FASTA file which contains protein sequences")
    return input_group

def add_output_args(parser):
    output_group = arg_parser.add_argument_group("Outputs")
    output_group.add_argument("--output-csv", default=None)
    return output_group

add_input_args(arg_parser)
add_output_args(arg_parser)

def parse_args(args_list=None):
    if args_list is None:
        args_list = sys.argv[1:]
    return arg_parser.parse_args(args_list)

def run_predictor(args):
    predictor = mhc_binding_predictor_from_args(args)

    if args.input_fasta_file:
        input_dictionary = parse_fasta_dictionary(args.input_fasta_file)
        if not input_dictionary:
            raise ValueError(
                "No sequences could be parsed from fasta file: %s" % (
                    args.input_fasta_file))
        # Capitalize sequences
        input_dictionary = dict(
            (key, value.upper()) for (key, value) in input_dictionary.items())
        binding_predictions = predictor.predict_subsequences(input_dictionary)
    elif args.sequence:
        if args.extract_subsequences:
            binding_predictions = predictor.predict_subsequences(args.sequence)
        else:
            binding_predictions = predictor.predict_peptides(args.sequence)
    elif args.input_peptides_file:
        with open(args.input_peptides_file) as f:
            peptides = [line.strip() for line in f if line]
        if args.extract_subsequences:
            binding_predictions = predictor.predict_subsequences(peptides)
        else:
            binding_predictions = predictor.predict_peptides(peptides)
    else:
        raise ValueError(
            ("No input sequences provided, "
             "use --sequence, --input-fasta-file, or input-peptides-file"))
    return binding_predictions

def main(args_list=None):
    """
    Script to make pMHC binding predictions from amino acid sequences.

    Usage example:
        mhctools
            --sequence SFFPIQQQQQAAALLLI \
            --sequence SILQQQAQAQQAQAASSSC \
            --extract-subsequences \
            --mhc-predictor netmhc \
            --mhc-alleles HLA-A0201 H2-Db \
            --mhc-predictor netmhc \
            --output-csv epitope.csv
    """
    args = parse_args(args_list)
    binding_predictions = run_predictor(args)
    df = binding_predictions.to_dataframe()
    pd.set_option('display.max_columns', None)
    logger.info('\n%s', df)
    if args.output_csv:
        df.to_csv(args.output_csv, index=False)
        print("Wrote: %s" % args.output_csv)
