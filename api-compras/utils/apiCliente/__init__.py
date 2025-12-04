"""Paquete de clientes HTTP para servicios externos.

Exporta: BaseAPIClient está en `base.py`. Clientes concretos: `StockClient`, `LogisticsClient`, `EnviosClient`.
"""
from .base import BaseAPIClient, APIError
from .stock import StockClient
from .logistica import LogisticsClient

__all__ = ["BaseAPIClient", "APIError", "StockClient", "LogisticsClient"]
