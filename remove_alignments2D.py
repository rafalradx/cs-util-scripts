import os
import argparse
from cryosparc_compute import dataset

myparser = argparse.ArgumentParser(
    prog="RP_partcicles_manip",
    description="Remove aligments2D from particles stack",
)
myparser.add_argument(
    "-p",
    "--prtcls_path",
    type=str,
    required=True,
    help="path to exported particle stack e.g. 'project/exports/groups/J789_particles/J789_particles_exported.cs'",
)


def main(args: argparse.Namespace):

    particle_dset = dataset.Dataset.load(args.prtcls_path)

    alignments2D = [
        "alignments2D/split",
        "alignments2D/shift",
        "alignments2D/pose",
        "alignments2D/psize_A",
        "alignments2D/error",
        "alignments2D/error_min",
        "alignments2D/resid_pow",
        "alignments2D/slice_pow",
        "alignments2D/image_pow",
        "alignments2D/cross_cor",
        "alignments2D/alpha",
        "alignments2D/alpha_min",
        "alignments2D/weight",
        "alignments2D/pose_ess",
        "alignments2D/shift_ess",
        "alignments2D/class_posterior",
        "alignments2D/class",
        "alignments2D/class_ess",
    ]

    particle_dset.drop_fields(alignments2D)
    particle_dset.save(args.prtcls_path)


if __name__ == "__main__":
    main(myparser.parse_args())
