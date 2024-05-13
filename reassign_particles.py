import os
import argparse
from cryosparc_compute import dataset

myparser = argparse.ArgumentParser(
    prog="RP_partcicles_manip",
    description="Reassings CS particles to newly imported micrographs. Substitutes old uuid with uuid of new micrograph. Correspondance is checked by mictrographs path",
)
myparser.add_argument(
    "-p",
    "--prtcls_path",
    type=str,
    required=True,
    help="path to exported particle stack e.g. 'project/exports/groups/J789_particles/J789_particles_exported.cs'",
)
myparser.add_argument(
    "-m",
    "--micr_path",
    type=str,
    required=True,
    help="path to micrographs e.g. '/path/to/P37_J350_passthrough_exposures.cs'",
)


def main(args: argparse.Namespace):

    exp_dset = dataset.Dataset.load(args.micr_path)
    particle_dset = dataset.Dataset.load(args.prtcls_path)

    def clean_path_to_match(path):
        # get the basename of the micrograph
        output_path = os.path.basename(path)
        # remove any leading characters in the path
        output_path = output_path.strip(">")
        # remove any leading UIDs in the path
        output_path = "_".join(output_path.split("_")[1:])
        return output_path

    # {path: uid} in newly imported micrographs
    path_to_uid_map = {
        clean_path_to_match(path): exp_dset["uid"][idx]
        for idx, path in enumerate(exp_dset["micrograph_blob/path"])
    }
    # inverted map {uid:path}
    uid_to_path_map = {v: k for k, v in path_to_uid_map.items()}

    for index, particle in enumerate(particle_dset.rows()):
        # get the micrograph path associated with the particle
        path_to_match = clean_path_to_match(particle["location/micrograph_path"])
        # get new id from map based on micrograph path stored in particle data
        new_uid = path_to_uid_map[path_to_match]
        # assign the uid to the particle dataset after lookup
        particle_dset["location/micrograph_uid"][index] = new_uid
        # to nie dziala
        # update also a path to micrograph in particle data (add > in front)
        particle_dset["location/micrograph_path"][index] = (
            uid_to_path_map[new_uid]
        )

    # remove local motion correction description fields
    motion = [
        "motion/type",
        "motion/path",
        "motion/idx",
        "motion/frame_start",
        "motion/frame_end",
        "motion/zero_shift_frame",
        "motion/psize_A",
    ]
    particle_dset.drop_fields(motion)
    # # normalize 2Dshifts
    # # get pixel_size used in 2D classification of all particles
    # pixel_size = particle_dset["alignments2D/psize_A"].reshape(-1, 1)
    # micrograph_pixel_size = 0.8456
    # # normalize shifts obtained from 2D classification in
    # new_shifts = (
    #     particle_dset["alignments2D/shift"] * pixel_size / micrograph_pixel_size
    # )
    # # store new shifts
    # particle_dset["alignments2D/shift"] = new_shifts
    # # store new pixelsize
    # particle_dset["alignments2D/psize_A"] = 0.8456

    particle_dset.save(args.prtcls_path + ".new_uid")


if __name__ == "__main__":
    main(myparser.parse_args())
