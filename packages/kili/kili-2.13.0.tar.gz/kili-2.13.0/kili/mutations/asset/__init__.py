from json import dumps
from uuid import uuid4
from typing import List

from ...helpers import content_escape, encode_image, format_result, is_url, deprecate
from ...queries.project import QueriesProject
from ...queries.asset import QueriesAsset
from .queries import (GQL_APPEND_MANY_TO_DATASET,
                      GQL_DELETE_MANY_FROM_DATASET,
                      GQL_UPDATE_PROPERTIES_IN_ASSET)
from ...constants import NO_ACCESS_RIGHT


class MutationsAsset:

    def __init__(self, auth):
        """
        Initializes the subclass

        Parameters
        ----------
        - auth : KiliAuth object
        """
        self.auth = auth

    def append_many_to_dataset(self, project_id: str, content_array: List[str] = None, external_id_array: List[str] = None,
                               is_honeypot_array: List[bool] = None, status_array: List[str] = None, json_content_array: List[List[str]] = None,
                               json_metadata_array: List[dict] = None):
        """
        Append assets to a project

        Parameters
        ----------
        - project_id : str
            Identifier of the project
        - content_array : List[str], optional (default = None)
            List of elements added to the assets of the project
            - For a Text project, the content is directly in text format.
            - For an Image project, the content can be paths to existing images on your computer.
            - For an Image / Video / Pdf project, the content must be hosted on a web server,
            and you point Kili to your data by giving the URLs.
            Must not be None except if you provide json_content_array.
        - external_id_array : List[str], optional (default = None)
            List of external ids given to identify the assets. If None, random identifiers are created.
        - is_honeypot_array : List[bool], optional (default = None)
        - status_array : List[str], optional (default = None)
            By default, all imported assets are set to 'TODO'. It can also be set to
            'ONGOING', 'LABELED', 'REVIEWED'
        - json_content_array : List[List[str]], optional (default = None)
            Useful for 'FRAME' projects only. Each element is a sequence of frames,
            i.e. a list of URLs to images.
        - json_metadata_array : List[Dict] , optional (default = None)
            The metadata given to each asset should be stored in a json like dict with keys 
            "imageUrl", "text", "url".
            json_metadata_array = [{'imageUrl': '','text': '','url': ''}] to upload one asset.

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.
        """
        if content_array is None and json_content_array is None:
            raise ValueError(
                f"Variables content_array and json_content_array cannot be both None.")
        if content_array is None:
            content_array = [''] * len(json_content_array)
        if external_id_array is None:
            external_id_array = [
                uuid4().hex for _ in range(len(content_array))]
        is_honeypot_array = [
            False] * len(content_array) if not is_honeypot_array else is_honeypot_array
        status_array = ['TODO'] * \
            len(content_array) if not status_array else status_array
        formatted_json_content_array = [''] * len(content_array) if not json_content_array else list(map(lambda json_content: dumps(dict(
            zip(range(len(json_content)), json_content))), json_content_array))
        json_metadata_array = [
            {}] * len(content_array) if not json_metadata_array else json_metadata_array
        formatted_json_metadata_array = [
            dumps(elem) for elem in json_metadata_array]
        playground = QueriesProject(self.auth)
        projects = playground.projects(project_id)
        assert len(projects) == 1, NO_ACCESS_RIGHT
        input_type = projects[0]['inputType']
        if input_type == 'IMAGE':
            content_array = [content if is_url(content) else encode_image(
                content) for content in content_array]
        elif input_type == 'FRAME' and json_content_array is None:
            for content in content_array:
                if not is_url(content):
                    raise ValueError(
                        f"Content {content} isn't a link to a video")
        variables = {
            'projectID': project_id,
            'contentArray': content_array,
            'externalIDArray': external_id_array,
            'isHoneypotArray': is_honeypot_array,
            'statusArray': status_array,
            'jsonContentArray': formatted_json_content_array,
            'jsonMetadataArray': formatted_json_metadata_array}
        result = self.auth.client.execute(
            GQL_APPEND_MANY_TO_DATASET, variables)
        return format_result('data', result)

    def update_properties_in_asset(self, asset_id: str, external_id: str = None,
                                   priority: int = None, json_metadata: dict = None, consensus_mark: float = None,
                                   honeypot_mark: float = None, to_be_labeled_by: List[str] = None, content: str = None,
                                   status: str = None, is_used_for_consensus: bool = None, is_honeypot: bool = None):
        """
        Update the properties of one asset

        Parameters
        ----------
        - asset_id : str
            The id of the asset to delete
        - external_id : str, optional (default = None)
            If given, the asset identified by this external identifier will be modified.
        - priority : int, optional (default = None)
            By default, all assets have a priority of 0
        - json_metadata : dict , optional (default = None)
            The metadata given to an asset should be stored in a json like dict with keys 
            "imageUrl", "text", "url".
            json_metadata = {'imageUrl': '','text': '','url': ''}
        - consensus_mark : float (default = None)
            Should be between 0 and 1
        - honeypot_mark : float (default = None)
            Should be between 0 and 1
        - to_be_labeled_by : list of str (default = None)
            If given, should contain the emails of the labelers authorized to label the asset
        - content : str (default = None)
            - For a NLP project, the content is directly in text format
            - For an Image / Video / Pdf project, the content must be hosted on a web server,
            and you point Kili to your data by giving the URLs
        - status : str (default = None)
            Should be in {'TODO', 'ONGOING', 'LABELED', 'REVIEWED'}
        - is_used_for_consensus : bool (default = None)
            Whether to use the asset to compute consensus kpis or not
        - is_honeypot : bool (default = None)
            Whether to use the asset for honeypot

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.
        """

        formatted_json_metadata = None
        if json_metadata is None:
            formatted_json_metadata = None
        elif isinstance(json_metadata, str):
            formatted_json_metadata = json_metadata
        elif isinstance(json_metadata, dict) or isinstance(json_metadata, list):
            formatted_json_metadata = dumps(json_metadata)
        else:
            raise Exception('json_metadata',
                            'Should be either a dict, a list or a string url')
        should_reset_to_be_labeled_by = to_be_labeled_by is not None and len(
            to_be_labeled_by) == 0
        variables = {
            'assetID': asset_id,
            'externalID': external_id,
            'priority': priority,
            'jsonMetadata': formatted_json_metadata,
            'consensusMark': consensus_mark,
            'honeypotMark': honeypot_mark,
            'toBeLabeledBy': to_be_labeled_by,
            'shouldResetToBeLabeledBy': should_reset_to_be_labeled_by,
            'content': content,
            'status': status,
            'isUsedForConsensus': is_used_for_consensus,
            'isHoneypot': is_honeypot,
        }
        result = self.auth.client.execute(
            GQL_UPDATE_PROPERTIES_IN_ASSET, variables)
        return format_result('data', result)

    def delete_many_from_dataset(self, asset_ids: List[str]):
        """
        Delete assets from a project

        Parameters
        ----------
        - asset_ids : list of str
            The list of identifiers of the assets to delete.

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.
        """
        variables = {'assetIDs': asset_ids}
        result = self.auth.client.execute(
            GQL_DELETE_MANY_FROM_DATASET, variables)
        return format_result('data', result)
