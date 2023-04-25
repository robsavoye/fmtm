# Copyright (c) 2022, 2023 Humanitarian OpenStreetMap Team
#
# This file is part of FMTM.
#
#     FMTM is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     FMTM is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with FMTM.  If not, see <https:#www.gnu.org/licenses/>.
#

import os
import zipfile
from sqlalchemy.orm import Session
from ..central.central_crud import xform
from ..projects import project_crud
from ..central.central_crud import project
from fastapi.responses import FileResponse


def get_submission_of_project(
        db: Session,
        project_id: int,
        task_id: int = None
        ):
    """ 
        Gets the submission of project.
        This function takes project_id and task_id as a parameter.
        If task_id is provided, it returns all the submission made to that particular task, else all the submission made in the projects are returned.
    """

    project_info = project_crud.get_project_by_id(db, project_id)
    odkid = project_info.odkid
    project_name = project_info.project_name_prefix
    form_category = project_info.xform_title
    project_tasks = project_info.tasks

    # If task id is not provided, submission for all the task are listed
    if task_id is None:
        task_list = []

        task_list = [x.id for x in project_tasks]

        data = []
        for id in task_list:

            # XML Form Id is a combination or project_name, category and task_id
            xml_form_id = f'{project_name}_{form_category}_{id}'.split('_')[2]

            print('xml_form_id',xml_form_id)
            submission_list = xform.listSubmissions(odkid, xml_form_id)
            print('submission_list ',submission_list)
            if isinstance(submission_list,list):
                for submission in submission_list:
                    # App User Id is a combination of project_name, category and task_id 
                    # Need to access from api
                    submission['submitted_by'] = f'{project_name}_{form_category}_{id}'
                    data.append(submission)
        return data

    else:
        # If task_id is provided, submission made to this particular task is returned.
        xml_form_id = f'{project_name}_{form_category}_{task_id}'.split('_')[2]
        submission_list = xform.listSubmissions(odkid, xml_form_id)
        for x in submission_list:
            x['submitted_by'] = f'{project_name}_{form_category}_{task_id}'
        return submission_list


def get_forms_of_project(
        db : Session,
        project_id: int
    ):
    project_info = project_crud.get_project_by_id(db, project_id)
    odkid = project_info.odkid

    result = project.listForms(odkid)
    return result


def list_app_users_or_project(
        db : Session,
        project_id: int
    ):
    project_info = project_crud.get_project_by_id(db, project_id)
    odkid = project_info.odkid
    result = project.listAppUsers(odkid)
    return result


def create_zip_file(files, output_file_path):
    with zipfile.ZipFile(output_file_path, mode='w') as zip_file:
        for file_path in files:
            zip_file.write(file_path)
    return output_file_path


def download_submission(
    db: Session,
    project_id: int,
    task_id: int    
    ):

    project_info = project_crud.get_project_by_id(db, project_id)
    central_url = project_info.odk_central_url
    odkid = project_info.odkid
    project_name = project_info.project_name_prefix
    form_category = project_info.xform_title
    project_tasks = project_info.tasks

    file_path = f"{project_id}_submissions.zip"

    # If task id is not provided, submission for all the task are listed
    if task_id is None:
        task_list = []

        task_list = [x.id for x in project_tasks]

        # zip_file_path = f"{project_name}_{form_category}_submissions.zip"  # Create a new ZIP file for all submissions
        files = []

        for id in task_list:

            # XML Form Id is a combination or project_name, category and task_id
            # FIXME: fix xml_form_id
            xml_form_id = f'{project_name}_{form_category}_{id}'.split('_')[2]
            file = xform.getSubmissionMedia(odkid, xml_form_id)

            file_path = f"{project_name}_{form_category}_submission_{id}.zip"  # Create a new output file for each submission
            with open(file_path, "wb") as f:
                f.write(file.content)

            files.append(file_path)  # Add the output file path to the list of files for the final ZIP file

        extracted_files = []
        for file_path in files:
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                zip_file.extractall(os.path.splitext(file_path)[0])  # Extract the contents of the nested ZIP files to a directory with the same name as the ZIP file
                extracted_files += [os.path.join(os.path.splitext(file_path)[0], f) for f in zip_file.namelist()]  # Add the extracted file paths to the list of extracted files

        final_zip_file_path = f"{project_name}_{form_category}_submissions_final.zip"  # Create a new ZIP file for the extracted files
        with zipfile.ZipFile(final_zip_file_path, mode='w') as final_zip_file:
            for file_path in extracted_files:
                final_zip_file.write(file_path)

        return FileResponse(final_zip_file_path)


    xml_form_id = f'{project_name}_{form_category}_{task_id}'.split('_')[2]
    file = xform.getSubmissionMedia(odkid, xml_form_id)
    with open(file_path, "wb") as f:
        f.write(file.content)
    return FileResponse(file_path)



