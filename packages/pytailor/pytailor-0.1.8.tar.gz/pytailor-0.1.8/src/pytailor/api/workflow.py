from __future__ import annotations

from typing import Optional
import uuid
from collections import defaultdict

from pytailor.models import Workflow as WorkflowModel, WorkflowCreate
from pytailor.clients import RestClient
from pytailor.utils import dict_keys_str_to_int, dict_keys_int_to_str
from pytailor.common.state import State
from pytailor.execution import SerialRunner
from pytailor.common.base import APIBase
from pytailor.exceptions import BackendResourceError
from .project import Project
from .fileset import FileSet
from .dag import DAG


class Workflow(APIBase):
    """
    The Workflow class is used to create new workflows or operate on existing workflows.

    **Instantiation patterns:**
    - To create a new workflow use the default constructor
    - To retrieve a workflow from the backend use *Workflow.from_project_and_id()*

    """

    # new workflows are instantiated with __init__
    # existing workflows are instantiated with:
    # - Workflow.from_project_and_id()
    # - Workflow.from_model()

    def __init__(
        self,
        project: Project,
        dag: DAG,
        name: Optional[str] = None,
        inputs: Optional[dict] = None,
        fileset: Optional[FileSet] = None,
    ):
        """
        Create a new workflow.

        Parameters
        ----------
        project : Project
            The project for which to create the workflow.
        dag : DAG
            Provide a dag object for this workflow.
        name : str, optional
            Provide a name for this workflow.
        inputs : dict, optional
            Input data which can be queried from tasks during workflow execution.
            the data must be JSON/BSON serializable.
        fileset : FileSet, optional
            Files to upload is specified in a tag: file(s) dict.
        """

        self.__project = project
        self.__dag = dag
        self.__name = name or "Unnamed workflow"
        self.__inputs = inputs or {}
        self.__state = State.PRE
        self.__fileset = fileset or FileSet(self.__project)
        self.__outputs = {}
        self.__id = None
        self.__model = None

    @property
    def project(self):
        return self.__project

    @property
    def dag(self):
        return self.__dag

    @property
    def name(self):
        return self.__name

    @property
    def inputs(self):
        return self.__inputs

    @property
    def state(self):
        return self.__state.name

    @property
    def outputs(self):
        return self.__outputs

    @property
    def id(self):
        return self.__id

    def __str__(self):
        self.refresh()
        return self.__pretty_printed()

    def __update_from_backend(self, wf_model: WorkflowModel):
        # used to set a references to the backend database record for the
        # workflow
        self.__state = State[wf_model.state]
        self.__outputs = wf_model.outputs
        self.__id = wf_model.id
        self.__model = wf_model

    def refresh(self) -> None:
        """Update with latest data from backend."""
        if self.__state == State.PRE:
            raise BackendResourceError(
                "This workflow has not been run yet and can "
                "therefore not be refreshed."
            )
        wf_model = self.__fetch_model(self.project.id, self.id)
        self.__update_from_backend(wf_model)

    @classmethod
    def __fetch_model(cls, project_id: str, wf_id: str) -> WorkflowModel:
        with RestClient() as client:
            return cls._handle_rest_client_call(
                client.get_workflow,
                project_id,
                wf_id,
                error_msg="Could not retrieve workflow.",
            )

    @classmethod
    def from_project_and_id(cls, project: Project, wf_id: int) -> Workflow:
        """
        Retrieve a workflow from the backend.
        """
        wf_model = cls.__fetch_model(project.id, str(wf_id))
        wf = Workflow(
            project=Project(wf_model.project_id),
            dag=DAG.from_dict(dict_keys_str_to_int(wf_model.dag)),
            name=wf_model.name,
            inputs=wf_model.inputs,
            fileset=wf_model.fileset_id,
        )
        wf.__update_from_backend(wf_model)
        return wf

    def run(self, distributed: bool = False, worker_name: Optional[str] = None) -> None:
        """
        Start the workflow.

        **Parameters**

        - **distributed** (bool, Optional) If False (default) the workflow is executed
        immediately in the current python process one task at a time. Useful for
        development and debugging. If True the workflow will be launched to
        the database, and tasks will be executed in parallel on one or more workers.
        - **worker_name** (str, Optional) A worker name can be provided to control which
        worker(s) will execute the workflow's tasks. This parameter is ignored for
        *mode='here_and_now'*

        """

        if self.__state != State.PRE:
            raise BackendResourceError("Cannot run an existing workflow.")

        if not distributed:
            worker_name = str(uuid.uuid4())

        # create data model
        create_data = WorkflowCreate(
            dag=dict_keys_int_to_str(self.dag.to_dict()),
            name=self.name,
            inputs=self.inputs,
            fileset_id=self.__fileset.id,
            worker_name_restriction=worker_name,
        )

        # add workflow to backend
        with RestClient() as client:
            wf_model = self._handle_rest_client_call(
                client.new_workflow,
                self.__project.id,
                create_data,
                error_msg="Could not create workflow.",
            )
            self.__update_from_backend(wf_model)

        if not distributed:
            # starts the SerialRunner
            # blocks until complete
            runner = SerialRunner(self.project.id, worker_name, wf_model.id)
            runner.run()

            # get the updated workflow and update self
            wf_model = self._handle_rest_client_call(
                client.get_workflow,
                self.__project.id,
                self.__id,
                error_msg="Could not fetch workflow.",
            )
            self.__update_from_backend(wf_model)

        # else:
        #     # launches to backend and returns
        #     # no actions needed here
        #     raise NotImplementedError

    def __add_to_backend(self):
        pass

    def __pretty_printed(self):
        lines = []
        # columns
        tf = "{:^6.6}"  # task id
        n1 = "{:<21.20}"  # name
        p1 = "{:^22.21}"  # parents
        n2 = "{:<19.19}.."  # name
        p2 = "{:^20.20}.."  # parents
        typ = "{:^12.12}"  # type
        s = "{:^12.12}"  # state

        row = "|" + tf + "|" + n1 + "|" + p1 + "|" + typ + "|" + s + "|\n"
        top = "+" + "-" * 77 + "+" + "\n"
        vsep = (
            "+"
            + "-" * 6
            + "+"
            + "-" * 21
            + "+"
            + "-" * 22
            + "+"
            + "-" * 12
            + "+"
            + "-" * 12
            + "+\n"
        )
        header = f"| Workflow {self.id}: {self.name}"
        header = header + " " * (78 - len(header)) + "|\n"
        colheader = row.format("id", " Task name", "Parents", "Type", "State")
        lines.append(top)
        lines.append(header)
        lines.append(vsep)
        lines.append(colheader)
        lines.append(vsep)

        added_tasks = set()
        rows_dict = {}
        id_task_mapping = {t.id: t for t in self.__model.tasks}
        parent_links = defaultdict(list)
        for p, c in self.__model.task_links.items():
            for ci in c:
                parent_links[str(ci)].append(int(p))

        def add_row(tid):
            if not tid in added_tasks:
                added_tasks.add(tid)
                t = id_task_mapping[tid]
                task_name = " " + t.name
                n = n1 if len(task_name) < 21 else n2
                parents = str(parent_links[tid])[1:-1] if tid in parent_links else "-"
                p = p1 if len(parents) < 22 else p2
                row = "|" + tf + "|" + n + "|" + p + "|" + typ + "|" + s + "|\n"
                rows_dict[tid] = row.format(
                    str(tid),
                    task_name,
                    parents,
                    t.type.upper(),
                    self.__model.task_states[tid],
                )

                for cid in self.__model.task_links[tid]:
                    add_row(str(cid))

        for rt_id in self.__model.root_tasks:
            add_row(rt_id)

        lines.extend([v for k, v in sorted(rows_dict.items())])
        lines.append(vsep)

        return "".join(lines)
