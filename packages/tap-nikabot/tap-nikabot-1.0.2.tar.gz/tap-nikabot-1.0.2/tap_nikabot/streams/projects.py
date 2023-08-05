from typing import List, Iterator, Dict, Any, Optional

from singer.schema import Schema

from ..replication_method import ReplicationMethod
from .stream import Stream
from ..client import Client
from ..typing import JsonResult


class Projects(Stream):
    stream_id: str = "projects"

    def _map_to_schema(self, swagger: JsonResult) -> Schema:
        return Schema.from_dict(swagger["definitions"]["ProjectDTO"])

    def get_records(
        self,
        client: Client,
        config: Dict[str, Any],
        bookmark_column: str,
        last_bookmark: Any,
        replication_method: Optional[ReplicationMethod],
    ) -> Iterator[List[JsonResult]]:
        return client.get_all_pages("/api/v1/projects")
