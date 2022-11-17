import logging
from fastapi import APIRouter, Depends
from tracardi.config import tracardi
from tracardi.domain.event_redirect import EventRedirect
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.storage.driver import storage
from .auth.permissions import Permissions
from ..config import server

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.post("/event-redirect",
             tags=["event-redirect"],
             include_in_schema=server.expose_gui_api)
async def save_redirect(data: EventRedirect):
    """
        Saves redirect configuration
    """
    result = await storage.driver.event_redirect.save(data)
    await storage.driver.event_redirect.refresh()
    return result


@router.get("/event-redirect/{id}",
            tags=["event-redirect"],
            include_in_schema=server.expose_gui_api)
async def get_redirect(id: str):
    """
        Returns redirect configuration or NULL if none
    """
    id = id.strip()
    return await storage.driver.event_redirect.load_by_id(id)


@router.delete("/event-redirect/{id}",
               tags=["event-redirect"],
               include_in_schema=server.expose_gui_api)
async def delete_redirect(id: str):
    """
    Deletes redirect configuration
    """
    id = id.strip()
    result = await storage.driver.event_redirect.delete_by_id(id)
    await storage.driver.event_redirect.refresh()
    return result
