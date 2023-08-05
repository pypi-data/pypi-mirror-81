import pandas as pd
import eccpy.tools as tools
import os
from time import strftime

from eccpy.tools import assert_df_contains_no_nan_values


def read_settings_file(settings_excel_file):
    """ Opens the settings excel file tabs as individual dataframes.

    Also creates paths for output files, and adds them to the output dff dataframe.

    Parameters
    ----------
    settings_excel_file : settings file containing the list of datafiles for analysis, and also chosen parameters

    Returns
    -------
    settings : pandas Series
        Dataframe containing user settings for EC50 calculation and data analysis.
        Created from the "settings" tab of the settings excel file.
    dff : pandas DataFrame
        Dataframe for Files. Contains all the paths for input and output files.
        Created from the "files" tab of the settings excel file.
        Contains the "True" / "False" list of input files to analyse in that run.
    samplenames_dict : dict
        Dictionary to convert long sample names to short ones that are easier to fit into figures.
        Created from the "samplenames" tab of the settings excel file.
    """
    # convert settings file to pandas dataframe, set the first column "User-defined variable" as the index
    df_settings = pd.read_excel(settings_excel_file, sheet_name="settings").set_index("User-defined variable")
    # extract the column with the settings as a pandas Series
    settings = df_settings["Value"]
    # read the settings file tab that contains a list of short names to describe the data
    df_samplenames = pd.read_excel(settings_excel_file, sheet_name="samplenames")
    # open tab with list of files for analysis as a pandas dataframe (data frame files, dff)
    dff = pd.read_excel(settings_excel_file, sheet_name = "files")
    # raise an error if there are empty values, except in the notes and comments column
    dff_data = dff.drop("notes & comments", axis=1)

    assert_df_contains_no_nan_values(dff_data)

    # convert true-like objects (TRUE, true, WAHR, etc) to python bool True
    dff["run curvefit"] = dff["run curvefit"].apply(tools.convert_truelike_to_bool)
    dff["run gatherer"] = dff["run gatherer"].apply(tools.convert_truelike_to_bool)

    # the "output_directory" is optional. replace blank "Not a number, NaN" values with an empty string ""
    dff["output file directory"].fillna("", inplace=True)
    # define Series as the output directory given in the settings file
    ofd = dff.loc[:, "output file directory"]
    # select only empty rows in the output file directory (ofd), obtain index
    ofd_empty_index = ofd.loc[ofd == ""].index
    # replace empty rows with the input file directory
    dff.loc[ofd_empty_index,"output file directory"] = dff.loc[ofd_empty_index,"input file directory"]
    dff.loc[:,"data_file_path"] = dff["input file directory"] + '/' + dff["response data file"]
    # define an output file directory (ofd), normalise the path so that it is os independent
    dff.loc[:,"ofd"] = dff.loc[:,"output file directory"].apply(lambda x: os.path.normpath(x))
    # create the "output_folder" as the directory plus a new folder with the orig response data filename
    dff.loc[:,"data_file_base"] = dff.loc[:,"response data file"].apply(lambda name: ".".join(name.split(".")[:-1]))
    dff.loc[:,"output_folder"] = dff.loc[:,"ofd"] + "/" + dff.loc[:,"data_file_base"]
    dff.loc[:,"ofd_pdfs"] = dff.loc[:,"output_folder"] + "/" + "pdfs"
    dff.loc[:,"ofd_csv"] = dff.loc[:,"output_folder"] + "/" + "csv"
    dff.loc[:,"ofd_curves"] = dff.loc[:, "output_folder"] + "/" + "curves"
    dff.loc[:,"ofd_EC50_eval_excel"] = dff.loc[:,"output_folder"] + "/" + dff.loc[:,"data_file_base"] + ".xlsx"
    dff.loc[:,"ofd_EC50_eval_csv"] = dff.loc[:,"ofd_csv"]  + "/" + dff.loc[:,"data_file_base"] + "(comma_separated).csv"
    dff.loc[:,"ofd_EC50_eval_tabsep_csv"] = dff.loc[:,"ofd_csv"]  + "/" + dff.loc[:,"data_file_base"] +  "(tab_separated).csv"
    dff.loc[:,"EC50_analysis_fig_basename"] = dff.loc[:,"output_folder"] + "/" + dff.loc[:,"data_file_base"] + "_summary"
    dff.loc[:,"EC50_analysis_fig_basename_pdf"] = dff.loc[:,"ofd_pdfs"] + "/" + dff.loc[:,"data_file_base"] + "_summary"
    list_paths_to_normalise = ["data_file_path", "ofd", "output_folder", "ofd_pdfs", "ofd_csv", "ofd_curves",
                               "ofd_EC50_eval_excel", "ofd_EC50_eval_csv", "ofd_EC50_eval_tabsep_csv"]
    # normalise the paths for selected columns, so that they are appropriate for the operating system
    for path in list_paths_to_normalise:
        dff.loc[:,path] = dff.loc[:,path].apply(lambda x: os.path.normpath(x))

    return settings, dff, df_samplenames


def setup_output_folder(settings_file, subfolder_name):
    """ Defines an output folder based on the path of the settings file.
    Creates output folder if necessary.

    Simply creates a subfolder in the location of the settings_file, as follows:
        ORIGINAL_SUBFOLDER_WITH_SETTINGS_EXCEL_FILE/subfolder_name/todays_datestring/
        todays_datestring is represented as YEAR|MONTH|DATE, e.g. 20151215.

    Parameters
    ----------
    settings_file : filepath, string
        settings file containing the list of datafiles for analysis, and also chosen parameters
    subfolder_name: string
        name of the subfolder, to be created in the parent folder containing the settings file.
        Example: "analysed" or "output"

    Returns
    -------
    output_path : filepath, string
        Output subfolder.
    """
    # create a string with the current date
    date_string = strftime("%Y%m%d")
    # obtain the path and filename
    settings_path, settings_excel_filename = os.path.split(settings_file)
    # create an output folder path
    output_path = os.path.join(settings_path, subfolder_name, date_string)
    # if the folder doesn't exist, make it
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # create an output file for the output data
    output_basename = date_string
    return output_path, output_basename