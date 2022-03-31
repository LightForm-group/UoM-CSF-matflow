from formable import load_cases
import sys
import hickle
from pathlib import Path


def main(load_case_specs):
    load_case = build_load_case(load_case_specs)

    return load_case


def build_load_case(load_case_specs):
    """
    Build a list of load cases using `formable`.

    Parameters
    ----------
    load_case_specs : list of dict
        Each dict contains a key "type", and all remaining keys are used to parametrise
        a list of load cases of that type. See the `foramble.load_cases` module for the
        different types of load case that are available.

    Returns
    -------
    load_case : list of dict

    """

    repeated_defaults = {
        "target_strains": None,
        "target_strain_rates": None,
        "dump_frequency": 1,
        "rotations": None,
    }

    METHOD_INFO = {
        "uniaxial": {
            "func": load_cases.get_load_case_uniaxial,
            "func_returns_list": False,
            "length_identifier": "total_times",
            "defaults": repeated_defaults,
            "keep_singular": [],
        },
        "biaxial": {
            "func": load_cases.get_load_case_biaxial,
            "func_returns_list": False,
            "length_identifier": "total_times",
            "defaults": repeated_defaults,
            "keep_singular": [],
        },
        "plane_strain": {
            "func": load_cases.get_load_case_plane_strain,
            "func_returns_list": False,
            "length_identifier": "total_times",
            "defaults": {"strain_rate_modes": None, **repeated_defaults,},
            "keep_singular": [],
        },
        "planar_2d": {
            "func": load_cases.get_load_case_planar_2D,
            "func_returns_list": False,
            "length_identifier": "total_times",
            "defaults": repeated_defaults,
            "keep_singular": [],
        },
        "random_2d": {
            "func": load_cases.get_load_case_random_2D,
            "func_returns_list": False,
            "length_identifier": "total_times",
            "defaults": repeated_defaults,
            "keep_singular": [],
        },
        "random_3d": {
            "func": load_cases.get_load_case_random_3D,
            "func_returns_list": False,
            "length_identifier": "total_times",
            "defaults": {"non_random_rotation": None, "dump_frequency": 1,},
            "keep_singular": ["rotation", "rotation_max_angle", "rotation_load_case"],
        },
        "cyclic_uniaxial": {
            "func": load_cases.get_load_case_uniaxial_cyclic,
            "func_returns_list": True,
            "length_identifier": "max_stresses",
            "defaults": {"waveforms": "sine", "dump_frequency": 1,},
            "keep_singular": [],
        },
    }

    PLURALS_MAP = {
        "total_times": "total_time",
        "num_increments": "num_increments",
        "directions": "direction",
        "normal_directions": "normal_direction",
        "target_strains": "target_strain",
        "target_strain_rates": "target_strain_rate",
        "rotations": "rotation",
        "dump_frequency": "dump_frequency",
        "strain_rate_modes": "strain_rate_mode",
        "non_random_rotation": "non_random_rotation",
        "waveforms": "waveform",
        "max_stresses": "max_stress",
        "min_stresses": "min_stress",
        "cycle_frequencies": "cycle_frequency",
    }

    load_case = []

    for lc_spec in load_case_specs:

        lc_type = lc_spec.pop("type").lower()

        if lc_type not in METHOD_INFO:
            msg = (
                f'Load case type "{lc_type}" unknown. Allowed `type` keys '
                f"are: {list(METHOD_INFO.keys())}"
            )
            raise ValueError(msg)

        method_info_i = METHOD_INFO[lc_type]
        num_cases_i = len(lc_spec[method_info_i["length_identifier"]])

        # Apply defaults: # TODO fix this!
        for def_i_key, def_i_val in method_info_i["defaults"].items():
            if not lc_spec.get(def_i_key):
                if def_i_key in method_info_i["keep_singular"]:
                    lc_spec.update({def_i_key: def_i_val})
                else:
                    lc_spec.update({def_i_key: [def_i_val] * num_cases_i})

        # Normalise:
        lc_spec_normed = invert_dict_of_lists(
            lc_spec, key_map=PLURALS_MAP, keep_singular=method_info_i["keep_singular"],
        )

        # Generate load cases with `formable`:
        for lc_spec_normed_i in lc_spec_normed:
            lc = method_info_i["func"](**lc_spec_normed_i)
            if method_info_i["func_returns_list"]:
                load_case.extend(lc)
            else:
                load_case.append(lc)

    return load_case


def invert_dict_of_lists(dct, key_map=None, keep_singular=None):
    """Convert a dict whose values are lists of equal lengths into a 
    list of dicts whose values are singular. `key_map` is to modify key names."""

    if not key_map:
        key_map = {}

    if not keep_singular:
        keep_singular = []

    for key in dct.keys():
        if key not in key_map:
            key_map[key] = key

    num_vals = len(dct[[k for k in dct if k not in keep_singular][0]])

    new_lst = [{key_map.get(k, k): None for k in dct} for _ in range(num_vals)]

    for lst_idx in range(num_vals):
        for key, val in dct.items():
            new_lst[lst_idx][key_map.get(key, key)] = (
                val if key in keep_singular else val[lst_idx]
            )

    return new_lst


if __name__ == "__main__":
    inputs = hickle.load(sys.argv[1])
    outputs = main(**inputs)
    hickle.dump(outputs, "outputs.hdf5")
