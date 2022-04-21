from formable.tensile_test import TensileTest
from formable.levenberg_marquardt import (
    FittingParameter,
    LMFitterOptimisation,
    LMFitter,
)
import sys
import hickle
from pathlib import Path


def main(
    single_crystal_parameters,
    experimental_tensile_test,
    initial_damping,
    perturbed_volume_element_responses,
    single_crystal_parameter_perturbations,
):
    outputs = optimise_SC_parameters_LM(
        single_crystal_parameters,
        single_crystal_parameter_perturbations,
        perturbed_volume_element_responses,
        experimental_tensile_test,
        initial_damping,
    )

    return outputs


def optimise_SC_parameters_LM(
    single_crystal_parameters,
    single_crystal_parameter_perturbations,
    perturbed_volume_element_responses,
    experimental_tensile_test,
    initial_damping,
):
    """Perform Levenburg-Marquart optimisation.

    Parameters
    ----------
    single_crystal_parameters : dict of (list of dict)
        For each iteration, list of length equal to the number of perturbations. For
        generating the LMFitter object, we will just need the original parameters (i.e.
        from the first iteration).
    single_crystal_parameter_perturbations : dict of (list of dict)
        For each iteration, list of length equal to the number of perturbations. All
        iterations will in fact have the same list of perturbation. However, all
        iterations are included for consistency with `single_crystal_parameters` and
        `perturbed_volume_element_responses`.
    perturbed_volume_element_responses : dict of (str: list of dict)
        Keys identify the iteration to which the responses belong and values are the list
        of volume element responses associated with each dict in 
        `single_crystal_parameter_perturbations` (one for each perturbation).
    experimental_tensile_test : dict
    initial_damping : list of float

    """

    # Generate FittingParameter objects:
    fitting_params = []
    null_perturbation_idx = None
    for idx, (perts, base_vals) in enumerate(
        zip(
            single_crystal_parameter_perturbations["iteration_0"],
            single_crystal_parameters["iteration_0"],
        )
    ):
        if "address" in perts:

            name = "__".join([str(i) for i in perts["address"]])
            value = get_by_path(base_vals, perts["address"])

            fitting_param_i = FittingParameter(
                name=name,
                values=[value],
                address=perts["address"],
                perturbation=perts["perturbation"],
            )
            fitting_params.append(fitting_param_i)
        else:
            # The null-perturbation does not correspond to a FittingParameter:
            null_perturbation_idx = idx

    # Collect volume element responses:
    tensile_tests_by_iteration = []
    for iteration_idx, all_vol_elem_resp in perturbed_volume_element_responses.items():

        tensile_tests = []
        for vol_elem_resp in all_vol_elem_resp:
            true_stress = vol_elem_resp["volume_data"]["vol_avg_equivalent_stress"][
                "data"
            ]
            true_strain = vol_elem_resp["volume_data"]["vol_avg_equivalent_strain"][
                "data"
            ]
            tensile_tests.append(
                TensileTest(true_stress=true_stress, true_strain=true_strain)
            )

        # Need to reorder if null-perturbation is not first:
        num_sims_per_iteration = len(
            single_crystal_parameter_perturbations["iteration_0"]
        )
        if null_perturbation_idx != 0:
            non_null_pert_idx = list(
                set(range(num_sims_per_iteration)) - {null_perturbation_idx}
            )
            tensile_tests = [tensile_tests[null_perturbation_idx]] + [
                tensile_tests[i] for i in non_null_pert_idx
            ]

        tensile_tests_by_iteration.append(tensile_tests)

    # Generate fitter object:
    lm_fitter = LMFitter(
        exp_tensile_test=TensileTest(**experimental_tensile_test),
        single_crystal_parameters=single_crystal_parameters["iteration_0"][0],
        fitting_params=fitting_params,
        initial_damping=initial_damping,
    )

    # Add simulated tests:
    for tensile_tests in tensile_tests_by_iteration:
        lm_fitter.add_simulated_tensile_tests(tensile_tests)

    optimised_single_crystal_parameters = lm_fitter.get_new_single_crystal_params(-1)

    outputs = {
        "single_crystal_parameters": optimised_single_crystal_parameters,
        "levenberg_marquardt_fitter": lm_fitter.to_dict(),
    }

    return outputs


def get_by_path(root, path):
    """Get a nested dict or list item according to its "key path"

    Parameters
    ----------
    root : dict or list
        Can be arbitrarily nested.
    path : list of str
        The address of the item to get within the `root` structure.

    Returns
    -------
    sub_data : any

    """

    sub_data = root
    for key in path:
        sub_data = sub_data[key]

    return sub_data


if __name__ == "__main__":
    inputs = hickle.load(sys.argv[1])
    outputs = main(**inputs)
    hickle.dump(outputs, "outputs.hdf5")
