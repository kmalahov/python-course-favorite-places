import geocoder
from geocoder.ipinfo import IpinfoQuery
from fastapi import APIRouter, Depends, Query, status, Request
from fastapi_pagination import Page, paginate
from geocoder.ipinfo import IpinfoQuery

from exceptions import ApiHTTPException, ObjectNotFoundException
from models.places import Place
from schemas.places import PlaceResponse, PlacesListResponse, PlaceBase
from schemas.routes import MetadataTag, Description
from services.places_service import PlacesService

router = APIRouter()

tag_places = MetadataTag(
    name="places",
    description="Управление любимыми местами.",
)


@router.get(
    "",
    summary="Получение списка объектов",
    response_model=Page[Place],
)
async def get_list(limit: int = Query(20, gt=0, le=100,
                                      description="Ограничение на количество объектов в выборке"),
                   places_service: PlacesService = Depends(),
                   ) -> Page[Place]:
    """
    Получение списка любимых мест.

    :param limit: Ограничение на количество объектов в выборке.
    :param places_service: Сервис для работы с информацией о любимых местах.
    :return:
    """

    return paginate(await places_service.get_places_list(limit=limit))


@router.get(
    "/{primary_key}",
    summary="Получение объекта по его идентификатору",
    response_model=PlaceResponse,
)
async def get_one(
        primary_key: int, places_service: PlacesService = Depends()
) -> PlaceResponse:
    """
    Получение объекта любимого места по его идентификатору.

    :param primary_key: Идентификатор объекта.
    :param places_service: Сервис для работы с информацией о любимых местах.
    :return:
    """

    if place := await places_service.get_place(primary_key):
        return PlaceResponse(data=place)

    raise ObjectNotFoundException


@router.post(
    "",
    summary="Создание нового объекта",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
        place: Place, places_service: PlacesService = Depends()
) -> PlaceResponse:
    """
    Создание нового объекта любимого места по переданным данным.

    :param place: Данные создаваемого объекта.
    :param places_service: Сервис для работы с информацией о любимых местах.
    :return:
    """

    place = Place(description=place.description,
                  latitude=place.latitude,
                  longitude=place.longitude,
                  )

    if primary_key := await places_service.create_place(place):
        return PlaceResponse(data=await places_service.get_place(primary_key))

    raise ApiHTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Объект не был создан",
    )


@router.patch(
    "/{primary_key}",
    summary="Обновление объекта по его идентификатору",
    response_model=PlaceResponse,
)
async def update(
        primary_key: int, place: PlaceBase, places_service: PlacesService = Depends()
) -> PlaceResponse:
    """
    Обновление объекта любимого места по переданным данным.

    :param primary_key: Идентификатор объекта.
    :param place: Данные для обновления объекта.
    :param places_service: Сервис для работы с информацией о любимых местах.
    :return:
    """

    if not await places_service.update_place(primary_key, place):
        raise ObjectNotFoundException

    return PlaceResponse(data=await places_service.get_place(primary_key))


@router.delete(
    "/{primary_key}",
    summary="Удаление объекта по его идентификатору",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(primary_key: int, places_service: PlacesService = Depends()) -> None:
    """
    Удаление объекта любимого места по его идентификатору.

    :param primary_key: Идентификатор объекта.
    :param places_service: Сервис для работы с информацией о любимых местах.
    :return:
    """

    if not await places_service.delete_place(primary_key):
        raise ObjectNotFoundException


@router.post("/auto", summary="Создание нового объекта с автоматическим определением координат",
             response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
async def create_auto(request: Request, description: Description,
                      places_service: PlacesService = Depends()) -> PlaceResponse:
    """
    Создание нового объекта любимого места с автоматическим определением координат.
    :return:
    """
    print(request.client)
    if request.client is None:
        raise ApiHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ip-адрес не найден")

    ip_info: IpinfoQuery = geocoder.ip(request.client.host)
    if (ip_info.geojson.get("features", None) is None or len(ip_info.geojson["features"]) == 0
            or ip_info.geojson["features"][0].get("geometry", None) is None):
        raise ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет данных о местоположении",
        )

    coordinates = ip_info.geojson["features"][0]["geometry"]["coordinates"]

    place = Place(description=description.description, longitude=coordinates[0], latitude=coordinates[1])

    if primary_key := await places_service.create_place(place):
        return PlaceResponse(data=await places_service.get_place(primary_key))

    raise ApiHTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Объект не был создан",
    )