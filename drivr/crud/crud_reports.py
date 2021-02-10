from drivr import model, schema

from .crud_base import CRUDBase


class CRUDReports(
    CRUDBase[
        model.Report,
        schema.ReportCreate,
        schema.ReportUpdate,
    ]
):
    """CRUD actions associated to the 'report' entity."""


reports = CRUDReports(model=model.Report)
