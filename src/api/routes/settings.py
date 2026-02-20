"""
设置路由
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from src.api.dependencies import verify_api_key
from src.api.client import client
from src.models.settings_models import AccountSubjectSaveRequest, AuxiliaryItemSaveRequest
from src.services.settings_service import SettingsService

router = APIRouter(prefix="/settings", tags=["设置"], dependencies=[Depends(verify_api_key)])

_settings_service = SettingsService(client)


@router.get("/profile", summary="系统参数")
def get_system_profile(
    key: str = Query(..., description="参数键名"),
):
    """获取系统参数值。"""
    result = _settings_service.get_system_profile(key)
    return result.model_dump()


@router.get("/account-subjects", summary="科目查询")
def get_account_subjects(
    number: Optional[str] = Query(None, description="科目编码"),
    name: Optional[str] = Query(None, description="科目名称"),
    group_name: Optional[str] = Query(None, alias="groupName", description="科目分组"),
    class_id: Optional[str] = Query(None, alias="classId", description="科目分类ID"),
):
    """查询会计科目列表。"""
    result = _settings_service.get_account_subjects(
        number=number, name=name, groupName=group_name, classId=class_id
    )
    return result.model_dump()


@router.post("/account-subjects", summary="科目保存")
def save_account_subject(subjects: List[AccountSubjectSaveRequest]):
    """批量保存会计科目。"""
    return _settings_service.save_account_subject(subjects)


@router.get("/voucher-words", summary="凭证字查询")
def get_voucher_words(
    page: int = Query(1, description="页码"),
    page_size: int = Query(100, alias="pageSize", description="每页条数"),
):
    """查询凭证字列表。"""
    result = _settings_service.get_voucher_words(page, page_size)
    return result.model_dump()


@router.get("/auxiliary-item-classes", summary="辅助核算类别查询")
def get_auxiliary_item_classes():
    """查询辅助核算类别列表。"""
    result = _settings_service.get_auxiliary_item_classes()
    return result.model_dump()


@router.get("/auxiliary-items", summary="辅助核算查询")
def get_auxiliary_items(
    item_cls_name: Optional[str] = Query(None, alias="itemClsName", description="核算类别名称"),
    number: Optional[str] = Query(None, description="编码"),
    name: Optional[str] = Query(None, description="名称"),
    is_deleted: Optional[str] = Query(None, alias="isDeleted", description="是否已删除"),
    page: Optional[int] = Query(None, description="页码"),
    page_size: Optional[int] = Query(None, alias="pageSize", description="每页条数"),
):
    """查询辅助核算项目列表。"""
    result = _settings_service.get_auxiliary_items(
        itemClsName=item_cls_name, number=number, name=name,
        isDeleted=is_deleted, page=page, pageSize=page_size,
    )
    return result.model_dump()


@router.post("/auxiliary-items", summary="辅助核算保存")
def save_auxiliary_items(items: List[AuxiliaryItemSaveRequest]):
    """批量保存辅助核算项目。"""
    return _settings_service.save_auxiliary_items(items)


@router.post("/auxiliary-items/delete", summary="辅助核算删除")
def delete_auxiliary_items(item_class_name: str, numbers: List[str]):
    """删除指定类别下的辅助核算项目。"""
    return _settings_service.delete_auxiliary_items(item_class_name, numbers)
